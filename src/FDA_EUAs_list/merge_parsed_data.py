import json
import os
import re
import sys


dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path + "/..")

from common.paths import (
    DATA_DIRECTORY_EUAs_PARSED_DATA,
    get_FDA_file_id_from_FDA_url,
    ANOT8_VAULT_CONFIG,
)
from common.data_compression import flat_list_to_json_data
from common import filter_for_urls



expected_headers = [
    "test_id",
    "Date EUA First Issued",
    "Most recent revision",
    "Entity",
    "Diagnostic name",
    "Most Recent Letter of Authorization (URL to PDF)",
    "Technology",
    "Authorized Setting(s)",
    "Fact Sheet for Healthcare Providers (HCP) (URL to PDF)",
    "Fact Sheet for Patients / Recipients (URL to PDF)",
    "Information for Use (IFU) (URL to PDF)",
    "Emergency Use Authorisation (URL to PDF)",
    "Amendments and Other Documents (PDF)"
]


def get_temporal_fda_eua_parsed_data ():
    file_names = get_file_names_of_fda_eua_parsed_data()

    json_fda_eua_parsed_data = get_all_json_fda_eua_parsed_data(file_names)
    make_all_relevant_urls_unique(json_fda_eua_parsed_data)
    add_relative_file_infos(json_fda_eua_parsed_data)

    return json_fda_eua_parsed_data



def get_file_names_of_fda_eua_parsed_data ():
    file_names = os.listdir(DATA_DIRECTORY_EUAs_PARSED_DATA)

    json_file_names = []
    for file_name in file_names:
        if file_name == "latest.json":
            # No need to include as identical data already present in other json file with date
            continue

        if file_name == "merged.json":
            continue

        if ".json" not in file_name:
            continue

        json_file_names.append(file_name)

    json_file_names = sorted(json_file_names)
    return json_file_names



def get_all_json_fda_eua_parsed_data (file_names):
    json_fda_eua_parsed_data = []
    json_fda_eua_parsed_data_by_test_id = dict()

    unfound_test_ids_by_file_name = dict()
    unfound_test_ids = set()

    for file_name in file_names:
        snapshot_date = file_name.replace(".json", "")
        json_data = get_json_fda_eua_parsed_data(file_name)

        for row in json_data:
            test_id = row["test_id"]
            if is_new_test(snapshot_date, test_id):
                row["all_relevant_urls"] = filter_for_urls(row)
                row["present_in_snap_shots"] = [snapshot_date]
                json_fda_eua_parsed_data_by_test_id[test_id] = row
                json_fda_eua_parsed_data.append(row)
                continue


            if test_id not in json_fda_eua_parsed_data_by_test_id:
                test_id = map_new_to_old_test_id(snapshot_date, test_id)
                row["test_id"] = test_id

            if test_id not in json_fda_eua_parsed_data_by_test_id:
                if test_id in unfound_test_ids:
                    continue
                if file_name not in unfound_test_ids_by_file_name:
                    unfound_test_ids_by_file_name[file_name] = []
                unfound_test_ids_by_file_name[file_name].append(test_id)
                unfound_test_ids.add(test_id)
                continue

            existing_row = json_fda_eua_parsed_data_by_test_id[test_id]
            existing_row.update(row)
            existing_row["all_relevant_urls"] += filter_for_urls(row)
            existing_row["present_in_snap_shots"] += [snapshot_date]

    error_and_exit_on_unfound_test_ids(unfound_test_ids_by_file_name)

    for row in json_fda_eua_parsed_data:
        seen_urls = set()
        unique_urls = []
        for url in row["all_relevant_urls"]:
            if url in seen_urls:
                continue
            unique_urls.append(url)
            seen_urls.add(url)

        row["all_relevant_urls"] = unique_urls

    return json_fda_eua_parsed_data



def error_and_exit_on_unfound_test_ids (unfound_test_ids_by_file_name):
    if unfound_test_ids_by_file_name:
        print("Could not find the following test_ids in any of the previous FDA EUA parsed data ({}).".format(DATA_DIRECTORY_EUAs_PARSED_DATA))
        print("Go through each of the following test_ids and make sure they are new tests or renaming of old tests.  i.e.:\n\n 0. Copy and paste the below code into `new_tests` dictionary {file} \n 1. Open the most recent and the preceeding data/FDA-EUA/parsed/202d-dd-dd.json file.\n 2. Then search for the test manufacturer.\n 3. If more occurences in newer file than older file, assume this means it is a new test rather than a renaming of an older test.\n 4. Uncomment corresponding line in the newly added dictionary in `new_tests`.\n 5. Otherwise if not a new test then add to `custom_test_id_map`".format(file=__file__))

    for file_name, test_ids in unfound_test_ids_by_file_name.items():
        date = file_name.replace(".json", "")
        print("\nNew test ids from file {}:\n\n    \"{}\": set([".format(file_name, date))
        for test_id in test_ids:
            print("        # \"{}\",".format(test_id))
        print("    ]),")

    if unfound_test_ids_by_file_name:
        print("\nExiting as one or more test_id not found.  These are for new tests that needs to be added to the sets of test_ids stored in new_tests but may also be a change of test name.")
        sys.exit(1)



def make_all_relevant_urls_unique (json_fda_eua_parsed_data):
    for row in json_fda_eua_parsed_data:
        row["all_relevant_urls"] = sorted(list(set(row["all_relevant_urls"])))



def add_relative_file_infos (json_fda_eua_parsed_data):
    FDA_file_id_to_versioned_file_infos_map = get_FDA_file_id_to_versioned_file_info_map()

    for row in json_fda_eua_parsed_data:
        all_relative_file_infos = []
        for url in row["all_relevant_urls"]:
            FDA_file_id = get_FDA_file_id_from_FDA_url(url)

            relative_file_infos = get_versioned_relative_file_infos_for_FDA_file_id(FDA_file_id, FDA_file_id_to_versioned_file_infos_map)

            all_relative_file_infos += relative_file_infos

        # 1. may contain files that are not related to this test: because the FDA does not make this easy by deleting files and then uploading completely different files to the same file id
        # 2. may not contain all files, or versions of files that are related to this test
        # 3. may contain files that have no annotations on them yet
        row["relevant_relative_file_infos"] = all_relative_file_infos



def get_IFU_or_EUA_URL_from_row (row):
    IFUs = row["Information for Use (IFU) (URL to PDF)"]
    url_to_IFU_or_EUA = IFUs[0] if IFUs else row["Emergency Use Authorisation (URL to PDF)"]
    return url_to_IFU_or_EUA



def get_json_fda_eua_parsed_data (file_name):
    file_path = DATA_DIRECTORY_EUAs_PARSED_DATA + file_name
    with open(file_path, "r", encoding="utf8") as f:
        fda_eua_parsed_data = json.load(f)

    headers = fda_eua_parsed_data[0]
    if headers != expected_headers:
        raise Exception("Actual and expected headers for fda_eua_parsed data are different: {} != {}".format(headers, expected_headers))

    json_fda_eua_parsed_data = flat_list_to_json_data(fda_eua_parsed_data[1:], headers=headers)
    return json_fda_eua_parsed_data


new_tests = {
    "2021-01-22": set([
        "genmark diagnostics, inc.__eplex respiratory pathogen panel 2",
        "access bio, inc.__carestart covid-19 antigen test",
        "beckman coulter, inc.__access sars-cov-2 igm",
        "genalyte, inc.__maverick sars-cov-2 multi-antigen serology panel v2",
        "spectrum solutions llc__sdna-1000 saliva collection device",
        "abbott laboratories inc.__advisedx sars-cov-2 igm",
        "dna genotek inc.__omnigene·oral om-505 and ome-505 (omnigene·oral) saliva collection devices",
        "lumiradx uk ltd.__lumiradx sars-cov-2 rna star complete",
        "clinical enterprise, inc.__empowerdx at-home covid-19 pcr test kit",
        "binx health, inc.__binx health at-home nasal swab covid-19 sample collection kit",
        "celltrion usa, inc.__sampinute covid-19 antigen mia",
        "agena bioscience, inc.__massarray sars-cov-2 panel",
        "quansys biosciences, inc.__q-plex sars-cov-2 human igg (4 plex)",
        "dna genotek inc.__oracollect∙rna or-100 and oracollect∙rna ore-100 saliva collection devices",
        "genscript usa inc.__cpass sars-cov-2 neutralization antibody detection kit",
        "lucira health, inc.__lucira covid-19 all-in-one test kit",
        "innovita (tangshan) biological technology co., ltd.__innovita 2019-ncov ab test (colloidal gold)",
        "gravity diagnostics, llc__gravity diagnostics sars-cov-2 rt-pcr assay",
        "rapidrona, inc.__rapidrona self-collection kit",
        "kantaro biosciences, llc__covid-seroklir, kantaro semi-quantitative sars-cov-2 igg antibody kit",
        "roche diagnostics, inc.__elecsys anti-sars-cov-2 s",
        "cepheid__xpert omni sars-cov-2",
        "quest diagnostics infectious disease, inc.__quest diagnostics rc covid-19+flu rt-pcr",
        "luminostics, inc.__clip covid rapid antigen test",
        "laboratory corporation of america (labcorp)__pixel by labcorp covid-19 test home collection kit",
        "researchdx, inc., dba pacific diagnostics__pacificdx covid-19",
        "acon laboratories, inc.__acon sars-cov-2 igg/igm rapid test",
        "rca laboratory services llc dba genetworx__genetworx covid-19 nasal swab test",
        "hologic, inc.__aptima sars-cov-2/flu assay",
        "abbott diagnostics scarborough, inc.__binaxnow covid-19 ag card home test",
        "ellume limited__ellume covid-19 home test",
        "materials and machines corporation of america (dba matmacorp, inc.)__matmacorp covid-19 2sf test",
        "siemens healthcare diagnostics inc.__advia centaur il6 assay",
        "quidel corporation__quickvue sars antigen test",
        "cepheid__xpert xpress sars-cov-2 dod",
        "quanterix corporation__simoa semi-quantitative sars-cov-2 igg antibody test",
        "quidel corporation__solana sars-cov-2 assay",
        "nirmidas biotech, inc.__midaspot covid-19 antibody combo detection kit",
        "quanterix corporation__simoa sars-cov-2 n protein antigen test",
        "siemens healthcare diagnostics inc.__dimension exl sars‑cov‑2 igg (cv2g)",
        "siemens healthcare diagnostics inc.__dimension vista sars‑cov‑2 igg (cov2g)",
        "ortho clinical diagnostics, inc.__vitros immunodiagnostic products sars-cov-2 antigen reagent pack",
        "phadia ab__elia sars-cov-2-sp1 igg test",
        "advaite, inc.__rapcov rapid covid-19 test",
        "sml genetree co., ltd.__ezplex sars-cov-2 g kit",
        "united biomedical, inc.__ubi sars-cov-2 elisa",
        "bio-rad laboratories, inc.__bio-rad reliance sars-cov-2 rt-pcr assay kit",
    ]),
    "2021-02-02": set([
        "ambry genetics laboratory__ambry covid-19 rt-pcr test"
    ]),
    "2021-02-08": set([
        "hospital of the university of pennsylvania__bd max covid-19 assay",
        "inno diagnostics reference laboratory, ponce medical school__pmsf-inno sars-cov-2 rt-pcr test",
        "clinomics usa inc.__clinomics triodx rt-pcr covid-19 test",
        "princ.eton biomeditech corp.__status covid-19/flu",
    ]),
    "2021-02-22": set([
        "visby medical, inc.__visby medical covid-19 point of care test",
        "becton, dickinson and company (bd)__bd sars-cov-2/flu for bd max system",
        "thermo fisher scientific__taqpath covid-19, flua, flub combo kit",
        "grifols diagnostic solutions inc.__procleix sars-cov-2 assay",
        "immunodiagnostic systems ltd.__ids sars-cov-2 igg",
        "bio-rad laboratories, inc.__bio-rad reliance sars-cov-2/flua/flub rt-pcr assay kit",
        "gravity diagnostics, llc__gravity diagnostics sars-cov-2 rt-pcr for use with dtc kits",
        "assurance scientific laboratories__assurance sars-cov-2 panel dtc",
        "everlywell, inc.__everlywell covid-19 test home collection kit dtc",
    ]),
    "2021-03-08": set([
        "color health, inc.__color covid-19 test self-swab collection kit",
        "university of illinois office of the vice president for economic development and innovation__covidshield",
        "viracor eurofins clinical diagnostics__viracor sars-cov-2 assay dtc",
        "abbott laboratories inc.__advisedx sars-cov-2 igg ii",
        "quidel corporation__quickvue at-home covid-19 test",
        "luminex molecular diagnostics, inc.__nxtag respiratory pathogen panel + sars-cov-2",
        "abbott molecular inc.__alinity m resp-4-plex",
        "clinical research sequencing platform (crsp), llc at the broad institute of mit and harvard__crsp sars-cov-2 real-time reverse transcriptase (rt)-pcr diagnostic assay (version 3)",
        "adaptive biotechnologies corporation__t-detect covid test",
        "cue health inc.__cue covid-19 test for home and over the counter (otc) use",
    ]),
}
def is_new_test (snapshot_date, test_id):
    if snapshot_date == "2020-10-08":
        return True

    return test_id in new_tests.get(snapshot_date, set())



# Maps from newer to older (canonical) ids.
custom_test_id_map_2021_01_22 = {
    "stanford health care clinical virology laboratory__sars-cov-2 rt-pcr assay": "stanford health care clinical virology laboratory__stanford sars-cov-2 assay",

    "ortho-clinical diagnostics, inc.__vitros immunodiagnostic products anti-sars-cov-2 igg reagent pack": "ortho-clinical diagnostics, inc.__vitros immunodiagnostic products anti-sars-cov-2 igg reagent",

    "color genomics, inc.__color sars-cov-2 rt-lamp diagnostic assay": "color genomics, inc.__color genomics sars-cov-2 rt-lamp diagnostic assay",

    "helix opco llc__helix covid-19 test": "helix opco llc (dba helix)__helix covid-19 test",
}
custom_test_id_map_2021_03_08 = {
    **custom_test_id_map_2021_01_22,
    "letsgetchecked, inc.__letsgetchecked coronavirus (covid-19) test": "privapath diagnostics, inc.__letsgetchecked coronavirus (covid-19) test",

    "clinical enterprise, inc.__empowerdx covid-19 home collection kit dtc": "clinical enterprise, inc.__empowerdx at-home covid-19 pcr test kit",
}
custom_test_id_map = {
    "2021-01-22": custom_test_id_map_2021_01_22,
    "2021-02-02": custom_test_id_map_2021_01_22,
    "2021-02-08": custom_test_id_map_2021_01_22,
    "2021-02-22": custom_test_id_map_2021_01_22,
    "2021-03-08": custom_test_id_map_2021_03_08,
}
def map_new_to_old_test_id (snapshot_date, test_id):
    return custom_test_id_map.get(snapshot_date, {}).get(test_id, test_id)



def get_versioned_relative_file_infos_for_FDA_file_id (FDA_file_id, FDA_file_id_to_versioned_file_infos_map, error_on_absence=True):

    versioned_relative_file_infos = []
    if FDA_file_id in FDA_file_id_to_versioned_file_infos_map:
        versioned_relative_file_infos = FDA_file_id_to_versioned_file_infos_map[FDA_file_id]

    elif error_on_absence:
        print("FDA_file_id \"{}\" not found in FDA_file_id_to_versioned_file_infos_map".format(FDA_file_id))
        print("\nYou likely just need to visit:  http://localhost:5003/vault/sars-2-diagnostics  to fresh (update) the list of files in data/anot8_vault_config.json")
        sys.exit(1)

    return versioned_relative_file_infos



FDA_file_id_to_versioned_file_infos_map = None
anot8_config = None
def get_FDA_file_id_to_versioned_file_info_map ():
    global FDA_file_id_to_versioned_file_infos_map
    global anot8_config

    with open(ANOT8_VAULT_CONFIG, "r", encoding="utf8") as f:
        new_anot8_config = json.load(f)

    if anot8_config != new_anot8_config:
        FDA_file_id_to_versioned_file_infos_map = dict()
        anot8_config = new_anot8_config

        for (anot8_org_file_id, file_path) in anot8_config["DO_NOT_EDIT_auto_generated_fields"]["id_to_relative_file_name"].items():
            FDA_file_id = versioned_file_path_to_FDA_file_id(file_path)

            if not FDA_file_id:
                # Will be a non-versioned file_path like: "papers/2007_Tang ... .pdf"
                continue

            if FDA_file_id not in FDA_file_id_to_versioned_file_infos_map:
                FDA_file_id_to_versioned_file_infos_map[FDA_file_id] = []

            file_info = { "file_path": file_path, "anot8_org_file_id": anot8_org_file_id}
            FDA_file_id_to_versioned_file_infos_map[FDA_file_id].append(file_info)

    return FDA_file_id_to_versioned_file_infos_map



def versioned_file_path_to_FDA_file_id (file_path):
    match = re.match("FDA-EUA\/PDFs\/\d{4}-\d{2}-\d{2}__\d{2}-\d{2}__(\d+).pdf", file_path)

    is_versioned_file_path = bool(match)

    return match.groups()[0] if is_versioned_file_path else None



def write_merged_data():
    merged_data = get_temporal_fda_eua_parsed_data()
    with open(DATA_DIRECTORY_EUAs_PARSED_DATA + "/merged.json", "w", encoding="utf8") as f:
        json.dump(merged_data, f, indent=2, ensure_ascii=False)



if __name__ == "__main__":
    write_merged_data()
