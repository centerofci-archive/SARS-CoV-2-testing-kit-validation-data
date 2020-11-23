
# Manually tagging and structuring FDA EUA data

Whilst extracting data, it's useful to break task in seperate work units.  Each with their corresponding prioritised label sets.

It's useful to have these common meta labels:

        "Meta/Not specified",
        "Meta/Not specified/Reasonable assumption",
        "Meta/Not specified/Partial information to reproduce"


## LOD

    localStorage.setItem("priority_labels", JSON.stringify([
        "Limit of Detection (LOD)/Value",
        "Limit of Detection (LOD)/Units",
        "Limit of Detection (LOD)/Minimum Replicates",
        "Specimen/Synthetic Specimen/Virus",
        "Specimen/Synthetic Specimen/Virus/Source",

        "Specimen/Synthetic Specimen/Virus/Type/Inactivated Virus (method unspecified)",
        "Specimen/Synthetic Specimen/Virus/Type/Live Virus",
        "Specimen/Synthetic Specimen/Virus/Type/Naked RNA",
        "Specimen/Synthetic Specimen/Virus/Type/Partial Live Virus",
        "Specimen/Synthetic Specimen/Virus/Type/Synthetic Viral Particles",

        "Specimen/Synthetic Specimen/Clinical matrix",
        "Specimen/Synthetic Specimen/Clinical matrix/Source",

        "Meta/Not specified",
        "Meta/Not specified/Reasonable assumption",
        "Meta/Not specified/Partial information to reproduce"
    ]))


## Sample types

    localStorage.setItem("priority_labels", JSON.stringify([
        "Supported specimen types",
        "Viral gene(s) targetted",
        "Controls/Internal/Human gene target",

        "Meta/Not specified",
        "Meta/Not specified/Reasonable assumption",
        "Meta/Not specified/Partial information to reproduce"
    ]))


## Primer probe Sequences

    localStorage.setItem("priority_labels", JSON.stringify([
        "Primers and probes/Sequences",
        "Primers and probes/Sequences/Explicitly specified",
        "Primers and probes/Sequences/Not assessed",
        "Primers and probes/Sequences/Not specified",
        "Primers and probes/Sequences/Reference available",

        "Meta/Not specified",
        "Meta/Not specified/Reasonable assumption",
        "Meta/Not specified/Partial information to reproduce"
    ]))

