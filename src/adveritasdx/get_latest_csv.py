from datetime import datetime, timezone
import os
import sys

import requests


dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path + "/..")

from common.paths import (
    DATA_DIRECTORY_adveritasdx_CSVs,
    DATA_DIRECTORY_adveritasdx_parsed,
)



def CSV_file_path (file_name):
    return DATA_DIRECTORY_adveritasdx_CSVs + file_name + ".csv"



def get_latest_csv ():
    print("Requesting latest AdVeritasDx CSV page")

    google_doc_id = get_google_doc_id()
    url = "https://docs.google.com/spreadsheets/d/{}/export?format=csv&gid=0".format(google_doc_id)
    response = requests.get(url)

    response.raise_for_status()

    datetime_str = datetime.now(timezone.utc).strftime("%Y-%m-%d--%H-%M")
    file_path_datetime = CSV_file_path(datetime_str)
    file_path_latest = CSV_file_path("latest")

    response.encoding = "utf-8"
    csv_text = response.text

    print("Got latest AdVeritasDx CSV page, saving to: {}".format(file_path_datetime))

    with open(file_path_datetime, "w", encoding="utf8") as f:
        f.write(csv_text)

    with open(file_path_latest, "w", encoding="utf8") as f:
        f.write(csv_text)



def get_google_doc_id ():
    file_path = dir_path + "/secret_google_doc_id.txt"
    if not os.path.isfile(file_path):
        print("Must create a file at \"{}\"".format(file_path))
        sys.exit(1)

    with open(file_path, "r") as f:
        return f.read().strip()



if __name__ == "__main__":
    get_latest_csv()
