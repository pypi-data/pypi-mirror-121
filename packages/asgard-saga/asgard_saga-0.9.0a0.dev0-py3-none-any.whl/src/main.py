import logging

from icecream import ic
from .asgard import arguments_handler as args_handler
##import asgard.arguments_handler as args_handler
from .asgard import checkpoint as checkpoint
from .asgard import configuration as config
from .asgard import scheduler as scheduler
from .asgard import constants
system = constants.system


def main():
    ic.disable()
    config_files, checkpoint_files = args_handler.get_arguments(system.NAME,
                                                                system.DESCRIPTION,
                                                                system.EPILOG,
                                                                system.VERSION)

    for config_file in config_files:

        new_config = config.initialize(config_file)
        logging.basicConfig(
            format='%(levelname)s: %(message)s %(asctime)s',
            datefmt='%m/%d/%Y %I:%M:%S %p')

        checkpoint.initialize(new_config.constant.output_directory,
                              new_config["execute"],
                              config_file.stem,
                              checkpoint_files)

        scheduler.run_config(new_config)


if __name__ == '__main__':
    main()
# pprint.pprint(conf)
