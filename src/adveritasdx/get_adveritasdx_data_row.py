from enum import Enum, auto

import csv
import json
import os
import re
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))

latest_data_file_path = os.path.join(dir_path, "../../data/adveritasdx/parsed/latest.json")


def get_adveritasdx_data ():
    with open(latest_data_file_path, "r", encoding="utf8") as f:
        adveritas_dx_data = json.load(f)

    return adveritas_dx_data



adveritas_dx_data_by_test_id = None
def get_adveritas_dx_data_by_test_id ():
    global adveritas_dx_data_by_test_id

    if adveritas_dx_data_by_test_id is None:
        adveritas_dx_data_by_test_id = dict()

        data = get_adveritasdx_data()

        for row in data:
            test_id = row["test_id"]
            del row["test_id"]
            adveritas_dx_data_by_test_id[test_id] = row

    return adveritas_dx_data_by_test_id



def get_adveritasdx_data_row (test_id):
    data_row = get_adveritas_dx_data_by_test_id().get(test_id, None)

    if data_row is None:
        print("Missing test_id in AdVeritasDx data: " + test_id)

    return data_row
