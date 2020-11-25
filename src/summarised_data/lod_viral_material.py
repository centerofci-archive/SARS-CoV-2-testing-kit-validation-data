from common import (
    Labels,
    get_label_tip_parts,
)


label_antigens = get_label_tip_parts(Labels.specimen__synthetic_specimen__virus__type__antigens)

label_inactivated_virus_chemical = get_label_tip_parts(Labels.specimen__synthetic_specimen__virus__type__inactivated_virus_chemical)

label_inactivated_virus_gamma_radiation = get_label_tip_parts(Labels.specimen__synthetic_specimen__virus__type__inactivated_virus_gamma_radiation)

label_inactivated_virus_heat = get_label_tip_parts(Labels.specimen__synthetic_specimen__virus__type__inactivated_virus_heat)

label_inactivated_virus_method_unspecified = get_label_tip_parts(Labels.specimen__synthetic_specimen__virus__type__inactivated_virus_method_unspecified)

label_live_virus = get_label_tip_parts(Labels.specimen__synthetic_specimen__virus__type__live_virus)

label_naked_rna = get_label_tip_parts(Labels.specimen__synthetic_specimen__virus__type__naked_rna)

label_partial_live_virus = get_label_tip_parts(Labels.specimen__synthetic_specimen__virus__type__partial_live_virus)

label_synthetic_viral_particles = get_label_tip_parts(Labels.specimen__synthetic_specimen__virus__type__synthetic_viral_particles)


def get_lod_viral_material (data, filter_and_weight_by_top10_tests):
    have_parsed = 0
    not_parsed = 0

    count_antigens = 0
    count_inactivated_virus_chemical = 0
    count_inactivated_virus_gamma_radiation = 0
    count_inactivated_virus_heat = 0
    count_inactivated_virus_method_unspecified = 0
    count_live_virus = 0
    count_naked_rna = 0
    count_partial_live_virus = 0
    count_synthetic_viral_particles = 0

    count_not_specified = 0

    references_antigens = [None]
    references_inactivated_virus_chemical = [None]
    references_inactivated_virus_gamma_radiation = [None]
    references_inactivated_virus_heat = [None]
    references_inactivated_virus_method_unspecified = [None]
    references_live_virus = [None]
    references_naked_rna = [None]
    references_partial_live_virus = [None]
    references_synthetic_viral_particles = [None]
    references_not_specified = [None]


    for row in data:
        primary_lab_percentage = row["amp_survey"]["aug"]["primary_lab_percentage"]
        if filter_and_weight_by_top10_tests and not primary_lab_percentage:
            continue

        viral_material = row["self_declared_EUA_data"]["synthetic_specimen__viral_material"]
        viral_material_values = viral_material["parsed"]

        # Some EUAs use multiple materials.  Will use only last one as this is more likely to be the one used
        # for the actual LOD assessment
        viral_material_value = viral_material_values.split(", ")[-1]

        increment = primary_lab_percentage if filter_and_weight_by_top10_tests else 1

        if viral_material_value:
            have_parsed += 1

            annotation = viral_material["annotations"][-1]
            ref = "{anot8_org_file_id}?h={id}".format(**annotation)

            if viral_material_value == label_antigens:
                count_antigens += increment
                references_antigens.append(ref)

            elif viral_material_value == label_inactivated_virus_chemical:
                count_inactivated_virus_chemical += increment
                references_inactivated_virus_chemical.append(ref)

            elif viral_material_value == label_inactivated_virus_gamma_radiation:
                count_inactivated_virus_gamma_radiation += increment
                references_inactivated_virus_gamma_radiation.append(ref)

            elif viral_material_value == label_inactivated_virus_heat:
                count_inactivated_virus_heat += increment
                references_inactivated_virus_heat.append(ref)

            elif viral_material_value == label_inactivated_virus_method_unspecified:
                count_inactivated_virus_method_unspecified += increment
                references_inactivated_virus_method_unspecified.append(ref)

            elif viral_material_value == label_live_virus:
                count_live_virus += increment
                references_live_virus.append(ref)

            elif viral_material_value == label_naked_rna:
                count_naked_rna += increment
                references_naked_rna.append(ref)

            elif viral_material_value == label_partial_live_virus:
                count_partial_live_virus += increment
                references_partial_live_virus.append(ref)

            elif viral_material_value == label_synthetic_viral_particles:
                count_synthetic_viral_particles += increment
                references_synthetic_viral_particles.append(ref)

            elif viral_material_value == Labels.meta__not_specified:
                count_not_specified += increment
                references_not_specified.append(ref)

            else:
                print("ERROR in get_lod_units, viral_material_value = ", viral_material_value)

        else:
            not_parsed += 1

    summary = {
        "have_parsed": have_parsed,
        "not_parsed": not_parsed,
        "antigens": {
            "count": count_antigens,
            "example_ref": references_antigens[-1],
        },
        "inactivated_virus_chemical": {
            "count": count_inactivated_virus_chemical,
            "example_ref": references_inactivated_virus_chemical[-1],
        },
        "inactivated_virus_gamma_radiation": {
            "count": count_inactivated_virus_gamma_radiation,
            "example_ref": references_inactivated_virus_gamma_radiation[-1],
        },
        "inactivated_virus_heat": {
            "count": count_inactivated_virus_heat,
            "example_ref": references_inactivated_virus_heat[-1],
        },
        "inactivated_virus_method_unspecified": {
            "count": count_inactivated_virus_method_unspecified,
            "example_ref": references_inactivated_virus_method_unspecified[-1],
        },
        "live_virus": {
            "count": count_live_virus,
            "example_ref": references_live_virus[-1],
        },
        "naked_rna": {
            "count": count_naked_rna,
            "example_ref": references_naked_rna[-1],
        },
        "partial_live_virus": {
            "count": count_partial_live_virus,
            "example_ref": references_partial_live_virus[-1],
        },
        "synthetic_viral_particles": {
            "count": count_synthetic_viral_particles,
            "example_ref": references_synthetic_viral_particles[-1],
        },
        "not_specified": {
            "count": count_not_specified,
            "example_ref": references_not_specified[-1],
        },
    }

    return summary
