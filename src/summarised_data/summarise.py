##
#
# Takes merged data and produces a summary
#
##
import json
import math
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path + "/..")


from common import (
    DATA_FILE_PATH_summarised_data,
    DATA_FILE_PATH_merged_data,
    get_merged_data,
    Labels,
)

from primer_probe_sequences import (
    get_primer_probe_sequences_summary,
    get_top_10_tests_primer_probe_sequences_summary,
)
from lod_units import get_lod_units
from lod_viral_material import get_lod_viral_material


def get_summarised_data ():
    data = get_merged_data()

    filtered_data = [row for row in data if row["self_declared_EUA_data"]["lod_value"]["annotations"]]

    summary = {
        "_README": "This data is generated from https://github.com/centerofci/SARS-CoV-2-testing-kit-validation-data/blob/master/src/summarised_data/summarise.py",
        "primer_probe_sequences": get_primer_probe_sequences_summary(filtered_data),
        "primer_probe_sequences_in_top_10_test_EUAs": get_top_10_tests_primer_probe_sequences_summary(filtered_data, False),
        "weighted_primer_probe_sequences_in_top_10_test_EUAs": get_top_10_tests_primer_probe_sequences_summary(filtered_data, True),
        "lod_units": get_lod_units(filtered_data, False),
        "lod_units_top_10_tests_weighted": get_lod_units(filtered_data, True),
        "lod_viral_material": get_lod_viral_material(filtered_data, False),
        "lod_viral_material_top_10_tests_weighted": get_lod_viral_material(filtered_data, True),
    }

    return summary


def store_data (data):
    with open(DATA_FILE_PATH_summarised_data, "w", encoding="utf8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


summarised_data = get_summarised_data()
store_data(summarised_data)
