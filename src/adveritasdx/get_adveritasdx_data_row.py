from enum import Enum, auto

import csv
import json
import os
import re
import sys

from common import (
    Labels,
)

from annotations import (
    minimal_annotation,
    minimal_annotations,
    warn_of_multiple_annotation,
    annotation_contains_error_labels,
    get_link_to_annotation,
)

dir_path = os.path.dirname(os.path.realpath(__file__))

latest_data_file_path = os.path.join(dir_path, "../../data/adveritasdx/parsed/latest.json")


def get_adveritasdx_data ():
    with open(latest_data_file_path, "r", encoding="utf8") as f:
        adveritas_dx_data = json.load(f)

    return adveritas_dx_data



adveritas_dx_data_by_test_id = None
def get_adveritas_dx_data_by_test_id (test_id_to_find):
    global adveritas_dx_data_by_test_id

    if adveritas_dx_data_by_test_id is None:
        adveritas_dx_data_by_test_id = dict()

        data = get_adveritasdx_data()

        for row in data:
            tid = row["test_id"]
            del row["test_id"]
            adveritas_dx_data_by_test_id[tid] = row

    return adveritas_dx_data_by_test_id.get(test_id_to_find, None)



def get_adveritasdx_data_row (test_id, annotations_by_label_id):
    data_row = get_adveritas_dx_data_by_test_id(test_id)

    if data_row is None:
        print("Missing test_id in AdVeritasDx data: " + test_id)

    _mutate_data_node = factory_mutate_data_node(data_row, annotations_by_label_id)

    _mutate_data_node("Analyte", Labels.analyte)
    _mutate_data_node("Assay", Labels.assay)
    _mutate_data_node("Antigen", Labels.antigen)
    _mutate_data_node("Category", Labels.category)
    _mutate_data_node("NPA/Specificity", Labels.calculated_npa__specificity)
    _mutate_data_node("PPA/Sensitivity", Labels.calculated_ppa__sensitivity)
    _mutate_data_node("Company/Organization", Labels.company__organization)
    _mutate_data_node("Cross- Reactivity", Labels.cross_reactivity)
    _mutate_data_node("Detection", Labels.detection)
    _mutate_data_node("External Quality Control", Labels.external_quality_control)
    _mutate_data_node("NPA Sample Size", Labels.npa_sample_size)
    _mutate_data_node("Positive Control", Labels.positive_control)
    _mutate_data_node("PPA Sample Size", Labels.ppa_sample_size)
    _mutate_data_node("PPA Specimen Type", Labels.ppa_specimen_type)
    _mutate_data_node("Sample Prep", Labels.sample_prep)
    _mutate_data_node("Technology", Labels.technology)
    _mutate_data_node("Transport Media", Labels.transport_media)

    return data_row



def mutate_data_node (row, key, label, annotations_by_label_id):
    annotations = annotations_by_label_id.get(label, [])

    data_node = {
        # avd is the value from the AdVeritasDx spreadsheet
        "avd": row[key],
        "annotations": [],
    }

    if annotations:
        if len(annotations) > 1:
            print("WARNING: more than one annotation for label: \"{}\" ".format(label))

        data_node["annotations"] = minimal_annotations(annotations)

    row[key] = data_node


def factory_mutate_data_node (row, annotations_by_label_id):
    def _mutate_data_node (key, label):
        mutate_data_node(row, key, label, annotations_by_label_id)

    return _mutate_data_node
