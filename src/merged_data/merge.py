##
#
# Merges data from:
#   * FDA EUA json
#   * annotations made on the FDA EUA PDFs
#   # FDA reference panel LoD data
#
##
import json
import math
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path + "/..")


from common import (
    DATA_FILE_PATH_merged_data,
    get_annotation_files_by_test_id,
    get_annotations_by_label_id,
    Labels,
)


from FDA_EUAs_list.FDA_EUAs_parsed_data import get_temporal_fda_eua_parsed_data

from FDA_reference_panel_lod_data import (
    get_fda_reference_panel_lod_data_by_test_id,
    get_fda_reference_panel_lod_data,
)
from self_declared_EUA_data import get_self_declared_EUA_data
from amp_survey import get_amp_survey
from adveritasdx import get_adveritasdx_data_row, add_adveritasdx_data
from auto_calculated import auto_calculated



def get_merged_rows ():
    fda_eua_parsed_data = get_temporal_fda_eua_parsed_data()
    annotation_files_by_test_id = get_annotation_files_by_test_id(fda_eua_parsed_data)
    fda_reference_panel_lod_data_by_test_id = get_fda_reference_panel_lod_data_by_test_id()

    merged_rows = []
    adveritasdx_missing_test_ids = set([
        "infinity biologix llc__infinity biologix taqpath sars-cov-2 assay",
        "roche diagnostics__elecsys il-6",
        "hospital of the university of pennsylvania__bd max covid-19 assay",
        "inno diagnostics reference laboratory, ponce medical school__pmsf-inno sars-cov-2 rt-pcr test",
        "clinomics usa inc.__clinomics triodx rt-pcr covid-19 test",
        "princ.eton biomeditech corp.__status covid-19/flu",
        "visby medical, inc.__visby medical covid-19 point of care test",
        "becton, dickinson and company (bd)__bd sars-cov-2/flu for bd max system",
        "thermo fisher scientific__taqpath covid-19, flua, flub combo kit",
        "grifols diagnostic solutions inc.__procleix sars-cov-2 assay",
        "immunodiagnostic systems ltd.__ids sars-cov-2 igg",
        "bio-rad laboratories, inc.__bio-rad reliance sars-cov-2/flua/flub rt-pcr assay kit",
        "gravity diagnostics, llc__gravity diagnostics sars-cov-2 rt-pcr for use with dtc kits",
        "assurance scientific laboratories__assurance sars-cov-2 panel dtc",
        "everlywell, inc.__everlywell covid-19 test home collection kit dtc",
    ])
    missing_AVD_test_ids = []

    for fda_eua_row in fda_eua_parsed_data:
        test_id = fda_eua_row["test_id"]
        first_issued_date = fda_eua_row["Date EUA First Issued"]
        developer_name = fda_eua_row["Entity"]
        test_name = fda_eua_row["Diagnostic name"]
        test_technology = fda_eua_row["Technology"]
        IFUs = fda_eua_row["Information for Use (IFU) (URL to PDF)"]
        url_to_IFU_or_EUA = IFUs[0] if IFUs else fda_eua_row["Emergency Use Authorisation (URL to PDF)"]

        annotation_files_for_test = annotation_files_by_test_id[test_id]
        annotations_by_label_id = get_annotations_by_label_id(annotation_files_for_test)

        anot8_org_data_row = get_anot8_org_data(fda_eua_row, annotation_files_for_test)
        fda_reference_panel_lod_data_row = get_fda_reference_panel_lod_data(developer_name, test_name, test_id, fda_reference_panel_lod_data_by_test_id)
        self_declared_EUA_data_row = get_self_declared_EUA_data(annotations_by_label_id)
        amp_survey_data_row = get_amp_survey(test_id)
        adveritasdx_data_row = get_adveritasdx_data_row(test_id, annotations_by_label_id)

        row = {
            "test_id": test_id,
            "FDA_EUAs_list": {
                "first_issued_date": first_issued_date,
                "developer_name": developer_name,
                "test_name": test_name,
                "test_technology": test_technology,
                "url_to_IFU_or_EUA": url_to_IFU_or_EUA,
            },
            "anot8_org": anot8_org_data_row,
            "fda_reference_panel_lod_data": fda_reference_panel_lod_data_row,
            "self_declared_EUA_data": self_declared_EUA_data_row,
            "amp_survey": amp_survey_data_row,
            "adveritasdx": adveritasdx_data_row,
        }
        row["auto_calculated"] = auto_calculated(row)

        merged_rows.append(row)

        if test_id in adveritasdx_missing_test_ids:
            if adveritasdx_data_row:
                print("Can now remove from adveritasdx_missing_test_ids the following test_id: ", test_id)
        elif not adveritasdx_data_row:
            missing_AVD_test_ids.append(test_id)

    # For now we will just warn about missing the AdVeritasDx data in the CCI data
    if missing_AVD_test_ids:
        print("Missing test_ids in AdVeritasDx data.")
        print("Try to search for the test_ids in 'data/adveritasdx/parsed/latest.json' or the spreadsheet and then add to: 'map_AVD_test_id_to_FDA_EUA_list_test_id' in 'src/adveritasdx/parse_versions.py' if a different name, or add to 'adveritasdx_missing_test_ids' in 'merge.py' if it is missing from AdVeritasDx spreadsheet.\n")
        print("        # \"" + "\",\n        # \"".join(missing_AVD_test_ids) + "\",\n\n")

    add_adveritasdx_data(merged_rows)

    return merged_rows



def get_anot8_org_data (fda_eua_row, annotation_files_for_test):
    file_infos_of_annotated = []
    file_infos_of_unannotated = list(fda_eua_row["relevant_relative_file_infos"])

    for annotation_file in annotation_files_for_test:
        if annotation_file["annotations"]:
            file_infos_of_annotated.append(annotation_file["file_info_of_annotated_file"])
        else:
            file_infos_of_unannotated.append(annotation_file["file_info_of_annotated_file"])

    file_infos_of_annotated = sorted(file_infos_of_annotated, key=lambda file_info: file_info["file_path"])
    file_infos_of_unannotated = sorted(file_infos_of_unannotated, key=lambda file_info: file_info["file_path"])
    file_ids_of_annotated = list(map(lambda fi: fi["anot8_org_file_id"], file_infos_of_annotated))
    file_ids_of_unannotated = list(map(lambda fi: fi["anot8_org_file_id"], file_infos_of_unannotated))

    annotated_set = set(file_ids_of_annotated)
    file_ids_of_unannotated = [i for i in file_ids_of_unannotated if i not in annotated_set]

    return {
        "file_ids_of_annotated": file_ids_of_annotated,
        "file_ids_of_unannotated": file_ids_of_unannotated,
        # Could add these here.  For the moment they are hard coded in the frontend code
        # like src/FDA_EUA_assessment/v3.ts etc
        # ANOT8_ORG_NAMING_AUTHORITY_ID = "1772"
        # ANOT8_ORG_VAULT_ID = "2"
    }



def store_data(data):
    with open(DATA_FILE_PATH_merged_data, "w", encoding="utf8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


merged_rows = get_merged_rows()
store_data(merged_rows)
print("Finished")
