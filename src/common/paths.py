from datetime import datetime
import json
import os
import re


dir_path = os.path.dirname(os.path.realpath(__file__))
DATA_DIR_PATH = dir_path + "/../../data/"


ANOT8_VAULT_CONFIG = DATA_DIR_PATH + "anot8_vault_config.json"


DATA_DIRECTORY_adveritasdx = DATA_DIR_PATH + "adveritasdx/"
DATA_DIRECTORY_adveritasdx_CSVs = DATA_DIRECTORY_adveritasdx + "csv_from_adveritasdx/"
DATA_DIRECTORY_adveritasdx_parsed = DATA_DIRECTORY_adveritasdx + "parsed/"


DATA_DIRECTORY_EUAs = DATA_DIR_PATH + "FDA-EUA/"
DATA_DIRECTORY_EUA_PDFs = DATA_DIRECTORY_EUAs + "PDFs/"
DATA_DIRECTORY_EUAs_PARSED_DATA = DATA_DIRECTORY_EUAs + "parsed/"
DATA_FILE_PATH_EUAs_LATEST_PARSED_DATA = DATA_DIRECTORY_EUAs_PARSED_DATA + "latest.json"


DATA_DIRECTORY_FDA_reference_panel = DATA_DIR_PATH + "FDA_reference_panel/"
DATA_FILE_PATH_FDA_reference_panel_LATEST_PARSED_DATA = DATA_DIRECTORY_FDA_reference_panel + "parsed/latest.json"


DATA_DIRECTORY_merged_data = DATA_DIR_PATH + "merged_data/"
DATA_FILE_PATH_merged_data = DATA_DIRECTORY_merged_data + "latest.json"


DATA_DIRECTORY_summarised_data = DATA_DIR_PATH + "summarised_data/"
DATA_FILE_PATH_summarised_data = DATA_DIRECTORY_summarised_data + "latest.json"


def get_FDA_file_id_from_FDA_url (FDA_url):
    matches = re.match("https://www.fda.gov/media/(\d+)/download", FDA_url)
    try:
        file_id = matches.groups()[0]
    except Exception as e:
        print("failed on url: ", FDA_url)
        raise e

    return file_id
