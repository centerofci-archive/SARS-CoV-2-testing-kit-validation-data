import json
import os
import re
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path + "/..")

from common.paths import (
    DATA_FILE_PATH_EUAs_MERGED_PARSED_DATA,
)
from common.printing import print_padded_hashes, print_warning, print_error
from get_adveritasdx_data_row import get_adveritasdx_data



def check_test_ids ():
    with open(DATA_FILE_PATH_EUAs_MERGED_PARSED_DATA, "r", encoding="utf8") as f:
        merged_data = json.load(f)
        cci_test_ids = list(map(lambda x: x["test_id"], merged_data))


    avd_data = get_adveritasdx_data()
    avd_test_ids = list(map(lambda x: x["test_id"], avd_data))

    avd_ids_to_exclude = set(cci_test_ids).union(AVD_test_ids_to_ignored)
    cci_ids_to_exclude = set(avd_test_ids).union(test_ids_known_to_be_missing_in_AVD_data)
    avd_test_ids_not_found_in_cci_data = [i for i in avd_test_ids if i not in avd_ids_to_exclude]
    cci_test_ids_not_found_in_avd_data = [i for i in cci_test_ids if i not in cci_ids_to_exclude]

    if cci_test_ids_not_found_in_avd_data:
        print_padded_hashes()
        print_error("Missing test_ids in AdVeritasDx data.")
        print(" 1. Open 'data/adveritasdx/parsed/latest.json' (or the spreadsheet).\n 2. Open 'src/adveritasdx/check_test_ids.py'")

        ensure_commented_test_ids_in_map(cci_test_ids_not_found_in_avd_data)

        print(" 3. Try to search for each of the above tests in the AdVeritasDx data.\n 4. If present in the AdVeritas data and it's just using a different name then complete the mapping by adding the corresponding AdVeritasDx derived test_id.\n 5. If absent from the AVD data, move entry to the 'test_ids_known_to_be_missing_in_AVD_data'.\n")
        print_padded_hashes()
        sys.exit(1)


    if avd_test_ids_not_found_in_cci_data:
        print_padded_hashes
        print_error("{} test_ids from AdVeritasDx are missing in merged (CCI) data.  Likely suprious and should be added to 'AVD_test_ids_to_ignored'".format(len(avd_test_ids_not_found_in_cci_data)))

        ids = "".join(map(lambda i: "\n   \"{}\",".format(i), avd_test_ids_not_found_in_cci_data))
        print(ids)
        print_padded_hashes()
        sys.exit(1)


    original_avd_test_ids = list(map(lambda x: x["original_test_id"], avd_data))
    potential_avd_test_ids_in_map = set(map_AVD_test_id_to_FDA_EUA_list_test_id.keys())
    redundant_potential_avd_test_ids_in_map = potential_avd_test_ids_in_map - set(original_avd_test_ids)
    if redundant_potential_avd_test_ids_in_map:
        print_warning("\n{} keys can be removed from 'map_AVD_test_id_to_FDA_EUA_list_test_id'".format(len(redundant_potential_avd_test_ids_in_map)))
        print("\n   * " + "\n   * ".join(list(redundant_potential_avd_test_ids_in_map)))
        print("\n\n")


    avd_test_ids_now_present = test_ids_known_to_be_missing_in_AVD_data.intersection(set(avd_test_ids))
    if avd_test_ids_now_present:
        print_warning("\n{} keys can be removed from 'test_ids_known_to_be_missing_in_AVD_data'".format(len(avd_test_ids_now_present)))
        print("\n   * " + "\n   * ".join(list(avd_test_ids_now_present)))
        print("\n\n")



def ensure_commented_test_ids_in_map(test_ids):
    if not test_ids:
        return

    with open(__file__, "r", encoding="utf8") as f:
        file_contents = f.read()

    print_warning("ids to resolve: \n")
    print("\n   * " + "\n   * ".join(test_ids))
    print("\n")

    a_test_id_in_code = "\": \"" + test_ids[-1] + "\""
    if a_test_id_in_code in file_contents:
        #print("    Skipping automatic code insertion: `{}` found in {}".format(a_test_id_in_code, __file__))
        return

    insertion_text_point = "# LEAVE_THIS_TEMPLATE_IT_IS_FOR_AUTOMATIC_CODE_INSERTION"
    insertion_text = (
        "# Mapped as of 2021-__-__\n" +
        "\n".join(map(lambda x: """#"": "{}",""".format(x), test_ids)) + "\n\n" +
        insertion_text_point
    )

    new_contents = re.sub(r"^" + insertion_text_point, insertion_text, file_contents, flags=re.M)

    print_warning("     Automatically inserting code into {}".format(__file__))
    with open(__file__, "w", encoding="utf8") as f:
        f.write(new_contents)



map_AVD_test_id_to_FDA_EUA_list_test_id = {
"centers for disease control and prevention's (cdc)__cdc 2019-novel coronavirus (2019-ncov) real-time rt-pcr diagnostic panel (cdc)": "cdc__cdc 2019-novel coronavirus (2019-ncov) real-time rt-pcr diagnostic panel",
"wadsworth center, new york state department of public health's (cdc)__new york sars-cov-2 real-time reverse transcriptase (rt)-pcr diagnostic panel": "wadsworth center, new york state department of health's (cdc)__new york sars-cov-2 real-time reverse transcriptase (rt)-pcr diagnostic panel",
"abbott molecular__abbott realtime sars-cov-2 eua test": "abbott molecular__abbott realtime sars-cov-2 assay",
"primerdesign ltd.__genesig real-time pcr covid-2019 assay": "primerdesign ltd__primerdesign ltd covid-19 genesig real-time pcr assay",
"avellino lab usa, inc.__avellino sars-cov-2/covid-19 (avellinocov2)": "avellino lab usa, inc.__avellinocov2 test",
"luminex molecular diagnostics, inc.__nxtagcov extended panel assay": "luminex molecular diagnostics, inc.__nxtag cov extended panel assay",
"cellex inc.__qsars-cov-2 igm/igg rapid test": "cellex inc.__qsars-cov-2 igg/igm rapid test",
"ipsum diagnostics__cov-19 idx assay": "ipsum diagnostics, llc__cov-19 idx assay",
"becton, dickinson & company (bd), biogx__biogx sars-cov-2 reagents for bd max system": "becton, dickinson & company (bd)__biogx sars-cov-2 reagents for bd max system",
"co-diagnostics, inc.__logix smart coronavirus covid-19": "co-diagnostics, inc.__logix smart coronavirus disease 2019 (covid-19) kit",
"viracor eurofins clinical diagnostics__coronavirus sars-cov-2 rt-pcr assay": "viracor eurofins clinical diagnostics__viracor sars-cov-2 assay",
"diacarta, inc.__quantivirus sars-cov-2 test": "diacarta, inc.__quantivirus sars-cov-2 test kit",
"specialty diagnostic (sdi) laboratories__sdi sars-cov-2 assay": "specialty diagnostic (sdi) laboratories__sdi sars-cov-2 assayletter granting inclusion",
"infectious diseases diagnostics laboratory (iddl), boston children’s hospital__childrens-altona-sars-cov-2 assay": "infectious diseases diagnostics laboratory (iddl), boston children's hospital__childrens-altona-sars-cov-2 assay",
"trax management services inc. (mfd by procomcure biotech gmbh)__phoenixdx 2019-cov": "trax management services inc.__phoenixdx 2019-cov",
"seegene__allplex 2019-ncov assay": "seegene, inc.__allplex 2019-ncov assay",
"altona diagnostics gmbh__realstar sars-cov02 rt-pcr kits": "altona diagnostics gmbh__realstar sars-cov02 rt-pcr kits u.s.",
"diasorin inc.__liason sars-cov-2 s1/s2 igg": "diasorin inc.__liaison sars-cov-2 s1/s2 igg",
"bio-rad laboratories, inc.__platelia sars-cov-2 total ab assay": "bio-rad laboratories__platelia sars-cov-2 total ab assay",
"bio-rad laboratories, inc.__bio-rad sars cov-2-ddpcr test": "bio-rad laboratories, inc.__bio-rad sars-cov-2 ddpcr test",
"biofire diagnostics, llc__biofire respiratory panel 2.1": "biofire diagnostics, llc__biofire respiratory panel 2.1 (rp2.1)",
"genematrix__neoplex covid-19 detection kit": "genematrix, inc.__neoplex covid-19 detection kit",
"fulgent therapeutics llc__fulgent covid-19 by rt-pcr test": "fulgent therapeutics, llc__fulgent covid-19 by rt-pcr test",
"assurance__assurance sars-cov-2 panel": "assurance scientific laboratories__assurance sars-cov-2 panel",
"color genomics, inc.__color sars cov-2 diagnostic assay": "color genomics, inc.__color genomics sars-cov-2 rt-lamp diagnostic assay",
"seasun biomaterials, inc.__aq-top covid-19 rapid detection kit": "seasun biomaterials, inc.__aq-top covid-19 rapid detection",
"exact sciences laboratories__exact sciences sars-cov-2 (n gene detection) test": "exact sciences laboratories__sars-cov-2 (n gene detection) test",
"color genomics, inc.__color covid-19 test unmonitored collection kit": "color genomics, inc.__color covid-19 test self-swab collection kit",
"abbott diagnostics scarborough, inc.__binaxnowtm covid-19 ag card home test": "abbott diagnostics scarborough, inc.__binaxnow covid-19 ag card home test",

# Mapped as of 2021-03-09
"ortho clinical diagnostics, inc.__vitros immunodiagnostic products anti-sars-cov-2 igg reagent pack": "ortho-clinical diagnostics, inc.__vitros immunodiagnostic products anti-sars-cov-2 igg reagent",

# LEAVE_THIS_TEMPLATE_IT_IS_FOR_AUTOMATIC_CODE_INSERTION
}



test_ids_known_to_be_missing_in_AVD_data = set([
    "infinity biologix llc__infinity biologix taqpath sars-cov-2 assay",
    "roche diagnostics__elecsys il-6",
    "hospital of the university of pennsylvania__bd max covid-19 assay",
    "inno diagnostics reference laboratory, ponce medical school__pmsf-inno sars-cov-2 rt-pcr test",
    "clinomics usa inc.__clinomics triodx rt-pcr covid-19 test",
    "princ.eton biomeditech corp.__status covid-19/flu",
    "visby medical, inc.__visby medical covid-19 point of care test",
    "becton, dickinson and company (bd)__bd sars-cov-2/flu for bd max system",
    "thermo fisher scientific__taqpath covid-19, flua, flub combo kit",
    "grifols diagnostic solutions inc.__procleix sars-cov-2 assay",
    "immunodiagnostic systems ltd.__ids sars-cov-2 igg",
    "bio-rad laboratories, inc.__bio-rad reliance sars-cov-2/flua/flub rt-pcr assay kit",
    "gravity diagnostics, llc__gravity diagnostics sars-cov-2 rt-pcr for use with dtc kits",
    "assurance scientific laboratories__assurance sars-cov-2 panel dtc",
    "everlywell, inc.__everlywell covid-19 test home collection kit dtc",
    # Mapped as of 2021-03-09
    "university of illinois office of the vice president for economic development and innovation__covidshield",
    "viracor eurofins clinical diagnostics__viracor sars-cov-2 assay dtc",
    "abbott laboratories inc.__advisedx sars-cov-2 igg ii",
    "quidel corporation__quickvue at-home covid-19 test",
    "luminex molecular diagnostics, inc.__nxtag respiratory pathogen panel + sars-cov-2",
    "abbott molecular inc.__alinity m resp-4-plex",
    "clinical research sequencing platform (crsp), llc at the broad institute of mit and harvard__crsp sars-cov-2 real-time reverse transcriptase (rt)-pcr diagnostic assay (version 3)",
    "adaptive biotechnologies corporation__t-detect covid test",
    "cue health inc.__cue covid-19 test for home and over the counter (otc) use",
])



AVD_test_ids_to_ignored = set([
    "__",
    "7/12/2020 update__",
    "6/21/2020 update__",
    "rutgers clinical genomics laboratory-rutgers university copy__thermofisher - applied biosystems taqpath covid-19 combo kit",
    "rutgers clinical genomics laboratory at rucdr infinite biologics - rutgers university__rutgers clinical genomics laboratory taqpath sars-cov-2-assay",
    "rutgers clinical genomics laboratory-rutgers university__thermofisher - applied biosystems taqpath covid-19 combo kit",
    "autobio diagnostics co.ltd.__anti-sars-cov-2 rapid test",
])
