import munch
from . import utils
import json
checkpoints = None
checkpoint_file = None


def initialize(checkpoints_directory, tasks, workflow_name, input_checkpoints):
    # TODO documentation
    """[summary]

    Args:
        checkpoints_directory ([type]): [description]
        tasks ([type]): [description]
        workflow_name ([type]): [description]
        input_checkpoints ([type]): [description]
    """
    global checkpoints
    global checkpoint_file
    checkpoints = None
    checkpoint_file = None
    checkpoints = munch.Munch()

    if input_checkpoints:

        next_checkpoint = next(
            file for file in
            input_checkpoints if workflow_name in file.name)

        if next_checkpoint:
            checkpoints = munch.munchify(
                json.load(next_checkpoint.open()))

    checkpoint_file = _new_checkpoints_file(
        checkpoints_directory, workflow_name)

    checkpoints = _tasks_to_checkpoints(tasks, checkpoints)


def _tasks_to_checkpoints(tasks, checkpoints):

    for task in tasks:
        if task not in checkpoints:
            checkpoints[task] = []

    return checkpoints


def _new_checkpoints_file(new_directory, workflow_name):
    checkpoint_file = utils.get_file(
        new_directory / (workflow_name+".cjson"))
    return checkpoint_file


def get_remaining_iterations(task, input_files):
    global checkpoints
    if isinstance(checkpoints[task], bool):
        if checkpoints[task]:
            return False
    elif isinstance(checkpoints[task], list):
        finished_tasks = set(checkpoints[task])
        return set(input_files) - finished_tasks


def write_checkpoint(task, iteration):
    global checkpoints
    global checkpoint_file
    if isinstance(iteration, bool):
        checkpoints[task] = iteration
    else:
        checkpoints[task].append(iteration)
    file = checkpoint_file.open("wt")
    file.write(checkpoints.toJSON(indent=4))
    file.close()
