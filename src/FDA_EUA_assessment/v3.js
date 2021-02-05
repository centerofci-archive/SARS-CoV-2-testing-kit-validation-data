var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
var __spreadArrays = (this && this.__spreadArrays) || function () {
    for (var s = 0, i = 0, il = arguments.length; i < il; i++) s += arguments[i].length;
    for (var r = Array(s), k = 0, i = 0; i < il; i++)
        for (var a = arguments[i], j = 0, jl = a.length; j < jl; j++, k++)
            r[k] = a[j];
    return r;
};
function is_adveritasdx_datum(field_value) {
    if (!field_value)
        return false;
    if (typeof field_value === "string" || typeof field_value === "number")
        return false;
    return true;
}
var adveritasdx_headers = [
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
];
function mainV3() {
    var get_comments_raw_and_references = function (annotations) {
        var raw = [];
        var comments = [];
        var references = [];
        annotations.forEach(function (_a) {
            var text = _a.text, comment = _a.comment, anot8_org_file_id = _a.anot8_org_file_id, id = _a.id;
            raw.push(text);
            comments.push(comment);
            references.push({ anot8_org_file_id: anot8_org_file_id, id: id });
        });
        return {
            raw: raw,
            comments: comments,
            references: references,
        };
    };
    var get_html_comments_raw_and_references = function (annotations) {
        var _a = get_comments_raw_and_references(annotations), raw = _a.raw, comments = _a.comments, references = _a.references;
        var raw_html = raw.map(escape_html).join(" &nbsp; ");
        var comments_html = comments
            .filter(function (comment) { return comment; })
            .map(function (comment) {
            return "<span title=\"" + escape_html(comment) + "\">C</span>";
        })
            .join(" ");
        var references_html = references.map(html_ref_link).join(" ");
        return {
            raw: raw_html,
            comments: comments_html,
            references: references_html,
        };
    };
    function ref_link(annotation) {
        var anot8_org_file_id = annotation.anot8_org_file_id, id = annotation.id;
        var host = safe_get_local_storage_item("anot8_server") || "https://anot8.org";
        var ref = host + "/r/1772.2/" + anot8_org_file_id;
        if (id !== undefined)
            ref += "?h=" + id;
        return ref;
    }
    function safe_get_local_storage_item(item) {
        return localStorage && localStorage.getItem(item);
    }
    function html_ref_link(annotation) {
        return "<a href=\"" + ref_link(annotation) + "\">R<a/>";
    }
    var value_renderer_EUA_URL = function (d) {
        var file_ids = d.anot8_org.file_ids_of_annotated;
        var references = file_ids.length ? "Perma Links: <a href=\"" + ref_link({ anot8_org_file_id: file_ids[0] }) + "\">1</a> " : "";
        if (file_ids.length > 1) {
            file_ids.slice(1).forEach(function (file_id, index) { return references += "<a href=\"" + ref_link({ anot8_org_file_id: file_id }) + "\">" + (index + 2) + "</a> "; });
        }
        if (d.anot8_org.file_ids_of_unannotated.length) {
            references += " <br /> Other: ";
            var offset_1 = d.anot8_org.file_ids_of_annotated.length + 1;
            d.anot8_org.file_ids_of_unannotated.forEach(function (file_id, index) {
                references += "<a href=\"" + ref_link({ anot8_org_file_id: file_id }) + "\">" + (index + offset_1) + "</a> ";
            });
        }
        references += " <br /> <a href=\"" + d.FDA_EUAs_list.url_to_IFU_or_EUA + "\">FDA site</a>";
        return { parsed: "&nbsp;", references: references };
    };
    var generic_value_renderer = function (data_node) {
        return __assign({ parsed: data_node.parsed }, get_html_comments_raw_and_references(data_node.annotations));
    };
    var ERROR_HTML_SYMBOL = "<span class=\"error_symbol\" title=\"Potential error\">\u26A0</span>";
    var adveritasdx_renderer = function (field) { return function (d) {
        var field_value = (d.adveritasdx || {})[field];
        if (!is_adveritasdx_datum(field_value)) {
            var raw_1 = (field_value || "").toString();
            return ({ raw: raw_1 });
        }
        var raw = escape_html((field_value.avd || "").toString().trim());
        var comments = "";
        var references = "";
        var annotations = field_value.annotations;
        if (annotations.length > 0) {
            var res = get_html_comments_raw_and_references(annotations);
            references = res.references;
            comments = res.comments;
            var annotations_raw = escape_html(res.raw).trim();
            if (!raw) {
                raw = annotations_raw;
            }
            else if (annotations_raw && raw !== annotations_raw) {
                raw = ERROR_HTML_SYMBOL + escape_html(raw + " != " + annotations_raw);
            }
        }
        return ({ parsed: "", raw: raw, comments: comments, references: references });
    }; };
    var table_fields = __spreadArrays([
        {
            title: "Export",
            value_renderer: function (d) { return ({ parsed: "<input type=\"checkbox\" onClick=\"export_toggled(event, '" + d.test_id + "')\"></input>" }); },
            category: "",
            disable_click_expand: true,
        },
        {
            title: "AdVeritasDx - CCI linked",
            value_renderer: function (d) { return ({ parsed: d.adveritasdx ? "" : "No" }); },
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
                    value_renderer: function (d) { return ({ parsed: d.FDA_EUAs_list.developer_name }); },
                },
                {
                    title: "Test name",
                    value_renderer: function (d) { return ({ parsed: d.FDA_EUAs_list.test_name }); },
                },
                {
                    title: "Latest<sup>*</sup> EUA or IFU",
                    value_renderer: value_renderer_EUA_URL,
                }
            ],
        }
    ], adveritasdx_headers.slice(3).map(function (field) { return ({
        title: field,
        value_renderer: adveritasdx_renderer(field),
        category: "",
    }); }), [
        {
            title: "Claims",
            value_renderer: null,
            category: "test_claims",
            children: [
                {
                    title: "Test technology",
                    value_renderer: function (d) { return ({ parsed: d.FDA_EUAs_list.test_technology }); },
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
                            value_renderer: function (d) { return generic_value_renderer(d.self_declared_EUA_data.supported_specimen_types); },
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
                    value_renderer: function (d) { return generic_value_renderer(d.self_declared_EUA_data.target_genes); },
                },
                {
                    title: "Primers and probes",
                    value_renderer: null,
                    children: [
                        {
                            title: "Sequences",
                            value_renderer: function (d) {
                                return generic_value_renderer(d.self_declared_EUA_data.primer_probe_sequences);
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
                            value_renderer: function (d) { return generic_value_renderer(d.self_declared_EUA_data.lod_value); },
                        },
                        {
                            title: "units",
                            value_renderer: function (d) { return generic_value_renderer(d.self_declared_EUA_data.lod_units); },
                        },
                        {
                            title: "Minimum replicates",
                            value_renderer: function (d) { return generic_value_renderer(d.self_declared_EUA_data.lod_minimum_replicates); },
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
                        { title: "Human gene", value_renderer: function (d) { return generic_value_renderer(d.self_declared_EUA_data.controls__human_gene_target); }, },
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
                    value_renderer: function (d) { return ({ parsed: "self" }); },
                },
                {
                    title: "Date",
                    value_renderer: function (d) { return ({ parsed: d.FDA_EUAs_list.first_issued_date }); },
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
                            value_renderer: function (d) { return generic_value_renderer(d.self_declared_EUA_data.synthetic_specimen__viral_material); },
                        },
                        {
                            title: "Viral material source",
                            value_renderer: null /**/,
                            hidden: true,
                        },
                        {
                            title: "Clinical matrix",
                            value_renderer: function (d) { return generic_value_renderer(d.self_declared_EUA_data.synthetic_specimen__clinical_matrix); },
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
                            value_renderer: function (d) { return ({
                                parsed: (d.amp_survey.aug.primary_rank || "").toString(),
                                references: d.amp_survey.aug.primary_rank ? html_ref_link(d.amp_survey.aug) : "",
                            }); },
                        },
                        {
                            title: "Percentage Labs",
                            value_renderer: function (d) { return ({
                                parsed: (d.amp_survey.aug.primary_lab_percentage || "").toString(),
                                references: d.amp_survey.aug.primary_rank ? html_ref_link(d.amp_survey.aug) : "",
                            }); },
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
    ]);
    function update_header(table_fields, columns_hidden) {
        var table_el = document.getElementById("data_table");
        var thead_el = table_el.getElementsByTagName("thead")[0];
        thead_el.innerHTML = "";
        var row1 = thead_el.insertRow();
        var row2 = thead_el.insertRow();
        var row3 = thead_el.insertRow();
        for (var i1 = 0; i1 < table_fields.length; ++i1) {
            var element1 = table_fields[i1];
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
    function activate_options(table_fields) {
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
        update_header(table_fields, columns_hidden);
        document.getElementById("toggle_hidden_columns").onclick = function () {
            columns_hidden = !columns_hidden;
            update_computed_styles(columns_hidden);
            update_header(table_fields, columns_hidden);
        };
        setup_exporter();
    }
    function update_computed_styles(columns_hidden) {
        var style_el = document.getElementById("computed_style");
        style_el.innerHTML = columns_hidden ? ".hidden { display: none; }" : "";
    }
    function setup_exporter() {
        var test_ids_to_export = new Set();
        var export_button_el = document.getElementById("export_button");
        export_button_el.onclick = function () {
            var contents = [];
            test_ids_to_export.forEach(function (id) {
                var row = ordered_data.find(function (_a) {
                    var test_id = _a.test_id;
                    return test_id === id;
                });
                var result = format_row_for_adveritasdx_export(row);
                if (result)
                    contents.push(result);
            });
            var contents_string = Papa.unparse(contents);
            var date = date2str(new Date(), "yyyy-MM-dd__hh_mm");
            var file_name = "export_for_adveritasdx_" + date + ".csv";
            offer_download(file_name, contents_string);
        };
        window.export_toggled = function (e, test_id) {
            if (e.currentTarget.checked)
                test_ids_to_export.add(test_id);
            else
                test_ids_to_export.delete(test_id);
            var num = test_ids_to_export.size;
            export_button_el.disabled = num === 0;
            export_button_el.value = "Export " + (num ? num + " " : "") + "data rows";
        };
    }
    //
    function render_table_body(table_fields, data_rows) {
        var table_el = document.getElementById("data_table");
        var tbody_el = table_el.getElementsByTagName("tbody")[0];
        data_rows.forEach(function (data_row, i) {
            var row = tbody_el.insertRow();
            row.setAttribute("data-foo", data_row.test_id);
            iterate_lowest_table_field(table_fields, function (table_field) {
                var cell = row.insertCell();
                cell.className = table_field.hidden ? "hidden value_el" : "value_el";
                if (!table_field.disable_click_expand) {
                    cell.addEventListener("click", function () { return cell.classList.toggle("expanded"); });
                }
                if (!table_field.value_renderer)
                    return;
                var contents = table_field.value_renderer(data_row);
                var raw_el = document.createElement("div");
                var parsed_el = document.createElement("div");
                var comments_el = document.createElement("div");
                var references_el = document.createElement("div");
                raw_el.innerHTML = contents.raw || "&nbsp;";
                parsed_el.innerHTML = contents.parsed || "<span style=\"color: #fff; font-size: smaller;\">not parsed</span>";
                raw_el.className = "raw_data" + (contents.parsed ? " less_important" : "");
                parsed_el.className = "parsed_data";
                comments_el.innerHTML = contents.comments || "&nbsp;";
                references_el.innerHTML = contents.references || " ";
                cell.appendChild(raw_el);
                cell.appendChild(parsed_el);
                cell.appendChild(comments_el);
                cell.appendChild(references_el);
            });
        });
    }
    function iterate_lowest_table_field(table_fields, func) {
        for (var i1 = 0; i1 < table_fields.length; ++i1) {
            var element1 = table_fields[i1];
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
    var html_escape_table = {
        "&": "&amp;",
        '"': "&quot;",
        "'": "&apos;",
        ">": "&gt;",
        "<": "&lt;",
    };
    var html_escape_regexps = [];
    Object.keys(html_escape_table).forEach(function (key) {
        var regexp = new RegExp(key, "g");
        var replacement = html_escape_table[key];
        html_escape_regexps.push({ regexp: regexp, replacement: replacement });
    });
    function escape_html(html) {
        if (!html)
            return html;
        html_escape_regexps.forEach(function (_a) {
            var regexp = _a.regexp, replacement = _a.replacement;
            html = html.replace(regexp, replacement);
        });
        return html;
    }
    function offer_download(file_name, file_contents) {
        var element = document.createElement("a");
        element.setAttribute("href", "data:text/plain;charset=utf-8," + encodeURIComponent(file_contents));
        element.setAttribute("download", file_name);
        element.style.display = "none";
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    }
    // https://stackoverflow.com/a/23593278/539490
    function date2str(date, format) {
        var z = {
            M: date.getUTCMonth() + 1,
            d: date.getUTCDate(),
            h: date.getUTCHours(),
            m: date.getUTCMinutes(),
            s: date.getUTCSeconds()
        };
        format = format.replace(/(M+|d+|h+|m+|s+)/g, function (v) {
            return ((v.length > 1 ? "0" : "") + z[v.slice(-1)]).slice(-2);
        });
        return format.replace(/(y+)/g, function (v) {
            return date.getUTCFullYear().toString().slice(-v.length);
        });
    }
    //
    function format_row_for_adveritasdx_export(row) {
        if (!row || !row.adveritasdx)
            return;
        return adveritasdx_headers.map(function (header) { return row.adveritasdx[header].toString(); });
    }
    //
    // Smells as it contains update for table header due to colspan not being under CSS control
    // Need proper state / store manager
    activate_options(table_fields);
    // const filtered_data = filter_data_rows_to_remove_serology(merged_dataV3)
    var ordered_data = merged_dataV3.sort(function (a, b) { return (a.adveritasdx ? a.adveritasdx.ordinal : -1) < (b.adveritasdx ? b.adveritasdx.ordinal : -1) ? -1 : 1; });
    render_table_body(table_fields, ordered_data);
    hide_loading_status();
    document.getElementById("title_suffix").innerText = "(" + ordered_data.length + ")";
}
mainV3();
