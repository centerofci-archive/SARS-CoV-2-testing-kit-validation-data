from datetime import datetime
import json
import os
import re


dir_path = os.path.dirname(os.path.realpath(__file__))
DATA_DIR_PATH = dir_path + "/../../data/"


ANOT8_VAULT_CONFIG = DATA_DIR_PATH + "anot8_vault_config.json"


DATA_DIRECTORY_EUAs = DATA_DIR_PATH + "FDA-EUA/"
DATA_DIRECTORY_EUA_PDFs = DATA_DIRECTORY_EUAs + "PDFs/"
DATA_FILE_PATH_EUAs_LATEST_PARSED_DATA = DATA_DIRECTORY_EUAs + "parsed/latest.json"


DATA_DIRECTORY_FDA_reference_panel = DATA_DIR_PATH + "FDA_reference_panel/"
DATA_FILE_PATH_FDA_reference_panel_LATEST_PARSED_DATA = DATA_DIRECTORY_FDA_reference_panel + "parsed/latest.json"


DATA_DIRECTORY_merged_data = DATA_DIR_PATH + "merged_data/"
DATA_FILE_PATH_merged_data = DATA_DIRECTORY_merged_data + "latest.json"


DATA_DIRECTORY_summarised_data = DATA_DIR_PATH + "summarised_data/"
DATA_FILE_PATH_summarised_data = DATA_DIRECTORY_summarised_data + "latest.json"


ANOT8_ORG_NAMING_AUTHORITY_ID = "1772"
ANOT8_ORG_VAULT_ID = "2"


def get_FDA_EUA_pdf_file_id_from_FDA_url (FDA_url):
    matches = re.match("https://www.fda.gov/media/(\d+)/download", FDA_url)
    try:
        file_id = matches.groups()[0]
    except Exception as e:
        print("failed on url: ", FDA_url)
        raise e

    return file_id


def get_FDA_EUA_pdf_file_path_from_FDA_url (FDA_url, add_datetime = ""):
    file_id = get_FDA_EUA_pdf_file_id_from_FDA_url(FDA_url)

    if type(add_datetime) is bool:
        dt = datetime.now()
        add_datetime = format_datetime_as_version(dt)

    file_path = DATA_DIRECTORY_EUAs + "PDFs/{}{}.pdf".format(add_datetime, file_id)

    return file_path


def format_datetime_as_version (dt):
    return dt.strftime("%Y-%m-%d__%H-%M__")


def get_anot8_org_file_id_from_FDA_url (FDA_url, error_on_absence=True):
    full_file_path = get_FDA_EUA_pdf_file_path_from_FDA_url(FDA_url)
    partial_file_path = full_file_path.replace(DATA_DIR_PATH, "")
    anot8_org_file_id = get_anot8_org_id_for_file_path(partial_file_path, error_on_absence=error_on_absence)
    return anot8_org_file_id


file_path_to_anot8_org_id_map = None
anot8_config = None
def get_map_of_file_path_to_anot8_org_id ():
    global file_path_to_anot8_org_id_map
    global anot8_config

    with open(ANOT8_VAULT_CONFIG, "r", encoding="utf8") as f:
        new_anot8_config = json.load(f)

    if anot8_config != new_anot8_config:
        file_path_to_anot8_org_id_map = dict()
        anot8_config = new_anot8_config

        for (anot8_org_file_id, file_path) in anot8_config["DO_NOT_EDIT_auto_generated_fields"]["id_to_relative_file_name"].items():
            if file_path in file_path_to_anot8_org_id_map:
                raise Exception("Duplicate file_path: {}".format(file_path))

            file_path_to_anot8_org_id_map[file_path] = anot8_org_file_id

    return file_path_to_anot8_org_id_map


def get_anot8_org_id_for_file_path (file_path, error_on_absence=True):
    file_to_id_map = get_map_of_file_path_to_anot8_org_id()

    anot8_org_id = None
    if file_path in file_to_id_map:
        anot8_org_id = file_to_id_map[file_path]

    elif error_on_absence:
        raise Exception("file_path not found in anot8 file_to_id_map: {}".format(file_path))

    return anot8_org_id


def get_anot8_org_permalink_from_FDA_url (FDA_url, error_on_absence=True):
    anot8_org_file_id = get_anot8_org_file_id_from_FDA_url(FDA_url, error_on_absence=error_on_absence)

    if anot8_org_file_id is None:
        return None

    return "https://anot8.org/{}.{}/{}".format(
        ANOT8_ORG_NAMING_AUTHORITY_ID,
        ANOT8_ORG_VAULT_ID,
        anot8_org_file_id
    )
