import csv
import json
import os
import re
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path + "/..")

from common import get_test_id
from common.paths import (
    DATA_DIRECTORY_adveritasdx_CSVs,
    DATA_DIRECTORY_adveritasdx_parsed,
)

from check_test_ids import map_AVD_test_id_to_FDA_EUA_list_test_id



def parse_csv (csv_file_descriptor):
    raw_str = csv_file_descriptor.read()
    raw_str = (raw_str
        .replace("\u2013", "-")
        .replace("Triplex CII-CoV-1", "Triplex CII-SARS-CoV-2"))
    csv_rows = raw_str.split("\n")

    csv_reader = csv.reader(csv_rows)

    rows = []
    for raw_row in csv_reader:
        row_trimmed_cells = [cell.strip() for cell in raw_row]
        rows.append(row_trimmed_cells)

    return rows


DATA_KEY__developer_name = "Company/Organization"
DATA_KEY__test_name = "Test Name"
expected_headers = [
    "Done? (Y)",
    DATA_KEY__developer_name,
    DATA_KEY__test_name,
    "Select",
    "*URL",
    "Test Type (Lab or Kit)",
    "Country of Origin",
    "US Regulatory Status",
    "Category",
    "Authorized Setting(s) per FDA",
    "Technology",
    "Analyte",
    "Assay",
    "Specimen Type",
    "Transport Media",
    "Gene",
    "Antigen",
    "Sample Prep",
    "Detection",
    "TAT",
    "Analytical Sensitivity (LOD)",
    "LOD of FDA Reference Panel (NDU/mL)",
    "Cross- Reactivity",
    "PPA/Sensitivity",
    "PPA Sample Size",
    "PPA Specimen Type",
    "NPA/Specificity",
    "NPA Sample Size",
    "NPV @ 5% prevalence",
    "PPV@ 5% prevalence",
    "Manufacturer's Validation Notes",
    "External Quality Control",
    "Process (internal) Control",
    "Positive Control",
    "*Publications",
    "*IFU",
    "*Letter of Authorization (EUA)",
    "Creation Date",
    "Modified Date",
    "",
    "",
    "Needs Review"
]


def check_headers (data_rows):
    headers = data_rows[0]
    if headers != expected_headers:
        extra_headers = set(headers) - set(expected_headers)
        missing_headers = set(expected_headers) - set(headers)

        if len(expected_headers) != len(headers):
            print("********\n\n\nERROR: expecting {} headers but got {} headers\n\n\n********".format(
                len(expected_headers), len(headers)))
        else:
            msg = "********\n\n\nERROR: "
            if extra_headers:
                msg += "\nGot extra headers: {} ".format(extra_headers)
            if missing_headers:
                msg += "\nMissing headers: {}".format(missing_headers)

            print(msg + "\n\n\n********")

        sys.exit(1)


def clean_data (parsed_result):
    if parsed_result[1][1]:
        print("Got unexpected value: \"{}\" in row two that was expected to be empty as previously used for formatting".format(parsed_result[1][1]))
        sys.exit(1)

    # Drop the first row of headers now that we know they are the same as those we expect
    # And drop the second row which is used for formatting purposes only
    cleaned_data = parsed_result[2:]
    return cleaned_data


def data_to_json (cleaned_data):
    rows = []

    for (i, raw_row) in enumerate(cleaned_data):
        data_row = { "test_id": "", "ordinal": i }
        data_row.update(dict(zip(expected_headers, raw_row)))

        del data_row[""]

        developer_name = data_row[DATA_KEY__developer_name]
        test_name = data_row[DATA_KEY__test_name]
        test_id = get_test_id(developer_name, test_name)
        data_row["test_id"] = test_id

        rows.append(data_row)

    return rows



def map_test_ids (parsed_result):
    for row in parsed_result:
        test_id = row["test_id"]
        row["original_test_id"] = ""

        if test_id in map_AVD_test_id_to_FDA_EUA_list_test_id:
            new_test_id = map_AVD_test_id_to_FDA_EUA_list_test_id[test_id]
            row["test_id"] = new_test_id
            row["original_test_id"] = test_id


def parse_versions ():
    file_names = os.listdir(DATA_DIRECTORY_adveritasdx_CSVs)

    for file_name in file_names:
        if not file_name.endswith(".csv"):
            continue

        print("Parsing AdVeritasDx CSVs: {}".format(file_name))
        file_path = DATA_DIRECTORY_adveritasdx_CSVs + file_name
        if os.path.isdir(file_path):
            continue
        with open(file_path, "r", encoding="utf8") as f:
            parsed_result = parse_csv(f)

        check_headers(parsed_result)

        cleaned_data = clean_data(parsed_result)

        json_data = data_to_json(cleaned_data)

        print("Extracted {} rows".format(len(json_data)))

        map_test_ids(json_data)

        output_file_name = file_name.replace(".csv", ".json")
        file_path = DATA_DIRECTORY_adveritasdx_parsed + output_file_name
        with open(file_path, "w", encoding="utf8") as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)



if __name__ == "__main__":
    parse_versions()
