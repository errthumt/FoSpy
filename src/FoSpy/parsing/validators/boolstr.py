from ..._docs.properties import _validator_rules

true_values = ["true", "t", "yes", "y", "1", "on"]
false_values = ["false", "f", "no", "n", "0", "off"]

@_validator_rules(
    "A boolen value (True or False)",
    "Acceptable 'True' values (not case sensitive):",true_values,
    "Acceptable 'False' values (not case sensitive):",false_values
)
def str_to_bool(s):
    if isinstance(s, bool):
        return s

    if not isinstance(s, str):
        raise TypeError("Expected a string or bool")

    s = s.strip().lower()
    if s in true_values:
        return True
    if s in false_values:
        return False

    raise ValueError(f"Could not parse '{s!r}' as a boolean")