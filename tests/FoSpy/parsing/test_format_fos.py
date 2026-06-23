import pytest

import FoSpy.parsing.format_fos


@pytest.mark.parametrize(
    "st,ind,expected",
    [
        # TODO: fill in test data for test_indent
        # pytest.param(, , id="")
    ]
)
def test_indent(st, ind, expected):
    # TODO: create assertions for test_indent
    # FoSpy.parsing.format_fos._indent(st, ind)
    pass


@pytest.mark.parametrize(
    "name,list_type,expected",
    [
        # TODO: fill in test data for test_format_block_header
        # pytest.param(, , id="")
    ]
)
def test_format_block_header(name, list_type, expected):
    # TODO: create assertions for test_format_block_header
    # FoSpy.parsing.format_fos.format_block_header(name, list_type)
    pass


@pytest.mark.parametrize(
    "key,val,ind,looped,expected",
    [
        # TODO: fill in test data for test_format_key_value
        # pytest.param(, , , , id="")
    ]
)
def test_format_key_value(key, val, ind, looped, expected):
    # TODO: create assertions for test_format_key_value
    # FoSpy.parsing.format_fos.format_key_value(key, val, ind, looped)
    pass


@pytest.mark.parametrize(
    "key,ind,looped,expected",
    [
        # TODO: fill in test data for test_format_embed_start
        # pytest.param(, , , id="")
    ]
)
def test_format_embed_start(key, ind, looped, expected):
    # TODO: create assertions for test_format_embed_start
    # FoSpy.parsing.format_fos.format_embed_start(key, ind, looped)
    pass


@pytest.mark.parametrize(
    "text,ind,expected",
    [
        # TODO: fill in test data for test_format_comment
        # pytest.param(, , id="")
    ]
)
def test_format_comment(text, ind, expected):
    # TODO: create assertions for test_format_comment
    # FoSpy.parsing.format_fos.format_comment(text, ind)
    pass


@pytest.mark.parametrize(
    "text,expected",
    [
        # TODO: fill in test data for test_format_calc_comment
        # pytest.param(, id="")
    ]
)
def test_format_calc_comment(text, expected):
    # TODO: create assertions for test_format_calc_comment
    # FoSpy.parsing.format_fos.format_calc_comment(text)
    pass


@pytest.mark.parametrize(
    "key,is_list,looped,ind,expected",
    [
        # TODO: fill in test data for test_format_nested_start
        # pytest.param(, , , , id="")
    ]
)
def test_format_nested_start(key, is_list, looped, ind, expected):
    # TODO: create assertions for test_format_nested_start
    # FoSpy.parsing.format_fos.format_nested_start(key, is_list, looped, ind)
    pass


@pytest.mark.parametrize(
    "is_list,ind,expected",
    [
        # TODO: fill in test data for test_format_nested_end
        # pytest.param(, , id="")
    ]
)
def test_format_nested_end(is_list, ind, expected):
    # TODO: create assertions for test_format_nested_end
    # FoSpy.parsing.format_fos.format_nested_end(is_list, ind)
    pass


@pytest.mark.parametrize(
    "is_list,expected",
    [
        # TODO: fill in test data for test_empty_nested
        # pytest.param(, id="")
    ]
)
def test_empty_nested(is_list, expected):
    # TODO: create assertions for test_empty_nested
    # FoSpy.parsing.format_fos.empty_nested(is_list)
    pass


@pytest.mark.parametrize(
    "key,ind,expected",
    [
        # TODO: fill in test data for test_format_loop_key
        # pytest.param(, , id="")
    ]
)
def test_format_loop_key(key, ind, expected):
    # TODO: create assertions for test_format_loop_key
    # FoSpy.parsing.format_fos.format_loop_key(key, ind)
    pass


@pytest.mark.parametrize(
    "label,expected",
    [
        # TODO: fill in test data for test_format_field
        # pytest.param(, id="")
    ]
)
def test_format_field(label, expected):
    # TODO: create assertions for test_format_field
    # FoSpy.parsing.format_fos.format_field(label)
    pass