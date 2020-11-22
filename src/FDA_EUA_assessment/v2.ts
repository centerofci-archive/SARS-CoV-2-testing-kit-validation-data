
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

declare var merged_data: DATA_ROW[]


interface HEADER {
    title: string
    accessor: (data_row: DATA_ROW) => string
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
        title: "Developer",
        accessor: null,
        category: "test_descriptor",
        children: [
            {
                title: "Name",
                accessor: d => d.FDA_EUAs_list.developer_name,
            },
            {
                title: "Test name",
                accessor: d => d.FDA_EUAs_list.test_name,
            },
            {
                title: "IFU or EUA",
                accessor: d => d.FDA_EUAs_list.url_to_IFU_or_EUA,
            }
        ],
    },
    {
        title: "Claims",
        accessor: null,
        category: "test_claims",
        children: [
            {
                title: "Test technology",
                accessor: d => d.FDA_EUAs_list.test_technology,
            },
            {
                title: "Specimens",
                accessor: null,
                children: [
                    {
                        title: "Supported specimen types",
                        accessor: null /**/,
                    },
                    {
                        title: "Transport medium",
                        accessor: null,
                    },
                ]
            },
            {
                // Not in May 13th version of FDA EUA template
                title: "Appropriate testing population",
                // e.g. * patients suspected of COVID-19 by a healthcare provider
                //      * pooled samples
                //      * general, asymptomatic screening population i.e. screening of individuals without symptoms or other reasons to suspect COVID-19
                accessor: null,
                hidden: true,
            },
            {
                // Not in May 13th version of FDA EUA template
                title: "Sample pooling",
                accessor: null,
                hidden: true,
                children: [
                    { title: "Approach", accessor: null, hidden: true, },
                    { title: "Max no. specimens", accessor: null, hidden: true, },
                ]
            },
            { title: "Target gene(s) of SARS-CoV-2", accessor: null /**/, },
            {
                title: "Primers and probes",
                accessor: null,
                children: [
                    { title: "Sequences", accessor: null /**/, },
                    { title: "Sources", accessor: null /**/, hidden: true, },
                ]
            },
            {
                // Not in May 13th version of FDA EUA template
                // i.e. can include more than just SARS-CoV-2
                title: "Detects pathogen(s)",
                accessor: null,
                hidden: true,
            },
            {
                title: "Limit of Detection (LOD)",
                accessor: null,
                children: [
                    {
                        title: "value",
                        accessor: d => {
                            const min = d.self_declared_EUA_data.lod_min
                            const max = d.self_declared_EUA_data.lod_max

                            if (min === max) return min.toString()

                            return `${min} <-> ${max}`
                        },
                    },
                    {
                        title: "units",
                        accessor: d => d.self_declared_EUA_data.lod_units,
                    },
                    {
                        title: "Minimum replicates",
                        accessor: null /*d => d.self_declared_EUA_data.*/,
                    },
                ]
            },
            {
                title: "Intended user",
                // e.g. CLIA labs
                accessor: null,
                hidden: true,
            },
            { title: "Compatible equipment", accessor: null, hidden: true, },
            // {
                // Product Overview/Test Principle...
                //     // primer and probe sets and briefly describe what they detect. Please include the nucleic acid sequences for all primers and probes used in the test. Please indicate if the test uses biotin-Streptavidin/avidin chemistry
                // },
            {
                title: "Controls",
                accessor: null,
                children: [
                    { title: "Human gene", accessor: null /**/, },
                ]
            },
            {
                title: "RNA extraction",
                accessor: null,
                children: [
                    { title: "Specimen input volume", accessor: null, hidden: true, },
                    { title: "RNA extraction method(s)", accessor: null, hidden: true, },
                    { title: "Nucleic acid elution volume", accessor: null, hidden: true, },
                    { title: "Purification manual &/ automated", accessor: null, hidden: true, },
                ]
            },
            {
                title: "Reverse transcription",
                accessor: null,
                children: [
                    { title: "Input volume", accessor: null, hidden: true, },
                    { title: "Enzyme mix / kits", accessor: null, hidden: true, },
                ]
            },
            {
                title: "PCR / amplification",
                accessor: null,
                children: [
                    { title: "Instrument", accessor: null, hidden: true, },
                    { title: "Enzyme mix / kits", accessor: null, hidden: true, },
                    { title: "Reaction volume / μL", accessor: null /**/, },
                ]
            },
            {
                title: "PCR quantification fluoresence detection",
                accessor: null,
                children: [
                    { title: "Instrument", accessor: null, hidden: true, },
                ]
            },
        ],
    },
    {
        title: "Validation conditions",
        accessor: null,
        category: "validation_condition",
        children: [
            {
                title: "Author",
                accessor: d => "self",
            },
            {
                title: "Date",
                accessor: d => d.FDA_EUAs_list.first_issued_date,
            },
            {
                title: "Patient details",
                accessor: null,
                children: [
                    { title: "Age", accessor: null, hidden: true, },
                    { title: "Race", accessor: null, hidden: true, },
                    { title: "Gender", accessor: null, hidden: true, },
                ]
            },
            { title: "Disease stage", accessor: null, hidden: true, },
            {
                title: "Synthetic Specimen",
                accessor: null,
                children: [
                    {
                        title: "Viral material",
                        accessor: d => d.self_declared_EUA_data.synthetic_specimen__viral_material.join(", "),
                    },
                    {
                        title: "Viral material source",
                        accessor: null /**/,
                    },
                    {
                        title: "Clinical matrix",
                        accessor: null /**/,
                    },
                    {
                        title: "Clinical matrix source",
                        accessor: null /**/,
                    },
                ]
            },
            {
                title: "Specimen",
                accessor: null,
                children: [
                    {
                        title: "Type",
                        accessor: null /**/,
                        hidden: true,
                    },
                    {
                        title: "Swab type",
                        accessor: null /**/,
                        hidden: true,
                    },
                    {
                        title: "Transport medium",
                        accessor: null /**/,
                        hidden: true,
                    },
                    {
                        title: "Sample volume",
                        accessor: null /**/,
                        hidden: true,
                    },
                ]
            },
        ],
    },
    {
        title: "Metrics",
        accessor: null,
        category: "metric",
        children: [
            {
                title: "Number of clinical samples",
                accessor: null,
                children: [
                    {
                        title: "Positives",
                        accessor: null /**/,
                        hidden: true,
                    },
                    {
                        title: "Controls (negatives)",
                        accessor: null /**/,
                        hidden: true,
                    },
                ]
            },
            {
                title: "Comparator test",
                accessor: null /**/,
                hidden: true,
            },
            {
                title: "Confusion matrix",
                accessor: null,
                children: [
                    {
                        title: "True positives",
                        accessor: null /**/,
                        hidden: true,
                    },
                    {
                        title: "False negatives",
                        accessor: null /**/,
                        hidden: true,
                    },
                    {
                        title: "True negatives",
                        accessor: null /**/,
                        hidden: true,
                    },
                    {
                        title: "False positives",
                        accessor: null /**/,
                        hidden: true,
                    },
                ]
            },
        ],
    },
    {
        title: "Derived values",
        accessor: null,
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




function filter_data_rows_to_remove_serology (data_rows: DATA_ROW[])
{
    const filtered_data_rows = data_rows.filter(d => {
        const tech = d.FDA_EUAs_list.test_technology.toLowerCase()
        // Finds most of the them.
        const remove = tech.includes("serology") || tech.includes("igg") || tech.includes("igm") || tech.includes("total antibody") || tech.includes("immunoassay")
        return !remove
    })

    return filtered_data_rows
}


function render_table_body (headers: HEADERS, data_rows: DATA_ROW[])
{
    const table_el = document.getElementById("data_table")
    const tbody_el = table_el.getElementsByTagName("tbody")[0]

    data_rows.forEach((data_row, i) =>
    {
        const row = tbody_el.insertRow()

        iterate_lowest_header(headers, (header: HEADER) =>
        {
            const cell = row.insertCell()
            cell.className = header.hidden ? "hidden" : ""

            if (!header.accessor) return

            const contents = header.accessor(data_row)
            if (!contents) return

            cell.innerText = contents
        })
    })
}


function iterate_lowest_header (headers: HEADERS, func: (header: HEADER) => void)
{
    for (let i1 = 0; i1 < headers.length; ++i1)
    {
        const element1 = headers[i1]

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


// Smells as it contains update for table header due to colspan not being under CSS control
// Need proper state / store manager
activate_options(headers)

const filtered_data = filter_data_rows_to_remove_serology(merged_data)
render_table_body(headers, filtered_data)
hide_loading_status()


const v2 = 2
export { v2 }
