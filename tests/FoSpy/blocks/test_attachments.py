import pytest

import FoSpy.blocks.attachments


@pytest.mark.parametrize(
    "instance,name,value,expected",
    [
        # TODO: fill in test data for test_attachment_setattr
        # pytest.param(FoSpy.blocks.attachments.Attachment(blockDict), , , expected, id="")
    ]
)
def test_attachment_setattr(instance, name, value, expected):
    # TODO: write test for test_attachment_setattr
    # TODO: create assertions for test_attachment_setattr
    # instance.__setattr__(name, value)
    pass


@pytest.mark.parametrize(
    "instance,expected",
    [
        # TODO: fill in test data for test_attachment_get_filepath
        # pytest.param(FoSpy.blocks.attachments.Attachment(blockDict), expected, id="")
    ]
)
def test_attachment_get_filepath(instance, expected):
    # TODO: write test for test_attachment_get_filepath
    # TODO: create assertions for test_attachment_get_filepath
    # instance._get_filepath()
    pass


@pytest.mark.parametrize(
    "instance,cls,subcls,expected",
    [
        # TODO: fill in test data for test_attachment_enforce_subtype
        # pytest.param(FoSpy.blocks.attachments.Attachment(blockDict), , , expected, id="")
    ]
)
def test_attachment_enforce_subtype(instance, cls, subcls, expected):
    # TODO: write test for test_attachment_enforce_subtype
    # TODO: create assertions for test_attachment_enforce_subtype
    # instance.enforce_subtype(cls, subcls)
    pass


@pytest.mark.parametrize(
    "instance,cls,blockDict,expected",
    [
        # TODO: fill in test data for test_attachment_dispatch_subclass
        # pytest.param(FoSpy.blocks.attachments.Attachment(blockDict), , , expected, id="")
    ]
)
def test_attachment_dispatch_subclass(instance, cls, blockDict, expected):
    # TODO: write test for test_attachment_dispatch_subclass
    # TODO: create assertions for test_attachment_dispatch_subclass
    # instance.dispatch_subclass(cls, blockDict)
    pass


@pytest.mark.parametrize(
    "instance,expected",
    [
        # TODO: fill in test data for test_pathfile_get_abspath
        # pytest.param(FoSpy.blocks.attachments.PathFile(blockDict), expected, id="")
    ]
)
def test_pathfile_get_abspath(instance, expected):
    # TODO: write test for test_pathfile_get_abspath
    # TODO: create assertions for test_pathfile_get_abspath
    # instance._get_abspath()
    pass


@pytest.mark.parametrize(
    "instance,expected",
    [
        # TODO: fill in test data for test_pathfile_get_filedir
        # pytest.param(FoSpy.blocks.attachments.PathFile(blockDict), expected, id="")
    ]
)
def test_pathfile_get_filedir(instance, expected):
    # TODO: write test for test_pathfile_get_filedir
    # TODO: create assertions for test_pathfile_get_filedir
    # instance._get_filedir()
    pass


@pytest.mark.parametrize(
    "instance,expected",
    [
        # TODO: fill in test data for test_pathfile_exists
        # pytest.param(FoSpy.blocks.attachments.PathFile(blockDict), expected, id="")
    ]
)
def test_pathfile_exists(instance, expected):
    # TODO: write test for test_pathfile_exists
    # TODO: create assertions for test_pathfile_exists
    # instance.exists()
    pass


@pytest.mark.parametrize(
    "instance,new_copy,overwrite,expected",
    [
        # TODO: fill in test data for test_pathfile_refresh
        # pytest.param(FoSpy.blocks.attachments.PathFile(blockDict), , , expected, id="")
    ]
)
def test_pathfile_refresh(instance, new_copy, overwrite, expected):
    # TODO: write test for test_pathfile_refresh
    # TODO: create assertions for test_pathfile_refresh
    # instance.refresh(new_copy, overwrite)
    pass


@pytest.mark.parametrize(
    "instance,rf_new_copy,rf_overwrite,expected",
    [
        # TODO: fill in test data for test_pathfile_get_filepath
        # pytest.param(FoSpy.blocks.attachments.PathFile(blockDict), , , expected, id="")
    ]
)
def test_pathfile_get_filepath(instance, rf_new_copy, rf_overwrite, expected):
    # TODO: write test for test_pathfile_get_filepath
    # TODO: create assertions for test_pathfile_get_filepath
    # instance._get_filepath(rf_new_copy, rf_overwrite)
    pass


@pytest.mark.parametrize(
    "instance,expected",
    [
        # TODO: fill in test data for test_pathfile_copy
        # pytest.param(FoSpy.blocks.attachments.PathFile(blockDict), expected, id="")
    ]
)
def test_pathfile_copy(instance, expected):
    # TODO: write test for test_pathfile_copy
    # TODO: create assertions for test_pathfile_copy
    # instance.copy()
    pass


@pytest.mark.parametrize(
    "instance,engine_name,expected",
    [
        # TODO: fill in test data for test_ciffile_get_engine
        # pytest.param(FoSpy.blocks.attachments.CIFFile(blockDict), , expected, id="")
    ]
)
def test_ciffile_get_engine(instance, engine_name, expected):
    # TODO: write test for test_ciffile_get_engine
    # TODO: create assertions for test_ciffile_get_engine
    # instance._get_engine(engine_name)
    pass


@pytest.mark.parametrize(
    "instance,engine_name,expected",
    [
        # TODO: fill in test data for test_ciffile_get_pattern
        # pytest.param(FoSpy.blocks.attachments.CIFFile(blockDict), , expected, id="")
    ]
)
def test_ciffile_get_pattern(instance, engine_name, expected):
    # TODO: write test for test_ciffile_get_pattern
    # TODO: create assertions for test_ciffile_get_pattern
    # instance.get_pattern(engine_name)
    pass


@pytest.mark.parametrize(
    "instance,engine_name,expected",
    [
        # TODO: fill in test data for test_ciffile_get_peaks
        # pytest.param(FoSpy.blocks.attachments.CIFFile(blockDict), , expected, id="")
    ]
)
def test_ciffile_get_peaks(instance, engine_name, expected):
    # TODO: write test for test_ciffile_get_peaks
    # TODO: create assertions for test_ciffile_get_peaks
    # instance.get_peaks(engine_name)
    pass


@pytest.mark.parametrize(
    "instance,engine_name,expected",
    [
        # TODO: fill in test data for test_ciffile_new_engine
        # pytest.param(FoSpy.blocks.attachments.CIFFile(blockDict), , expected, id="")
    ]
)
def test_ciffile_new_engine(instance, engine_name, expected):
    # TODO: write test for test_ciffile_new_engine
    # TODO: create assertions for test_ciffile_new_engine
    # instance.new_engine(engine_name)
    pass


@pytest.mark.parametrize(
    "instance,subprocess,expected",
    [
        # TODO: fill in test data for test_ciffile_quick_pattern
        # pytest.param(FoSpy.blocks.attachments.CIFFile(blockDict), , expected, id="")
    ]
)
def test_ciffile_quick_pattern(instance, subprocess, expected):
    # TODO: write test for test_ciffile_quick_pattern
    # TODO: create assertions for test_ciffile_quick_pattern
    # instance.quick_pattern(subprocess)
    pass