

interface MinimalAnnotationV3
{
    id: number,
    text: string,
    labels: string[],
    comment: string,
    anot8_org_file_id: string,
}

interface DATA_NODEV3
{
    parsed: string
    annotations: MinimalAnnotationV3[]
}

interface DATA_ROWV3
{
    test_id: string
    FDA_EUAs_list: {
        first_issued_date: string
        developer_name: string
        test_name: string
        test_technology: string
        url_to_IFU_or_EUA: string
    }
    anot8_org: {
        file_id: string | null
        permalink: string | null
    }
    fda_reference_panel_lod_data: {
        different_developer_name: string
        different_test_name: string
        results_status: string
        lod: number
        sample_media_type: string
    }
    self_declared_EUA_data: {
        supported_specimen_types: DATA_NODEV3
        target_genes: DATA_NODEV3
        controls__human_gene_target: DATA_NODEV3
        primer_probe_sequences: DATA_NODEV3
        lod_value: DATA_NODEV3 & { min: number, max: number }
        lod_units: DATA_NODEV3
        lod_minimum_replicates: DATA_NODEV3
        synthetic_specimen__viral_material: DATA_NODEV3
        synthetic_specimen__clinical_matrix: DATA_NODEV3
    }
    amp_survey: {
        aug: {
            primary_rank: number | null
            primary_lab_percentage: number | null
            id: number,
            anot8_org_file_id: string,
        }
    }
    adveritasdx: adveritasdx | undefined
    auto_calculated:
    {
        is_serology: boolean
    }
}


interface adveritasdx
{
    "ordinal": number
    "Done? (Y)": string
    "Company/Organization": string
    "Test Name": string
    "Select": string
    "*URL": string
    "Test Type (Lab or Kit)": string
    "Country of Origin": string
    "US Regulatory Status": string
    "Category": string
    "Authorized Setting(s) per FDA": string
    "Technology": string
    "Analyte": string
    "Assay": string
    "Specimen Type": string
    "Transport Media": string
    "Gene": string
    "Antigen": string
    "Sample Prep": string
    "Detection": string
    "TAT": string
    "Analytical Sensitivity (LOD)": string
    "LOD of FDA Reference Panel (NDU/mL)": string
    "Cross- Reactivity": string
    "PPA/Sensitivity": string
    "PPA Sample Size": string
    "PPA Specimen Type": string
    "NPA/Specificity": string
    "NPA Sample Size": string
    "NPV @ 5% prevalence": string
    "PPV@ 5% prevalence": string
    "Manufacturer's Validation Notes": string
    "External Quality Control": string
    "Process (internal) Control": string
    "Positive Control": string
    "*Publications": string
    "*IFU": string
    "*Letter of Authorization (EUA)": string
    "Creation Date": string
    "Modified Date": string
    "Needs Review": string
}
type adveritasdx_keys = keyof adveritasdx

const adveritasdx_headers: adveritasdx_keys[] = [
    "Done? (Y)",
    "Company/Organization",
    "Test Name",
    "Select",
    "*URL",
    "Test Type (Lab or Kit)",
    "Country of Origin",
    "US Regulatory Status",
    "Category",
    "Authorized Setting(s) per FDA",
    "Technology",
    "Analyte",
    "Assay",
    "Specimen Type",
    "Transport Media",
    "Gene",
    "Antigen",
    "Sample Prep",
    "Detection",
    "TAT",
    "Analytical Sensitivity (LOD)",
    "LOD of FDA Reference Panel (NDU/mL)",
    "Cross- Reactivity",
    "PPA/Sensitivity",
    "PPA Sample Size",
    "PPA Specimen Type",
    "NPA/Specificity",
    "NPA Sample Size",
    "NPV @ 5% prevalence",
    "PPV@ 5% prevalence",
    "Manufacturer's Validation Notes",
    "External Quality Control",
    "Process (internal) Control",
    "Positive Control",
    "*Publications",
    "*IFU",
    "*Letter of Authorization (EUA)",
    "Creation Date",
    "Modified Date",
    "Needs Review",
]


declare var merged_dataV3: DATA_ROWV3[]


function mainV3 ()
{


interface ValueRendererV3
{
    (data_row: DATA_ROWV3): {
        raw?: string
        parsed?: string
        comments?: string
        references?: string
    }
}

interface TABLE_FIELDV3 {
    title: string
    value_renderer: ValueRendererV3
    hidden?: boolean
}
type TABLE_FIELDSV3 =
(TABLE_FIELDV3 & {
    category: string
    children?: (TABLE_FIELDV3 & {
        children?: TABLE_FIELDV3[]
    })[]
})[]



const get_comments_raw_and_references = (annotations: MinimalAnnotationV3[]) =>
{
    const raw: string[] = []
    const comments: string[] = []
    const references: { anot8_org_file_id, id }[] = []
    annotations.forEach(({ text, comment, anot8_org_file_id, id }) =>
    {
        raw.push(text)
        comments.push(comment)
        references.push({ anot8_org_file_id, id })
    })

    return {
        raw,
        comments,
        references,
    }
}


const get_html_comments_raw_and_references = (annotations: MinimalAnnotationV3[]) =>
{
    const { raw, comments, references } = get_comments_raw_and_references(annotations)

    const raw_html = raw.map(escape_html).join(" &nbsp; ")

    const comments_html = comments
    .filter(comment => comment)
    .map(comment => {
        return `<span title="${escape_html(comment)}">C</span>`
    })
    .join(" ")

    const references_html = references.map(html_ref_link).join(" ")

    return {
        raw: raw_html,
        comments: comments_html,
        references: references_html,
    }
}


function ref_link (annotation: { anot8_org_file_id: string, id?: number })
{
    const { anot8_org_file_id, id } = annotation

    const host = safe_get_local_storage_item("anot8_server") || "https://anot8.org"
    let ref = `${host}/r/1772.2/${anot8_org_file_id}`

    if (id !== undefined) ref += `?h=${id}`

    return ref
}


function safe_get_local_storage_item (item: string)
{
    return localStorage && localStorage.getItem(item)
}


function html_ref_link (annotation: { anot8_org_file_id: string, id?: number })
{
    return `<a href="${ref_link(annotation)}">R<a/>`
}


const value_renderer_EUA_URL: ValueRendererV3 = d =>
{
    const references = `<a href="${d.FDA_EUAs_list.url_to_IFU_or_EUA}">R</a>`
    return { parsed: "&nbsp;", references }
}


const generic_value_renderer = (data_node: DATA_NODEV3) =>
{
    return {
        parsed: data_node.parsed,
        ...get_html_comments_raw_and_references(data_node.annotations)
    }
}


const adveritasdx_renderer = (field: adveritasdx_keys): ValueRendererV3 => d =>
{
    const field_value = (d.adveritasdx || {})[field]
    const parsed = (field_value || "").toString()
    return ({ parsed })
}


const table_fields: TABLE_FIELDSV3 = [
    {
        title: "AdVeritasDx - CCI linked",
        value_renderer: d => ({ parsed: d.adveritasdx ? "" : "No" }),
        category: "",
    },
    {
        title: "Done? (Y)",
        value_renderer: adveritasdx_renderer("Done? (Y)"),
        category: "",
    },
    {
        title: "Developer",
        value_renderer: null,
        category: "test_descriptor",
        children: [
            {
                title: "Company/Organization",
                value_renderer: d => ({ parsed: d.FDA_EUAs_list.developer_name }),
            },
            {
                title: "Test name",
                value_renderer: d => ({ parsed: d.FDA_EUAs_list.test_name }),
            },
            {
                title: "Latest<sup>*</sup> EUA or IFU",
                value_renderer: value_renderer_EUA_URL,
            }
        ],
    },
    ...adveritasdx_headers.slice(3).map(field => ({
        title: field,
        value_renderer: adveritasdx_renderer(field),
        category: "",
    })),
    {
        title: "Claims",
        value_renderer: null,
        category: "test_claims",
        children: [
            {
                title: "Test technology",
                value_renderer: d => ({ parsed: d.FDA_EUAs_list.test_technology }),
            },
            {
                title: "Assay",
                value_renderer: null //d => ({ parsed: d.FDA_EUAs_list.assay }),
            },
            {
                title: "Specimens",
                value_renderer: null,
                children: [
                    {
                        title: "Supported specimen types",
                        value_renderer: d => generic_value_renderer(d.self_declared_EUA_data.supported_specimen_types),
                    },
                    {
                        title: "Transport media",
                        value_renderer: null,
                        hidden: true,
                    },
                ]
            },
            {
                // Not in May 13th version of FDA EUA template
                title: "Appropriate testing population",
                // e.g. * patients suspected of COVID-19 by a healthcare provider
                //      * pooled samples
                //      * general, asymptomatic screening population i.e. screening of individuals without symptoms or other reasons to suspect COVID-19
                value_renderer: null,
                hidden: true,
            },
            {
                // Not in May 13th version of FDA EUA template
                title: "Sample pooling",
                value_renderer: null,
                hidden: true,
                children: [
                    { title: "Approach", value_renderer: null, hidden: true, },
                    { title: "Max no. specimens", value_renderer: null, hidden: true, },
                ]
            },
            {
                title: "Target gene(s) of SARS-CoV-2",
                value_renderer: d => generic_value_renderer(d.self_declared_EUA_data.target_genes),
            },
            {
                title: "Primers and probes",
                value_renderer: null,
                children: [
                    {
                        title: "Sequences",
                        value_renderer: d => {
                            return generic_value_renderer(d.self_declared_EUA_data.primer_probe_sequences)
                        },
                    },
                    { title: "Sources", value_renderer: null /**/, hidden: true, },
                ]
            },
            {
                // Not in May 13th version of FDA EUA template
                // i.e. can include more than just SARS-CoV-2
                title: "Detects pathogen(s)",
                value_renderer: null,
                hidden: true,
            },
            {
                title: "Limit of Detection (LOD)",
                value_renderer: null,
                children: [
                    {
                        title: "value",
                        value_renderer: d => generic_value_renderer(d.self_declared_EUA_data.lod_value),
                    },
                    {
                        title: "units",
                        value_renderer: d => generic_value_renderer(d.self_declared_EUA_data.lod_units),
                    },
                    {
                        title: "Minimum replicates",
                        value_renderer: d => generic_value_renderer(d.self_declared_EUA_data.lod_minimum_replicates) ,
                    },
                ]
            },
            {
                title: "Intended user",
                // e.g. CLIA labs
                value_renderer: null,
                hidden: true,
            },
            { title: "Compatible equipment", value_renderer: null, hidden: true, },
            // {
                // Product Overview/Test Principle...
                //     // primer and probe sets and briefly describe what they detect. Please include the nucleic acid sequences for all primers and probes used in the test. Please indicate if the test uses biotin-Streptavidin/avidin chemistry
                // },
            {
                title: "Controls",
                value_renderer: null,
                children: [
                    { title: "Human gene", value_renderer: d => generic_value_renderer(d.self_declared_EUA_data.controls__human_gene_target), },
                ]
            },
            {
                title: "RNA extraction",
                value_renderer: null,
                children: [
                    { title: "Specimen input volume", value_renderer: null, hidden: true, },
                    { title: "RNA extraction method(s)", value_renderer: null, hidden: true, },
                    { title: "Nucleic acid elution volume", value_renderer: null, hidden: true, },
                    { title: "Purification manual &/ automated", value_renderer: null, hidden: true, },
                ]
            },
            {
                title: "Reverse transcription",
                value_renderer: null,
                children: [
                    { title: "Input volume", value_renderer: null, hidden: true, },
                    { title: "Enzyme mix / kits", value_renderer: null, hidden: true, },
                ]
            },
            {
                title: "PCR / amplification",
                value_renderer: null,
                children: [
                    { title: "Instrument", value_renderer: null, hidden: true, },
                    { title: "Enzyme mix / kits", value_renderer: null, hidden: true, },
                    { title: "Reaction volume / μL", value_renderer: null, hidden: true, },
                ]
            },
            {
                title: "PCR quantification fluoresence detection",
                value_renderer: null,
                children: [
                    { title: "Instrument", value_renderer: null, hidden: true, },
                ]
            },
        ],
    },
    {
        title: "Validation conditions",
        value_renderer: null,
        category: "validation_condition",
        children: [
            {
                title: "Author",
                value_renderer: d => ({ parsed: "self" }),
            },
            {
                title: "Date",
                value_renderer: d => ({ parsed: d.FDA_EUAs_list.first_issued_date }),
            },
            {
                title: "Patient details",
                value_renderer: null,
                children: [
                    { title: "Age", value_renderer: null, hidden: true, },
                    { title: "Race", value_renderer: null, hidden: true, },
                    { title: "Gender", value_renderer: null, hidden: true, },
                ]
            },
            { title: "Disease stage", value_renderer: null, hidden: true, },
            {
                title: "Synthetic Specimen",
                value_renderer: null,
                children: [
                    {
                        title: "Viral material",
                        value_renderer: d => generic_value_renderer(d.self_declared_EUA_data.synthetic_specimen__viral_material),
                    },
                    {
                        title: "Viral material source",
                        value_renderer: null /**/,
                        hidden: true,
                    },
                    {
                        title: "Clinical matrix",
                        value_renderer: d => generic_value_renderer(d.self_declared_EUA_data.synthetic_specimen__clinical_matrix),
                    },
                    {
                        title: "Clinical matrix source",
                        value_renderer: null /**/,
                        hidden: true,
                    },
                ]
            },
            {
                title: "Specimen",
                value_renderer: null,
                children: [
                    {
                        title: "Type",
                        value_renderer: null /**/,
                        hidden: true,
                    },
                    {
                        title: "Swab type",
                        value_renderer: null /**/,
                        hidden: true,
                    },
                    {
                        title: "Transport medium",
                        value_renderer: null /**/,
                        hidden: true,
                    },
                    {
                        title: "Sample volume",
                        value_renderer: null /**/,
                        hidden: true,
                    },
                ]
            },
        ],
    },
    {
        title: "Metrics",
        value_renderer: null,
        category: "metric",
        children: [
            {
                title: "Number of clinical samples",
                value_renderer: null,
                children: [
                    {
                        title: "Positives",
                        value_renderer: null /**/,
                        hidden: true,
                    },
                    {
                        title: "Controls (negatives)",
                        value_renderer: null /**/,
                        hidden: true,
                    },
                ]
            },
            {
                title: "Comparator test",
                value_renderer: null /**/,
                hidden: true,
            },
            {
                title: "Confusion matrix",
                value_renderer: null,
                children: [
                    {
                        title: "True positives",
                        value_renderer: null /**/,
                        hidden: true,
                    },
                    {
                        title: "False negatives",
                        value_renderer: null /**/,
                        hidden: true,
                    },
                    {
                        title: "True negatives",
                        value_renderer: null /**/,
                        hidden: true,
                    },
                    {
                        title: "False positives",
                        value_renderer: null /**/,
                        hidden: true,
                    },
                ]
            },
        ],
    },
    {
        title: "Usage",
        value_renderer: null,
        category: "usage",
        children: [
            {
                title: "AMP August Survey",
                value_renderer: null,
                children: [
                    {
                        title: "Rank",
                        value_renderer: d => ({
                            parsed: (d.amp_survey.aug.primary_rank || "").toString(),
                            references: d.amp_survey.aug.primary_rank ? html_ref_link(d.amp_survey.aug) : "",
                        }),
                    },
                    {
                        title: "Percentage Labs",
                        value_renderer: d => ({
                            parsed: (d.amp_survey.aug.primary_lab_percentage || "").toString(),
                            references: d.amp_survey.aug.primary_rank ? html_ref_link(d.amp_survey.aug): "",
                        }),
                    }
                ]
            },
        ],
    },
    {
        title: "Derived values",
        value_renderer: null,
        category: "derived_values",
        children: [],
        hidden: true,
    },
]


function update_header (table_fields: TABLE_FIELDS, columns_hidden: boolean)
{
    const table_el = document.getElementById("data_table")
    const thead_el = table_el.getElementsByTagName("thead")[0]
    thead_el.innerHTML = ""
    const row1 = thead_el.insertRow()
    const row2 = thead_el.insertRow()
    const row3 = thead_el.insertRow()

    for (let i1 = 0; i1 < table_fields.length; ++i1)
    {
        const element1 = table_fields[i1]
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


function activate_options (table_fields: TABLE_FIELDS)
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
    update_header(table_fields, columns_hidden)
    document.getElementById("toggle_hidden_columns").onclick = () =>
    {
        columns_hidden = !columns_hidden
        update_computed_styles(columns_hidden)
        update_header(table_fields, columns_hidden)
    }
}

function update_computed_styles (columns_hidden: boolean)
{
    const style_el = document.getElementById("computed_style")
    style_el.innerHTML = columns_hidden ? `.hidden { display: none; }` : ``
}


function render_table_body (table_fields: TABLE_FIELDS, data_rows: DATA_ROWV3[])
{
    const table_el = document.getElementById("data_table")
    const tbody_el = table_el.getElementsByTagName("tbody")[0]

    data_rows.forEach((data_row, i) =>
    {
        const row = tbody_el.insertRow()

        iterate_lowest_table_field(table_fields, (table_field: TABLE_FIELDV3) =>
        {
            const cell = row.insertCell()
            cell.className = table_field.hidden ? "hidden value_el" : "value_el"
            cell.addEventListener("click", () => cell.classList.toggle("expanded"))

            if (!table_field.value_renderer) return

            const contents = table_field.value_renderer(data_row)

            const raw_el = document.createElement("div")
            const parsed_el = document.createElement("div")
            const comments_el = document.createElement("div")
            const references_el = document.createElement("div")

            raw_el.innerHTML = contents.raw || "&nbsp;"
            parsed_el.innerHTML = contents.parsed || `<span style="color: #fff; font-size: smaller;">not parsed</span>`
            raw_el.className = "raw_data" + (contents.parsed ? " less_important" : "")
            parsed_el.className = "parsed_data"
            comments_el.innerHTML = contents.comments || "&nbsp;"
            references_el.innerHTML = contents.references || " "

            cell.appendChild(raw_el)
            cell.appendChild(parsed_el)
            cell.appendChild(comments_el)
            cell.appendChild(references_el)
        })
    })
}


function iterate_lowest_table_field (table_fields: TABLE_FIELDS, func: (table_field: TABLE_FIELDV3) => void)
{
    for (let i1 = 0; i1 < table_fields.length; ++i1)
    {
        const element1 = table_fields[i1]

        if (!(element1.children && element1.children.length))
        {
            func(element1)
        }
        else for (let i2 = 0; i2 < element1.children.length; ++i2)
        {
            const element2 = element1.children[i2]

            if (!(element2.children && element2.children.length))
            {
                func(element2)
            }
            else for (let i3 = 0; i3 < element2.children.length; ++i3)
            {
                const element3 = element2.children[i3]
                func(element3)
            }
        }
    }
}


function hide_loading_status ()
{
    const loading_status_el = document.getElementById("loading_status")
    loading_status_el.style.display = "none"
}


const html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
}

const html_escape_regexps: { regexp: RegExp, replacement: string }[] = []
Object.keys(html_escape_table).forEach(key => {
    const regexp = new RegExp(key, "g")
    const replacement = html_escape_table[key]
    html_escape_regexps.push({ regexp, replacement })
})

function escape_html (html)
{
    if (!html) return html

    html_escape_regexps.forEach(({ regexp, replacement }) =>
        {
            html = html.replace(regexp, replacement)
        })

    return html
}


// Smells as it contains update for table header due to colspan not being under CSS control
// Need proper state / store manager
activate_options(table_fields)

// const filtered_data = filter_data_rows_to_remove_serology(merged_dataV3)
const ordered_data = merged_dataV3.sort((a, b) => (a.adveritasdx ? a.adveritasdx.ordinal : -1) < (b.adveritasdx ? b.adveritasdx.ordinal : -1) ? -1 : 1)
render_table_body(table_fields, ordered_data)
hide_loading_status()
document.getElementById("title_suffix").innerText = `(${ordered_data.length})`

}

mainV3()
