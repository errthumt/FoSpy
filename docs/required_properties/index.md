# Expected Properties for Classes in a File of Synthesis
During construction of a parsed FOS into a Synthesis object, or when reassigning a property of an exising object, most classes have properties that should be expected in a certain format, or might contain nested objects with their own properties. The parsed properties are passed as either strings or (in the case of nested objects) a `list` or `dict` structure to the validation routine mapped to them in `FoSpy.parsing.validation.py`. In the case of nested objects, the validation routine is usually the constructor of the required object. 

Classes can have required properties, which must be present at read time, or optional properties, which have validation routines but might not be expected for all syntheses.

During attribute assignment, expected properties are built up in order of parent classes. Any subclass inherits all the expected properties of its parent classes, but they may be overwritten to other validators.

## Dispatching Subclasses
Properties marked with (dispatched) are used to identify and delegate construction to the respective subclass. A class with a dispatch key is rarely constructed as itself, but may be used to inherit methods or required/optional properties.

## `ListBlock` and Simple Lists
`ListBlock` subclasses do not have required properties. Instead, they are a rich list of objects with a certain required `SingleBlock` subclass. Some `ListBlock` subclasses have their own methods and unique attributes. If a `ListBlock` is required for a given `SingleBlock` subclass but it doesn't need any method or attribute overrides, it can be instantiated with the class method `ListBlock.Simple(SingleBlockSubclass)`.

## `AnnealSection`
**[Subclass of `SingleBlock`](#singleblock)**

### Required properties
| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| type | str (dispatched) | Examples: `"dwell", "ramp", "quench" |

---

## `Annealing`
**[Subclass of `Treatment`](#treatment)**

### Required properties
| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| program | `AnnealProgram` | A list of [`AnnealSection` objects](#annealsection) |
| start_temp | validators.numbers.positive_decimal | The initial temperature of the annealing profile |
| start_temp_unit | validators.units.FOSTempUnit | FOSTempUnit is a [subclass of `pint`'s `Unit`](https://pint.readthedocs.io/en/stable/) which allows a little more coersion of temperature units. (Like recognizing `"C"` as degrees celsius as opposed to coulombs)|

### Optional properties
| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| gas_flow | FlowList | A [simple list](#listblock-and-simple-lists) of [`GasFlow` objects](#gasflow) |

---

## `Dwell`
**[Subclass of `AnnealSection`](#annealsection)**

### Required properties
| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| time | validators.numbers.positive_decimal("Dwell/time", "time", True) | |
| time_unit | validators.units.FOSUnit.enforce_dims("[time]") | |

---

## `EmbeddedFile`
**[Subclass of ``](#)**

### Required properties
| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| file_name | validators.filenames.file_name | |
| extension | validators.filenames.file_extension | |
| embedded | list | |

---

## `Experimenter`
**[Subclass of ``](#)**

### Required properties
| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| name | str | |
| affiliation | str | |

### Optional properties
| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| orcid | str | |

---

## `GasFlow`
This section is still in progress

## `Material`
**[Subclass of ``](#)**

### Required properties
| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| name | str | |
| type | str | |
| formula | ChemFormula | |
| supplier | str | |
| cas | str | |
| form | str | |
| env | str | |
| amount | validators.numbers.positive_decimal("Material/amount", "amount") | |
| amount_unit | str | |

### Optional properties
| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| purity | validators.numbers.decimal_range("Material/purity","purity", 0, 1) | |
| treatments | ListBlock.Simple(Treatment) | |

---

## `MetaData`
**[Subclass of ``](#)**

### Required properties
| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| name | str | |
| date | str | |

---

## `Product`
**[Subclass of ``](#)**

### Required properties
| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| name | str | |
| expected | bool | |
| obtained | bool | |
| formula | ChemFormula | |
| observations | str | |

### Optional properties
| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| expected_amount | validators.numbers.positive_decimal("Product/expected_amount", "expected_amount", require_unit=True) | |
| expected_amount_unit | validators.units.FOSUnit.enforce_dims(["[mass]",{"[length]":3}]) | |
| obtained_amount | validators.numbers.positive_decimal("Product/obtained_amount", "obtained_amount", require_unit=True) | |
| obtained_amount_unit | validators.units.FOSUnit.enforce_dims(["[mass]",{"[length]":3}]) | |
| characterizations | str | |
| structure_comments | str | |

---

## `Quench`
**[Subclass of `AnnealSection`](#annealsection)**

### Required properties
| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| medium | str | |

---

## `RampNoRate`
**[Subclass of `AnnealSection`](#annealsection)**

### Required properties
| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| temp | validators.numbers.positive_decimal("RampNoRate/temp", "temp", True) | |
| time | validators.numbers.positive_decimal("RampNoRate/time", "time", True) | |
| temp_unit | validators.units.FOSTempUnit | |
| time_unit | validators.units.FOSUnit.enforce_dims("[time]") | |

---

## `RampNoTemp`
**[Subclass of `AnnealSection`](#annealsection)**

### Required properties
| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| time | validators.numbers.positive_decimal("RampNoTemp/time", "time", True) | |
| rate | validators.numbers.positive_decimal("RampNoTemp/rate", "rate", True) | |
| time_unit | validators.units.FOSUnit.enforce_dims("[time]") | |
| rate_unit | validators.units.temp_rate_unit | |

---

## `RampNoTime`
**[Subclass of `AnnealSection`](#annealsection)**

### Required properties
| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| temp | validators.numbers.positive_decimal("RampNoTime/temp", "temp", True) | |
| rate | validators.numbers.positive_decimal("RampNoTime/rate", "rate", True) | |
| temp_unit | validators.units.FOSTempUnit | |
| rate_unit | validators.units.temp_rate_unit | |

---

## `Reaction`
**[Subclass of ``](#)**

### Required properties
| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| nominal_formula | ChemFormula | |
| nominal_mass | validators.numbers.positive_decimal("Reaction/nominal_mass", "nominal_mass") | |
| nominal_mass_unit | validators.units.mass_unit("Reaction/nominal_mass_units") | |

---

## `SingleBlock`
**[Subclass of ``](#)**

### Required properties
| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| ext | SubContainer | |

### Optional properties
| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| rename | validators.rename.rename_dict | |

---

## `Synthesis`
**[Subclass of `SingleBlock`](#singleblock)**

### Required properties
| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| metadata | MetaData | |
| experimenters | ExperimenterList | |
| reaction | Reaction | |
| products | ProductList | |
| materials | MaterialList | |
| treatments | TreatmentList | |

### Optional properties
| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| cif | EmbeddedCIF | |
| cifs | ListBlock.Simple(EmbeddedCIF) | |
| laboratory_conditions | LabConditions | |
| equipment | EquipmentList | |

---

## `TemplateBlock`
**[Subclass of `SingleBlock`](#singleblock)**

### Required properties
| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| template_name | str | |

---

## `TemplateMeta`
**[Subclass of ``](#)**

### Required properties
| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| name | str | |
| description | str | |

---

## `TemplateSet`
**[Subclass of ``](#)**

### Required properties
| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| metadata | TemplateMeta | |

### Optional properties
| Property | Validation Routine or Class | Description |
|---------|-----------------------------|-------------|
| *(all from TemplateLists)* | TemplateLists | |
