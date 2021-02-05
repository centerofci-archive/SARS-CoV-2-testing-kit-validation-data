from flask import Flask, make_response
import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from common import get_merged_data

dir_path = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__)


@app.route("/")
def index ():
    return v3()


@app.route("/v2")
def v2 ():
    html_file_path = dir_path + "/v2.html"
    with open(html_file_path, "r", encoding="utf8") as f:
        html_contents = f.read()

    data = get_merged_data()

    src_file_path = dir_path + "/v2.js"
    with open(src_file_path, "r", encoding="utf8") as f:
        src = f.read()

    js_data_statement = "const merged_data = " + json.dumps(data, ensure_ascii=False)
    html_contents = html_contents.replace("\"<MERGED_DATA>\"", js_data_statement)
    html_contents = html_contents.replace("\"<SRC>\"", src)

    return html_contents


@app.route("/v3")
def v3 ():
    html_file_path = dir_path + "/v3.html"
    with open(html_file_path, "r", encoding="utf8") as f:
        html_contents = f.read()

    data = get_merged_data()

    src_file_path = dir_path + "/v3.js"
    with open(src_file_path, "r", encoding="utf8") as f:
        src = f.read()

    js_data_statement = "const merged_dataV3 = " + json.dumps(data, ensure_ascii=False)
    html_contents = html_contents.replace("\"<MERGED_DATA>\"", js_data_statement)
    html_contents = html_contents.replace("\"<SRC>\"", src)

    return html_contents

