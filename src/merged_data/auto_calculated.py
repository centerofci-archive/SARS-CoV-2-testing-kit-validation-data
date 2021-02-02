

def auto_calculated (row):
    tech = row["FDA_EUAs_list"]["test_technology"].lower()
    # Finds most of the them.
    is_serology = ("serology" in tech) or ("igg" in tech) or ("igm" in tech) or ("total antibody" in tech) or ("immunoassay" in tech)

    return {
        "is_serology": is_serology,
    }
