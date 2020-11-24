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


def get_summarised_data ():
    data = get_merged_data()

    filtered_data = [row for row in data if row["self_declared_EUA_data"]["lod_value"]["annotations"]]

    summary = {
        "_README": "This data is generated from https://github.com/centerofci/SARS-CoV-2-testing-kit-validation-data/blob/master/src/summarised_data/summarise.py",
        "primer_probe_sequences": get_primer_probe_sequences_summary(filtered_data),
    }

    return summary


def get_primer_probe_sequences_summary (data):

    have_parsed = 0
    not_parsed = 0

    explicitly_specified = 0
    not_specified = 0
    reference_available = 0

    for row in data:
        primer_probe_sequences = row["self_declared_EUA_data"]["primer_probe_sequences"]
        parsed_value = primer_probe_sequences["parsed"]

        if parsed_value:
            have_parsed += 1

            if parsed_value == Labels.primers_and_probes__sequences__explicitly_specified:
                explicitly_specified += 1
            elif parsed_value == Labels.primers_and_probes__sequences__not_specified:
                not_specified += 1
            elif parsed_value == Labels.primers_and_probes__sequences__reference_available:
                reference_available += 1
            else:
                print("ERROR in get_primer_probe_sequences_summary, parsed_value = ", parsed_value)

        else:
            not_parsed += 1


    summary = {
        "have_parsed": have_parsed,
        "not_parsed": not_parsed,
        "explicitly_specified": explicitly_specified,
        "not_specified": not_specified,
        "reference_available": reference_available,
    }

    return summary


def store_data (data):
    with open(DATA_FILE_PATH_summarised_data, "w", encoding="utf8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


summarised_data = get_summarised_data()
store_data(summarised_data)
