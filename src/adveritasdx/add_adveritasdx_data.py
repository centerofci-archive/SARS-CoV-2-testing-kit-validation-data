import os
import sys


dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from get_adveritasdx_data_row import get_adveritasdx_data


def add_adveritasdx_data (rows):
    rows = list(rows)

    test_ids = set()
    for row in rows:
        test_ids.add(row["test_id"])


    adveritasdx_data = get_adveritasdx_data()


    for row in adveritasdx_data:
        if row["test_id"] not in test_ids:
            print("Missing test_id in CCI data: " + row["test_id"])

            rows.append({
                "adveritasdx": row
            })

    return rows
