from flask import Flask, make_response
import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from common import (
    get_fda_eua_parsed_data,
    get_annotation_files_by_test_id,
    get_anot8_org_file_id_from_FDA_url,
    get_merged_data,
)

dir_path = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__)


@app.route("/")
def index ():
    return v2()


@app.route("/v1")
def v1 ():
    html_file_path = dir_path + "/v1.html"
    with open(html_file_path, "r", encoding="utf8") as f:
        html_contents = f.read()

    fda_eua_parsed_data = get_fda_eua_parsed_data()
    # skip first row as it is headers
    fda_eua_parsed_data = fda_eua_parsed_data[1:]

    # TODO REMOVE (copied from merge.py)
    for fda_eua_row in fda_eua_parsed_data:
        EUAs = fda_eua_row[10]
        url_to_IFU_or_EUA = EUAs[0] if EUAs else fda_eua_row[11]
        anot8_org_file_id = get_anot8_org_file_id_from_FDA_url(url_to_IFU_or_EUA)
        fda_eua_row.append(anot8_org_file_id)
    # ^^^ REMOVE section ^^^

    annotation_files_by_test_id = get_annotation_files_by_test_id(fda_eua_parsed_data)

    src_file_path = dir_path + "/v1.js"
    with open(src_file_path, "r", encoding="utf8") as f:
        src = f.read()

    html_contents = html_contents.replace("\"<FDA_EUA_PARSED_DATA>\"", json.dumps(fda_eua_parsed_data, ensure_ascii=False))
    html_contents = html_contents.replace("\"<ANNOTATION_FILES_BY_TEST_ID>\"", json.dumps(annotation_files_by_test_id, ensure_ascii=False))
    html_contents = html_contents.replace("\"<SRC>\"", src)

    return html_contents


@app.route("/v2")
def v2 ():
    html_file_path = dir_path + "/v2.html"
    with open(html_file_path, "r", encoding="utf8") as f:
        html_contents = f.read()

    data = get_merged_data()

    src_file_path = dir_path + "/v2.js"
    with open(src_file_path, "r", encoding="utf8") as f:
        src = f.read()

    html_contents = html_contents.replace("\"<MERGED_DATA>\"", json.dumps(data, ensure_ascii=False))
    html_contents = html_contents.replace("\"<SRC>\"", src)

    return html_contents

