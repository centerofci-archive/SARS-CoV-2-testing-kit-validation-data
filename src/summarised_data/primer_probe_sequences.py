from common import (
    Labels,
)


explicitly_specified = Labels.primers_and_probes__sequences__explicitly_specified
not_specified = Labels.primers_and_probes__sequences__not_specified
reference_available = Labels.primers_and_probes__sequences__reference_available

label_root = Labels.primers_and_probes__sequences + "/"
label_explicitly_specified = explicitly_specified.replace(label_root, "")
label_not_specified = not_specified.replace(label_root, "")
label_reference_available = reference_available.replace(label_root, "")


def get_primer_probe_sequences_summary (data):

    have_parsed = 0
    not_parsed = 0

    explicitly_specified_count = 0
    reference_available_count = 0
    not_specified_count = 0

    for row in data:
        primer_probe_sequence__parsed_value = row["self_declared_EUA_data"]["primer_probe_sequences"]["parsed"]

        if primer_probe_sequence__parsed_value:
            have_parsed += 1

            if primer_probe_sequence__parsed_value == label_explicitly_specified:
                explicitly_specified_count += 1
            elif primer_probe_sequence__parsed_value == label_reference_available:
                reference_available_count += 1
            elif primer_probe_sequence__parsed_value == label_not_specified:
                not_specified_count += 1
            else:
                print("ERROR in get_primer_probe_sequences_summary, primer_probe_sequence__parsed_value = ", primer_probe_sequence__parsed_value)

        else:
            not_parsed += 1


    summary = {
        "have_parsed": have_parsed,
        "not_parsed": not_parsed,
        "explicitly_specified": explicitly_specified_count,
        "reference_available": reference_available_count,
        "not_specified": not_specified_count,
    }

    return summary


def get_top_10_tests_primer_probe_sequences_summary (data, weighted_by_test_usage):
    explicitly_specified_count = 0
    not_specified_count = 0
    reference_available_count = 0

    for row in data:
        primary_rank = row["amp_survey"]["aug"]["primary_rank"]
        if not primary_rank:
            # Test is not in top 10 tests with EUAs from AMP's survey of laboratories
            continue

        increment = row["amp_survey"]["aug"]["primary_lab_percentage"] if weighted_by_test_usage else 1

        primer_probe_sequence__parsed_value = row["self_declared_EUA_data"]["primer_probe_sequences"]["parsed"]


        if primer_probe_sequence__parsed_value == label_explicitly_specified:
            explicitly_specified_count += increment

        elif primer_probe_sequence__parsed_value == label_reference_available:
            reference_available_count += increment

        elif primer_probe_sequence__parsed_value == label_not_specified:
            if row["test_id"] == "cdc__cdc 2019-novel coronavirus (2019-ncov) real-time rt-pcr diagnostic panel":
                # Sequence is not in the EUA but is present on their website:
                # https://www.cdc.gov/coronavirus/2019-ncov/lab/rt-pcr-panel-primer-probes.html
                reference_available_count += increment
            else:
                not_specified_count += increment

        else:
            print("ERROR in get_top_10_tests_primer_probe_sequences_summary, primer_probe_sequence__parsed_value = ", primer_probe_sequence__parsed_value)


    return {
        "explicitly_specified": explicitly_specified_count,
        "not_specified": not_specified_count,
        "reference_available": reference_available_count,
    }
