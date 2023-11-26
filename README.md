
# Structured SARS-2 diagnostic data

This repository contains FDA EUA PDFs and data extracted from them using the [anot8 prototype annotation tool](https://github.com/Centerofci/anot8).

This annotated data is consolidated into a single data object [found here](/data/merged_data/latest.json).  This data object also contains data merged from other sources such as the FDA reference panel limit of detection data.

Latest data table [live](https://cci-files.s3.eu-west-2.amazonaws.com/sars_2_diagnostics_data_table/latest.html), [repo](/data_table/latest.html).


## Running locally

### Annotations

To view the EUA related files, their annotations, and make new annotations you
need to do the following (Anot8 instructions correct as of this writing in Oct
2022):

1. Clone this repository to your local computer
2. Clone the [Anot8 repository](https://github.com/Centerofci/anot8) to your local computer
3. Follow the installation instructions for Anot8:
    * `anot8$ python3 -m venv venv`
    * `anot8$ . venv/bin/activate`
    * `anot8$ pip install -r requirements.txt`
4. Configure Anot8 to use the anot8_vault_config in this repo:
    * `anot8$ cp config/local_vault_template.json config/FDA_EUA_diagnostics.json`
    (you can use a different name that `FDA_EUA_diagnostics` if you want)
    * Edit the "root_path" in the new FDA_EUA_diagnostics.json vault to point to
    the `data` directory in this repository.  For example it might look like:
    ```
    {
        "root_path": "/Users/your_username/SARS-CoV-2-testing-kit-validation-data/data"
    }
    ```
    Make sure you edit this file with a plain text and not a rich text editor.
5. Start the Anot8 server:
    * `anot8$ export FLASK_APP=src/server/annotator.py && flask run --port=5003`
    * Visit http://localhost:5003 in your browser
    * Click on the "FDA_EUA_diagnostics" vault
    * Choose a file to open and annotate or view its existing annotations



### Installation

    python3 -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt


### Runtime environment

    . venv/bin/activate

## Data processing pipeline scripts

### Update labels from config file

Need to run this when labels used by the merge script are changed (or added)

    python3 src/common/update_label_files.py

### FDA EUAs page and related PDF files

    python3 src/FDA_EUAs_list/get_latest_html_and_PDFs.py

### FDA reference panel html

    python3 src/FDA_reference_panel/get_latest_version.py
    python3 src/FDA_reference_panel/parse_versions.py

### AdveritasDx

    python3 src/AdveritasDx/get_and_parse_latest.py

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


### Files, URLs, ids, versions, etc

The FDA html pages have urls like `https://www.fda.gov/media/123456/download`

We call that number `123456` the `FDA_file_id`.  The FDA do not make it unique, either to a specific version of a file (they have mutate files and left them on the same `FDA_file_id`) or to the same file (they have deleted files and then uploaded new files re-using a vaccated `FDA_file_id`).

We store a dated version of this file at: `FDA-EUA/PDFs/2020-01-31__23-59__123456.pdf`, the `versioned_file_path`.

And associate this with an `anot8_file_id` like `123`.
