import os
import sys


dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from common.paths import DATA_DIRECTORY_EUAs_PARSED_DATA
from get_adveritasdx_data_row import get_adveritasdx_data
from check_test_ids import AVD_test_ids_to_ignored



def add_adveritasdx_data (rows):
    rows = list(rows)

    test_ids = set()
    for row in rows:
        test_ids.add(row["test_id"])


    adveritasdx_data = get_adveritasdx_data()


    adv_test_ids_missing_in_data = []

    for row in adveritasdx_data:
        test_id = row["test_id"]
        if test_id not in test_ids:
            if test_id not in AVD_test_ids_to_ignored:
                adv_test_ids_missing_in_data.append(test_id)
        elif test_id in AVD_test_ids_to_ignored:
            print("Can remove test_id from 'AVD_test_ids_to_ignored': " + test_id)

    if adv_test_ids_missing_in_data:
        print("{} test_ids from AdVeritasDx are still missing in merged (CCI) data".format(
            len(adv_test_ids_missing_in_data)
        ))
