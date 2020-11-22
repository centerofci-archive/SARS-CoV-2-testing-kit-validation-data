import json
import re


with open("./data/anot8_vault_config.json", "r") as f:
    anot8_vault_config = json.load(f)

labels = sorted(anot8_vault_config["labels"])


attributes_and_labels = []
viral_material_types__attribute_names = []
for label in labels:
    attribute = label.lower()
    attribute = re.sub(" ", "_", attribute)
    attribute = re.sub("/", "__", attribute)
    attribute = re.sub("[^\w]", "", attribute)

    attributes_and_labels.append({ "attribute" : attribute, "label": label })

    if "specimen__synthetic_specimen__virus__type__" in attribute:
        viral_material_types__attribute_names.append(attribute)


warning = "THIS FILE IS AUTO GENERATED.  DO NOT EDIT.  Change and re-run ./src/common/update_label_files.py\n"


python_labels_groups_part1 = """

    not_specified_label_ids = set([
        meta__not_specified,
        meta__not_specified__partial_information_to_reproduce,
    ])

    error_label_ids = set([
        meta__not_specified,
        meta__not_specified__partial_information_to_reproduce,
        meta__error,
        meta__error__omission,
        meta__potential_error,
    ])

    viral_material_type_label_ids = set([
"""

python_labels_groups_part2 = """
    ])
"""

def make_python_content ():
    python_labels = "#\n# " + warning + "#\n#\n\n"

    python_labels += "class Labels:\n"

    for attribute_and_label in attributes_and_labels:
        python_labels += """    {attribute} = "{label}"\n""".format(**attribute_and_label)

    python_labels += python_labels_groups_part1

    for (i, attribute) in enumerate(viral_material_types__attribute_names):
        python_labels += "        {},".format(attribute)
        if i < (len(viral_material_types__attribute_names) - 1):
            python_labels += "\n"

    python_labels += python_labels_groups_part2

    return python_labels


def make_ts_content ():
    ts_labels = "//\n// " + warning + "//\n//\n\n"
    ts_labels += "const labels =\n{\n"

    for attribute_and_label in attributes_and_labels:
        ts_labels += """    {attribute}: "{label}",\n""".format(**attribute_and_label)

    ts_labels += "}\n\n"

    return ts_labels


with open("./src/common/labels.py", "w") as f:
    python_labels = make_python_content()
    f.write(python_labels)

with open("./src/FDA_EUA_assessment/labels.ts", "w") as f:
    ts_labels = make_ts_content()
    f.write(ts_labels)
