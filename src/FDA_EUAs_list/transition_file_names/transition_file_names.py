from datetime import datetime
import json
import os
import sys


def check_script_is_valid_to_run_now ():
    now = datetime.now()
    if now.year >= 2021 and now.month > 2:
        print("Not valid to run this script now")
        sys.exit(1)


def get_data ():
    with open("./2021-02-03-FDA_EUA_PDF_file_names_and_datetimes.json", "r", encoding="utf8") as f:
        file_data = json.load(f)
    return file_data


# {"d":20, "m": "Nov", "t": "18:38", "f": "134919.pdf"},


def migrate_file_names (file_data):
    print ("Will migrate the following file names")

    root_path = "../../../data/FDA-EUA/PDFs/"

    file_name_map = build_file_name_map(file_data)

    for single_file_data in file_data:
        old_file_name = single_file_data["f"]

        core_old_file_name = old_file_name.replace(".annotations", "")

        new_file_name = file_name_map[core_old_file_name]

        is_annotations_file = old_file_name.endswith(".annotations")
        if is_annotations_file:
            new_file_name += ".annotations"

        print("{} -> {}".format(old_file_name, new_file_name))
        os.rename(root_path + old_file_name, root_path + new_file_name)


def build_file_name_map (file_data):
    file_name_map = dict()

    for single_file_data in file_data:
        old_file_name = single_file_data["f"]
        if old_file_name.endswith(".annotations"):
            continue

        new_file_name = get_new_file_name(single_file_data)
        if old_file_name in file_name_map:
            print("ERROR: old_file_name already in file_name_map")
            sys.exit(1)

        file_name_map[old_file_name] = new_file_name

    return file_name_map


month_num_map = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12",
}


def get_new_file_name (single_file_data):
    old_file_name = single_file_data["f"]
    day = ("0" + str(single_file_data["d"]))[-2:]
    month = single_file_data["m"]
    time = single_file_data["t"].replace(":", "-")

    year = 2020
    if month == "Jan" or month == "Feb":
        year = 2021

    month_num = month_num_map[month]

    return "{}-{}-{}__{}__{}".format(
        year, month_num, day, time, old_file_name
    )


def update_anot8_config (file_data):
    current_config = get_anot8_vault_config()

    current_ids_to_file_names = current_config["DO_NOT_EDIT_auto_generated_fields"]["id_to_relative_file_name"]

    reverse_map = {v: k for k, v in current_ids_to_file_names.items()}

    if len(current_ids_to_file_names) != len(reverse_map):
        print("ERROR, not all file names were unique")
        sys.exit(1)

    print("Updating file_names in anot8_vault_config")

    for single_file_data in file_data:
        if single_file_data["f"].endswith(".annotations"):
            continue

        old_file_name = "FDA-EUA/PDFs/" + single_file_data["f"]
        new_file_name = "FDA-EUA/PDFs/" + get_new_file_name(single_file_data)
        file_id = reverse_map[old_file_name]
        current_ids_to_file_names[file_id] = new_file_name

    save_anot8_config(current_config)


def get_anot8_vault_config ():
    with open("../../../data/anot8_vault_config.json", "r", encoding="utf8") as f:
        anot8_config = json.load(f)
        return anot8_config


def save_anot8_config (anot8_vault_config):
    with open("../../../data/anot8_vault_config.json", "w", encoding="utf8") as f:
        json.dump(anot8_vault_config, f, indent=2, ensure_ascii=False)


def main ():
    check_script_is_valid_to_run_now()

    file_data = get_data()
    print(len(file_data))

    migrate_file_names(file_data)
    update_anot8_config(file_data)


main()
