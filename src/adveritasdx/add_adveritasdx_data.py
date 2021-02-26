import os
import sys


dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from common.paths import DATA_DIRECTORY_EUAs_PARSED_DATA
from get_adveritasdx_data_row import get_adveritasdx_data


def add_adveritasdx_data (rows):
    rows = list(rows)

    test_ids = set()
    for row in rows:
        test_ids.add(row["test_id"])


    adveritasdx_data = get_adveritasdx_data()


    adv_test_ids_missing_in_data = []
    AVD_test_ids_to_ignored = set([
        "__",
        "7/12/2020 update__",
        "6/21/2020 update__",
        "rutgers clinical genomics laboratory-rutgers university copy__thermofisher - applied biosystems taqpath covid-19 combo kit",
        "rutgers clinical genomics laboratory at rucdr infinite biologics - rutgers university__rutgers clinical genomics laboratory taqpath sars-cov-2-assay",
        "rutgers clinical genomics laboratory-rutgers university__thermofisher - applied biosystems taqpath covid-19 combo kit",
        "autobio diagnostics co.ltd.__anti-sars-cov-2 rapid test",
    ])

    for row in adveritasdx_data:
        test_id = row["test_id"]
        if test_id not in test_ids:
            if test_id not in AVD_test_ids_to_ignored:
                adv_test_ids_missing_in_data.append(test_id)
        elif test_id in AVD_test_ids_to_ignored:
            print("Can remove test_id from 'AVD_test_ids_to_ignored' in 'add_adveritasdx_data.py': " + test_id)

    if adv_test_ids_missing_in_data:
        num = len(adv_test_ids_missing_in_data)
        print("{} test_ids from AdVeritasDx are missing in merged (CCI) data".format(num))
        ids = "\n   ".join(adv_test_ids_missing_in_data)
        print("Check the parsed FDA EUA data in {} to ensure the following test_ids from AVD are not just named something different in the rows from the parsed FDA EUA data: \n\n   {}".format(DATA_DIRECTORY_EUAs_PARSED_DATA, ids))
