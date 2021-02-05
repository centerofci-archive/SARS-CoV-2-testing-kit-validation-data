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
from adveritasdx import get_adveritasdx_data_row
from auto_calculated import auto_calculated



def get_merged_rows ():
    fda_eua_parsed_data = get_temporal_fda_eua_parsed_data()
    annotation_files_by_test_id = get_annotation_files_by_test_id(fda_eua_parsed_data)
    fda_reference_panel_lod_data_by_test_id = get_fda_reference_panel_lod_data_by_test_id()

    merged_rows = []

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

        row = {
            "test_id": test_id,
            "FDA_EUAs_list": {
                "first_issued_date": first_issued_date,
                "developer_name": developer_name,
                "test_name": test_name,
                "test_technology": test_technology,
                "url_to_IFU_or_EUA": url_to_IFU_or_EUA,
            },
            "anot8_org": {
                "file_ids": list(map(lambda a: a["anot8_org_file_id"], annotation_files_for_test)),
                # Could add these here.  For the moment they are hard coded in the frontend code
                # like src/FDA_EUA_assessment/v3.ts etc
                # ANOT8_ORG_NAMING_AUTHORITY_ID = "1772"
                # ANOT8_ORG_VAULT_ID = "2"
            },
            "fda_reference_panel_lod_data": get_fda_reference_panel_lod_data(developer_name, test_name, test_id, fda_reference_panel_lod_data_by_test_id),
            "self_declared_EUA_data": get_self_declared_EUA_data(annotations_by_label_id),
            "amp_survey": get_amp_survey(test_id),
            "adveritasdx": get_adveritasdx_data_row(test_id),
        }
        row["auto_calculated"] = auto_calculated(row)

        merged_rows.append(row)

    return merged_rows



def store_data(data):
    with open(DATA_FILE_PATH_merged_data, "w", encoding="utf8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


merged_rows = get_merged_rows()
store_data(merged_rows)
