import pytest

import FoSpy.config.__init__


@pytest.mark.parametrize(
    "filepath,prompt,expected",
    [
        # TODO: fill in test data for test_save_all
        # pytest.param(, , id="")
    ]
)
def test_save_all(filepath, prompt, expected):
    # TODO: create assertions for test_save_all
    # FoSpy.config.__init__.save_all(filepath, prompt)
    pass


@pytest.mark.parametrize(
    "filepath,expected",
    [
        # TODO: fill in test data for test_load_user
        # pytest.param(, id="")
    ]
)
def test_load_user(filepath, expected):
    # TODO: create assertions for test_load_user
    # FoSpy.config.__init__.load_user(filepath)
    pass


@pytest.mark.parametrize(
    "prompt,expected",
    [
        # TODO: fill in test data for test_revert
        # pytest.param(, id="")
    ]
)
def test_revert(prompt, expected):
    # TODO: create assertions for test_revert
    # FoSpy.config.__init__.revert(prompt)
    pass


@pytest.mark.parametrize(
    "prompt,expected",
    [
        # TODO: fill in test data for test_reset
        # pytest.param(, id="")
    ]
)
def test_reset(prompt, expected):
    # TODO: create assertions for test_reset
    # FoSpy.config.__init__.reset(prompt)
    pass


@pytest.mark.parametrize(
    "expected",
    [
        # TODO: fill in test data for test_restart_session
        # pytest.param(id="")
    ]
)
def test_restart_session(expected):
    # TODO: create assertions for test_restart_session
    # FoSpy.config.__init__._restart_session()
    pass


@pytest.mark.parametrize(
    "expected",
    [
        # TODO: fill in test data for test_load_defaults
        # pytest.param(id="")
    ]
)
def test_load_defaults(expected):
    # TODO: create assertions for test_load_defaults
    # FoSpy.config.__init__._load_defaults()
    pass


@pytest.mark.parametrize(
    "a,b,expected",
    [
        # TODO: fill in test data for test_deep_merge
        # pytest.param(, , id="")
    ]
)
def test_deep_merge(a, b, expected):
    # TODO: create assertions for test_deep_merge
    # FoSpy.config.__init__._deep_merge(a, b)
    pass


@pytest.mark.parametrize(
    "defaults,current,expected",
    [
        # TODO: fill in test data for test_extract_user
        # pytest.param(, , id="")
    ]
)
def test_extract_user(defaults, current, expected):
    # TODO: create assertions for test_extract_user
    # FoSpy.config.__init__._extract_user(defaults, current)
    pass


@pytest.mark.parametrize(
    "expected",
    [
        # TODO: fill in test data for test_load
        # pytest.param(id="")
    ]
)
def test_load(expected):
    # TODO: create assertions for test_load
    # FoSpy.config.__init__._load()
    pass


@pytest.mark.parametrize(
    "instance,key,expected",
    [
        # TODO: fill in test data for test_nestedconfig_getattr
        # pytest.param(FoSpy.config.__init__.NestedConfig(config_dict, name), , expected, id="")
    ]
)
def test_nestedconfig_getattr(instance, key, expected):
    # TODO: write test for test_nestedconfig_getattr
    # TODO: create assertions for test_nestedconfig_getattr
    # instance.__getattr__(key)
    pass


@pytest.mark.parametrize(
    "instance,key,val,expected",
    [
        # TODO: fill in test data for test_nestedconfig_setattr
        # pytest.param(FoSpy.config.__init__.NestedConfig(config_dict, name), , , expected, id="")
    ]
)
def test_nestedconfig_setattr(instance, key, val, expected):
    # TODO: write test for test_nestedconfig_setattr
    # TODO: create assertions for test_nestedconfig_setattr
    # instance.__setattr__(key, val)
    pass


@pytest.mark.parametrize(
    "instance,expected",
    [
        # TODO: fill in test data for test_nestedconfig_iter
        # pytest.param(FoSpy.config.__init__.NestedConfig(config_dict, name), expected, id="")
    ]
)
def test_nestedconfig_iter(instance, expected):
    # TODO: write test for test_nestedconfig_iter
    # TODO: create assertions for test_nestedconfig_iter
    # instance.__iter__()
    pass


@pytest.mark.parametrize(
    "instance,expected",
    [
        # TODO: fill in test data for test_nestedconfig_to_dict
        # pytest.param(FoSpy.config.__init__.NestedConfig(config_dict, name), expected, id="")
    ]
)
def test_nestedconfig_to_dict(instance, expected):
    # TODO: write test for test_nestedconfig_to_dict
    # TODO: create assertions for test_nestedconfig_to_dict
    # instance.to_dict()
    pass


@pytest.mark.parametrize(
    "instance,key,default,expected",
    [
        # TODO: fill in test data for test_nestedconfig_get
        # pytest.param(FoSpy.config.__init__.NestedConfig(config_dict, name), , , expected, id="")
    ]
)
def test_nestedconfig_get(instance, key, default, expected):
    # TODO: write test for test_nestedconfig_get
    # TODO: create assertions for test_nestedconfig_get
    # instance.get(key, default)
    pass


@pytest.mark.parametrize(
    "instance,key,value,expected",
    [
        # TODO: fill in test data for test_nestedconfig_update
        # pytest.param(FoSpy.config.__init__.NestedConfig(config_dict, name), , , expected, id="")
    ]
)
def test_nestedconfig_update(instance, key, value, expected):
    # TODO: write test for test_nestedconfig_update
    # TODO: create assertions for test_nestedconfig_update
    # instance.update(key, value)
    pass


@pytest.mark.parametrize(
    "instance,expected",
    [
        # TODO: fill in test data for test_nestedconfig_call
        # pytest.param(FoSpy.config.__init__.NestedConfig(config_dict, name), expected, id="")
    ]
)
def test_nestedconfig_call(instance, expected):
    # TODO: write test for test_nestedconfig_call
    # TODO: create assertions for test_nestedconfig_call
    # instance.__call__()
    pass