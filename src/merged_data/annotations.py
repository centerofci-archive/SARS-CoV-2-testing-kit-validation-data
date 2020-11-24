from common import (
    Labels,
)


def annotation_contains_error_labels (annotation):
    for label_id in annotation["labels"]:
        if label_id in Labels.error_label_ids:
            return True


def get_link_to_annotation (annotation):
    return "http://localhost:5003/r/1772.2/{}?h={}".format(annotation["anot8_org_file_id"], annotation["id"])


# anot8_org_file_id is denormalised data, makes it easier to get links to annotations
minimal_annotation_keys = ["id", "text", "labels", "comment", "anot8_org_file_id"]
def minimal_annotation (annotation):
    try:
        return { key: annotation[key] for key in minimal_annotation_keys if key in annotation }
    except Exception as e:
        print(annotation)
        raise e


def minimal_annotations (annotations):
    return [ minimal_annotation(a) for a in annotations ]


def warn_of_multiple_annotation (annotations, field_expects_one_or_fewer_annotations=""):
    if field_expects_one_or_fewer_annotations and len(annotations) > 1:
        print("Warning: More than 1 annotation for {}: {}".format(
            field_expects_one_or_fewer_annotations,
            json.dumps(annotations, indent=4, ensure_ascii=False)
        ))

