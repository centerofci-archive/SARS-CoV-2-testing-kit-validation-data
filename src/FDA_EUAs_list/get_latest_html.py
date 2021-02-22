from datetime import datetime
import os
import sys

import requests


dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path + "/..")

from common import DATA_DIRECTORY_EUAs



HTML_DIR = DATA_DIRECTORY_EUAs + "html_pages/"

def HTML_file_path (file_name):
    return HTML_DIR + file_name + ".htm"



def get_latest_html ():
    print("Requesting latest FDA EUAs page")
    response = requests.get("https://www.fda.gov/emergency-preparedness-and-response/mcm-legal-regulatory-and-policy-framework/emergency-use-authorization")

    response.raise_for_status()

    date_str = datetime.now().strftime("%Y-%m-%d")
    file_path_date = HTML_file_path(date_str)
    file_path_latest = HTML_file_path("latest")

    html = response.text

    print("Got latest FDA EUAs page, saving to: {}".format(file_path_date))

    with open(file_path_date, "w") as f:
        f.write(html)

    with open(file_path_latest, "w") as f:
        f.write(html)



if __name__ == "__main__":
    get_latest_html()
