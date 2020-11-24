
# Structured SARS-2 diagnostic data

This repository contains FDA EUA PDFs and data extracted from them using the [anot8 prototype annotation tool](https://github.com/Centerofci/anot8).

This annotated data is consolidated into a single data object [found here](/data/merged_data/latest.json).  This data object also contains data merged from other sources such as the FDA reference panel limit of detection data.

Latest data table [live](https://cci-files.s3.eu-west-2.amazonaws.com/sars_2_diagnostics_data_table/latest.html), [repo](/data_table/latest.html).


## Running locally

### Installation

    python3 -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt


### Runtime environment

    . venv/bin/activate

## Run scripts

### FDA EUAs page and related PDF files

    python3 src/FDA_EUAs_list/parse_html.py
    python3 src/FDA_EUAs_list/get_PDFs.py

### FDA reference panel html

    python3 src/FDA_reference_panel/get_latest_version.py
    python3 src/FDA_reference_panel/parse_versions.py

### Merge data

    python3 src/merged_data/merge.py

### Summarised data

    python3 src/summarised_data/summarise.py

## Run local pages

### FDA EUA html pages

    export FLASK_APP=src/FDA_EUAs_list/serve_html.py && flask run --port=5001

### Assessment page of FDA EUAs

    export FLASK_APP=src/FDA_EUA_assessment/serve.py && flask run --port=5002


## Dev

### Updating dependencies

Remember to:

    pip freeze > requirements.txt

### FDA EUA assessment page

    npm run watch

