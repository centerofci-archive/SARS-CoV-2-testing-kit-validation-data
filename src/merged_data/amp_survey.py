
test_id_to_primary_rank = {
    "roche molecular systems, inc. (rms)__cobas sars-cov-2": 1,
    # LDT: 2,
    "abbott molecular__abbott realtime sars-cov-2 assay": 3,
    "hologic, inc.__aptima sars-cov-2 assay": 4,
    "thermo fisher scientific, inc.__taqpath covid-19 combo kit": 5,
    "cepheid__xpert xpress sars-cov-2 test": 6,
    "abbott molecular inc.__alinity m sars-cov-2 assay": 7,
    "cdc__cdc 2019-novel coronavirus (2019-ncov) real-time rt-pcr diagnostic panel": 8,
    "hologic, inc.__panther fusion sars-cov-2 assay": 9,
    "perkinelmer, inc.__perkinelmer new coronavirus nucleic acid detection kit": 10,
}

# Data from https://anot8.org/r/1772.2/1162?h=0
def get_amp_survey (test_id):

    primary_rank = test_id_to_primary_rank.get(test_id, False)

    return {
        "aug": {
            "primary_rank": primary_rank,
        }
    }

