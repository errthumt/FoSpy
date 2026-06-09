# Synthesis Examples

Each file on this page was generated at the corresponding checkpoint in the [walkthrough](../API_example/index.md) script.

---

## Initial Synthesis (FOS)

```fos
fos_id: TE001
fos_type: synthesis
description: My First Synthesis
group_id: kovnir-0000-0003-1152-1912
project_id: travis5672/clathrates/Ba2-TM5-Sb6

[Experimenters]
name: Travis Errthum
affiliation: Kovnir Group - Iowa State University
orcid: 0009-0006-1937-5672

// Single brackets on a header mean there is only one group
[Reaction]
nominal_formula: Ba2Zn5Sb6
nominal_amount: 250.0
nominal_amount_unit: mg

[Products]
name: Barium Zinc Antimonide (2-5-6)
formula: Ba2Zn5Sb6
expected: true
obtained: true
expected_amount: 250.0
expected_amount_unit: mg
obtained_amount: 200.0
obtained_amount_unit: mg
observations: Black Powder
characterizations: PXRD, EDS, Eyeballs
structure_comments: [;;;
    Unique clathrate with novel polyhedra.
    Space group Pnma]

// Double brackets on a header mean there are multiple similar groups
[[Materials]]
:name
:type
:formula
:supplier
:cas
:form
:purity
:env
:amount
:amount_unit
:treatments

    Barium
    reagent
    Ba
    Thermofisher
    7440-39-3
    lump
    0.999
    Ar (g)
    // The comment below will be correctly re-calculated using a calc_routine
    // ! Total weight percent: 200%
    2.0
    mol ratio
    // Similar to headers, single brackets mean there is only one group,
    // in this case for treatments of Barium
    [
        type: cutting
        repeats: 1
        observations: smaller pieces improve homogenization
    ]

    Zinc
    reagent
    Zn
    Sigma Aldrich
    7440-66-6
    powder
    0.995
    Ar (g)
    5.0
    mol ratio
    []

    Antimony
    reagent
    Sb
    Chem Stores?
    7440-36-0
    powder
    0.999
    Ar (g)
    6.0
    mol ratio
    []

    

// This is a comment on the treatments block
[[Treatments]]
:type
:repeats
:observations

    weigh
    1
    // The syntax below allows me to use multiple lines for longer texts.
    [;;;
    Weighed stoichiometrically to carbonized ampoule.
    Barium added last to avoid contact with ampoule 
    during reaction]
    recovered_mass: 250.0

    seal
    1
    Evacuated ampoule and sealed with H2/O2 torch

    anneal
    2
    Opened under argon atmosphere and ground well before sealing in new ampoule in between annealings.
    start_temp: 25
    start_temp_unit: C
    // Here, the double brackets signal that there are multiple program sections.
    program: [[
        type: ramp
        temp: 600
        time: 10
        temp_unit: C
        time_unit: h


        type: dwell
        time: 120
        time_unit: h
    ]]

    grind
    3
    dark gray powder now
    recovered_mass: 200.0

[CIFs]
file_name: Ba2Zn5Sb6_ICSD
extension: .cif
embedded: {{{

#(C) 2025 by FIZ Karlsruhe - Leibniz Institute for Information Infrastructure.  All rights reserved.
data_71031-ICSD
_database_code_ICSD 71031
_audit_creation_date 2023-08-01
_chemical_name_common 'Barium zinc antimonide (2/5/6)'
_chemical_formula_structural 'Ba2 Zn5 Sb6'
_chemical_formula_sum 'Ba2 Sb6 Zn5'
_exptl_crystal_density_diffrn 6.13
_diffrn_ambient_temperature 100.
_citation_title
;
New trick for an old dog: from prediction to properties of  hidden clathrates 
\(Ba_2 Zn_5As_6\) and \(Ba_2 Zn_5Sb_6\)
;
loop_
_citation_id
_citation_journal_full
_citation_year
_citation_journal_volume
_citation_page_first
_citation_page_last
_citation_journal_id_ASTM
primary 'Journal of the American Chemical Society' 2023 145 4638 4646 JACSAT
loop_
_citation_author_citation_id
_citation_author_name
primary 'Yox, Philip'
primary 'Cerasoli, Frank'
primary 'Sarkar, Arka'
primary 'Kyveryga, Victoria'
primary 'Viswanathan, Gayatri'
primary 'Donadio, Davide'
primary 'Kovnir, Kirill'
_cell_length_a 11.4154(5)
_cell_length_b 10.0135(4)
_cell_length_c 12.6172(5)
_cell_angle_alpha 90
_cell_angle_beta 90
_cell_angle_gamma 90
_cell_volume 1442.24
_cell_formula_units_Z 4
_space_group_name_H-M_alt 'P m n a'
_space_group_IT_number 53
loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1 'x+1/2, y, -z+1/2'
2 'x+1/2, -y, z+1/2'
3 '-x, y, z'
4 '-x, -y, -z'
5 '-x+1/2, -y, z+1/2'
6 '-x+1/2, y, -z+1/2'
7 'x, -y, -z'
8 'x, y, z'
loop_
_atom_type_symbol
_atom_type_oxidation_number
Ba0+ 0
Sb0+ 0
Zn0+ 0
loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_symmetry_multiplicity
_atom_site_Wyckoff_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_U_iso_or_equiv
_atom_site_occupancy
Ba1 Ba0+ 4 h 0.5 0.23891(4) 0.64640(3) 0.00367(9) 1
Ba2 Ba0+ 4 g 0.75 0.71608(4) 0.75 0.00794(10) 1
Sb1 Sb0+ 4 f 0.32061(4) 0.5 0.5 0.00275(10) 1
Sb2 Sb0+ 4 h 0.5 0.86799(4) 0.61427(3) 0.00219(10) 1
Sb3 Sb0+ 4 h 0.5 0.73181(4) 0.93973(3) 0.00287(10) 1
Sb4 Sb0+ 8 i 0.19164(3) 0.10079(3) 0.65092(2) 0.00228(8) 1
Sb5 Sb0+ 4 h 0.5 0.50694(4) 0.80966(3) 0.00258(10) 1
Zn1 Zn0+ 4 h 0.5 0.94723(7) 0.81658(6) 0.00330(16) 1
Zn2 Zn0+ 4 e 0.33104(7) 0. 0.5 0.00356(16) 1
Zn3 Zn0+ 4 h 0.5 0.60202(7) 0.61084(6) 0.00339(16) 1
Zn4 Zn0+ 8 i 0.15880(5) 0.65041(5) 0.41232(4) 0.00452(13) 1
loop_
_atom_site_aniso_label
_atom_site_aniso_type_symbol
_atom_site_aniso_U_11
_atom_site_aniso_U_22
_atom_site_aniso_U_33
_atom_site_aniso_U_12
_atom_site_aniso_U_13
_atom_site_aniso_U_23
Ba1 Ba0+ 0.0056(2) 0.00269(19) 0.00270(18) 0. 0. -0.00066(15)
Ba2 Ba0+ 0.0031(2) 0.0110(2) 0.0097(2) 0. -0.00029(16) 0.
Sb1 Sb0+ 0.0025(2) 0.0026(2) 0.0031(2) 0. 0. 0.00002(17)
Sb2 Sb0+ 0.0037(2) 0.0013(2) 0.0015(2) 0. 0. -0.00028(17)
Sb3 Sb0+ 0.0053(2) 0.0017(2) 0.0016(2) 0. 0. -0.00002(17)
Sb4 Sb0+ 0.00259(16) 0.00227(16) 0.00198(14) 0.00013(12) 0.00028(12)
-0.00016(12)
Sb5 Sb0+ 0.0043(2) 0.0014(2) 0.0020(2) 0. 0. 0.00017(17)
Zn1 Zn0+ 0.0041(4) 0.0027(4) 0.0032(4) 0. 0. 0.0000(3)
Zn2 Zn0+ 0.0034(4) 0.0039(4) 0.0034(4) 0. 0. -0.0007(3)
Zn3 Zn0+ 0.0043(4) 0.0023(4) 0.0036(4) 0. 0. 0.0006(3)
Zn4 Zn0+ 0.0051(3) 0.0030(3) 0.0054(3) -0.0001(2) -0.0003(2) 0.0010(2)
#End of TTdata_71031-ICSD
#################### END FOS EMBED }}}
```

## Initial Synthesis (JSON)

```json
{
    "metadata": {
        "fos_id": "TE001",
        "fos_type": "synthesis",
        "description": "My First Synthesis",
        "group_id": "kovnir-0000-0003-1152-1912",
        "project_id": "travis5672/clathrates/Ba2-TM5-Sb6"
    },
    "experimenters": [
        {
            "name": "Travis Errthum",
            "affiliation": "Kovnir Group - Iowa State University",
            "orcid": "0009-0006-1937-5672"
        }
    ],
    "reaction": {
        "nominal_formula": "Ba2Zn5Sb6",
        "nominal_amount": "250.0",
        "nominal_amount_unit": "milligram"
    },
    "products": [
        {
            "name": "Barium Zinc Antimonide (2-5-6)",
            "formula": "Ba2Zn5Sb6",
            "expected": "True",
            "obtained": "True",
            "expected_amount": "250.0",
            "expected_amount_unit": "milligram",
            "obtained_amount": "200.0",
            "obtained_amount_unit": "milligram",
            "observations": "Black Powder",
            "characterizations": "PXRD, EDS, Eyeballs",
            "structure_comments": "Unique clathrate with novel polyhedra. Space group Pnma"
        }
    ],
    "materials": [
        {
            "name": "Barium",
            "type": "reagent",
            "formula": "Ba",
            "supplier": "Thermofisher",
            "cas": "7440-39-3",
            "form": "lump",
            "purity": "0.999",
            "env": "Ar (g)",
            "amount": "2.0",
            "amount_unit": "mol ratio",
            "treatments": [
                {
                    "type": "cutting",
                    "repeats": "1",
                    "observations": "smaller pieces improve homogenization"
                }
            ]
        },
        {
            "name": "Zinc",
            "type": "reagent",
            "formula": "Zn",
            "supplier": "Sigma Aldrich",
            "cas": "7440-66-6",
            "form": "powder",
            "purity": "0.995",
            "env": "Ar (g)",
            "amount": "5.0",
            "amount_unit": "mol ratio",
            "treatments": []
        },
        {
            "name": "Antimony",
            "type": "reagent",
            "formula": "Sb",
            "supplier": "Chem Stores?",
            "cas": "7440-36-0",
            "form": "powder",
            "purity": "0.999",
            "env": "Ar (g)",
            "amount": "6.0",
            "amount_unit": "mol ratio",
            "treatments": []
        }
    ],
    "treatments": [
        {
            "type": "weigh",
            "repeats": "1",
            "observations": "Weighed stoichiometrically to carbonized ampoule. Barium added last to avoid contact with ampoule during reaction",
            "recovered_mass": "250.0"
        },
        {
            "type": "seal",
            "repeats": "1",
            "observations": "Evacuated ampoule and sealed with H2/O2 torch"
        },
        {
            "type": "anneal",
            "repeats": "2",
            "observations": "Opened under argon atmosphere and ground well before sealing in new ampoule in between annealings.",
            "start_temp": "25",
            "start_temp_unit": "degree_Celsius",
            "program": [
                {
                    "type": "ramp",
                    "temp": "600",
                    "time": "10",
                    "temp_unit": "degree_Celsius",
                    "time_unit": "hour"
                },
                {
                    "type": "dwell",
                    "time": "120",
                    "time_unit": "hour"
                }
            ]
        },
        {
            "type": "grind",
            "repeats": "3",
            "observations": "dark gray powder now",
            "recovered_mass": "200.0"
        }
    ],
    "cifs": [
        {
            "file_name": "Ba2Zn5Sb6_ICSD",
            "extension": ".cif",
            "embedded": [
                "\n",
                "#(C) 2025 by FIZ Karlsruhe - Leibniz Institute for Information Infrastructure.  All rights reserved.\n",
                "data_71031-ICSD\n",
                "_database_code_ICSD 71031\n",
                "_audit_creation_date 2023-08-01\n",
                "_chemical_name_common 'Barium zinc antimonide (2/5/6)'\n",
                "_chemical_formula_structural 'Ba2 Zn5 Sb6'\n",
                "_chemical_formula_sum 'Ba2 Sb6 Zn5'\n",
                "_exptl_crystal_density_diffrn 6.13\n",
                "_diffrn_ambient_temperature 100.\n",
                "_citation_title\n",
                ";\n",
                "New trick for an old dog: from prediction to properties of  hidden clathrates \n",
                "\\(Ba_2 Zn_5As_6\\) and \\(Ba_2 Zn_5Sb_6\\)\n",
                ";\n",
                "loop_\n",
                "_citation_id\n",
                "_citation_journal_full\n",
                "_citation_year\n",
                "_citation_journal_volume\n",
                "_citation_page_first\n",
                "_citation_page_last\n",
                "_citation_journal_id_ASTM\n",
                "primary 'Journal of the American Chemical Society' 2023 145 4638 4646 JACSAT\n",
                "loop_\n",
                "_citation_author_citation_id\n",
                "_citation_author_name\n",
                "primary 'Yox, Philip'\n",
                "primary 'Cerasoli, Frank'\n",
                "primary 'Sarkar, Arka'\n",
                "primary 'Kyveryga, Victoria'\n",
                "primary 'Viswanathan, Gayatri'\n",
                "primary 'Donadio, Davide'\n",
                "primary 'Kovnir, Kirill'\n",
                "_cell_length_a 11.4154(5)\n",
                "_cell_length_b 10.0135(4)\n",
                "_cell_length_c 12.6172(5)\n",
                "_cell_angle_alpha 90\n",
                "_cell_angle_beta 90\n",
                "_cell_angle_gamma 90\n",
                "_cell_volume 1442.24\n",
                "_cell_formula_units_Z 4\n",
                "_space_group_name_H-M_alt 'P m n a'\n",
                "_space_group_IT_number 53\n",
                "loop_\n",
                "_space_group_symop_id\n",
                "_space_group_symop_operation_xyz\n",
                "1 'x+1/2, y, -z+1/2'\n",
                "2 'x+1/2, -y, z+1/2'\n",
                "3 '-x, y, z'\n",
                "4 '-x, -y, -z'\n",
                "5 '-x+1/2, -y, z+1/2'\n",
                "6 '-x+1/2, y, -z+1/2'\n",
                "7 'x, -y, -z'\n",
                "8 'x, y, z'\n",
                "loop_\n",
                "_atom_type_symbol\n",
                "_atom_type_oxidation_number\n",
                "Ba0+ 0\n",
                "Sb0+ 0\n",
                "Zn0+ 0\n",
                "loop_\n",
                "_atom_site_label\n",
                "_atom_site_type_symbol\n",
                "_atom_site_symmetry_multiplicity\n",
                "_atom_site_Wyckoff_symbol\n",
                "_atom_site_fract_x\n",
                "_atom_site_fract_y\n",
                "_atom_site_fract_z\n",
                "_atom_site_U_iso_or_equiv\n",
                "_atom_site_occupancy\n",
                "Ba1 Ba0+ 4 h 0.5 0.23891(4) 0.64640(3) 0.00367(9) 1\n",
                "Ba2 Ba0+ 4 g 0.75 0.71608(4) 0.75 0.00794(10) 1\n",
                "Sb1 Sb0+ 4 f 0.32061(4) 0.5 0.5 0.00275(10) 1\n",
                "Sb2 Sb0+ 4 h 0.5 0.86799(4) 0.61427(3) 0.00219(10) 1\n",
                "Sb3 Sb0+ 4 h 0.5 0.73181(4) 0.93973(3) 0.00287(10) 1\n",
                "Sb4 Sb0+ 8 i 0.19164(3) 0.10079(3) 0.65092(2) 0.00228(8) 1\n",
                "Sb5 Sb0+ 4 h 0.5 0.50694(4) 0.80966(3) 0.00258(10) 1\n",
                "Zn1 Zn0+ 4 h 0.5 0.94723(7) 0.81658(6) 0.00330(16) 1\n",
                "Zn2 Zn0+ 4 e 0.33104(7) 0. 0.5 0.00356(16) 1\n",
                "Zn3 Zn0+ 4 h 0.5 0.60202(7) 0.61084(6) 0.00339(16) 1\n",
                "Zn4 Zn0+ 8 i 0.15880(5) 0.65041(5) 0.41232(4) 0.00452(13) 1\n",
                "loop_\n",
                "_atom_site_aniso_label\n",
                "_atom_site_aniso_type_symbol\n",
                "_atom_site_aniso_U_11\n",
                "_atom_site_aniso_U_22\n",
                "_atom_site_aniso_U_33\n",
                "_atom_site_aniso_U_12\n",
                "_atom_site_aniso_U_13\n",
                "_atom_site_aniso_U_23\n",
                "Ba1 Ba0+ 0.0056(2) 0.00269(19) 0.00270(18) 0. 0. -0.00066(15)\n",
                "Ba2 Ba0+ 0.0031(2) 0.0110(2) 0.0097(2) 0. -0.00029(16) 0.\n",
                "Sb1 Sb0+ 0.0025(2) 0.0026(2) 0.0031(2) 0. 0. 0.00002(17)\n",
                "Sb2 Sb0+ 0.0037(2) 0.0013(2) 0.0015(2) 0. 0. -0.00028(17)\n",
                "Sb3 Sb0+ 0.0053(2) 0.0017(2) 0.0016(2) 0. 0. -0.00002(17)\n",
                "Sb4 Sb0+ 0.00259(16) 0.00227(16) 0.00198(14) 0.00013(12) 0.00028(12)\n",
                "-0.00016(12)\n",
                "Sb5 Sb0+ 0.0043(2) 0.0014(2) 0.0020(2) 0. 0. 0.00017(17)\n",
                "Zn1 Zn0+ 0.0041(4) 0.0027(4) 0.0032(4) 0. 0. 0.0000(3)\n",
                "Zn2 Zn0+ 0.0034(4) 0.0039(4) 0.0034(4) 0. 0. -0.0007(3)\n",
                "Zn3 Zn0+ 0.0043(4) 0.0023(4) 0.0036(4) 0. 0. 0.0006(3)\n",
                "Zn4 Zn0+ 0.0051(3) 0.0030(3) 0.0054(3) -0.0001(2) -0.0003(2) 0.0010(2)\n",
                "#End of TTdata_71031-ICSD\n"
            ]
        }
    ]
}
```

## Checkpoint 1

```fos
fos_id: TE001
fos_type: synthesis
description: My First Synthesis
group_id: kovnir-0000-0003-1152-1912
project_id: travis5672/clathrates/Ba2-TM5-Sb6

[Experimenters]
name: Travis Errthum
affiliation: Kovnir Group - Iowa State University
orcid: 0009-0006-1937-5672

// Single brackets on a header mean there is only one group
[Reaction]
nominal_formula: Ba2Zn5Sb6
nominal_amount: 250.0
nominal_amount_unit: milligram

[Products]
name: Barium Zinc Antimonide (2-5-6)
formula: Ba2Zn5Sb6
expected: True
obtained: True
expected_amount: 250.0
expected_amount_unit: milligram
obtained_amount: 200.0
obtained_amount_unit: milligram
observations: Black Powder
characterizations: PXRD, EDS, Eyeballs
structure_comments: Unique clathrate with novel polyhedra. Space group Pnma

// Double brackets on a header mean there are multiple similar groups
[[Materials]]
:name
:type
:formula
:supplier
:cas
:form
:purity
:env
:amount
:amount_unit
:treatments

    Barium
    reagent
    Ba
    Thermofisher
    7440-39-3
    lump
    0.999
    Ar (g)
    // The comment below will be correctly re-calculated using a calc_routine
    2.0
    mol ratio
    // Similar to headers, single brackets mean there is only one group,
    // in this case for treatments of Barium
    [
        type: cutting
        repeats: 1
        observations: smaller pieces improve homogenization
    ]

    Zinc
    reagent
    Zn
    Sigma Aldrich
    7440-66-6
    powder
    0.995
    Ar (g)
    5.0
    mol ratio
    []

    Antimony
    reagent
    Sb
    Chem Stores?
    7440-36-0
    powder
    0.999
    Ar (g)
    6.0
    mol ratio
    []

// This is a comment on the treatments block
[[Treatments]]
:type
:repeats
:observations

    weigh
    1
    // The syntax below allows me to use multiple lines for longer texts.
    [;;;
    Weighed stoichiometrically to carbonized ampoule. Barium added last to avoid
    contact with ampoule during reaction]
    recovered_mass: 250.0

    seal
    1
    Evacuated ampoule and sealed with H2/O2 torch

    anneal
    2
    [;;;
    Opened under argon atmosphere and ground well before sealing in new ampoule
    in between annealings.]
    start_temp: 25
    start_temp_unit: degree_Celsius
    // Here, the double brackets signal that there are multiple program sections.
    program: [[
        type: ramp
        temp: 600
        time: 10
        temp_unit: degree_Celsius
        time_unit: hour

        type: dwell
        time: 120
        time_unit: hour
    ]]

    grind
    3
    dark gray powder now
    recovered_mass: 200.0

[Cifs]
file_name: Ba2Zn5Sb6_ICSD
extension: .cif
embedded: {{{

#(C) 2025 by FIZ Karlsruhe - Leibniz Institute for Information Infrastructure.  All rights reserved.
data_71031-ICSD
_database_code_ICSD 71031
_audit_creation_date 2023-08-01
_chemical_name_common 'Barium zinc antimonide (2/5/6)'
_chemical_formula_structural 'Ba2 Zn5 Sb6'
_chemical_formula_sum 'Ba2 Sb6 Zn5'
_exptl_crystal_density_diffrn 6.13
_diffrn_ambient_temperature 100.
_citation_title
;
New trick for an old dog: from prediction to properties of  hidden clathrates
\(Ba_2 Zn_5As_6\) and \(Ba_2 Zn_5Sb_6\)
;
loop_
_citation_id
_citation_journal_full
_citation_year
_citation_journal_volume
_citation_page_first
_citation_page_last
_citation_journal_id_ASTM
primary 'Journal of the American Chemical Society' 2023 145 4638 4646 JACSAT
loop_
_citation_author_citation_id
_citation_author_name
primary 'Yox, Philip'
primary 'Cerasoli, Frank'
primary 'Sarkar, Arka'
primary 'Kyveryga, Victoria'
primary 'Viswanathan, Gayatri'
primary 'Donadio, Davide'
primary 'Kovnir, Kirill'
_cell_length_a 11.4154(5)
_cell_length_b 10.0135(4)
_cell_length_c 12.6172(5)
_cell_angle_alpha 90
_cell_angle_beta 90
_cell_angle_gamma 90
_cell_volume 1442.24
_cell_formula_units_Z 4
_space_group_name_H-M_alt 'P m n a'
_space_group_IT_number 53
loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1 'x+1/2, y, -z+1/2'
2 'x+1/2, -y, z+1/2'
3 '-x, y, z'
4 '-x, -y, -z'
5 '-x+1/2, -y, z+1/2'
6 '-x+1/2, y, -z+1/2'
7 'x, -y, -z'
8 'x, y, z'
loop_
_atom_type_symbol
_atom_type_oxidation_number
Ba0+ 0
Sb0+ 0
Zn0+ 0
loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_symmetry_multiplicity
_atom_site_Wyckoff_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_U_iso_or_equiv
_atom_site_occupancy
Ba1 Ba0+ 4 h 0.5 0.23891(4) 0.64640(3) 0.00367(9) 1
Ba2 Ba0+ 4 g 0.75 0.71608(4) 0.75 0.00794(10) 1
Sb1 Sb0+ 4 f 0.32061(4) 0.5 0.5 0.00275(10) 1
Sb2 Sb0+ 4 h 0.5 0.86799(4) 0.61427(3) 0.00219(10) 1
Sb3 Sb0+ 4 h 0.5 0.73181(4) 0.93973(3) 0.00287(10) 1
Sb4 Sb0+ 8 i 0.19164(3) 0.10079(3) 0.65092(2) 0.00228(8) 1
Sb5 Sb0+ 4 h 0.5 0.50694(4) 0.80966(3) 0.00258(10) 1
Zn1 Zn0+ 4 h 0.5 0.94723(7) 0.81658(6) 0.00330(16) 1
Zn2 Zn0+ 4 e 0.33104(7) 0. 0.5 0.00356(16) 1
Zn3 Zn0+ 4 h 0.5 0.60202(7) 0.61084(6) 0.00339(16) 1
Zn4 Zn0+ 8 i 0.15880(5) 0.65041(5) 0.41232(4) 0.00452(13) 1
loop_
_atom_site_aniso_label
_atom_site_aniso_type_symbol
_atom_site_aniso_U_11
_atom_site_aniso_U_22
_atom_site_aniso_U_33
_atom_site_aniso_U_12
_atom_site_aniso_U_13
_atom_site_aniso_U_23
Ba1 Ba0+ 0.0056(2) 0.00269(19) 0.00270(18) 0. 0. -0.00066(15)
Ba2 Ba0+ 0.0031(2) 0.0110(2) 0.0097(2) 0. -0.00029(16) 0.
Sb1 Sb0+ 0.0025(2) 0.0026(2) 0.0031(2) 0. 0. 0.00002(17)
Sb2 Sb0+ 0.0037(2) 0.0013(2) 0.0015(2) 0. 0. -0.00028(17)
Sb3 Sb0+ 0.0053(2) 0.0017(2) 0.0016(2) 0. 0. -0.00002(17)
Sb4 Sb0+ 0.00259(16) 0.00227(16) 0.00198(14) 0.00013(12) 0.00028(12)
-0.00016(12)
Sb5 Sb0+ 0.0043(2) 0.0014(2) 0.0020(2) 0. 0. 0.00017(17)
Zn1 Zn0+ 0.0041(4) 0.0027(4) 0.0032(4) 0. 0. 0.0000(3)
Zn2 Zn0+ 0.0034(4) 0.0039(4) 0.0034(4) 0. 0. -0.0007(3)
Zn3 Zn0+ 0.0043(4) 0.0023(4) 0.0036(4) 0. 0. 0.0006(3)
Zn4 Zn0+ 0.0051(3) 0.0030(3) 0.0054(3) -0.0001(2) -0.0003(2) 0.0010(2)
#End of TTdata_71031-ICSD
#################### END FOS EMBED }}}


```

## Checkpoint 2

```fos
fos_id: TE001
fos_type: synthesis
description: My First Synthesis
group_id: kovnir-0000-0003-1152-1912
project_id: travis5672/clathrates/Ba2-TM5-Sb6

[Experimenters]
name: Travis Errthum
isu_research_group: Kovnir Group - Iowa State University
orcid: 0009-0006-1937-5672
rename: [
    affiliation: isu_research_group
]

[Reaction]
nominal_formula: Ba2Zn5Sb6
nominal_amount: 250.0
nominal_amount_unit: milligram

[Products]
name: Barium Zinc Antimonide (2-5-6)
formula: Ba2Zn5Sb6
expected: True
obtained: True
expected_amount: 250.0
expected_amount_unit: milligram
obtained_amount: 200.0
obtained_amount_unit: milligram
observations: Black Powder
characterizations: PXRD, EDS, Eyeballs
structure_comments: Unique clathrate with novel polyhedra. Space group Pnma

[[Reagents]]
:name
:type
:formula
:supplier
:cas
:form
:purity
:env
:amount
:amount_unit
:treatments

    Barium
    reagent
    Ba
    Thermofisher
    7440-39-3
    lump
    0.999
    Ar (g)
    2.0
    mol ratio
    [
        type: cutting
        repeats: 1
        observations: smaller pieces improve homogenization
    ]

    Zinc
    reagent
    Zn
    Sigma Aldrich
    7440-66-6
    powder
    0.995
    Ar (g)
    5.0
    mol ratio
    []

    Antimony
    reagent
    Sb
    Chem Stores?
    7440-36-0
    powder
    0.999
    Ar (g)
    6.0
    mol ratio
    []

[[Treatments]]
:type
:repeats
:observations

    weigh
    1
    [;;;
    Weighed stoichiometrically to carbonized ampoule. Barium added last to avoid
    contact with ampoule during reaction]
    recovered_mass: 250.0

    seal
    1
    Evacuated ampoule and sealed with H2/O2 torch

    anneal
    2
    [;;;
    Opened under argon atmosphere and ground well before sealing in new ampoule
    in between annealings.]
    start_temp: 25
    start_temp_unit: degree_Celsius
    program: [[
        type: ramp
        temp: 600
        time: 10
        temp_unit: degree_Celsius
        time_unit: hour

        type: dwell
        time: 120
        time_unit: hour
    ]]

    grind
    3
    dark gray powder now
    recovered_mass: 200.0

// This new block has been added because I renamed a required block.
[Rename]
// Synthesis files are required to have a materials block, so
// this line specifies that it has been renamed to reagents.
materials: reagents

[Cifs]
file_name: Ba2Zn5Sb6_ICSD
extension: .cif
embedded: {{{

#(C) 2025 by FIZ Karlsruhe - Leibniz Institute for Information Infrastructure.  All rights reserved.
data_71031-ICSD
_database_code_ICSD 71031
_audit_creation_date 2023-08-01
_chemical_name_common 'Barium zinc antimonide (2/5/6)'
_chemical_formula_structural 'Ba2 Zn5 Sb6'
_chemical_formula_sum 'Ba2 Sb6 Zn5'
_exptl_crystal_density_diffrn 6.13
_diffrn_ambient_temperature 100.
_citation_title
;
New trick for an old dog: from prediction to properties of  hidden clathrates
\(Ba_2 Zn_5As_6\) and \(Ba_2 Zn_5Sb_6\)
;
loop_
_citation_id
_citation_journal_full
_citation_year
_citation_journal_volume
_citation_page_first
_citation_page_last
_citation_journal_id_ASTM
primary 'Journal of the American Chemical Society' 2023 145 4638 4646 JACSAT
loop_
_citation_author_citation_id
_citation_author_name
primary 'Yox, Philip'
primary 'Cerasoli, Frank'
primary 'Sarkar, Arka'
primary 'Kyveryga, Victoria'
primary 'Viswanathan, Gayatri'
primary 'Donadio, Davide'
primary 'Kovnir, Kirill'
_cell_length_a 11.4154(5)
_cell_length_b 10.0135(4)
_cell_length_c 12.6172(5)
_cell_angle_alpha 90
_cell_angle_beta 90
_cell_angle_gamma 90
_cell_volume 1442.24
_cell_formula_units_Z 4
_space_group_name_H-M_alt 'P m n a'
_space_group_IT_number 53
loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1 'x+1/2, y, -z+1/2'
2 'x+1/2, -y, z+1/2'
3 '-x, y, z'
4 '-x, -y, -z'
5 '-x+1/2, -y, z+1/2'
6 '-x+1/2, y, -z+1/2'
7 'x, -y, -z'
8 'x, y, z'
loop_
_atom_type_symbol
_atom_type_oxidation_number
Ba0+ 0
Sb0+ 0
Zn0+ 0
loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_symmetry_multiplicity
_atom_site_Wyckoff_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_U_iso_or_equiv
_atom_site_occupancy
Ba1 Ba0+ 4 h 0.5 0.23891(4) 0.64640(3) 0.00367(9) 1
Ba2 Ba0+ 4 g 0.75 0.71608(4) 0.75 0.00794(10) 1
Sb1 Sb0+ 4 f 0.32061(4) 0.5 0.5 0.00275(10) 1
Sb2 Sb0+ 4 h 0.5 0.86799(4) 0.61427(3) 0.00219(10) 1
Sb3 Sb0+ 4 h 0.5 0.73181(4) 0.93973(3) 0.00287(10) 1
Sb4 Sb0+ 8 i 0.19164(3) 0.10079(3) 0.65092(2) 0.00228(8) 1
Sb5 Sb0+ 4 h 0.5 0.50694(4) 0.80966(3) 0.00258(10) 1
Zn1 Zn0+ 4 h 0.5 0.94723(7) 0.81658(6) 0.00330(16) 1
Zn2 Zn0+ 4 e 0.33104(7) 0. 0.5 0.00356(16) 1
Zn3 Zn0+ 4 h 0.5 0.60202(7) 0.61084(6) 0.00339(16) 1
Zn4 Zn0+ 8 i 0.15880(5) 0.65041(5) 0.41232(4) 0.00452(13) 1
loop_
_atom_site_aniso_label
_atom_site_aniso_type_symbol
_atom_site_aniso_U_11
_atom_site_aniso_U_22
_atom_site_aniso_U_33
_atom_site_aniso_U_12
_atom_site_aniso_U_13
_atom_site_aniso_U_23
Ba1 Ba0+ 0.0056(2) 0.00269(19) 0.00270(18) 0. 0. -0.00066(15)
Ba2 Ba0+ 0.0031(2) 0.0110(2) 0.0097(2) 0. -0.00029(16) 0.
Sb1 Sb0+ 0.0025(2) 0.0026(2) 0.0031(2) 0. 0. 0.00002(17)
Sb2 Sb0+ 0.0037(2) 0.0013(2) 0.0015(2) 0. 0. -0.00028(17)
Sb3 Sb0+ 0.0053(2) 0.0017(2) 0.0016(2) 0. 0. -0.00002(17)
Sb4 Sb0+ 0.00259(16) 0.00227(16) 0.00198(14) 0.00013(12) 0.00028(12)
-0.00016(12)
Sb5 Sb0+ 0.0043(2) 0.0014(2) 0.0020(2) 0. 0. 0.00017(17)
Zn1 Zn0+ 0.0041(4) 0.0027(4) 0.0032(4) 0. 0. 0.0000(3)
Zn2 Zn0+ 0.0034(4) 0.0039(4) 0.0034(4) 0. 0. -0.0007(3)
Zn3 Zn0+ 0.0043(4) 0.0023(4) 0.0036(4) 0. 0. 0.0006(3)
Zn4 Zn0+ 0.0051(3) 0.0030(3) 0.0054(3) -0.0001(2) -0.0003(2) 0.0010(2)
#End of TTdata_71031-ICSD
#################### END FOS EMBED }}}


```

## Checkpoint 3

```fos
fos_id: TE002
fos_type: synthesis
description: My Second Synthesis
group_id: kovnir-0000-0003-1152-1912
project_id: travis5672/clathrates/As28+d

[Experimenters]
name: Travis Errthum
isu_research_group: Kovnir Group - Iowa State University
orcid: 0009-0006-1937-5672
rename: [
    affiliation: isu_research_group
]

[Reaction]
nominal_formula: Ba8Cu13Zn11As28.5
nominal_amount: 250.0
nominal_amount_unit: milligram

[Products]
name: Barium transition-metal arsenide (8-24-28.5)
formula: Ba8Cu13Zn11As28.5
expected: True
obtained: True
expected_amount: 250.0
expected_amount_unit: milligram
obtained_amount: 150.0
obtained_amount_unit: milligram
observations: Gray Powder
characterizations: PXRD
structure_comments: [;;;
Unique clathrate with variable occupancy on hyper-coordinate Arsenic site. Space
group Cmcm]

[[Reagents]]
:name
:type
:formula
:supplier
:cas
:form
:purity
:env
:amount
:amount_unit
:treatments

    Barium
    reagent
    Ba
    Thermofisher
    7440-39-3
    lump
    0.999
    Ar (g)
    2.0
    mol ratio
    [
        type: cutting
        repeats: 1
        observations: smaller pieces improve homogenization
    ]

    Zinc
    reagent
    Zn
    Sigma Aldrich
    7440-66-6
    powder
    0.995
    Ar (g)
    5.0
    mol ratio
    []

    Antimony
    reagent
    Sb
    Chem Stores?
    7440-36-0
    powder
    0.999
    Ar (g)
    6.0
    mol ratio
    []

[[Treatments]]
:type
:repeats
:observations

    weigh
    1
    [;;;
    Weighed stoichiometrically to carbonized ampoule. Barium added last to avoid
    contact with ampoule during reaction]
    recovered_mass: 250.0

    seal
    1
    Evacuated ampoule and sealed with H2/O2 torch

    anneal
    2
    [;;;
    Opened under argon atmosphere and ground well before sealing in new ampoule
    in between annealings.]
    start_temp: 25
    start_temp_unit: degree_Celsius
    program: [[
        type: ramp
        temp: 600
        time: 10
        temp_unit: degree_Celsius
        time_unit: hour

        type: dwell
        time: 120
        time_unit: hour
    ]]

    grind
    3
    dark gray powder now
    recovered_mass: 200.0

// This new block has been added because I renamed a required block.
[Rename]
// Synthesis files are required to have a materials block, so
// this line specifies that it has been renamed to reagents.
materials: reagents

[Cifs]
file_name: Ba2Zn5Sb6_ICSD
extension: .cif
embedded: {{{

#(C) 2025 by FIZ Karlsruhe - Leibniz Institute for Information Infrastructure.  All rights reserved.
data_71031-ICSD
_database_code_ICSD 71031
_audit_creation_date 2023-08-01
_chemical_name_common 'Barium zinc antimonide (2/5/6)'
_chemical_formula_structural 'Ba2 Zn5 Sb6'
_chemical_formula_sum 'Ba2 Sb6 Zn5'
_exptl_crystal_density_diffrn 6.13
_diffrn_ambient_temperature 100.
_citation_title
;
New trick for an old dog: from prediction to properties of  hidden clathrates
\(Ba_2 Zn_5As_6\) and \(Ba_2 Zn_5Sb_6\)
;
loop_
_citation_id
_citation_journal_full
_citation_year
_citation_journal_volume
_citation_page_first
_citation_page_last
_citation_journal_id_ASTM
primary 'Journal of the American Chemical Society' 2023 145 4638 4646 JACSAT
loop_
_citation_author_citation_id
_citation_author_name
primary 'Yox, Philip'
primary 'Cerasoli, Frank'
primary 'Sarkar, Arka'
primary 'Kyveryga, Victoria'
primary 'Viswanathan, Gayatri'
primary 'Donadio, Davide'
primary 'Kovnir, Kirill'
_cell_length_a 11.4154(5)
_cell_length_b 10.0135(4)
_cell_length_c 12.6172(5)
_cell_angle_alpha 90
_cell_angle_beta 90
_cell_angle_gamma 90
_cell_volume 1442.24
_cell_formula_units_Z 4
_space_group_name_H-M_alt 'P m n a'
_space_group_IT_number 53
loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1 'x+1/2, y, -z+1/2'
2 'x+1/2, -y, z+1/2'
3 '-x, y, z'
4 '-x, -y, -z'
5 '-x+1/2, -y, z+1/2'
6 '-x+1/2, y, -z+1/2'
7 'x, -y, -z'
8 'x, y, z'
loop_
_atom_type_symbol
_atom_type_oxidation_number
Ba0+ 0
Sb0+ 0
Zn0+ 0
loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_symmetry_multiplicity
_atom_site_Wyckoff_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_U_iso_or_equiv
_atom_site_occupancy
Ba1 Ba0+ 4 h 0.5 0.23891(4) 0.64640(3) 0.00367(9) 1
Ba2 Ba0+ 4 g 0.75 0.71608(4) 0.75 0.00794(10) 1
Sb1 Sb0+ 4 f 0.32061(4) 0.5 0.5 0.00275(10) 1
Sb2 Sb0+ 4 h 0.5 0.86799(4) 0.61427(3) 0.00219(10) 1
Sb3 Sb0+ 4 h 0.5 0.73181(4) 0.93973(3) 0.00287(10) 1
Sb4 Sb0+ 8 i 0.19164(3) 0.10079(3) 0.65092(2) 0.00228(8) 1
Sb5 Sb0+ 4 h 0.5 0.50694(4) 0.80966(3) 0.00258(10) 1
Zn1 Zn0+ 4 h 0.5 0.94723(7) 0.81658(6) 0.00330(16) 1
Zn2 Zn0+ 4 e 0.33104(7) 0. 0.5 0.00356(16) 1
Zn3 Zn0+ 4 h 0.5 0.60202(7) 0.61084(6) 0.00339(16) 1
Zn4 Zn0+ 8 i 0.15880(5) 0.65041(5) 0.41232(4) 0.00452(13) 1
loop_
_atom_site_aniso_label
_atom_site_aniso_type_symbol
_atom_site_aniso_U_11
_atom_site_aniso_U_22
_atom_site_aniso_U_33
_atom_site_aniso_U_12
_atom_site_aniso_U_13
_atom_site_aniso_U_23
Ba1 Ba0+ 0.0056(2) 0.00269(19) 0.00270(18) 0. 0. -0.00066(15)
Ba2 Ba0+ 0.0031(2) 0.0110(2) 0.0097(2) 0. -0.00029(16) 0.
Sb1 Sb0+ 0.0025(2) 0.0026(2) 0.0031(2) 0. 0. 0.00002(17)
Sb2 Sb0+ 0.0037(2) 0.0013(2) 0.0015(2) 0. 0. -0.00028(17)
Sb3 Sb0+ 0.0053(2) 0.0017(2) 0.0016(2) 0. 0. -0.00002(17)
Sb4 Sb0+ 0.00259(16) 0.00227(16) 0.00198(14) 0.00013(12) 0.00028(12)
-0.00016(12)
Sb5 Sb0+ 0.0043(2) 0.0014(2) 0.0020(2) 0. 0. 0.00017(17)
Zn1 Zn0+ 0.0041(4) 0.0027(4) 0.0032(4) 0. 0. 0.0000(3)
Zn2 Zn0+ 0.0034(4) 0.0039(4) 0.0034(4) 0. 0. -0.0007(3)
Zn3 Zn0+ 0.0043(4) 0.0023(4) 0.0036(4) 0. 0. 0.0006(3)
Zn4 Zn0+ 0.0051(3) 0.0030(3) 0.0054(3) -0.0001(2) -0.0003(2) 0.0010(2)
#End of TTdata_71031-ICSD
#################### END FOS EMBED }}}


```

## Checkpoint 4

```fos
fos_id: TE002
fos_type: synthesis
description: My Second Synthesis
group_id: kovnir-0000-0003-1152-1912
project_id: travis5672/clathrates/As28+d

// Note that now there are two experimenters, so the
// experimenters header has changed to double brackets
[[Experimenters]]
name: Travis Errthum
isu_research_group: Kovnir Group - Iowa State University
orcid: 0009-0006-1937-5672
rename: [
    affiliation: isu_research_group
]

name: Joseph Race
affiliation: Kovnir Group - Iowa State University
orcid: 0000-0002-8551-3627

[Reaction]
nominal_formula: Ba8Cu13Zn11As28.5
nominal_amount: 250.0
nominal_amount_unit: milligram

[Products]
name: Barium transition-metal arsenide (8-24-28.5)
formula: Ba8Cu13Zn11As28.5
expected: True
obtained: True
expected_amount: 250.0
expected_amount_unit: milligram
obtained_amount: 150.0
obtained_amount_unit: milligram
observations: Gray Powder
characterizations: PXRD
structure_comments: [;;;
Unique clathrate with variable occupancy on hyper-coordinate Arsenic site. Space
group Cmcm]

[[Reagents]]
:name
:type
:formula
:supplier
:cas
:form
:purity
:env
:amount
:amount_unit
:treatments

    Barium
    reagent
    Ba
    Thermofisher
    7440-39-3
    lump
    0.999
    Ar (g)
    2.0
    mol ratio
    [
        type: cutting
        repeats: 1
        observations: smaller pieces improve homogenization
    ]

    Zinc
    reagent
    Zn
    Sigma Aldrich
    7440-66-6
    powder
    0.995
    Ar (g)
    5.0
    mol ratio
    []

    Antimony
    reagent
    Sb
    Chem Stores?
    7440-36-0
    powder
    0.999
    Ar (g)
    6.0
    mol ratio
    []

[[Treatments]]
:type
:repeats
:observations

    weigh
    1
    [;;;
    Weighed stoichiometrically to carbonized ampoule. Barium added last to avoid
    contact with ampoule during reaction]
    recovered_mass: 250.0

    seal
    1
    Evacuated ampoule and sealed with H2/O2 torch

    anneal
    2
    [;;;
    Opened under argon atmosphere and ground well before sealing in new ampoule
    in between annealings.]
    start_temp: 25
    start_temp_unit: degree_Celsius
    program: [[
        type: ramp
        temp: 600
        time: 10
        temp_unit: degree_Celsius
        time_unit: hour

        type: dwell
        time: 120
        time_unit: hour
    ]]

    grind
    3
    dark gray powder now
    recovered_mass: 200.0

[Rename]
materials: reagents

[Cifs]
file_name: Ba2Zn5Sb6_ICSD
extension: .cif
embedded: {{{

#(C) 2025 by FIZ Karlsruhe - Leibniz Institute for Information Infrastructure.  All rights reserved.
data_71031-ICSD
_database_code_ICSD 71031
_audit_creation_date 2023-08-01
_chemical_name_common 'Barium zinc antimonide (2/5/6)'
_chemical_formula_structural 'Ba2 Zn5 Sb6'
_chemical_formula_sum 'Ba2 Sb6 Zn5'
_exptl_crystal_density_diffrn 6.13
_diffrn_ambient_temperature 100.
_citation_title
;
New trick for an old dog: from prediction to properties of  hidden clathrates
\(Ba_2 Zn_5As_6\) and \(Ba_2 Zn_5Sb_6\)
;
loop_
_citation_id
_citation_journal_full
_citation_year
_citation_journal_volume
_citation_page_first
_citation_page_last
_citation_journal_id_ASTM
primary 'Journal of the American Chemical Society' 2023 145 4638 4646 JACSAT
loop_
_citation_author_citation_id
_citation_author_name
primary 'Yox, Philip'
primary 'Cerasoli, Frank'
primary 'Sarkar, Arka'
primary 'Kyveryga, Victoria'
primary 'Viswanathan, Gayatri'
primary 'Donadio, Davide'
primary 'Kovnir, Kirill'
_cell_length_a 11.4154(5)
_cell_length_b 10.0135(4)
_cell_length_c 12.6172(5)
_cell_angle_alpha 90
_cell_angle_beta 90
_cell_angle_gamma 90
_cell_volume 1442.24
_cell_formula_units_Z 4
_space_group_name_H-M_alt 'P m n a'
_space_group_IT_number 53
loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1 'x+1/2, y, -z+1/2'
2 'x+1/2, -y, z+1/2'
3 '-x, y, z'
4 '-x, -y, -z'
5 '-x+1/2, -y, z+1/2'
6 '-x+1/2, y, -z+1/2'
7 'x, -y, -z'
8 'x, y, z'
loop_
_atom_type_symbol
_atom_type_oxidation_number
Ba0+ 0
Sb0+ 0
Zn0+ 0
loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_symmetry_multiplicity
_atom_site_Wyckoff_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_U_iso_or_equiv
_atom_site_occupancy
Ba1 Ba0+ 4 h 0.5 0.23891(4) 0.64640(3) 0.00367(9) 1
Ba2 Ba0+ 4 g 0.75 0.71608(4) 0.75 0.00794(10) 1
Sb1 Sb0+ 4 f 0.32061(4) 0.5 0.5 0.00275(10) 1
Sb2 Sb0+ 4 h 0.5 0.86799(4) 0.61427(3) 0.00219(10) 1
Sb3 Sb0+ 4 h 0.5 0.73181(4) 0.93973(3) 0.00287(10) 1
Sb4 Sb0+ 8 i 0.19164(3) 0.10079(3) 0.65092(2) 0.00228(8) 1
Sb5 Sb0+ 4 h 0.5 0.50694(4) 0.80966(3) 0.00258(10) 1
Zn1 Zn0+ 4 h 0.5 0.94723(7) 0.81658(6) 0.00330(16) 1
Zn2 Zn0+ 4 e 0.33104(7) 0. 0.5 0.00356(16) 1
Zn3 Zn0+ 4 h 0.5 0.60202(7) 0.61084(6) 0.00339(16) 1
Zn4 Zn0+ 8 i 0.15880(5) 0.65041(5) 0.41232(4) 0.00452(13) 1
loop_
_atom_site_aniso_label
_atom_site_aniso_type_symbol
_atom_site_aniso_U_11
_atom_site_aniso_U_22
_atom_site_aniso_U_33
_atom_site_aniso_U_12
_atom_site_aniso_U_13
_atom_site_aniso_U_23
Ba1 Ba0+ 0.0056(2) 0.00269(19) 0.00270(18) 0. 0. -0.00066(15)
Ba2 Ba0+ 0.0031(2) 0.0110(2) 0.0097(2) 0. -0.00029(16) 0.
Sb1 Sb0+ 0.0025(2) 0.0026(2) 0.0031(2) 0. 0. 0.00002(17)
Sb2 Sb0+ 0.0037(2) 0.0013(2) 0.0015(2) 0. 0. -0.00028(17)
Sb3 Sb0+ 0.0053(2) 0.0017(2) 0.0016(2) 0. 0. -0.00002(17)
Sb4 Sb0+ 0.00259(16) 0.00227(16) 0.00198(14) 0.00013(12) 0.00028(12)
-0.00016(12)
Sb5 Sb0+ 0.0043(2) 0.0014(2) 0.0020(2) 0. 0. 0.00017(17)
Zn1 Zn0+ 0.0041(4) 0.0027(4) 0.0032(4) 0. 0. 0.0000(3)
Zn2 Zn0+ 0.0034(4) 0.0039(4) 0.0034(4) 0. 0. -0.0007(3)
Zn3 Zn0+ 0.0043(4) 0.0023(4) 0.0036(4) 0. 0. 0.0006(3)
Zn4 Zn0+ 0.0051(3) 0.0030(3) 0.0054(3) -0.0001(2) -0.0003(2) 0.0010(2)
#End of TTdata_71031-ICSD
#################### END FOS EMBED }}}


```

## Checkpoint 5

```fos
fos_id: TE002
fos_type: synthesis
description: My Second Synthesis
group_id: kovnir-0000-0003-1152-1912
project_id: travis5672/clathrates/As28+d

// Note that there are now multiple experimenters in this block,
// So the header now has double brackets
[[Experimenters]]
name: Travis Errthum
isu_research_group: Kovnir Group - Iowa State University
orcid: 0009-0006-1937-5672
rename: [
    affiliation: isu_research_group
]
// This copy of Joe has information about him as Travis's colleague
colleague$experimenter: [
    name: Joseph Race
    affiliation: Graham's Dad
    orcid: 0000-0002-8551-3627
]

// This copy of Joe has information about him as an experimenter
name: Joseph Race
affiliation: Kovnir Group - Iowa State University
orcid: 0000-0002-8551-3627

[Reaction]
nominal_formula: Ba8Cu13Zn11As28.5
nominal_amount: 250.0
nominal_amount_unit: milligram

[Products]
name: Barium transition-metal arsenide (8-24-28.5)
formula: Ba8Cu13Zn11As28.5
expected: True
obtained: True
expected_amount: 250.0
expected_amount_unit: milligram
obtained_amount: 150.0
obtained_amount_unit: milligram
observations: Gray Powder
characterizations: PXRD
structure_comments: [;;;
Unique clathrate with variable occupancy on hyper-coordinate Arsenic site. Space
group Cmcm]

[[Reagents]]
:name
:type
:formula
:supplier
:cas
:form
:purity
:env
:amount
:amount_unit
:treatments

    Barium
    reagent
    Ba
    Thermofisher
    7440-39-3
    lump
    0.999
    Ar (g)
    2.0
    mol ratio
    [
        type: cutting
        repeats: 1
        observations: smaller pieces improve homogenization
    ]

    Zinc
    reagent
    Zn
    Sigma Aldrich
    7440-66-6
    powder
    0.995
    Ar (g)
    5.0
    mol ratio
    []

    Antimony
    reagent
    Sb
    Chem Stores?
    7440-36-0
    powder
    0.999
    Ar (g)
    6.0
    mol ratio
    []

[[Treatments]]
:type
:repeats
:observations

    weigh
    1
    [;;;
    Weighed stoichiometrically to carbonized ampoule. Barium added last to avoid
    contact with ampoule during reaction]
    recovered_mass: 250.0

    seal
    1
    Evacuated ampoule and sealed with H2/O2 torch

    anneal
    2
    [;;;
    Opened under argon atmosphere and ground well before sealing in new ampoule
    in between annealings.]
    start_temp: 25
    start_temp_unit: degree_Celsius
    program: [[
        type: ramp
        temp: 600
        time: 10
        temp_unit: degree_Celsius
        time_unit: hour

        type: dwell
        time: 120
        time_unit: hour
    ]]

    grind
    3
    dark gray powder now
    recovered_mass: 200.0

[Rename]
materials: reagents

[Cifs]
file_name: Ba2Zn5Sb6_ICSD
extension: .cif
embedded: {{{

#(C) 2025 by FIZ Karlsruhe - Leibniz Institute for Information Infrastructure.  All rights reserved.
data_71031-ICSD
_database_code_ICSD 71031
_audit_creation_date 2023-08-01
_chemical_name_common 'Barium zinc antimonide (2/5/6)'
_chemical_formula_structural 'Ba2 Zn5 Sb6'
_chemical_formula_sum 'Ba2 Sb6 Zn5'
_exptl_crystal_density_diffrn 6.13
_diffrn_ambient_temperature 100.
_citation_title
;
New trick for an old dog: from prediction to properties of  hidden clathrates
\(Ba_2 Zn_5As_6\) and \(Ba_2 Zn_5Sb_6\)
;
loop_
_citation_id
_citation_journal_full
_citation_year
_citation_journal_volume
_citation_page_first
_citation_page_last
_citation_journal_id_ASTM
primary 'Journal of the American Chemical Society' 2023 145 4638 4646 JACSAT
loop_
_citation_author_citation_id
_citation_author_name
primary 'Yox, Philip'
primary 'Cerasoli, Frank'
primary 'Sarkar, Arka'
primary 'Kyveryga, Victoria'
primary 'Viswanathan, Gayatri'
primary 'Donadio, Davide'
primary 'Kovnir, Kirill'
_cell_length_a 11.4154(5)
_cell_length_b 10.0135(4)
_cell_length_c 12.6172(5)
_cell_angle_alpha 90
_cell_angle_beta 90
_cell_angle_gamma 90
_cell_volume 1442.24
_cell_formula_units_Z 4
_space_group_name_H-M_alt 'P m n a'
_space_group_IT_number 53
loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1 'x+1/2, y, -z+1/2'
2 'x+1/2, -y, z+1/2'
3 '-x, y, z'
4 '-x, -y, -z'
5 '-x+1/2, -y, z+1/2'
6 '-x+1/2, y, -z+1/2'
7 'x, -y, -z'
8 'x, y, z'
loop_
_atom_type_symbol
_atom_type_oxidation_number
Ba0+ 0
Sb0+ 0
Zn0+ 0
loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_symmetry_multiplicity
_atom_site_Wyckoff_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_U_iso_or_equiv
_atom_site_occupancy
Ba1 Ba0+ 4 h 0.5 0.23891(4) 0.64640(3) 0.00367(9) 1
Ba2 Ba0+ 4 g 0.75 0.71608(4) 0.75 0.00794(10) 1
Sb1 Sb0+ 4 f 0.32061(4) 0.5 0.5 0.00275(10) 1
Sb2 Sb0+ 4 h 0.5 0.86799(4) 0.61427(3) 0.00219(10) 1
Sb3 Sb0+ 4 h 0.5 0.73181(4) 0.93973(3) 0.00287(10) 1
Sb4 Sb0+ 8 i 0.19164(3) 0.10079(3) 0.65092(2) 0.00228(8) 1
Sb5 Sb0+ 4 h 0.5 0.50694(4) 0.80966(3) 0.00258(10) 1
Zn1 Zn0+ 4 h 0.5 0.94723(7) 0.81658(6) 0.00330(16) 1
Zn2 Zn0+ 4 e 0.33104(7) 0. 0.5 0.00356(16) 1
Zn3 Zn0+ 4 h 0.5 0.60202(7) 0.61084(6) 0.00339(16) 1
Zn4 Zn0+ 8 i 0.15880(5) 0.65041(5) 0.41232(4) 0.00452(13) 1
loop_
_atom_site_aniso_label
_atom_site_aniso_type_symbol
_atom_site_aniso_U_11
_atom_site_aniso_U_22
_atom_site_aniso_U_33
_atom_site_aniso_U_12
_atom_site_aniso_U_13
_atom_site_aniso_U_23
Ba1 Ba0+ 0.0056(2) 0.00269(19) 0.00270(18) 0. 0. -0.00066(15)
Ba2 Ba0+ 0.0031(2) 0.0110(2) 0.0097(2) 0. -0.00029(16) 0.
Sb1 Sb0+ 0.0025(2) 0.0026(2) 0.0031(2) 0. 0. 0.00002(17)
Sb2 Sb0+ 0.0037(2) 0.0013(2) 0.0015(2) 0. 0. -0.00028(17)
Sb3 Sb0+ 0.0053(2) 0.0017(2) 0.0016(2) 0. 0. -0.00002(17)
Sb4 Sb0+ 0.00259(16) 0.00227(16) 0.00198(14) 0.00013(12) 0.00028(12)
-0.00016(12)
Sb5 Sb0+ 0.0043(2) 0.0014(2) 0.0020(2) 0. 0. 0.00017(17)
Zn1 Zn0+ 0.0041(4) 0.0027(4) 0.0032(4) 0. 0. 0.0000(3)
Zn2 Zn0+ 0.0034(4) 0.0039(4) 0.0034(4) 0. 0. -0.0007(3)
Zn3 Zn0+ 0.0043(4) 0.0023(4) 0.0036(4) 0. 0. 0.0006(3)
Zn4 Zn0+ 0.0051(3) 0.0030(3) 0.0054(3) -0.0001(2) -0.0003(2) 0.0010(2)
#End of TTdata_71031-ICSD
#################### END FOS EMBED }}}


```

## Checkpoint 6

```fos
fos_id: TE002
fos_type: synthesis
description: My Second Synthesis
group_id: kovnir-0000-0003-1152-1912
project_id: travis5672/clathrates/As28+d

[[Experimenters]]
name: Travis Errthum
isu_research_group: Kovnir Group - Iowa State University
orcid: 0009-0006-1937-5672
rename: [
    affiliation: isu_research_group
]
colleague$experimenter: [
    name: Joseph Race
    affiliation: Graham's Dad
    orcid: 0000-0002-8551-3627
]

name: Joseph Race
affiliation: Kovnir Group - Iowa State University
orcid: 0000-0002-8551-3627

[Reaction]
nominal_formula: Ba8Cu13Zn11As28.5
nominal_amount: 250.0
nominal_amount_unit: milligram

[Products]
name: Barium transition-metal arsenide (8-24-28.5)
formula: Ba8Cu13Zn11As28.5
expected: True
obtained: True
expected_amount: 250.0
expected_amount_unit: milligram
obtained_amount: 150.0
obtained_amount_unit: milligram
observations: Gray Powder
characterizations: PXRD
structure_comments: [;;;
Unique clathrate with variable occupancy on hyper-coordinate Arsenic site. Space
group Cmcm]

[[Reagents]]
name: Barium
type: reagent
formula: Ba
supplier: Thermofisher
cas: 7440-39-3
form: lump
purity: 0.999
env: Ar (g)
amount: 8
amount_unit: mol ratio
treatments: [
    type: cutting
    repeats: 1
    observations: smaller pieces improve homogenization
]

name: Zinc
type: reagent
formula: Zn
supplier: Sigma Aldrich
cas: 7440-66-6
form: powder
purity: 0.995
env: Ar (g)
amount: 11
amount_unit: mol ratio
treatments: []

name: Copper
type: reagent
formula: Cu
supplier: Sigma Aldrich
cas: 7440-50-8
form: powder
env: Ar (g)
amount: 13
amount_unit: mol ratio
purity: 0.995
treatments: []

name: Arsenic
type: reagent
formula: As
supplier: Furukama
cas: 7440-38-2
form: lump
env: Ar (g)
amount: 28.5
amount_unit: mol ratio
purity: 0.9995
treatments: [
    type: Grinding
    repeats: 1
    observations: ground lumps into powder for weighing and homogenization
]

[[Treatments]]
:type
:repeats
:observations

    weigh
    1
    [;;;
    Weighed stoichiometrically to carbonized ampoule. Barium added last to avoid
    contact with ampoule during reaction]
    recovered_mass: 250.0

    seal
    1
    Evacuated ampoule and sealed with H2/O2 torch

    anneal
    2
    [;;;
    Opened under argon atmosphere and ground well before sealing in new ampoule
    in between annealings.]
    start_temp: 25
    start_temp_unit: degree_Celsius
    program: [[
        type: ramp
        temp: 600
        time: 10
        temp_unit: degree_Celsius
        time_unit: hour

        type: dwell
        time: 120
        time_unit: hour
    ]]

    grind
    3
    dark gray powder now
    recovered_mass: 200.0

[Rename]
materials: reagents

[Cifs]
file_name: Ba2Zn5Sb6_ICSD
extension: .cif
embedded: {{{

#(C) 2025 by FIZ Karlsruhe - Leibniz Institute for Information Infrastructure.  All rights reserved.
data_71031-ICSD
_database_code_ICSD 71031
_audit_creation_date 2023-08-01
_chemical_name_common 'Barium zinc antimonide (2/5/6)'
_chemical_formula_structural 'Ba2 Zn5 Sb6'
_chemical_formula_sum 'Ba2 Sb6 Zn5'
_exptl_crystal_density_diffrn 6.13
_diffrn_ambient_temperature 100.
_citation_title
;
New trick for an old dog: from prediction to properties of  hidden clathrates
\(Ba_2 Zn_5As_6\) and \(Ba_2 Zn_5Sb_6\)
;
loop_
_citation_id
_citation_journal_full
_citation_year
_citation_journal_volume
_citation_page_first
_citation_page_last
_citation_journal_id_ASTM
primary 'Journal of the American Chemical Society' 2023 145 4638 4646 JACSAT
loop_
_citation_author_citation_id
_citation_author_name
primary 'Yox, Philip'
primary 'Cerasoli, Frank'
primary 'Sarkar, Arka'
primary 'Kyveryga, Victoria'
primary 'Viswanathan, Gayatri'
primary 'Donadio, Davide'
primary 'Kovnir, Kirill'
_cell_length_a 11.4154(5)
_cell_length_b 10.0135(4)
_cell_length_c 12.6172(5)
_cell_angle_alpha 90
_cell_angle_beta 90
_cell_angle_gamma 90
_cell_volume 1442.24
_cell_formula_units_Z 4
_space_group_name_H-M_alt 'P m n a'
_space_group_IT_number 53
loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1 'x+1/2, y, -z+1/2'
2 'x+1/2, -y, z+1/2'
3 '-x, y, z'
4 '-x, -y, -z'
5 '-x+1/2, -y, z+1/2'
6 '-x+1/2, y, -z+1/2'
7 'x, -y, -z'
8 'x, y, z'
loop_
_atom_type_symbol
_atom_type_oxidation_number
Ba0+ 0
Sb0+ 0
Zn0+ 0
loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_symmetry_multiplicity
_atom_site_Wyckoff_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_U_iso_or_equiv
_atom_site_occupancy
Ba1 Ba0+ 4 h 0.5 0.23891(4) 0.64640(3) 0.00367(9) 1
Ba2 Ba0+ 4 g 0.75 0.71608(4) 0.75 0.00794(10) 1
Sb1 Sb0+ 4 f 0.32061(4) 0.5 0.5 0.00275(10) 1
Sb2 Sb0+ 4 h 0.5 0.86799(4) 0.61427(3) 0.00219(10) 1
Sb3 Sb0+ 4 h 0.5 0.73181(4) 0.93973(3) 0.00287(10) 1
Sb4 Sb0+ 8 i 0.19164(3) 0.10079(3) 0.65092(2) 0.00228(8) 1
Sb5 Sb0+ 4 h 0.5 0.50694(4) 0.80966(3) 0.00258(10) 1
Zn1 Zn0+ 4 h 0.5 0.94723(7) 0.81658(6) 0.00330(16) 1
Zn2 Zn0+ 4 e 0.33104(7) 0. 0.5 0.00356(16) 1
Zn3 Zn0+ 4 h 0.5 0.60202(7) 0.61084(6) 0.00339(16) 1
Zn4 Zn0+ 8 i 0.15880(5) 0.65041(5) 0.41232(4) 0.00452(13) 1
loop_
_atom_site_aniso_label
_atom_site_aniso_type_symbol
_atom_site_aniso_U_11
_atom_site_aniso_U_22
_atom_site_aniso_U_33
_atom_site_aniso_U_12
_atom_site_aniso_U_13
_atom_site_aniso_U_23
Ba1 Ba0+ 0.0056(2) 0.00269(19) 0.00270(18) 0. 0. -0.00066(15)
Ba2 Ba0+ 0.0031(2) 0.0110(2) 0.0097(2) 0. -0.00029(16) 0.
Sb1 Sb0+ 0.0025(2) 0.0026(2) 0.0031(2) 0. 0. 0.00002(17)
Sb2 Sb0+ 0.0037(2) 0.0013(2) 0.0015(2) 0. 0. -0.00028(17)
Sb3 Sb0+ 0.0053(2) 0.0017(2) 0.0016(2) 0. 0. -0.00002(17)
Sb4 Sb0+ 0.00259(16) 0.00227(16) 0.00198(14) 0.00013(12) 0.00028(12)
-0.00016(12)
Sb5 Sb0+ 0.0043(2) 0.0014(2) 0.0020(2) 0. 0. 0.00017(17)
Zn1 Zn0+ 0.0041(4) 0.0027(4) 0.0032(4) 0. 0. 0.0000(3)
Zn2 Zn0+ 0.0034(4) 0.0039(4) 0.0034(4) 0. 0. -0.0007(3)
Zn3 Zn0+ 0.0043(4) 0.0023(4) 0.0036(4) 0. 0. 0.0006(3)
Zn4 Zn0+ 0.0051(3) 0.0030(3) 0.0054(3) -0.0001(2) -0.0003(2) 0.0010(2)
#End of TTdata_71031-ICSD
#################### END FOS EMBED }}}


```

## Checkpoint 8

```fos
fos_id: TE002
fos_type: synthesis
description: My Second Synthesis
group_id: kovnir-0000-0003-1152-1912
project_id: travis5672/clathrates/As28+d

[[Experimenters]]
name: Travis Errthum
isu_research_group: Kovnir Group - Iowa State University
orcid: 0009-0006-1937-5672
rename: [
    affiliation: isu_research_group
]
colleague$experimenter: [
    name: Joseph Race
    affiliation: Graham's Dad
    orcid: 0000-0002-8551-3627
]

name: Joseph Race
affiliation: Kovnir Group - Iowa State University
orcid: 0000-0002-8551-3627

[Reaction]
nominal_formula: Ba8Cu13Zn11As28.5
nominal_amount: 250.0
nominal_amount_unit: milligram

[Products]
name: Barium transition-metal arsenide (8-24-28.5)
formula: Ba8Cu13Zn11As28.5
expected: True
obtained: True
expected_amount: 250.0
expected_amount_unit: milligram
obtained_amount: 150.0
obtained_amount_unit: milligram
observations: Gray Powder
characterizations: PXRD
structure_comments: [;;;
Unique clathrate with variable occupancy on hyper-coordinate Arsenic site. Space
group Cmcm]

[[Reagents]]
name: Barium
type: reagent
formula: Ba
supplier: Thermofisher
cas: 7440-39-3
form: lump
purity: 0.999
env: Ar (g)
amount: 8
amount_unit: mol ratio
treatments: [
    type: cutting
    repeats: 1
    observations: smaller pieces improve homogenization
]

name: Zinc
type: reagent
formula: Zn
supplier: Sigma Aldrich
cas: 7440-66-6
form: powder
purity: 0.995
env: Ar (g)
amount: 11
amount_unit: mol ratio
treatments: []

name: Copper
type: reagent
formula: Cu
supplier: Sigma Aldrich
cas: 7440-50-8
form: powder
env: Ar (g)
amount: 13
amount_unit: mol ratio
purity: 0.995
treatments: []

name: Arsenic
type: reagent
formula: As
supplier: Furukama
cas: 7440-38-2
form: lump
env: Ar (g)
amount: 28.5
amount_unit: mol ratio
purity: 0.9995
treatments: [
    type: Grinding
    repeats: 1
    observations: ground lumps into powder for weighing and homogenization
]

[[Treatments]]
:type
:repeats
:observations

    weigh
    1
    [;;;
    Weighed stoichiometrically to carbonized ampoule. Barium added last to avoid
    contact with ampoule during reaction]
    recovered_mass: 250.0

    seal
    1
    Evacuated ampoule and sealed with H2/O2 torch

    anneal
    1
    None
    program: [[
        type: ramp
        temp: 550
        time: 2
        temp_unit: degree_Celsius
        time_unit: hour

        type: dwell
        time: 12
        time_unit: hour

        type: quench
        medium: water
    ]]
    start_temp: 25
    start_temp_unit: degree_Celsius

    anneal
    1
    None
    program: [[
        type: ramp
        temp: 650
        time: 10
        temp_unit: degree_Celsius
        time_unit: hour

        type: dwell
        time: 72
        time_unit: hour
    ]]
    start_temp: 25
    start_temp_unit: degree_Celsius

[Rename]
materials: reagents

[Cifs]
file_name: Ba2Zn5Sb6_ICSD
extension: .cif
embedded: {{{

#(C) 2025 by FIZ Karlsruhe - Leibniz Institute for Information Infrastructure.  All rights reserved.
data_71031-ICSD
_database_code_ICSD 71031
_audit_creation_date 2023-08-01
_chemical_name_common 'Barium zinc antimonide (2/5/6)'
_chemical_formula_structural 'Ba2 Zn5 Sb6'
_chemical_formula_sum 'Ba2 Sb6 Zn5'
_exptl_crystal_density_diffrn 6.13
_diffrn_ambient_temperature 100.
_citation_title
;
New trick for an old dog: from prediction to properties of  hidden clathrates
\(Ba_2 Zn_5As_6\) and \(Ba_2 Zn_5Sb_6\)
;
loop_
_citation_id
_citation_journal_full
_citation_year
_citation_journal_volume
_citation_page_first
_citation_page_last
_citation_journal_id_ASTM
primary 'Journal of the American Chemical Society' 2023 145 4638 4646 JACSAT
loop_
_citation_author_citation_id
_citation_author_name
primary 'Yox, Philip'
primary 'Cerasoli, Frank'
primary 'Sarkar, Arka'
primary 'Kyveryga, Victoria'
primary 'Viswanathan, Gayatri'
primary 'Donadio, Davide'
primary 'Kovnir, Kirill'
_cell_length_a 11.4154(5)
_cell_length_b 10.0135(4)
_cell_length_c 12.6172(5)
_cell_angle_alpha 90
_cell_angle_beta 90
_cell_angle_gamma 90
_cell_volume 1442.24
_cell_formula_units_Z 4
_space_group_name_H-M_alt 'P m n a'
_space_group_IT_number 53
loop_
_space_group_symop_id
_space_group_symop_operation_xyz
1 'x+1/2, y, -z+1/2'
2 'x+1/2, -y, z+1/2'
3 '-x, y, z'
4 '-x, -y, -z'
5 '-x+1/2, -y, z+1/2'
6 '-x+1/2, y, -z+1/2'
7 'x, -y, -z'
8 'x, y, z'
loop_
_atom_type_symbol
_atom_type_oxidation_number
Ba0+ 0
Sb0+ 0
Zn0+ 0
loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_symmetry_multiplicity
_atom_site_Wyckoff_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_U_iso_or_equiv
_atom_site_occupancy
Ba1 Ba0+ 4 h 0.5 0.23891(4) 0.64640(3) 0.00367(9) 1
Ba2 Ba0+ 4 g 0.75 0.71608(4) 0.75 0.00794(10) 1
Sb1 Sb0+ 4 f 0.32061(4) 0.5 0.5 0.00275(10) 1
Sb2 Sb0+ 4 h 0.5 0.86799(4) 0.61427(3) 0.00219(10) 1
Sb3 Sb0+ 4 h 0.5 0.73181(4) 0.93973(3) 0.00287(10) 1
Sb4 Sb0+ 8 i 0.19164(3) 0.10079(3) 0.65092(2) 0.00228(8) 1
Sb5 Sb0+ 4 h 0.5 0.50694(4) 0.80966(3) 0.00258(10) 1
Zn1 Zn0+ 4 h 0.5 0.94723(7) 0.81658(6) 0.00330(16) 1
Zn2 Zn0+ 4 e 0.33104(7) 0. 0.5 0.00356(16) 1
Zn3 Zn0+ 4 h 0.5 0.60202(7) 0.61084(6) 0.00339(16) 1
Zn4 Zn0+ 8 i 0.15880(5) 0.65041(5) 0.41232(4) 0.00452(13) 1
loop_
_atom_site_aniso_label
_atom_site_aniso_type_symbol
_atom_site_aniso_U_11
_atom_site_aniso_U_22
_atom_site_aniso_U_33
_atom_site_aniso_U_12
_atom_site_aniso_U_13
_atom_site_aniso_U_23
Ba1 Ba0+ 0.0056(2) 0.00269(19) 0.00270(18) 0. 0. -0.00066(15)
Ba2 Ba0+ 0.0031(2) 0.0110(2) 0.0097(2) 0. -0.00029(16) 0.
Sb1 Sb0+ 0.0025(2) 0.0026(2) 0.0031(2) 0. 0. 0.00002(17)
Sb2 Sb0+ 0.0037(2) 0.0013(2) 0.0015(2) 0. 0. -0.00028(17)
Sb3 Sb0+ 0.0053(2) 0.0017(2) 0.0016(2) 0. 0. -0.00002(17)
Sb4 Sb0+ 0.00259(16) 0.00227(16) 0.00198(14) 0.00013(12) 0.00028(12)
-0.00016(12)
Sb5 Sb0+ 0.0043(2) 0.0014(2) 0.0020(2) 0. 0. 0.00017(17)
Zn1 Zn0+ 0.0041(4) 0.0027(4) 0.0032(4) 0. 0. 0.0000(3)
Zn2 Zn0+ 0.0034(4) 0.0039(4) 0.0034(4) 0. 0. -0.0007(3)
Zn3 Zn0+ 0.0043(4) 0.0023(4) 0.0036(4) 0. 0. 0.0006(3)
Zn4 Zn0+ 0.0051(3) 0.0030(3) 0.0054(3) -0.0001(2) -0.0003(2) 0.0010(2)
#End of TTdata_71031-ICSD
#################### END FOS EMBED }}}


```

## Checkpoint 9

```fos
fos_id: TE002
fos_type: synthesis
description: My Second Synthesis
group_id: kovnir-0000-0003-1152-1912
project_id: travis5672/clathrates/As28+d

[[Experimenters]]
name: Travis Errthum
isu_research_group: Kovnir Group - Iowa State University
orcid: 0009-0006-1937-5672
rename: [
    affiliation: isu_research_group
]
colleague$experimenter: [
    name: Joseph Race
    affiliation: Graham's Dad
    orcid: 0000-0002-8551-3627
]

name: Joseph Race
affiliation: Kovnir Group - Iowa State University
orcid: 0000-0002-8551-3627

[Reaction]
nominal_formula: Ba8Cu13Zn11As28.5
nominal_amount: 250.0
nominal_amount_unit: milligram

[Products]
name: Barium transition-metal arsenide (8-24-28.5)
formula: Ba8Cu13Zn11As28.5
expected: True
obtained: True
expected_amount: 250.0
expected_amount_unit: milligram
obtained_amount: 150.0
obtained_amount_unit: milligram
observations: Gray Powder
characterizations: PXRD
structure_comments: [;;;
Unique clathrate with variable occupancy on hyper-coordinate Arsenic site. Space
group Cmcm]

[[Reagents]]
name: Barium
type: reagent
formula: Ba
supplier: Thermofisher
cas: 7440-39-3
form: lump
purity: 0.999
env: Ar (g)
amount: 8
amount_unit: mol ratio
treatments: [
    type: cutting
    repeats: 1
    observations: smaller pieces improve homogenization
]

name: Zinc
type: reagent
formula: Zn
supplier: Sigma Aldrich
cas: 7440-66-6
form: powder
purity: 0.995
env: Ar (g)
amount: 11
amount_unit: mol ratio
treatments: []

name: Copper
type: reagent
formula: Cu
supplier: Sigma Aldrich
cas: 7440-50-8
form: powder
env: Ar (g)
amount: 13
amount_unit: mol ratio
purity: 0.995
treatments: []

name: Arsenic
type: reagent
formula: As
supplier: Furukama
cas: 7440-38-2
form: lump
env: Ar (g)
amount: 28.5
amount_unit: mol ratio
purity: 0.9995
treatments: [
    type: Grinding
    repeats: 1
    observations: ground lumps into powder for weighing and homogenization
]

[[Treatments]]
:type
:repeats
:observations

    weigh
    1
    [;;;
    Weighed stoichiometrically to carbonized ampoule. Barium added last to avoid
    contact with ampoule during reaction]
    recovered_mass: 250.0

    seal
    1
    Evacuated ampoule and sealed with H2/O2 torch

    anneal
    1
    None
    program: [[
        type: ramp
        temp: 550
        time: 2
        temp_unit: degree_Celsius
        time_unit: hour

        type: dwell
        time: 12
        time_unit: hour

        type: quench
        medium: water
    ]]
    start_temp: 25
    start_temp_unit: degree_Celsius

    anneal
    1
    None
    program: [[
        type: ramp
        temp: 650
        time: 10
        temp_unit: degree_Celsius
        time_unit: hour

        type: dwell
        time: 72
        time_unit: hour
    ]]
    start_temp: 25
    start_temp_unit: degree_Celsius

[Rename]
materials: reagents

[Cifs]
file_name: PY618_Ba8-Cu12-Zn12-As29,8
extension: .cif
path: ..\templates


```

## Checkpoint 10

```fos
fos_id: TE002
fos_type: synthesis
description: My Second Synthesis
group_id: kovnir-0000-0003-1152-1912
project_id: travis5672/clathrates/As28+d

[Rename]
materials: reagents

[[Experimenters]]
name: Travis Errthum
isu_research_group: Kovnir Group - Iowa State University
orcid: 0009-0006-1937-5672
rename: [
    affiliation: isu_research_group
]
colleague$experimenter: [
    name: Joseph Race
    affiliation: Graham's Dad
    orcid: 0000-0002-8551-3627
]

name: Joseph Race
affiliation: Kovnir Group - Iowa State University
orcid: 0000-0002-8551-3627

[Reaction]
nominal_formula: Ba8Cu13Zn11As28.5
nominal_amount: 250.0
nominal_amount_unit: milligram

[Products]
name: Barium transition-metal arsenide (8-24-28.5)
formula: Ba8Cu13Zn11As28.5
expected: True
obtained: True
expected_amount: 250.0
expected_amount_unit: milligram
obtained_amount: 150.0
obtained_amount_unit: milligram
observations: Gray Powder
characterizations: PXRD
structure_comments: [;;;
Unique clathrate with variable occupancy on hyper-coordinate Arsenic site. Space
group Cmcm]

[[Reagents]]
:name
:type
:formula
:supplier
:cas
:form
:purity
:env
:amount
:amount_unit
:treatments

    Barium
    reagent
    Ba
    Thermofisher
    7440-39-3
    lump
    0.999
    Ar (g)
    // Weight percents were calculated automatically when saving.
    // ! Total weight percent: 22.99%
    8
    mol ratio
    [
        type: cutting
        repeats: 1
        observations: smaller pieces improve homogenization
    ]

    Zinc
    reagent
    Zn
    Sigma Aldrich
    7440-66-6
    powder
    0.995
    Ar (g)
    // ! Total weight percent: 15.05%
    11
    mol ratio
    []

    Copper
    reagent
    Cu
    Sigma Aldrich
    7440-50-8
    powder
    0.995
    Ar (g)
    // ! Total weight percent: 17.29%
    13
    mol ratio
    []

    Arsenic
    reagent
    As
    Furukama
    7440-38-2
    lump
    0.9995
    Ar (g)
    // ! Total weight percent: 44.68%
    28.5
    mol ratio
    [
        type: Grinding
        repeats: 1
        observations: ground lumps into powder for weighing and homogenization
    ]

[[Treatments]]
:type
:repeats
:observations

    weigh
    1
    [;;;
    Weighed stoichiometrically to carbonized ampoule. Barium added last to avoid
    contact with ampoule during reaction]
    recovered_mass: 250.0

    seal
    1
    Evacuated ampoule and sealed with H2/O2 torch

    anneal
    1
    None
    program: [[
        type: ramp
        // ! Rate for ramp: 262.5 delta_degree_Celsius / hour
        temp: 550
        time: 2
        temp_unit: degree_Celsius
        time_unit: hour

        type: dwell
        time: 12
        time_unit: hour

        type: quench
        medium: water
    ]]
    start_temp: 25
    start_temp_unit: degree_Celsius

    anneal
    1
    None
    program: [[
        type: ramp
        // ! Rate for ramp: 62.5 delta_degree_Celsius / hour
        temp: 650
        time: 10
        temp_unit: degree_Celsius
        time_unit: hour

        type: dwell
        time: 72
        time_unit: hour
    ]]
    start_temp: 25
    start_temp_unit: degree_Celsius

[Cifs]
file_name: PY618_Ba8-Cu12-Zn12-As29,8
extension: .cif
path: .


```

