# Created by the starfile Python package (version 0.5.13) at 17:14:12 on 05/06/2026


data_metadata

_name			TE001
_date			03-11-2026
_internal_project_ID			Ba2-TM5-Pn6
_internal_project_description			"Unique Clathrate"


data_experimenters_0

_name			"Travis Errthum"
_affiliation			"Kovnir Group - Iowa State University"
_orcid			0009-0006-1937-5672


data_reaction

_nominal_formula			Ba2Zn5Sb6
_nominal_amount			250.0
_nominal_amount_unit			milligram


data_products_0

_name			"Barium Zinc Antimonide (2-5-6)"
_formula			Ba2Zn5Sb6
_expected			True
_obtained			True
_expected_amount			250.0
_expected_amount_unit			milligram
_obtained_amount			200.0
_obtained_amount_unit			milligram
_observations			"Black Powder"
_characterizations			"PXRD, EDS, Eyeballs"
_structure_comments			"Unique clathrate with novel polyhedra. Space group Pnma"


data_materials_0

_name			Barium
_type			reagent
_formula			Ba
_supplier			Thermofisher
_cas			7440-39-3
_form			lump
_purity			0.999
_env			"Ar (g)"
_amount			2.0
_amount_unit			"mol ratio"
_treatments_0			{'type': 'cutting', 'repeats': '1', 'observations': 'smaller pieces improve homogenization'}


data_materials_1

_name			Zinc
_type			reagent
_formula			Zn
_supplier			"Sigma Aldrich"
_cas			7440-66-6
_form			powder
_purity			0.995
_env			"Ar (g)"
_amount			5.0
_amount_unit			"mol ratio"


data_materials_2

_name			Antimony
_type			reagent
_formula			Sb
_supplier			"Chem Stores?"
_cas			7440-36-0
_form			powder
_purity			0.999
_env			"Ar (g)"
_amount			6.0
_amount_unit			"mol ratio"


data_treatments_0

_type			weigh
_repeats			1
_observations			"Weighed stoichiometrically to carbonized ampoule. Barium added last to avoid contact with ampoule during reaction"
_recovered_mass			250.0


data_treatments_1

_type			seal
_repeats			1
_observations			"Evacuated ampoule and sealed with H2/O2 torch"


data_treatments_2

_type			anneal
_repeats			2
_observations			"Opened under argon atmosphere and ground well before sealing in new ampoule in between annealings."
_start_temp			25
_start_temp_unit			degree_Celsius
_program_0			{'type': 'ramp', 'temp': '600', 'time': '10', 'temp_unit': 'degree_Celsius', 'time_unit': 'hour'}
_program_1			{'type': 'dwell', 'time': '120', 'time_unit': 'hour'}


data_treatments_3

_type			grind
_repeats			3
_observations			"dark gray powder now"
_recovered_mass			200.0


data_cifs_0

_file_name			Ba2Zn5Sb6_ICSD
_extension			.cif
_embedded			                                                     0
0                                                   \n
1    #(C) 2025 by FIZ Karlsruhe - Leibniz Institute...
2                                    data_71031-ICSD\n
3                          _database_code_ICSD 71031\n
4                    _audit_creation_date 2023-08-01\n
..                                                 ...
99   Zn1 Zn0+ 0.0041(4) 0.0027(4) 0.0032(4) 0. 0. 0...
100  Zn2 Zn0+ 0.0034(4) 0.0039(4) 0.0034(4) 0. 0. -...
101  Zn3 Zn0+ 0.0043(4) 0.0023(4) 0.0036(4) 0. 0. 0...
102  Zn4 Zn0+ 0.0051(3) 0.0030(3) 0.0054(3) -0.0001...
103                        #End of TTdata_71031-ICSD\n

[104 rows x 1 columns]


