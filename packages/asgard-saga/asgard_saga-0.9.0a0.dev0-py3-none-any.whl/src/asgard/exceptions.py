from .constants import error
import requests


class NoConfigFilesError(Exception):
    def __init__(self, path, message="No ajson configuration files found in directory"):
        self.path = path
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'ASGARD: {self.message}: {self.path}'


class NoDirectoryFoundError(Exception):
    def __init__(self, path, message="No such directory"):
        self.path = path
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'ASGARD: {self.message}: {self.path}'


class NoExcecutePropertyError(Exception):
    def __init__(self, message=error.EXECUTE_PROPERTY_MISSING):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"ASGARD: Invalid Configuration {self.message}"


class CommandNotFoundInConfig(Exception):
    def __init__(self, commands, message=error.COMMAND_NOT_FOUND_CONFIG):
        self.message = message
        self.commands = commands
        super().__init__(self.message)

    def __str__(self):

        return f"ASGARD: Invalid Command {self.message}" % self.commands


class UnMatchPairsError(Exception):
    def __init__(self, files, message=error.FILES_UNMATCHED_PAIR):
        self.message = message
        self.files = files
        super().__init__(self.message)

    def __str__(self):

        return f"ASGARD: The following files are not paired: {self.files}. {self.message}"


class NoInputFilesError(Exception):
    def __init__(self, path, message=error.FILES_NOT_FOUND):
        self.message = message
        self.path = path
        super().__init__(self.message)

    def __str__(self):
        return f"ASGARD: Invalid Input: {self.message} {self.path}"


class EntrezDownloadError(requests.exceptions.RequestException):
    def __init__(self, error_message, message=error.ENTREZ_DOWNLOAD):
        self.message = message
        self.error_message = error_message
        super().__init__(self.message)

    def __str__(self):
        return f"ASGARD: {self.message} {self.error_message}"


class EntrezRequestError(requests.exceptions.RequestException):
    def __init__(self, error_message, message=error.DOWNLOAD_REQUEST):
        self.message = message
        self.error_message = error_message
        super().__init__(self.message)

    def __str__(self):
        return f"ASGARD: {self.message} {self.error_message}"
