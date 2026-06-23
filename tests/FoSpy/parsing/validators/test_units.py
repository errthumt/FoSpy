import pytest

import FoSpy.parsing.validators.units


@pytest.mark.parametrize(
    "unitlike,expected",
    [
        # TODO: fill in test data for test_temp_rate_unit
        # pytest.param(, id="")
    ]
)
def test_temp_rate_unit(unitlike, expected):
    # TODO: create assertions for test_temp_rate_unit
    # FoSpy.parsing.validators.units.temp_rate_unit(unitlike)
    pass


@pytest.mark.parametrize(
    "value,value_key,cls,sourceDict,expected",
    [
        # TODO: fill in test data for test_attach_unit
        # pytest.param(, , , , id="")
    ]
)
def test_attach_unit(value, value_key, cls, sourceDict, expected):
    # TODO: create assertions for test_attach_unit
    # FoSpy.parsing.validators.units.attach_unit(value, value_key, cls, sourceDict)
    pass


@pytest.mark.parametrize(
    "instance,cls,allow_dims,expected",
    [
        # TODO: fill in test data for test_fosunit_enforce_dims
        # pytest.param(FoSpy.parsing.validators.units.FOSUnit(unitlike, allow_dims), , , expected, id="")
    ]
)
def test_fosunit_enforce_dims(instance, cls, allow_dims, expected):
    # TODO: write test for test_fosunit_enforce_dims
    # TODO: create assertions for test_fosunit_enforce_dims
    # instance.enforce_dims(cls, allow_dims)
    pass


@pytest.mark.parametrize(
    "instance,cls,expected",
    [
        # TODO: fill in test data for test_fostempunit_enforce_dims
        # pytest.param(FoSpy.parsing.validators.units.FOSTempUnit(unitlike, rate), , expected, id="")
    ]
)
def test_fostempunit_enforce_dims(instance, cls, expected):
    # TODO: write test for test_fostempunit_enforce_dims
    # TODO: create assertions for test_fostempunit_enforce_dims
    # instance.enforce_dims(cls)
    pass