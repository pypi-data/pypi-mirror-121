import os
import errno
import pathlib
import datetime

from .exceptions import NoDirectoryFoundError


def get_type(path):
    if path.is_file():
        return "file"
    elif path.is_dir():
        return "directory"
    elif path.is_socket():
        return "socket"
    elif path.is_fifo():
        return "fifo"
    elif path.is_block_device():
        return "disk"


def get_file(file_path, create_parents=True):
    file_path = resolved_path(file_path)
    get_dir(file_path.parent, create_if_missing=create_parents)
    if not check_if_exist(file_path, "file"):
        file_path.touch()
    return file_path


def to_path(path_string):
    new_path = resolved_path(path_string)

    get_dir(new_path.parent)

    return new_path


def get_dir(path_string, create_if_missing=False,
            append_datetime=False, suffix=None):

    path = resolved_path(path_string)

    if not check_if_exist(path, "directory"):
        if create_if_missing:
            if append_datetime:
                date = datetime.datetime.now()
                startup_time = date.strftime("-%d_%m_%Y-%H_%M_%S")
                path = path.parent / (path.name + str(startup_time))

            if suffix:
                path = path.parent / (path.name + "-" + str(suffix))
            path.mkdir(parents=True, exist_ok=True)
        else:
            raise NoDirectoryFoundError(
                "No such directory", str(path.absolute()))

    check_permissions(path, permission=os.R_OK)
    check_permissions(path, permission=os.W_OK)
    return path


def check_if_exist(path, desired_type):
    if path.exists():
        type = get_type(path)
        if type != desired_type:
            raise NoDirectoryFoundError(
                f"A {get_type(path)} with that name {path.name} already exists", str(path.absolute()))
        return True
    else:
        return False


def is_dir(path_string):
    path = resolved_path(path_string)
    if path.is_dir():
        return path
    else:
        raise NoDirectoryFoundError(
            "No such directory", str(path.absolute()))


def get_files(path_string, pattern):

    path = is_dir(path_string)
    return list(path.glob(pattern))  # transform object generator to list


def files_path_expansion(path: pathlib.Path):

    return get_files(path.parent, path.name)


def resolved_path(path):
    path = pathlib.Path(path)
    path = path.expanduser()
    path = path.resolve()
    return path


def is_file(path_string):
    path = resolved_path(path_string)
    if path.is_file():
        return path
    else:
        raise FileNotFoundError(
            "No such file", str(path.absolute()))


def check_permissions(path, permission=os.R_OK):
    if (os.access(path, mode=permission)):
        return True
    else:
        raise PermissionError(
            errno.EACCES, "Check the permissions on", str(path.absolute))


def to_str(object):
    if type(object) == pathlib.PosixPath:
        if object.is_dir():
            return str(object)+"/"

    return str(object)


def get_value_if_present(object, key, default_value=None):

    if key in object.keys():
        return object[key]
    else:
        return default_value
