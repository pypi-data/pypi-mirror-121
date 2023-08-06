from . import utils
import time
import shutil
import requests
from .constants import error


def create_file(new_file, force=None):
    if not force:
        force = False
    utils.get_file(new_file, create_parents=force)


def create_directory(directory_path, force=True):
    if not force:
        force = False
    utils.get_dir(directory_path, create_if_missing=force)


def entrez_download(database, accession, output_file, filetype=None,
                    mode=None):
    if not filetype:
        filetype = "fasta"

    if not mode:
        mode = "text"

    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db={database}&id={accession}&rettype={filetype}&retmode={mode}"

    if not download_file(url, output_file):
        print(error.FILE_DOWNLOAD)
        raise SystemExit(error.ENTREZ_DOWNLOAD)


def merge_files(files, file_output):
    with open(file_output, 'wb') as outfile:
        for file in files:
            if file != file_output:
                with open(file, 'rb') as input_file:
                    shutil.copyfileobj(input_file, outfile)


def download_file(url, output_file):

    try:
        request = requests.get(url, allow_redirects=True)
        request.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(error.DOWNLOAD_REQUEST)
        raise SystemExit(e)
    if (request.ok):
        file = open(output_file, "wb")
        file.write(request.content)
        file.close()
        time.sleep(4)  # Time to write all data to disk before its use.
        return True
    return False


def text_replace(file, output_file, replace_text, new_text):
    new_file = open(file, "rt")
    data = new_file.read()
    new_file.close()

    data = data.replace(replace_text, new_text)

    new_file = open(output_file, "wt")
    new_file.write(data)
    new_file.close()
