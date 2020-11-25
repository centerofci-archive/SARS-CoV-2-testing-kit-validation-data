import json5


with open("./data/amp_survey/aug.json5", "r") as f:
    test_id_to_data = json5.load(f)


default_data = {
    "primary_rank": None,
    "primary_lab_percentage": None,
}

def get_amp_survey (test_id):
    primary_data = test_id_to_data.get(test_id, default_data)

    return {
        "aug": {
            "primary_rank": primary_data["primary_rank"],
            "primary_lab_percentage": primary_data["primary_lab_percentage"],
            "id":                     0 if primary_data["primary_rank"] else "",
            "anot8_org_file_id": "1162" if primary_data["primary_rank"] else "",
        }
    }
