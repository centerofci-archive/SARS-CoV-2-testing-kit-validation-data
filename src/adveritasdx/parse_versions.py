from enum import Enum, auto

import csv
import json
import os
import re
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path + "/../common")

from get_test_id import get_test_id

data_path = os.path.join(dir_path, "../../data/adveritasdx")
csv_from_adveritasdx_dir = os.path.join(data_path, "csv_from_adveritasdx")
parsed_dir = os.path.join(data_path, "parsed")


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


map_reference_panel_test_id_to_EUA_list_test_id = {
"centers for disease control and prevention's (cdc)__cdc 2019-novel coronavirus (2019-ncov) real-time rt-pcr diagnostic panel (cdc)": "cdc__cdc 2019-novel coronavirus (2019-ncov) real-time rt-pcr diagnostic panel",
"wadsworth center, new york state department of public health's (cdc)__new york sars-cov-2 real-time reverse transcriptase (rt)-pcr diagnostic panel": "wadsworth center, new york state department of health's (cdc)__new york sars-cov-2 real-time reverse transcriptase (rt)-pcr diagnostic panel",
"abbott molecular__abbott realtime sars-cov-2 eua test": "abbott molecular__abbott realtime sars-cov-2 assay",
"primerdesign ltd.__genesig real-time pcr covid-2019 assay": "primerdesign ltd__primerdesign ltd covid-19 genesig real-time pcr assay",
"avellino lab usa, inc.__avellino sars-cov-2/covid-19 (avellinocov2)": "avellino lab usa, inc.__avellinocov2 test",
"luminex molecular diagnostics, inc.__nxtagcov extended panel assay": "luminex molecular diagnostics, inc.__nxtag cov extended panel assay",
"cellex inc.__qsars-cov-2 igm/igg rapid test": "cellex inc.__qsars-cov-2 igg/igm rapid test",
"ipsum diagnostics__cov-19 idx assay": "ipsum diagnostics, llc__cov-19 idx assay",
"becton, dickinson & company (bd), biogx__biogx sars-cov-2 reagents for bd max system": "becton, dickinson & company (bd)__biogx sars-cov-2 reagents for bd max system",
"co-diagnostics, inc.__logix smart coronavirus covid-19": "co-diagnostics, inc.__logix smart coronavirus disease 2019 (covid-19) kit",
"viracor eurofins clinical diagnostics__coronavirus sars-cov-2 rt-pcr assay": "viracor eurofins clinical diagnostics__viracor sars-cov-2 assay",
"diacarta, inc.__quantivirus sars-cov-2 test": "diacarta, inc.__quantivirus sars-cov-2 test kit",
"stanford health care clinical virology laboratory__stanford sars-cov-2 assay": "stanford health care clinical virology laboratory__sars-cov-2 rt-pcr assay",
# Missing from AdVeritasDx
"": "infinity biologix llc__infinity biologix taqpath sars-cov-2 assay",
"specialty diagnostic (sdi) laboratories__sdi sars-cov-2 assay": "specialty diagnostic (sdi) laboratories__sdi sars-cov-2 assayletter granting inclusion",
"infectious diseases diagnostics laboratory (iddl), boston children’s hospital__childrens-altona-sars-cov-2 assay": "infectious diseases diagnostics laboratory (iddl), boston children's hospital__childrens-altona-sars-cov-2 assay",
"trax management services inc. (mfd by procomcure biotech gmbh)__phoenixdx 2019-cov": "trax management services inc.__phoenixdx 2019-cov",
"seegene__allplex 2019-ncov assay": "seegene, inc.__allplex 2019-ncov assay",
"altona diagnostics gmbh__realstar sars-cov02 rt-pcr kits": "altona diagnostics gmbh__realstar sars-cov02 rt-pcr kits u.s.",
"diasorin inc.__liason sars-cov-2 s1/s2 igg": "diasorin inc.__liaison sars-cov-2 s1/s2 igg",
"ortho clinical diagnostics, inc.__vitros immunodiagnostic products anti-sars-cov-2 igg reagent pack": "ortho-clinical diagnostics, inc.__vitros immunodiagnostic products anti-sars-cov-2 igg reagent pack",
"bio-rad laboratories, inc.__platelia sars-cov-2 total ab assay": "bio-rad laboratories__platelia sars-cov-2 total ab assay",
"bio-rad laboratories, inc.__bio-rad sars cov-2-ddpcr test": "bio-rad laboratories, inc.__bio-rad sars-cov-2 ddpcr test",
"biofire diagnostics, llc__biofire respiratory panel 2.1": "biofire diagnostics, llc__biofire respiratory panel 2.1 (rp2.1)",
# Correct name in AdVeritasDx
# "columbia university laboratory of personalized genomic medicine__triplex cii-cov-2 rrt-pcr test": "columbia university laboratory of personalized genomic medicine__triplex cii-sars-cov-2 rrt-pcr test",
"genematrix__neoplex covid-19 detection kit": "genematrix, inc.__neoplex covid-19 detection kit",
"fulgent therapeutics llc__fulgent covid-19 by rt-pcr test": "fulgent therapeutics, llc__fulgent covid-19 by rt-pcr test",
"assurance__assurance sars-cov-2 panel": "assurance scientific laboratories__assurance sars-cov-2 panel",
"color genomics, inc.__color sars cov-2 diagnostic assay": "color genomics, inc.__color sars-cov-2 rt-lamp diagnostic assay",
"seasun biomaterials, inc.__aq-top covid-19 rapid detection kit": "seasun biomaterials, inc.__aq-top covid-19 rapid detection",
"exact sciences laboratories__exact sciences sars-cov-2 (n gene detection) test": "exact sciences laboratories__sars-cov-2 (n gene detection) test",
# Missing from AdVeritasDx
"": "roche diagnostics__elecsys il-6",
"helix opco llc (dba helix)__helix covid-19 test": "helix opco llc__helix covid-19 test",
"color genomics, inc.__color covid-19 test unmonitored collection kit": "color genomics, inc.__color covid-19 test self-swab collection kit",

# "quadrant biosciences inc.__clarifi covid-19 test kit": "quadrant biosciences inc.__clarifi covid-19 test kit 09/22/2020",
# "": "vela operations singapore pte. ltd.__virokey sars-cov-2 rt-pcr test v2.0 09/22/2020",
# "": "clear labs, inc.__clear dx sars-cov-2 test 09/23/2020",
# "": "jiangsu well biotech co., ltd.__orawell igm/igg rapid test 09/23/2020",
# "": "cepheid__xpert xpress sars-cov-2/flu/rsv 09/24/2020",
}


def map_test_ids (parsed_result):
    # Ignore headers
    parsed_result = parsed_result[1:]

    for row in parsed_result:
        test_id = row["test_id"]

        if test_id in map_reference_panel_test_id_to_EUA_list_test_id:
            test_id = map_reference_panel_test_id_to_EUA_list_test_id[test_id]
            row["test_id"] = test_id


def parse_versions ():
    file_names = os.listdir(csv_from_adveritasdx_dir)

    for file_name in file_names:
        print("Parsing AdVeritasDx CSVs: {}".format(file_name))
        file_path = csv_from_adveritasdx_dir + "/" + file_name
        if os.path.isdir(file_path):
            continue
        with open(file_path, "r", encoding="utf8") as f:
            parsed_result = parse_csv(f)

        check_headers(parsed_result)

        cleaned_data = clean_data(parsed_result)

        json_data = data_to_json(cleaned_data)

        print("Extracted {} rows".format(len(json_data)))

        map_test_ids(json_data)

        is_latest = "latest" in file_name

        output_file_name = file_name.replace(".csv", ".json").replace("latest-", "")
        with open(parsed_dir + "/" + output_file_name, "w", encoding="utf8") as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)

        if is_latest:
            with open(parsed_dir + "/latest.json", "w", encoding="utf8") as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)


parse_versions()
