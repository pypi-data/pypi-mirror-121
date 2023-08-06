import argparse
from . import utils
from icecream import ic
import sys
import pathlib
from .constants import help
from .exceptions import NoConfigFilesError, NoDirectoryFoundError


def get_arguments(name: str, description: str, epilog: str, version: str):
    """Parses the arguments passed via the CLI and validates them.

    Adds series of parsers to the program and validates its values,
    the arguments are namedand depend on the execution mode
    selected. If the values are valid, a tuple of dictionaries
    with the configuration and checkpoint information is returned.

    Args:
        name (str): Name of the software being executed.
        description (str): A brief description of the software.
        epilog (str): The contact information of the developer.

    Returns:
        tuple: a tuple containing the configuration and the checkpoints if any.
    """

    parser = create_parsers(name, description, epilog, version)

    args = parse_arguments(parser, sys.argv[1:])
    return _validate_arguments(args)


def parse_arguments(parser: argparse.ArgumentParser, args: list):
    """Takes the args parameter and parse it using the parse parameter


    Args:
        parser (argparse.ArgumentParser): Parser with the options configured
        args (list): List of strings to assign to the arguments

    Returns:
        argparse.Namespace: Namespace with the arguments passed to the program
    """
    ic(args)
    if len(args) == 0:
        parser.print_help(sys.stderr)
        raise SystemExit(2)

    return parser.parse_args(args)


def create_parsers(name, description, epilog, version):
    """Adds and configures the main parsers to the executable.

    The main parser allows to selection of the execution mode,
    two extra subparsers (single, multiple) adds the arguments for
    the configuration and checkpoints files.

    Args:
        name (str): Name of the software being executed.
        description (str): A brief description of the software.
        epilog (str): The contact information of the developer.

    Returns:
        argparse.ArgumentParser: Parser with for main arguments and the subparsers.
    """
    parser = argparse.ArgumentParser(prog=name,
                                     description=description,
                                     epilog=epilog)
    parser.add_argument("--preview", action="store_true",
                        help=help.PREVIEW)
    parser.add_argument("-v", '--version', action='version',
                        version=version)

    # Parser to choose between one file or multiple ajson files in a directory.
    config_subparsers = parser.add_subparsers(help="Select operating mode",
                                              dest="mode", required=False)

    add_subparser_single_single(config_subparsers)
    add_subparser_multiple_files(config_subparsers)

    return parser


def add_subparser_multiple_files(config_subparsers):
    """Adds a subparser for the multiple files mode

    Args:
        config_subparsers (argparse.ArgumentParser): Main parser in which the subparsers are added
    """
    # Options for multiple files mode (config_dir, checkpoint_dir).
    parser_multiple_file = config_subparsers.add_parser(
        'multiple', help=help.MODE_MULTIPLE)
    parser_multiple_file.add_argument('--config_dir',
                                      type=pathlib.Path,
                                      help=help.CONFIG_DIRECTORY,
                                      required=True,
                                      metavar="config_dir")
    parser_multiple_file.add_argument('--checkpoint_dir',
                                      type=pathlib.Path,
                                      help=help.CONFIG_DIRECTORY,
                                      metavar="checkpoint_dir")


def add_subparser_single_single(config_subparsers):
    """Adds a subparser for the single mode

    Args:
        config_subparsers (argparse.ArgumentParser): Main parser in which the subparsers are added
    """
    # Options for single file mode (config_file, checkpoint_file).
    parser_single_file = config_subparsers.add_parser(
        'single', help=help.MODE_SINGLE)
    parser_single_file.add_argument('--config_file',
                                    type=pathlib.Path,
                                    help=help.CONFIG_FILE,
                                    required=True,
                                    metavar="config_file")
    parser_single_file.add_argument('--checkpoint_file',
                                    type=pathlib.Path,
                                    help=help.CSV_FILE,
                                    metavar="checkpoint_file")


def _validate_arguments(args):
    """Private method to validate the arguments passed to the parser.

    Validates the configuration and checkpoints path.
    Paths are evaluated as directories or files depending on the selected mode.

    Args:
        args (argparse.Namespace): Namespace with the arguments passed to the program.

    Raises:
        NoDirectoryFoundError: Error raised if ajson files are not found in the directory.
        NoConfigFilesError: Error raised if ajson file is not found.

    Returns:
        tuple: configuration path and checkpoints path in a tuple in the form of Munch object.
    """
    args_dict = vars(args)

    # TODO: remove empty square braquets
    config_files = None
    checkpoint_files = None

    if (args_dict.get("mode") == "multiple"):
        if args_dict.get("config_dir"):
            config_files = utils.get_files(
                args_dict.get("config_dir"), "*.ajson")

        if args_dict.get("checkpoint_dir"):
            checkpoint_files = utils.get_files(
                args_dict.get("checkpoint_dir"), "*.cjson")

        if(not config_files):
            raise NoDirectoryFoundError(
                str(args_dict.get("config_dir").absolute()))

    elif (args_dict.get("mode") == "single"):
        if args_dict.get("config_file"):
            config_files = [utils.is_file(
                args_dict.get("config_file"))]
        if args_dict.get("checkpoint_file"):
            checkpoint_files = [utils.is_file(
                args_dict.get("checkpoint_file"))]

        if(not config_files):
            raise NoConfigFilesError(
                str(args_dict["config_file"].absolute()))

    return config_files, checkpoint_files
