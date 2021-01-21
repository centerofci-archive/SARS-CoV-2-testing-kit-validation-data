import json


from common.get_test_id import get_test_id
from common.FDA_EUAs_parsed_data import (
    get_fda_eua_parsed_data,
    deprecated_get_fda_eua_parsed_data,
)
from common.annotations_data import (
    filter_for_urls,
    get_annotation_files_by_test_id,
    get_annotations_by_label_id,
)
from common.FDA_reference_panel_lod_data import (
    get_fda_reference_panel_lod_data_by_test_id,
)
from common.paths import (
    dir_path,
    DATA_DIRECTORY_EUAs,
    DATA_FILE_PATH_EUAs_LATEST_PARSED_DATA,
    DATA_FILE_PATH_merged_data,
    DATA_FILE_PATH_summarised_data,
    get_FDA_EUA_pdf_file_path_from_FDA_url,
    get_anot8_org_file_id_from_FDA_url,
    get_anot8_org_permalink_from_FDA_url,
)
from common.labels import (
    Labels,
    get_label_tip_parts,
)


def get_merged_data ():
    with open(DATA_FILE_PATH_merged_data, "r", encoding="utf8") as f:
        data = json.load(f)

    return data
