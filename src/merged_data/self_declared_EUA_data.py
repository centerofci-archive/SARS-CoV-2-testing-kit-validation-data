import math


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


def get_self_declared_EUA_data (annotations_by_label_id):
    supported_specimen_types = get_supported_specimen_types(annotations_by_label_id)
    target_genes = get_target_genes(annotations_by_label_id)
    controls__human_gene_target = get_controls__human_gene_target(annotations_by_label_id)
    primer_probe_sequences = get_primer_probe_sequences(annotations_by_label_id)
    lod_value = get_lod_value(annotations_by_label_id)
    lod_units = get_lod_units(annotations_by_label_id)
    lod_minimum_replicates = get_lod_minimum_replicates(annotations_by_label_id)
    synthetic_specimen__viral_material = get_synthetic_specimen__viral_material(annotations_by_label_id)
    synthetic_specimen__clinical_matrix = get_synthetic_specimen__clinical_matrix(annotations_by_label_id)

    return {
        "supported_specimen_types": supported_specimen_types,
        "target_genes": target_genes,
        "controls__human_gene_target": controls__human_gene_target,
        "primer_probe_sequences": primer_probe_sequences,
        "lod_value": lod_value,
        "lod_units": lod_units,
        "lod_minimum_replicates": lod_minimum_replicates,
        "synthetic_specimen__viral_material": synthetic_specimen__viral_material,
        "synthetic_specimen__clinical_matrix": synthetic_specimen__clinical_matrix,
    }


def get_supported_specimen_types (annotations_by_label_id):
    annotations = annotations_by_label_id.get(Labels.supported_specimen_types, [])

    return {
        "annotations": annotations,
        "parsed": "",
    }


def get_target_genes (annotations_by_label_id):
    annotations = annotations_by_label_id.get(Labels.viral_genes_targetted, [])
    annotations += annotations_by_label_id.get(Labels.viral_proteins_targetted, [])

    return {
        "annotations": annotations,
        "parsed": "",
    }


def get_controls__human_gene_target (annotations_by_label_id):
    annotations = annotations_by_label_id.get(Labels.controls__internal__human_gene_target, [])

    return {
        "annotations": annotations,
        "parsed": "",
    }


def get_primer_probe_sequences (annotations_by_label_id):
    annotations = annotations_by_label_id.get(Labels.primers_and_probes__sequences, [])

    filtered_annotations = []
    parsed = []

    for annotation in annotations:
        sequence_labels = set.intersection(
            Labels.primer_probe_sequences__classification__label_ids,
            set(annotation["labels"])
        )
        if sequence_labels:
            filtered_annotations.append(minimal_annotation(annotation))
            parsed += list(sequence_labels)
        else:
            print("No sequence_labels for: " + get_link_to_annotation(annotation))

    if len(parsed) > 1:
        print("Got {} primer probe sequence labels for {}".format(len(parsed), get_link_to_annotation(filtered_annotations[0])))

    parsed = parsed[0] if parsed else ""

    return {
        "annotations": filtered_annotations,
        "parsed": parsed,
    }


def get_lod_value (annotations_by_label_id):
    annotations_lod_value = annotations_by_label_id.get(Labels.limit_of_detection_lod__value, [])

    min_value = math.inf
    max_value = -math.inf
    min_annotation = None
    max_annotation = None

    for annotation in annotations_lod_value:
        allowed_to_fail_silently = annotation_contains_error_labels(annotation)

        try:
            v = float(annotation["text"])
        except Exception as e:
            if allowed_to_fail_silently:
                continue
            else:
                print(annotation)
                raise e

        new_min = min(min_value, v)
        new_max = max(max_value, v)

        if new_min != min_value:
            min_value = new_min
            min_annotation = annotation

        if new_max != max_value:
            max_value = new_max
            max_annotation = annotation

    if not min_annotation:
        annotations = []
        min_value = None
        max_value = None
        parsed = ""
    else:
        same = min_value == max_value
        annotations = [min_annotation] if same else [min_annotation, max_annotation]
        parsed = "{}".format(min_value) if same else "{} ↔ {}".format(min_value, max_value)

    return {
        "annotations": minimal_annotations(annotations),
        "min": min_value,
        "max": max_value,
        "parsed": parsed,
    }


def get_lod_units (annotations_by_label_id):
    annotations = annotations_by_label_id.get(Labels.limit_of_detection_lod__units, [])
    warn_of_multiple_annotation(annotations, field_expects_one_or_fewer_annotations="LOD units")

    parsed = ""
    if annotations:
        parsed = annotations[0]["text"]

        # mapping
        if parsed == "GCE / reaction":
            parsed = "genome copies / reaction"

        if parsed not in ["genome copies / μL", "TCID50 / mL", "PFU / μL", "genome copies / reaction"]:
            parsed = "other"

    return {
        "annotations": minimal_annotations(annotations),
        "parsed": parsed
    }


def get_lod_minimum_replicates (annotations_by_label_id):
    annotations = annotations_by_label_id.get(Labels.limit_of_detection_lod__minimum_replicates, [])

    return {
        "annotations": minimal_annotations(annotations),
        "parsed": ""
    }


def get_synthetic_specimen__viral_material (annotations_by_label_id):
    annotations = annotations_by_label_id.get(Labels.specimen__synthetic_specimen__virus, [])

    types = []
    not_specified_types = []
    error_types = []

    for annotation in annotations:
        for label_id in annotation["labels"]:
            if label_id in Labels.viral_material_type_label_ids:
                parts = label_id.split("/")
                types.append(parts[-1])

            if label_id in Labels.not_specified_label_ids:
                not_specified_types.append(label_id)

            if label_id in Labels.error_label_ids:
                error_types.append(label_id)

    if not types:
        if not_specified_types:
            types = not_specified_types
        elif error_types:
            types = error_types

    return { "annotations": minimal_annotations(annotations), "parsed": ", ".join(types) }


def get_synthetic_specimen__clinical_matrix (annotations_by_label_id):
    annotations = annotations_by_label_id.get(Labels.specimen__synthetic_specimen__clinical_matrix, [])

    return {
        "annotations": minimal_annotations(annotations),
        "parsed": "",
    }

