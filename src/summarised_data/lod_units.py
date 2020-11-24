


def get_lod_units (data, filtered_and_weighted_by_top10_tests):
    have_parsed = 0
    not_parsed = 0

    genome_copies_per_vol = 0
    genome_copies_per_reaction = 0
    plaque_forming_units_pfu_per_vol = 0
    tcid50_per_vol = 0
    other = 0

    for row in data:
        primary_lab_percentage = row["amp_survey"]["aug"]["primary_lab_percentage"]
        if filtered_and_weighted_by_top10_tests and not primary_lab_percentage:
            continue

        increment = primary_lab_percentage if filtered_and_weighted_by_top10_tests else 1

        lod_units__parsed_value = row["self_declared_EUA_data"]["lod_units"]["parsed"]

        if lod_units__parsed_value:
            have_parsed += 1

            if lod_units__parsed_value == "genome copies / μL":
                genome_copies_per_vol += increment

            elif lod_units__parsed_value == "PFU / μL":
                plaque_forming_units_pfu_per_vol += increment

            elif lod_units__parsed_value == "TCID50 / mL":
                tcid50_per_vol += increment

            elif lod_units__parsed_value == "genome copies / reaction":
                genome_copies_per_reaction += increment

            elif lod_units__parsed_value == "other":
                other += increment

            else:
                print("ERROR in get_lod_units, lod_units__parsed_value = ", lod_units__parsed_value)

        else:
            not_parsed += 1


    summary = {
        "have_parsed": have_parsed,
        "not_parsed": not_parsed,
        "genome_copies_per_vol": genome_copies_per_vol,
        "plaque_forming_units_pfu_per_vol": plaque_forming_units_pfu_per_vol,
        "tcid50_per_vol": tcid50_per_vol,
        "genome_copies_per_reaction": genome_copies_per_reaction,
        "other": other,
    }

    return summary
