from enum import Enum, auto

import csv
import json
import os
import re
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))

latest_data_file_path = os.path.join(dir_path, "../../data/adveritasdx/parsed/latest.json")


with open(latest_data_file_path, "r") as f:
    adveritas_dx_data = json.load(f)

adveritas_dx_data_by_test_id = dict()
for row in adveritas_dx_data:
    test_id = row["test_id"]
    del row["test_id"]
    adveritas_dx_data_by_test_id[test_id] = row


def get_adveritasdx_data_row (test_id):
    data_row = adveritas_dx_data_by_test_id.get(test_id, None)

    if data_row is None:
        print("Missing test_id in AdVeritasDx data: " + test_id)

    return data_row
