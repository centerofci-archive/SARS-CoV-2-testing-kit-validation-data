import json
import os
import re


from common.paths import DATA_DIR_PATH


# pass it fda_eua_parsed_data or a data row to get all urls
def filter_for_urls (data):
    urls = []

    if isinstance(data, list):
        for v in data:
            urls += filter_for_urls(v)
    elif isinstance(data, dict):
        for v in data.values():
            urls += filter_for_urls(v)
    elif isinstance(data, str) and re.match(r'^https?://', data):
        urls.append(data)

    return urls



def get_annotation_files_by_test_id (fda_eua_parsed_data):
    annotation_files_by_test_id = dict()

    for data_row in fda_eua_parsed_data:
        test_id = data_row["test_id"]
        all_annotation_files = []

        file_infos = data_row["relevant_relative_file_infos"]

        for file_info in file_infos:
            file_path = file_info["file_path"]
            anot8_org_file_id = file_info["anot8_org_file_id"]
            annotations_file_path = DATA_DIR_PATH + file_path + ".annotations"

            if not os.path.isfile(annotations_file_path):
                # print("skipping " + annotations_file_path)
                continue

            with open(annotations_file_path, "r", encoding="utf8") as f:
                annotation_file_contents = json.load(f)

                annotation_file_contents["anot8_org_file_id"] = anot8_org_file_id
                for annotation in annotation_file_contents["annotations"]:
                    if "deleted" in annotation and annotation["deleted"]:
                        continue
                    annotation["anot8_org_file_id"] = anot8_org_file_id

                all_annotation_files.append(annotation_file_contents)

        annotation_files_by_test_id[test_id] = all_annotation_files

    return annotation_files_by_test_id



def get_annotations_by_label_id (annotation_files):
    annotations_by_label_id = dict()

    for annotation_file in annotation_files:
        for annotation in annotation_file["annotations"]:
            if "deleted" in annotation and annotation["deleted"]:
                continue

            for label_id in annotation["labels"]:

                if label_id not in annotations_by_label_id:
                    annotations_by_label_id[label_id] = []

                annotations_by_label_id[label_id].append(annotation)

    return annotations_by_label_id
