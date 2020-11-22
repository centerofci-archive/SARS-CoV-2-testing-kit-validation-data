"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.v2 = void 0;
var headers = [
    {
        title: "Developer",
        accessor: null,
        category: "test_descriptor",
        children: [
            {
                title: "Name",
                accessor: function (d) { return d.FDA_EUAs_list.developer_name; },
            },
            {
                title: "Test name",
                accessor: function (d) { return d.FDA_EUAs_list.test_name; },
            },
            {
                title: "IFU or EUA",
                accessor: function (d) { return d.FDA_EUAs_list.url_to_IFU_or_EUA; },
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
                accessor: function (d) { return d.FDA_EUAs_list.test_technology; },
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
                        accessor: function (d) {
                            var min = d.self_declared_EUA_data.lod_min;
                            var max = d.self_declared_EUA_data.lod_max;
                            if (min === max)
                                return min.toString();
                            return min + " <-> " + max;
                        },
                    },
                    {
                        title: "units",
                        accessor: function (d) { return d.self_declared_EUA_data.lod_units; },
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
                accessor: function (d) { return "self"; },
            },
            {
                title: "Date",
                accessor: function (d) { return d.FDA_EUAs_list.first_issued_date; },
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
                        accessor: function (d) { return d.self_declared_EUA_data.synthetic_specimen__viral_material.join(", "); },
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
];
function update_header(headers, columns_hidden) {
    var table_el = document.getElementById("data_table");
    var thead_el = table_el.getElementsByTagName("thead")[0];
    thead_el.innerHTML = "";
    var row1 = thead_el.insertRow();
    var row2 = thead_el.insertRow();
    var row3 = thead_el.insertRow();
    for (var i1 = 0; i1 < headers.length; ++i1) {
        var element1 = headers[i1];
        var className = element1.category + " header_label";
        var row1_width = 0;
        var row1_height = 1;
        if (!(element1.children && element1.children.length)) {
            row1_width = ((columns_hidden && element1.hidden) ? 0 : 1);
            row1_height = 3;
        }
        else
            for (var i2 = 0; i2 < element1.children.length; ++i2) {
                var element2 = element1.children[i2];
                var row2_width = 0;
                var row2_height = 1;
                if (!(element2.children && element2.children.length)) {
                    row2_width = ((columns_hidden && element2.hidden) ? 0 : 1);
                    row2_height = 2;
                }
                else
                    for (var i3 = 0; i3 < element2.children.length; ++i3) {
                        var element3 = element2.children[i3];
                        row2_width += ((columns_hidden && element3.hidden) ? 0 : 1);
                        var cell3 = document.createElement("th");
                        row3.appendChild(cell3);
                        cell3.innerHTML = element3.title;
                        cell3.className = className + ((columns_hidden && element3.hidden) ? " hidden" : "");
                    }
                var cell2 = document.createElement("th");
                row2.appendChild(cell2);
                cell2.innerHTML = element2.title;
                cell2.colSpan = row2_width;
                cell2.rowSpan = row2_height;
                cell2.className = className + (((columns_hidden && element2.hidden) || (row2_width === 0)) ? " hidden" : "");
                row1_width += row2_width;
            }
        var cell1 = document.createElement("th");
        row1.appendChild(cell1);
        cell1.innerHTML = element1.title;
        cell1.colSpan = row1_width;
        cell1.rowSpan = row1_height;
        cell1.className = className + (((columns_hidden && element1.hidden) || (row1_width === 0)) ? " hidden" : "");
    }
}
function activate_options(headers) {
    var cells_expanded = false;
    document.getElementById("toggle_expanded_cells").onclick = function () {
        cells_expanded = !cells_expanded;
        var cells = Array.from(document.getElementsByClassName("value_el"));
        if (cells_expanded) {
            cells.forEach(function (cell) { return cell.classList.add("expanded"); });
        }
        else {
            cells.forEach(function (cell) { return cell.classList.remove("expanded"); });
        }
    };
    var columns_hidden = true;
    update_computed_styles(columns_hidden);
    update_header(headers, columns_hidden);
    document.getElementById("toggle_hidden_columns").onclick = function () {
        columns_hidden = !columns_hidden;
        update_computed_styles(columns_hidden);
        update_header(headers, columns_hidden);
    };
}
function update_computed_styles(columns_hidden) {
    var style_el = document.getElementById("computed_style");
    style_el.innerHTML = columns_hidden ? ".hidden { display: none; }" : "";
}
function filter_data_rows_to_remove_serology(data_rows) {
    var filtered_data_rows = data_rows.filter(function (d) {
        var tech = d.FDA_EUAs_list.test_technology.toLowerCase();
        // Finds most of the them.
        var remove = tech.includes("serology") || tech.includes("igg") || tech.includes("igm") || tech.includes("total antibody") || tech.includes("immunoassay");
        return !remove;
    });
    return filtered_data_rows;
}
function render_table_body(headers, data_rows) {
    var table_el = document.getElementById("data_table");
    var tbody_el = table_el.getElementsByTagName("tbody")[0];
    data_rows.forEach(function (data_row, i) {
        var row = tbody_el.insertRow();
        iterate_lowest_header(headers, function (header) {
            var cell = row.insertCell();
            cell.className = header.hidden ? "hidden" : "";
            if (!header.accessor)
                return;
            var contents = header.accessor(data_row);
            if (!contents)
                return;
            cell.innerText = contents;
        });
    });
}
function iterate_lowest_header(headers, func) {
    for (var i1 = 0; i1 < headers.length; ++i1) {
        var element1 = headers[i1];
        if (!(element1.children && element1.children.length)) {
            func(element1);
        }
        else
            for (var i2 = 0; i2 < element1.children.length; ++i2) {
                var element2 = element1.children[i2];
                if (!(element2.children && element2.children.length)) {
                    func(element2);
                }
                else
                    for (var i3 = 0; i3 < element2.children.length; ++i3) {
                        var element3 = element2.children[i3];
                        func(element3);
                    }
            }
    }
}
function hide_loading_status() {
    var loading_status_el = document.getElementById("loading_status");
    loading_status_el.style.display = "none";
}
// Smells as it contains update for table header due to colspan not being under CSS control
// Need proper state / store manager
activate_options(headers);
var filtered_data = filter_data_rows_to_remove_serology(merged_data);
render_table_body(headers, filtered_data);
hide_loading_status();
var v2 = 2;
exports.v2 = v2;
