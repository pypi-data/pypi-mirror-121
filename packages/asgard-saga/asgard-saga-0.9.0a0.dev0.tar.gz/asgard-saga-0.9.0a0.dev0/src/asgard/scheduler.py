import re
from . import tasks
import munch
from . import utils
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
import subprocess
from . import checkpoint
from .configuration import resolve_iteration, get_prefixes

errors_file = "errors.txt"


def run_config(config):
    """run_config [summary]

    Args:
        config ([type]): [description]
    """
    global errors_file
    errors_file = "errors.txt"
    errors_file = utils.to_str(config.constant.output_directory)+errors_file
    input_files = list(get_prefixes(config, config.constant.forward))

    # Checks the type of excecution for the task++++
    for task in config["execute"].keys():

        if checkpoint.get_remaining_iterations(task, input_files):

            if config["execute"][task] in ["single", True, "True", "true"]:
                run_task(config[task], task)

            elif config["execute"][task] in ["iterate-parallel"]:
                queue_tasks(config[task], input_files, config, task)

            elif config["execute"][task] in ["iterate-sequential"]:
                queue_tasks(config[task], input_files,
                            config, task, sequential=True)
            elif config["execute"][task] in ["False", "false", False]:
                pass
            elif config["execute"][task] in ["iterator"]:
                pass
            else:
                pass


def create_iterator(config: munch.Munch) -> list:

    pass


def queue_tasks(task, input_files, config, task_name, sequential=False,):

    workers = _get_workers(task, config, sequential)

    with ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(run_task, repeat(task), repeat(task_name),
                     input_files,
                     repeat(config.dynamic.placeholder))


def run_task(new_task, task_name, iteration=None, placeholder=None):

    task = new_task.copy()

    if iteration and placeholder:
        task = resolve_iteration(task, iteration, placeholder)

    if isinstance(task["command"], str):

        if task["command"] == "create_file":
            force = utils.get_value_if_present(
                task, "force", default_value=True)
            tasks.create_file(
                task["output_file"], force=force)

        elif task["command"] == "create_directory":
            force = utils.get_value_if_present(
                task, "force", default_value=True)
            tasks.create_directory(task["directory"], force=force)

        elif task["command"] == "entrez_download":
            filetype = utils.get_value_if_present(task, "filetype")
            mode = utils.get_value_if_present(task, "mode")
            tasks.entrez_download(
                task["database"], task["accession"],
                task["output_file"], filetype=filetype, mode=mode)

        elif task["command"] == "download":
            tasks.download_file(
                task["url"], task["output_file"])

        elif task["command"] == "merge_files":
            tasks.merge_files(
                task["files"], task["output_file"])

        elif task["command"] == "replace":
            tasks.text_replace(task["file"],
                               task["output_file"],
                               task["replace_text"],
                               task["new_text"])

    elif (isinstance(task["command"], list)):
        execute_subprocess(task)

    checkpoint.write_checkpoint(task_name, iteration if iteration else True)


def execute_subprocess(task):
    global errors_file
    keys = task.keys()
    input_pipe = utils.get_value_if_present(task, "input_pipe")
    output_pipe = utils.get_value_if_present(task, "output_pipe")
    shell = utils.get_value_if_present(
        task, "run_as_shell", default_value=False)
    subprocess_command = task["command"]
    command_string = " ".join(subprocess_command)

    if shell:
        subprocess_command = command_string

    if output_pipe:
        output_pipe = utils.get_file(output_pipe).open("wt")

    if input_pipe:
        input_pipe = utils.get_file(input_pipe).open("rt")

    # TODO:  handle recursive properties
    for new_file in filter(re.compile(r"(\w*new_file$)").match, keys):
        tasks.create_file(new_file, force=True)

    # It waits for the process to finish then logs its excecution
    with open(errors_file, "a+") as file:
        subprocess.run(subprocess_command,
                       stdin=input_pipe,
                       stdout=output_pipe,
                       stderr=file,
                       shell=shell)


def _get_workers(task, config, sequential):
    if sequential:
        workers = 1

    elif("workers" in task.keys()):
        workers = task.workers

    elif ("threads" in config.constant.keys()):
        workers = int(multiprocessing.cpu_count() / config.constant.threads)

    elif ("workers" in config.constant.keys()):
        workers = config.constant.workers
    else:
        workers = multiprocessing.cpu_count()

    return workers
