import json

from common.paths import DATA_FILE_PATH_FDA_reference_panel_LATEST_PARSED_DATA



def get_fda_reference_panel_lod_parsed_data ():
    with open(DATA_FILE_PATH_FDA_reference_panel_LATEST_PARSED_DATA, "r", encoding="utf8") as f:
        fda_eua_merged_parsed_data = json.load(f)

    return fda_eua_merged_parsed_data



def get_fda_reference_panel_lod_data_by_test_id ():
    fda_reference_panel_lod_data = get_fda_reference_panel_lod_parsed_data()

    # drop first row of headers
    fda_reference_panel_lod_data = fda_reference_panel_lod_data[1:]

    reference_panel_lod_data_by_test_id = dict()

    for data_row in fda_reference_panel_lod_data:
        test_id = data_row[0]

        if test_id in reference_panel_lod_data_by_test_id:
            raise Exception("Duplicate test_id \"{}\" whilst preparing fda_reference_panel_lod_data_by_test_id".format(test_id))

        reference_panel_lod_data_by_test_id[test_id] = {
            "test_id": data_row[0],
            "developer_name": data_row[1],
            "test_name": data_row[2],
            "results_status": data_row[3],
            "lod": data_row[4],
            "sample_media_type": data_row[5],
        }

    return reference_panel_lod_data_by_test_id



def get_fda_reference_panel_lod_data (developer_name, test_name, test_id, fda_reference_panel_lod_data_by_test_id):

    different_developer_name = False
    different_test_name = False
    fda_reference_panel_lod_data = {}

    if test_id in fda_reference_panel_lod_data_by_test_id:
        fda_reference_panel_lod_data = fda_reference_panel_lod_data_by_test_id[test_id]

        d_name = fda_reference_panel_lod_data["developer_name"]
        different_developer_name = d_name if d_name != developer_name else False
        t_name = fda_reference_panel_lod_data["test_name"]
        different_test_name = t_name if t_name != test_name else False

    else:
        if False and test_id not in temporary_test_ids_not_in_fda_reference_panel_lod_data:
            print(" \"{}\"".format(test_id)),
            count_missing_fda_reference_panel_lod += 1

    return {
        "different_developer_name": different_developer_name,
        "different_test_name": different_test_name,
        "results_status": fda_reference_panel_lod_data.get("results_status", ""),
        "lod": fda_reference_panel_lod_data.get("lod", ""),
        "sample_media_type": fda_reference_panel_lod_data.get("sample_media_type", ""),
    }



# Tests not present on the FDA reference panel website as of 2020-10-13
# https://www.fda.gov/medical-devices/coronavirus-covid-19-and-medical-devices/sars-cov-2-reference-panel-comparative-data
temporary_test_ids_not_in_fda_reference_panel_lod_data = set([
    "helix opco llc (dba helix)__helix covid-19 ngs test",
    "abbott diagnostics scarborough, inc.__binaxnow covid-19 ag card",

    "university of california, los angeles (ucla)__ucla swabseq covid-19 diagnostic platform",
    "zeus scientific, inc.__zeus elisa sars-cov-2 igg test system",
    "thermo fisher scientific__omnipath covid-19 total antibody elisa test",
    "quidel corporation__sofia 2 flu + sars antigen fia",
    "tempus labs, inc.__ic sars-cov2 test",
    "beckman coulter, inc.__access il-6",
    "umass memorial medical center__umass molecular virology laboratory 2019-ncov rrt-pcr dx panel",
    "aeon global health__aeon global health sars-cov-2 assay",
    "alimetrix, inc.__alimetrix sars-cov-2 rt-pcr assay",
    "akron children’s hospital__akron children’s hospital sars-cov-2 assay",
    "centogene us, llc__centosure sars-cov-2 rt-pcr assay",
    "nirmidas biotech, inc.__nirmidas covid-19 (sars-cov-2) igm/igg antibody detection kit",
    "nanoentek america, inc.__frend covid-19 total ab",
    "diasorin, inc.__diasorin liaison sars-cov-2 igm assay",
    "quotient suisse sa__mosaiq covid-19 antibody magazine",
    "genetrack biolabs, inc.__genetrack sars-cov-2 molecular assay",
    "cepheid__xpert xpress sars-cov-2/flu/rsv",
    "university of california san diego health__ucsd rc sars-cov-2 assay",
    "poplar healthcare__poplar sars-cov-2 tma pooling assay",
    "ispm labs, llc dba capstone healthcare__genus sars-cov-2 assay",
    "alpha genomix laboratories__alpha genomix taqpath sars-cov-2 combo assay",
    "lumiradx uk ltd.__lumiradx sars-cov-2 ag test",
    "texas department of state health services, laboratory services section__texas department of state health services (dshs) sars-cov-2 assay",
    "dxterity diagnostics, inc.__dxterity sars-cov-2 rt-pcr test",
    "guardant health, inc.__guardant-19",
    "qdx pathology services__qdx sars-cov-2 assay",
    "cuur diagnostics__cuur diagnostics sars-cov-2 molecular assay",
    "dxterity diagnostics, inc.__dxterity sars-cov-2 rt pcr ce test",
    "baycare laboratories, llc__baycare sars-cov-2 rt pcr assay",
    "mammoth biosciences, inc.__sars-cov-2 detectr reagent kit",
    "miradx__miradx sars-cov-2 rt-pcr assay",
    "t2 biosystems, inc.__t2sars-cov-2 panel",
    "color genomics, inc.__color covid-19 test self-swab collection kit",
    "optolane technologies, inc.__kaira 2019-ncov detection kit",
    "detectachem inc.__mobiledetect bio bcc19 (md-bio bcc19) test kit",
    "bioeksen r&d technologies ltd.__bio-speedy direct rt-qpcr sars-cov-2",
    "billiontoone, inc.__qsanger-covid-19 assay",
    "verily life sciences__verily covid-19 rt-pcr test",
    "beijing wantai biological pharmacy enterprise co., ltd.__wantai sars-cov-2 ab elisa",
    "beijing wantai biological pharmacy enterprise co., ltd.__wantai sars-cov-2 rt-pcr kit",
    "visby medical, inc.__visby medical covid-19",
    "gk pharmaceuticals contract manufacturing operations__gk accu-right sars-cov-2 rt-pcr kit",
    "diasorin molecular llc__simplexa covid-19 direct",
    "kimforest enterprise co., ltd.__kimforest sars-cov-2 detection kit v1",
    "clear labs, inc.__clear dx sars-cov-2 test",
    "gencurix, inc.__genepro sars-cov-2 test",
    "babson diagnostics, inc.__babson diagnostics ac19g1",
    "the kroger co.__kroger health covid-19 test home collection kit",
    "becton, dickinson and company (bd)__bd veritor system for rapid detection of sars-cov-2",
    "quest diagnostics infectious disease, inc.__quest diagnostics ha sars-cov-2 assay",
    "quest diagnostics infectious disease, inc.__quest diagnostics rc sars-cov-2 assay",
    "quest diagnostics infectious disease, inc.__quest diagnostics pf sars-cov-2 assay",
    "avera institute for human genetics__avera institute for human genetics sars-cov-2 assay",
    "seasun biomaterials, inc.__aq-top covid-19 rapid detection kit plus",
    "viracor eurofins clinical diagnostics__viracor sars-cov-2 assay",
    "ortho clinical diagnostics, inc.__vitros immunodiagnostic products anti-sars-cov-2 total reagent pack",
    "exact sciences laboratories__sars-cov-2 test",
    "mayo clinic laboratories, rochester, mn__sars-cov-2 molecular detection assay",
    "quidel corporation__sofia 2 sars antigen fia",
    "everlywell, inc.__everlywell covid-19 test home collection kit",
    "roche molecular systems, inc.__cobas sars-cov-2 & influenza a/b nucleic acid test for use on the cobas liat system",
    "vela operations singapore pte. ltd.__virokey sars-cov-2 rt-pcr test v2.0",
    "national jewish health__sars-cov-2 massarray test",
    "biofire diagnostics, llc__biofire respiratory panel 2.1-ez (rp2.1-ez)",

    "roche diagnostics__elecsys anti-sars-cov-2",
    "roche diagnostics__elecsys il-6",
    "siemens healthcare diagnostics inc.__advia centaur sars-cov-2 total (cov2t)",
    "siemens healthcare diagnostics inc.__atellica im sars-cov-2 total (cov2t)",

    # + bulk processed on ig[gm]|immunoasssay|antibody, so there may be errors
    "cellex inc.__qsars-cov-2 igg/igm rapid test",
    "mount sinai laboratory__covid-19 elisa igg antibody test",
    "diasorin inc.__liaison sars-cov-2 s1/s2 igg",
    "ortho-clinical diagnostics, inc.__vitros immunodiagnostic products anti-sars-cov-2 igg reagent",
    "abbott laboratories inc.__sars-cov-2 igg assay",
    "wadsworth center, new york state department of health__new york sars-cov microsphere immunoassay for antibody detection",
    "euroimmun us inc.__anti-sars-cov-2 elisa (igg)",
    "healgen scientific llc__covid-19 igg/igm rapid test cassette (whole blood/serum/plasma)",
    "hangzhou biotest biotech co., ltd.__rightsign covid-19 igg/igm rapid test cassette",
    "siemens healthcare diagnostics inc.__dimension exl sars-cov-2 total antibody assay (cv2t)",
    "siemens healthcare diagnostics inc.__dimension vista sars-cov-2 total antibody assay (cov2t)",
    "inbios international, inc.__scov-2 detect igg elisa",
    "emory medical laboratories__sars-cov-2 rbd igg test",
    "biohit healthcare (hefei) co. ltd.__biohit sars-cov-2 igm/igg antibody test kit",
    "hangzhou laihe biotech co., ltd.__lyher novel coronavirus (2019-ncov) igm/igg antibody combo test kit (colloidal gold)",
    "beckman coulter, inc.__access sars-cov-2 igg",
    "inbios international, inc.__scov-2 detect igm elisa",
    "assure tech. (hangzhou co., ltd)__assure covid-19 igg/igm rapid test device",
    "diazyme laboratories, inc.__diazyme dz-lite sars-cov-2 igg clia kit",
    "salofa oy__sienna-clarity coviblock covid-19 igg/igm rapid test cassette",
    "luminex corporation__xmap sars-cov-2 multi-antigen igg assay",
    "megna health, inc.__rapid covid-19 igm/igg combo test kit",
    "xiamen biotime biotechnology co., ltd.__biotime sars-cov-2 igg/igm rapid qualitative test",
    "access bio, inc.__carestart covid-19 igm/igg",
    "siemens healthcare diagnostics inc.__atellica im sars-cov-2 igg (cov2g)",
    "siemens healthcare diagnostics inc.__advia centaur sars-cov-2 igg (cov2g)",
    "biomérieux sa__vidas sars-cov-2 igg",
    "biomérieux sa__vidas sars-cov-2 igm",
    "biocheck, inc.__biocheck sars-cov-2 igg and igm combo test",
    "diazyme laboratories, inc.__diazyme dz-lite sars-cov-2 igm clia kit",
    "biocan diagnostics inc.__tell me fast novel coronavirus (covid-19) igg/igm antibody test",
    "university of arizona genetics core for clinical services__covid-19 elisa pan-ig antibody test",
    "tbg biotechnology corp.__tbg sars-cov-2 igg / igm rapid test kit",
    "sugentech, inc.__sgti-flex covid-19 igg",
    "biocheck, inc.__biocheck sars-cov-2 igm antibody test kit",
    "biocheck, inc.__biocheck sars-cov-2 igg antibody test kit",
    "shenzhen new industries biomedical engineering co., ltd.__maglumi 2019-ncov igm/igg",
    "jiangsu well biotech co., ltd.__orawell igm/igg rapid test",
    "bio-rad laboratories__platelia sars-cov-2 total ab assay",
    "vibrant america clinical labs__vibrant covid-19 ab assay",
    "beijing wantai biological pharmacy enterprise co., ltd.__wantai sars-cov-2 ab rapid test",
    # - bulk processed on ig[gm]|immunoasssay|ab |antibody, so there may be errors

    # New tests
    "stanford health care clinical virology laboratory__sars-cov-2 rt-pcr assay",
    "infinity biologix llc__infinity biologix taqpath sars-cov-2 assay",
    "ortho-clinical diagnostics, inc.__vitros immunodiagnostic products anti-sars-cov-2 igg reagent pack",
    "color genomics, inc.__color sars-cov-2 rt-lamp diagnostic assay",
    "helix opco llc__helix covid-19 test",
    "genmark diagnostics, inc.__eplex respiratory pathogen panel 2",
    "access bio, inc.__carestart covid-19 antigen test",
    "beckman coulter, inc.__access sars-cov-2 igm",
    "genalyte, inc.__maverick sars-cov-2 multi-antigen serology panel v2",
    "spectrum solutions llc__sdna-1000 saliva collection device",
    "abbott laboratories inc.__advisedx sars-cov-2 igm",
    "dna genotek inc.__omnigene·oral om-505 and ome-505 (omnigene·oral) saliva collection devices",
    "lumiradx uk ltd.__lumiradx sars-cov-2 rna star complete",
    "clinical enterprise, inc.__empowerdx at-home covid-19 pcr test kit",
    "binx health, inc.__binx health at-home nasal swab covid-19 sample collection kit",
    "celltrion usa, inc.__sampinute covid-19 antigen mia",
    "agena bioscience, inc.__massarray sars-cov-2 panel",
    "quansys biosciences, inc.__q-plex sars-cov-2 human igg (4 plex)",
    "dna genotek inc.__oracollect∙rna or-100 and oracollect∙rna ore-100 saliva collection devices",
    "genscript usa inc.__cpass sars-cov-2 neutralization antibody detection kit",
    "lucira health, inc.__lucira covid-19 all-in-one test kit",
    "innovita (tangshan) biological technology co., ltd.__innovita 2019-ncov ab test (colloidal gold)",
    "gravity diagnostics, llc__gravity diagnostics sars-cov-2 rt-pcr assay",
    "rapidrona, inc.__rapidrona self-collection kit",
    "kantaro biosciences, llc__covid-seroklir, kantaro semi-quantitative sars-cov-2 igg antibody kit",
    "roche diagnostics, inc.__elecsys anti-sars-cov-2 s",
    "cepheid__xpert omni sars-cov-2",
    "quest diagnostics infectious disease, inc.__quest diagnostics rc covid-19+flu rt-pcr",
    "luminostics, inc.__clip covid rapid antigen test",
    "laboratory corporation of america (labcorp)__pixel by labcorp covid-19 test home collection kit",
    "researchdx, inc., dba pacific diagnostics__pacificdx covid-19",
    "acon laboratories, inc.__acon sars-cov-2 igg/igm rapid test",
    "rca laboratory services llc dba genetworx__genetworx covid-19 nasal swab test",
    "hologic, inc.__aptima sars-cov-2/flu assay",
    "abbott diagnostics scarborough, inc.__binaxnow covid-19 ag card home test",
    "ellume limited__ellume covid-19 home test",
    "materials and machines corporation of america (dba matmacorp, inc.)__matmacorp covid-19 2sf test",
    "siemens healthcare diagnostics inc.__advia centaur il6 assay",
    "quidel corporation__quickvue sars antigen test",
    "cepheid__xpert xpress sars-cov-2 dod",
    "quanterix corporation__simoa semi-quantitative sars-cov-2 igg antibody test",
    "quidel corporation__solana sars-cov-2 assay",
    "nirmidas biotech, inc.__midaspot covid-19 antibody combo detection kit",
    "quanterix corporation__simoa sars-cov-2 n protein antigen test",
    "siemens healthcare diagnostics inc.__dimension exl sars‑cov‑2 igg (cv2g)",
    "siemens healthcare diagnostics inc.__dimension vista sars‑cov‑2 igg (cov2g)",
    "ortho clinical diagnostics, inc.__vitros immunodiagnostic products sars-cov-2 antigen reagent pack",
    "phadia ab__elia sars-cov-2-sp1 igg test",
    "advaite, inc.__rapcov rapid covid-19 test",
    "sml genetree co., ltd.__ezplex sars-cov-2 g kit",
    "united biomedical, inc.__ubi sars-cov-2 elisa",
    "bio-rad laboratories, inc.__bio-rad reliance sars-cov-2 rt-pcr assay kit",
    "quadrant biosciences inc.__clarifi covid-19 test kit",
    "ambry genetics laboratory__ambry covid-19 rt-pcr test",
])
