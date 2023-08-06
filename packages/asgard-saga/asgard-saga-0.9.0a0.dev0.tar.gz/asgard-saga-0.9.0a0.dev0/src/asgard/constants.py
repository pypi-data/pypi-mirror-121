class system():

    NAME = "ASGARD"
    VERSION = NAME+" version 0.9.0-alpha"

    DESCRIPTION = "Analysis of Salmonella Genomes for Antibiotic \
    Resistance Detection and Salmonella Analysis by Genome Alignment (" + NAME + ") "
    EPILOG = "For support contact cnca@cenat.ac.cr"


class help():
    ARGUMENT_FASTQ = "path to the input fastq files"
    ARGUMENT_ACCESION = "accession ID of reference"
    ARGUMENT_ACCESSORIES = "ID of the accesory genes"
    ARGUMENT_DATABASE = "database name for the ARIBA analysis, default \
    value is argannot"
    ARGUMENT_OUTPUT_DIR = "path for the output files, use the -c \
    flag to create it in the current directory"
    ARGUMENT_CREATE_DIR = "creates output folder if doesn't \
    exist"
    ARGUMENT_OVERWRIDE = "overwrites the output files in the output directory"
    ARGUMENT_VERBOSE = "prints subcommands traces"
    ARGUMENT_CPU = "number of cpu processors available"
    ARGUMENT_MPI_DEPTH = "mpi depth for the bcftools"
    ARGUMENT_EFETCH = "Download the accession with efecth or wget"
    ARGUMENT_EFETCH_DATABASE = "Database to download the accession"
    MODE_SINGLE = 'Run a single configuration file and single checkpoint files.'
    MODE_MULTIPLE = 'Run multiple configuration files in a directory'
    CSV_FILE = "Checkpoint file to resume execution of past runs"
    CONFIG_DIRECTORY = "Directory of configuration files"
    CONFIG_FILE = "Path to ajson file containing the workflow"
    COLOR = "green"
    PREVIEW = "Show commands to be executed without running them"


class info():
    MESSAGE_FINISHED = "Process Finished"
    COLOR = "blue"


class error():
    COLOR = "red"

    PATH_CONFIG_NOT_DIRECTORY = "The path to the specified \
    directory for configuration files does not exist"
    NO_FILES = "No files present in the path:"
    CONFIG_FILES_NOT_FOUND = "No config files are not present in the path: "
    PATH_FASTQ_NOT_DIRECTORY = "The path to the specified fastq directory does not exist"
    FILES_NOT_FOUND = "No input files are not present in the path: "
    PATH_OUTPUT_NOT_DIRECTORY = "The path specified does not exist"
    FILES_UNMATCHED_PAIR = "All fastq files must come in pairs, please disable paired input files or make sure all fastq files are paired."
    FILES_UNMATCHED_NOT_PAIRS = "Some fastq files are unmatched"
    DIRECTORY_NOT_EMPTY = "The output directory is not empty\
    please select an empty directory or use the -o flag to \
    overwrite the output files"
    ARIBA_EXECUTION = "Ariba excecution error"
    DATABASE_DOWNLOAD = "Error downloading the ariba database"
    DATABASE_PREPAREREF = "Error on database preparation"
    DOWNLOAD_REQUEST = "Error in the download request, check you internet connection or your URL"
    FILE_DOWNLOAD = "Error downloading the requested file"
    ENTREZ_DOWNLOAD = "Error downloading ncbi accession fasta file using http"
    EXECUTE_PROPERTY_MISSING = "The execute property is not specified, please check your configuration file"""
    COMMAND_NOT_FOUND_CONFIG = "The command(s): %s was(where) not found in the configuration file. Please check the execute property and the name of the command in the configuration file."


class warning():
    INVALID_WORKERS_THREADS_RATIO = "More threads than workers, could reduce performance"
    WARNING_COLOR = "yellow"


# Options
DATABASES_ARIBA = ["argannot", "card", "ncbi", "megares",
                   "plasmidfinder", "resfinder", "srst2_argannot",
                   "vfdb_core", "vfdb_full", "virulencefinder"]
DATABASES_EFETCH = ["nuccore"]
