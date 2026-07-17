
# FoSpy JSON Map Guide - optional

[Download Here.](../../file_download/FoSpy_Map_Guides/optional_fields.json) If your browser does not download, save the page directly (usually with Ctrl + S).

[Return to Mapping Tutorial](./index.md)

```JSON
{
    "rename": {},
    "metadata": {
        "rename": {},
        "fos_id": "metadata.fos_id",
        "fos_type": "metadata.fos_type",
        "description": "metadata.description",
        "group_id": "metadata.group_id",
        "project_id": "metadata.project_id"
    },
    "experimenters": [
        {
            "rename": {},
            "name": "experimenters[0].name",
            "affiliation": "experimenters[0].affiliation",
            "orcid": "experimenters[0].orcid"
        },
        {
            "rename": {},
            "name": "experimenters[1].name",
            "affiliation": "experimenters[1].affiliation",
            "orcid": "experimenters[1].orcid"
        }
    ],
    "reaction": {
        "rename": {},
        "nominal_formula": "reaction.nominal_formula",
        "nominal_amount": "reaction.nominal_amount",
        "nominal_amount_unit": "reaction.nominal_amount_unit"
    },
    "products": [
        {
            "rename": {},
            "formula": "products[0].formula",
            "name": "products[0].name",
            "expected": "products[0].expected",
            "obtained": "products[0].obtained",
            "observations": "products[0].observations",
            "expected_amount": "products[0].expected_amount",
            "expected_amount_unit": "products[0].expected_amount_unit",
            "obtained_amount": "products[0].obtained_amount",
            "obtained_amount_unit": "products[0].obtained_amount_unit",
            "characterizations": "products[0].characterizations",
            "structure_comments": "products[0].structure_comments"
        },
        {
            "rename": {},
            "formula": "products[1].formula",
            "name": "products[1].name",
            "expected": "products[1].expected",
            "obtained": "products[1].obtained",
            "observations": "products[1].observations",
            "expected_amount": "products[1].expected_amount",
            "expected_amount_unit": "products[1].expected_amount_unit",
            "obtained_amount": "products[1].obtained_amount",
            "obtained_amount_unit": "products[1].obtained_amount_unit",
            "characterizations": "products[1].characterizations",
            "structure_comments": "products[1].structure_comments"
        }
    ],
    "materials": [
        {
            "rename": {},
            "name": "materials[0].name",
            "type": "materials[0].type",
            "formula": "materials[0].formula",
            "supplier": "materials[0].supplier",
            "cas": "materials[0].cas",
            "form": "materials[0].form",
            "env": "materials[0].env",
            "amount": "materials[0].amount",
            "amount_unit": "materials[0].amount_unit",
            "purity": "materials[0].purity",
            "treatments": [
                {
                    "rename": {},
                    "type": "materials[0].treatments[0].type",
                    "repeats": "materials[0].treatments[0].repeats",
                    "observations": "materials[0].treatments[0].observations",
                    "recovered_amount": "materials[0].treatments[0].recovered_amount",
                    "recovered_amount_unit": "materials[0].treatments[0].recovered_amount_unit",
                    "start_time": "materials[0].treatments[0].start_time",
                    "end_time": "materials[0].treatments[0].end_time"
                },
                {
                    "rename": {},
                    "type": "materials[0].treatments[1].type",
                    "repeats": "materials[0].treatments[1].repeats",
                    "observations": "materials[0].treatments[1].observations",
                    "recovered_amount": "materials[0].treatments[1].recovered_amount",
                    "recovered_amount_unit": "materials[0].treatments[1].recovered_amount_unit",
                    "start_time": "materials[0].treatments[1].start_time",
                    "end_time": "materials[0].treatments[1].end_time"
                }
            ]
        },
        {
            "rename": {},
            "name": "materials[1].name",
            "type": "materials[1].type",
            "formula": "materials[1].formula",
            "supplier": "materials[1].supplier",
            "cas": "materials[1].cas",
            "form": "materials[1].form",
            "env": "materials[1].env",
            "amount": "materials[1].amount",
            "amount_unit": "materials[1].amount_unit",
            "purity": "materials[1].purity",
            "treatments": [
                {
                    "rename": {},
                    "type": "materials[1].treatments[0].type",
                    "repeats": "materials[1].treatments[0].repeats",
                    "observations": "materials[1].treatments[0].observations",
                    "recovered_amount": "materials[1].treatments[0].recovered_amount",
                    "recovered_amount_unit": "materials[1].treatments[0].recovered_amount_unit",
                    "start_time": "materials[1].treatments[0].start_time",
                    "end_time": "materials[1].treatments[0].end_time"
                },
                {
                    "rename": {},
                    "type": "materials[1].treatments[1].type",
                    "repeats": "materials[1].treatments[1].repeats",
                    "observations": "materials[1].treatments[1].observations",
                    "recovered_amount": "materials[1].treatments[1].recovered_amount",
                    "recovered_amount_unit": "materials[1].treatments[1].recovered_amount_unit",
                    "start_time": "materials[1].treatments[1].start_time",
                    "end_time": "materials[1].treatments[1].end_time"
                }
            ]
        }
    ],
    "treatments": [
        {
            "rename": {},
            "type": "treatments[0].type",
            "repeats": "treatments[0].repeats",
            "observations": "treatments[0].observations",
            "recovered_amount": "treatments[0].recovered_amount",
            "recovered_amount_unit": "treatments[0].recovered_amount_unit",
            "start_time": "treatments[0].start_time",
            "end_time": "treatments[0].end_time"
        },
        {
            "rename": {},
            "type": "treatments[1].type",
            "repeats": "treatments[1].repeats",
            "observations": "treatments[1].observations",
            "recovered_amount": "treatments[1].recovered_amount",
            "recovered_amount_unit": "treatments[1].recovered_amount_unit",
            "start_time": "treatments[1].start_time",
            "end_time": "treatments[1].end_time"
        }
    ],
    "cif": {
        "rename": {},
        "file_name": "cif.file_name",
        "path": "cif.path",
        "embedded": "cif.embedded"
    },
    "cifs": [
        {
            "rename": {},
            "file_name": "cifs[0].file_name",
            "path": "cifs[0].path",
            "embedded": "cifs[0].embedded"
        },
        {
            "rename": {},
            "file_name": "cifs[1].file_name",
            "path": "cifs[1].path",
            "embedded": "cifs[1].embedded"
        }
    ],
    "laboratory_conditions": {
        "rename": {}
    },
    "equipment": [
        {
            "rename": {}
        },
        {
            "rename": {}
        }
    ]
}
```
