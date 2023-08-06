import json as json
import operator
import pathlib
import re
from functools import reduce

import munch
import numpy as np
from jsonschema import Draft7Validator

from . import utils
from .exceptions import (CommandNotFoundInConfig, NoInputFilesError,
                         UnMatchPairsError)


def initialize(ajson_file):
    config = _load_json(ajson_file)
    _validate_schema(config)
    _check_execute(config)
    _resolve_json(config, config)
    _validate_files_dirs(config)
    _check_input_files(config)

    return config


def _load_json(ajson_file):
    json_config = json.load(open(ajson_file, "rt"))
    return munch.munchify(json_config)


def _validate_schema(config):
    json_schema = json.load(open(f"config/ajson-schema.json", "rt"))
    json_validator = Draft7Validator(json_schema)
    json_validator.validate(config)


def _validate_files_dirs(config):
    execute_keys = config["execute"].keys()

    input_list = [config[task]
                  for task in execute_keys if config.execute[task] == "input"]
    output_list = [config[task]
                   for task in execute_keys if config.execute[task] == "output"]

    for input_task in input_list:
        input_task.directory = utils.get_dir(input_task.directory)

    for output_task in output_list:
        output_task.directory = utils.get_dir(
            output_task.directory, create_if_missing=True,
            append_datetime=True, suffix=config.constant.name)


def _resolve_json(rootObject, jObject, parent=None):
    for jValue in jObject:
        if isinstance(jObject[jValue], munch.Munch):
            _resolve_json(rootObject, jObject[jValue], jObject)
        elif isinstance(jObject[jValue], str):
            jObject[jValue] = _resolve_reference(
                rootObject, jObject[jValue], jObject)
        elif isinstance(jObject[jValue], int):
            pass
        elif isinstance(jObject[jValue], list):
            for index, jItem in enumerate(jObject[jValue]):
                if isinstance(jItem, str):
                    jObject[jValue][index] = _resolve_reference(
                        rootObject, jItem, jObject)


def _resolve_reference(rootObject, jString, parent):
    regex_pattern = '{{((?:.*?))}}'
    for match in re.findall(regex_pattern, jString):
        if "." in match:
            reference_match = reduce(
                operator.getitem, match.split('.'), rootObject)
        else:
            reference_match = parent[match]

        jString = jString.replace(
            f"{{{{{match}}}}}", utils.to_str(reference_match))  # 5 curly brackets are used due to python's formated string syntax

    return jString


def _check_execute(config):
    execute_keys = np.array(list(config["execute"].keys()))
    config_keys = np.array(list(config.keys()))
    orphan_commands = np.isin(execute_keys, config_keys, invert=True)
    if execute_keys[orphan_commands].size > 0:
        raise CommandNotFoundInConfig(
            ", ".join(config_keys[orphan_commands]))


def _check_input_files(config: munch.Munch):

    execute_keys = config["execute"].keys()
    input_tasks = []
    for task in execute_keys:
        if config.execute[task] == "input":

            config[task].files = utils.to_path(config[task].files)

            input_tasks.append(config[task])

    tasks_files = [utils.files_path_expansion(task.files)
                   for task in input_tasks]

    for task, files in zip(input_tasks, tasks_files):
        if len(list(files)) <= 0:
            NoInputFilesError(str(task.directory))

        _check_paired_task_files(task, files)


def _check_paired_task_files(task, files):

    if task.paired_input:

        forward_files = get_prefixes(files, task.extension, task.forward)
        reverse_files = get_prefixes(files, task.extension, task.reverse)
        unmatched_pairs = forward_files.symmetric_difference(reverse_files)

        if len(unmatched_pairs) > 0:
            raise UnMatchPairsError(str(unmatched_pairs))


def get_prefixes(files: list, extension: str,  suffix: str):

    files_ids = set(file.name.replace(suffix+extension, "") for file in files)

    return files_ids


def resolve_iteration(jObject, iteration_value, placeholder):
    for jValue in jObject:
        if isinstance(jObject[jValue], list):
            for index, jItem in enumerate(jObject[jValue]):
                if isinstance(jItem, str):
                    jObject[jValue][index] = _replace_iteration(
                        jItem, iteration_value, placeholder)
        elif isinstance(jObject[jValue], str):
            jObject[jValue] = _replace_iteration(
                jObject[jValue], iteration_value, placeholder)

    return jObject


def _replace_iteration(jString, iteration_value,  placeholder):
    findings = re.findall(placeholder, jString)
    for match in findings:
        jString = jString.replace(
            f"{match}", utils.to_str(iteration_value))

    return jString
