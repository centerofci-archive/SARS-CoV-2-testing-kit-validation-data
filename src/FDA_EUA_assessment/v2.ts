

const labels = {
    claims__controls__internal__human_gene_target: "Controls/Internal/Human gene target",
    claims__limit_of_detection__minimum_replicates: "Limit of Detection (LOD)/Minimum Replicates",
    claims__limit_of_detection__value: "Limit of Detection (LOD)/Value",
    claims__limit_of_detection__units: "Limit of Detection (LOD)/Units",
    claims__primers_and_probes__sequences: "Primers and probes/Sequences",
    claims__primers_and_probes__sources: "Primers and probes/Sources",
    claims__reaction_volume_uL: "Nucleic acid amplification/Reaction/Volume in μL",
    claims__specimen__supported_types: "Supported specimen types",
    claims__specimen__transport_medium: "Specimen/Transport medium",
    claims__target_viral_genes: "Viral gene(s) targetted",
    meta__error: "Meta/Error",
    meta__error__omission: "Meta/Error/Omission",
    meta__not_specified: "Meta/Not specified",
    meta__not_specified__partial_info: "Meta/Not specified/Partial information to reproduce",
    meta__potential_error: "Meta/Potential error",
    metrics__confusion_matrix__false_negatives: "Confusion matrix/False negatives",
    metrics__confusion_matrix__false_positives: "Confusion matrix/False positives",
    metrics__confusion_matrix__true_negatives: "Confusion matrix/True negatives",
    metrics__confusion_matrix__true_positives: "Confusion matrix/True positives",
    metrics__num_clinical_samples__negative_controls: "Number of clinical samples/Controls (negatives)",
    metrics__num_clinical_samples__positive: "Number of clinical samples/Positives",
    synthetic_specimen_virus_type_Naked_RNA: "Specimen/Synthetic Specimen/Virus/Type/Naked RNA",
    synthetic_specimen_virus_type_Antigens: "Specimen/Synthetic Specimen/Virus/Type/Antigens",
    synthetic_specimen_virus_type_Synthetic_Viral_Particles: "Specimen/Synthetic Specimen/Virus/Type/Synthetic Viral Particles",
    synthetic_specimen_virus_type_Inactivated_Virus__Heat: "Specimen/Synthetic Specimen/Virus/Type/Inactivated Virus (Heat)",
    synthetic_specimen_virus_type_Inactivated_Virus__Gammma: "Specimen/Synthetic Specimen/Virus/Type/Inactivated Virus (Gamma radiation)",
    synthetic_specimen_virus_type_Inactivated_Virus__Chemical: "Specimen/Synthetic Specimen/Virus/Type/Inactivated Virus (Chemical)",
    synthetic_specimen_virus_type_Inactivated_Virus__method_not_specified: "Specimen/Synthetic Specimen/Virus/Type/Inactivated Virus (method unspecified)",
    synthetic_specimen_virus_type_Live_Virus: "Specimen/Synthetic Specimen/Virus/Type/Live Virus",
    synthetic_specimen_virus_type_Partial_Live_Virus: "Specimen/Synthetic Specimen/Virus/Type/Partial Live Virus",
    test_descriptor__manufacturer_name: "Test manufacturer",
    test_descriptor__test_name: "Test name",
    test_technology: "Test technology",
    validation_condition__author: "Author",
    validation_condition__comparator_test: "-1",
    validation_condition__date: "Date",
    validation_condition__sample_volume: "-1",
    validation_condition__specimen_type: "-1",
    validation_condition__swab_type: "-1",
    validation_condition__synthetic_specimen__clinical_matrix: "Specimen/Synthetic Specimen/Clinical matrix",
    validation_condition__synthetic_specimen__clinical_matrix_source: "Specimen/Synthetic Specimen/Clinical matrix/Source",
    validation_condition__synthetic_specimen__viral_material: "Specimen/Synthetic Specimen/Virus",
    validation_condition__synthetic_specimen__viral_material_source: "Specimen/Synthetic Specimen/Virus/Source",
    validation_condition__transport_medium: "-1",

    // This smells and suggests we should have kept the second layer of data_keys in conjunction with labels
    _extra_url_to_IFU_or_EUA: "-2",
}


interface HEADER {
    title: string
    label: string
    hidden?: boolean
}
type HEADERS =
(HEADER & {
    category: string
    children?: (HEADER & {
        children?: HEADER[]
    })[]
})[]

const headers: HEADERS = [
    {
        title: "Manufacturer",
        label: null,
        category: "test_descriptor",
        children: [
            {
                title: "Name",
                label: labels.test_descriptor__manufacturer_name,
            },
            {
                title: "Test name",
                label: labels.test_descriptor__test_name,
            },
            {
                title: "IFU or EUA",
                label: labels._extra_url_to_IFU_or_EUA,
            }
        ],
    },
    {
        title: "Claims",
        label: null,
        category: "test_claims",
        children: [
            {
                title: "Test technology",
                label: labels.test_technology,
            },
            {
                title: "Specimens",
                label: null,
                children: [
                    {
                        title: "Supported specimen types",
                        label: labels.claims__specimen__supported_types,
                    },
                    {
                        title: "Transport medium",
                        label: labels.claims__specimen__transport_medium,
                    },
                ]
            },
            {
                // Not in May 13th version of FDA EUA template
                title: "Appropriate testing population",
                // e.g. * patients suspected of COVID-19 by a healthcare provider
                //      * pooled samples
                //      * general, asymptomatic screening population i.e. screening of individuals without symptoms or other reasons to suspect COVID-19
                label: null,
                hidden: true,
            },
            {
                // Not in May 13th version of FDA EUA template
                title: "Sample pooling",
                label: null,
                hidden: true,
                children: [
                    { title: "Approach", label: null, hidden: true, },
                    { title: "Max no. specimens", label: null, hidden: true, },
                ]
            },
            { title: "Target gene(s) of SARS-CoV-2", label: labels.claims__target_viral_genes, },
            {
                title: "Primers and probes",
                label: null,
                children: [
                    { title: "Sequences", label: labels.claims__primers_and_probes__sequences, },
                    { title: "Sources", label: labels.claims__primers_and_probes__sources, hidden: true, },
                ]
            },
            {
                // Not in May 13th version of FDA EUA template
                // i.e. can include more than just SARS-CoV-2
                title: "Detects pathogen(s)",
                label: null,
                hidden: true,
            },
            {
                title: "Limit of Detection (LOD)",
                label: null,
                children: [
                    {
                        title: "value",
                        label: labels.claims__limit_of_detection__value,
                    },
                    {
                        title: "units",
                        label: labels.claims__limit_of_detection__units,
                    },
                    {
                        title: "Minimum replicates",
                        label: labels.claims__limit_of_detection__minimum_replicates,
                    },
                ]
            },
            {
                title: "Intended user",
                // e.g. CLIA labs
                label: null,
                hidden: true,
            },
            { title: "Compatible equipment", label: null, hidden: true, },
            // {
                // Product Overview/Test Principle...
                //     // primer and probe sets and briefly describe what they detect. Please include the nucleic acid sequences for all primers and probes used in the test. Please indicate if the test uses biotin-Streptavidin/avidin chemistry
                // },
            {
                title: "Controls",
                label: null,
                children: [
                    { title: "Human gene", label: labels.claims__controls__internal__human_gene_target, },
                ]
            },
            {
                title: "RNA extraction",
                label: null,
                children: [
                    { title: "Specimen input volume", label: null, hidden: true, },
                    { title: "RNA extraction method(s)", label: null, hidden: true, },
                    { title: "Nucleic acid elution volume", label: null, hidden: true, },
                    { title: "Purification manual &/ automated", label: null, hidden: true, },
                ]
            },
            {
                title: "Reverse transcription",
                label: null,
                children: [
                    { title: "Input volume", label: null, hidden: true, },
                    { title: "Enzyme mix / kits", label: null, hidden: true, },
                ]
            },
            {
                title: "PCR / amplification",
                label: null,
                children: [
                    { title: "Instrument", label: null, hidden: true, },
                    { title: "Enzyme mix / kits", label: null, hidden: true, },
                    { title: "Reaction volume / μL", label: labels.claims__reaction_volume_uL, },
                ]
            },
            {
                title: "PCR quantification fluoresence detection",
                label: null,
                children: [
                    { title: "Instrument", label: null, hidden: true, },
                ]
            },
        ],
    },
    {
        title: "Validation conditions",
        label: null,
        category: "validation_condition",
        children: [
            {
                title: "Author",
                label: labels.validation_condition__author,
            },
            {
                title: "Date",
                label: labels.validation_condition__date,
            },
            {
                title: "Patient details",
                label: null,
                children: [
                    { title: "Age", label: null, hidden: true, },
                    { title: "Race", label: null, hidden: true, },
                    { title: "Gender", label: null, hidden: true, },
                ]
            },
            { title: "Disease stage", label: null, hidden: true, },
            {
                title: "Synthetic Specimen",
                label: null,
                children: [
                    { title: "Viral material", label:labels.validation_condition__synthetic_specimen__viral_material, },
                    { title: "Viral material source", label:labels.validation_condition__synthetic_specimen__viral_material_source, },
                    { title: "Clinical matrix", label:labels.validation_condition__synthetic_specimen__clinical_matrix, },
                    { title: "Clinical matrix source", label:labels.validation_condition__synthetic_specimen__clinical_matrix_source, },
                ]
            },
            {
                title: "Specimen",
                label: null,
                children: [
                    {
                        title: "Type",
                        label: labels.validation_condition__specimen_type,
                        hidden: true,
                    },
                    {
                        title: "Swab type",
                        label: labels.validation_condition__swab_type,
                        hidden: true,
                    },
                    {
                        title: "Transport medium",
                        label: labels.validation_condition__transport_medium,
                        hidden: true,
                    },
                    {
                        title: "Sample volume",
                        label: labels.validation_condition__sample_volume,
                        hidden: true,
                    },
                ]
            },
        ],
    },
    {
        title: "Metrics",
        label: null,
        category: "metric",
        children: [
            {
                title: "Number of clinical samples",
                label: null,
                children: [
                    {
                        title: "Positives",
                        label: labels.metrics__num_clinical_samples__positive,
                        hidden: true,
                    },
                    {
                        title: "Controls (negatives)",
                        label: labels.metrics__num_clinical_samples__negative_controls,
                        hidden: true,
                    },
                ]
            },
            {
                title: "Comparator test",
                label: labels.validation_condition__comparator_test,
                hidden: true,
            },
            {
                title: "Confusion matrix",
                label: null,
                children: [
                    {
                        title: "True positives",
                        label: labels.metrics__confusion_matrix__true_positives,
                        hidden: true,
                    },
                    {
                        title: "False negatives",
                        label: labels.metrics__confusion_matrix__false_negatives,
                        hidden: true,
                    },
                    {
                        title: "True negatives",
                        label: labels.metrics__confusion_matrix__true_negatives,
                        hidden: true,
                    },
                    {
                        title: "False positives",
                        label: labels.metrics__confusion_matrix__false_positives,
                        hidden: true,
                    },
                ]
            },
        ],
    },
    {
        title: "Derived values",
        label: null,
        category: "derived_values",
        children: [],
        hidden: true,
    },
]


function update_header (headers: HEADERS, columns_hidden: boolean)
{
    const table_el = document.getElementById("data_table")
    const thead_el = table_el.getElementsByTagName("thead")[0]
    thead_el.innerHTML = ""
    const row1 = thead_el.insertRow()
    const row2 = thead_el.insertRow()
    const row3 = thead_el.insertRow()

    for (let i1 = 0; i1 < headers.length; ++i1)
    {
        const element1 = headers[i1]
        const className = `${element1.category} header_label`

        let row1_width = 0
        let row1_height = 1
        if (!(element1.children && element1.children.length))
        {
            row1_width = ((columns_hidden && element1.hidden) ? 0 : 1)
            row1_height = 3
        }
        else for (let i2 = 0; i2 < element1.children.length; ++i2)
        {
            const element2 = element1.children[i2]

            let row2_width = 0
            let row2_height = 1
            if (!(element2.children && element2.children.length))
            {
                row2_width = ((columns_hidden && element2.hidden) ? 0 : 1)
                row2_height = 2
            }
            else for (let i3 = 0; i3 < element2.children.length; ++i3)
            {
                const element3 = element2.children[i3]
                row2_width += ((columns_hidden && element3.hidden) ? 0 : 1)

                const cell3 = document.createElement("th")
                row3.appendChild(cell3)
                cell3.innerHTML = element3.title
                cell3.className = className + ((columns_hidden && element3.hidden) ? " hidden" : "")
            }

            const cell2 = document.createElement("th")
            row2.appendChild(cell2)
            cell2.innerHTML = element2.title
            cell2.colSpan = row2_width
            cell2.rowSpan = row2_height
            cell2.className = className + (((columns_hidden && element2.hidden) || (row2_width === 0)) ? " hidden" : "")

            row1_width += row2_width
        }

        const cell1 = document.createElement("th")
        row1.appendChild(cell1)
        cell1.innerHTML = element1.title
        cell1.colSpan = row1_width
        cell1.rowSpan = row1_height
        cell1.className = className + (((columns_hidden && element1.hidden) || (row1_width === 0)) ? " hidden" : "")
    }
}


function activate_options (headers: HEADERS)
{
    let cells_expanded = false
    document.getElementById("toggle_expanded_cells").onclick = () =>
    {
        cells_expanded = !cells_expanded
        const cells = Array.from(document.getElementsByClassName("value_el"))
        if (cells_expanded)
        {
            cells.forEach(cell => cell.classList.add("expanded"))
        }
        else
        {
            cells.forEach(cell => cell.classList.remove("expanded"))
        }
    }

    let columns_hidden = true
    update_computed_styles(columns_hidden)
    update_header(headers, columns_hidden)
    document.getElementById("toggle_hidden_columns").onclick = () =>
    {
        columns_hidden = !columns_hidden
        update_computed_styles(columns_hidden)
        update_header(headers, columns_hidden)
    }
}

function update_computed_styles (columns_hidden: boolean)
{
    const style_el = document.getElementById("computed_style")
    style_el.innerHTML = columns_hidden ? `.hidden { display: none; }` : ``
}


interface DATA_ROW
{
    test_id: string
    FDA_EUAs_list: {
      first_issued_date: string
      developer_name: string
      test_name: string
      test_technology: string
      url_to_IFU_or_EUA: string
    },
    anot8_org: {
      file_id: string
      permalink: string
    },
    fda_reference_panel_lod_data: {
      different_developer_name: string
      different_test_name: string
      results_status: string
      lod: number,
      sample_media_type: string
    },
    self_declared_EUA_data: {
      lod_min: number,
      lod_max: number,
      lod_units: string
      synthetic_specimen__viral_material: []
    }
}


function filter_data_rows_to_remove_serology (data_rows: DATA_ROW[])
{
    // temporarily filter out rows of serology tests
    data_rows = data_rows.filter(d => {
        const tech = (d["Test technology"].data.value as string).toLowerCase()
        // Finds most of the them.
        const remove = tech.includes("serology") || tech.includes("igg") || tech.includes("igm") || tech.includes("total antibody") || tech.includes("immunoassay")
        return !remove
    })
}



// Smells as it contains update for table header due to colspan not being under CSS control
// Need proper state / store manager
activate_options(headers)


const v2 = 2
export { v2 }
