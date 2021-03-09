import json


from common.get_test_id import get_test_id
from common.annotations_data import (
    filter_for_urls,
    get_annotation_files_by_test_id,
    get_annotations_by_label_id,
)
from common.paths import (
    dir_path,
    DATA_DIRECTORY_EUAs,
    DATA_DIRECTORY_EUA_PDFs,
    DATA_FILE_PATH_EUAs_LATEST_PARSED_DATA,
    DATA_FILE_PATH_EUAs_MERGED_PARSED_DATA,
    DATA_FILE_PATH_merged_data,
    DATA_FILE_PATH_summarised_data,
    get_FDA_file_id_from_FDA_url,
    # get_FDA_EUA_pdf_fil e_path_from_FDA_url,
    # get_anot8_org_fi le_id_from_FDA_url,
)
from common.labels import (
    Labels,
    get_label_tip_parts,
)
from common.data_compression import (
    json_data_to_flat_list,
)


def get_merged_data ():
    with open(DATA_FILE_PATH_merged_data, "r", encoding="utf8") as f:
        data = json.load(f)

    return data
