import re

from .syntax import SYNTAX

def build_block_header_regex(spec):
    single = spec["single"]
    list_ = spec["list"]

    pattern = (
        rf"^(?:"
        rf"{re.escape(list_['open'])}(?P<list_name>[^\]]+){re.escape(list_['close'])}"
        rf"|"
        rf"{re.escape(single['open'])}(?P<single_name>[^\]]+){re.escape(single['close'])}"
        rf")$"
    )
    return re.compile(pattern)

BLOCK_HEADER = build_block_header_regex(SYNTAX["block_header"])

def build_key_value_regex(spec):
    delim = re.escape(spec["delimiter"])
    prefix = spec.get("prefix")

    # Key cannot contain the delimiter
    if prefix:
        prefix_esc = re.escape(prefix)
        key_pattern = rf"{prefix_esc}(?P<key>[^{delim}]+)"
    else:
        key_pattern = rf"(?P<key>[^{delim}]+)"

    if spec["require_value"]:
        pattern = rf"^{key_pattern}\s*{delim}\s*(?P<val>.+)$"
    else:
        pattern = rf"^{key_pattern}\s*{delim}\s*(?P<val>.*)$"

    return re.compile(pattern)

KEY_VALUE = build_key_value_regex(SYNTAX["key_value"])

def build_comment_regex(spec):
    prefix = re.escape(spec["prefix"])
    if spec["allow_leading_ws"]:
        return re.compile(rf"^\s*{prefix}(?P<text>.*)$")
    else:
        return re.compile(rf"^{prefix}(?P<text>.*)$")

COMMENT_LINE = build_comment_regex(SYNTAX["comment"])

def build_calc_comment_regex(spec):
    """
    Matches calculated comments of the form:
        <comment_prefix> <calc_prefix> <text>
    Example:
        // ## Calculated MW: 123.45 g/mol
    """
    comment_prefix = re.escape(SYNTAX["comment"]["prefix"])
    calc_prefix = re.escape(spec["prefix"])

    # Allow leading whitespace before the comment prefix
    return re.compile(
        rf"^\s*{comment_prefix}\s+{calc_prefix}\s+(?P<text>.*)$"
    )

CALC_COMMENT_LINE = build_calc_comment_regex(SYNTAX["calc_comment"])

def build_nested_start_regex(spec):
    open_bracket = re.escape(spec["open"])  # usually "["

    pattern = (
        rf"^{open_bracket}"
        rf"(?P<list>{open_bracket})?"
        rf"(?P<rest>.*)$"
    )

    return re.compile(pattern)

NESTED_START = build_nested_start_regex(SYNTAX["nested"])

def build_loop_key_regex(spec):
    prefix = spec.get("prefix")
    delim  = re.escape(spec["delimiter"])

    if prefix:
        # Require key followed by prefix, e.g. "key_"
        prefix = re.escape(prefix)
        pattern = rf"^(?P<key>[^{prefix}]+){prefix}$"
    else:
        # Default: delimiter before key, e.g. ":key"
        pattern = rf"^{delim}(?P<key>[^{delim}]+)$"

    return re.compile(pattern)

LOOP_KEY = build_loop_key_regex(SYNTAX["key_value"])

def build_comment_regex(spec):
    prefix = re.escape(spec["prefix"])  # usually "//"
    allow_ws = spec.get("allow_leading_ws", True)

    if allow_ws:
        pattern = rf"^\s*{prefix}(?P<text>.*)$"
    else:
        pattern = rf"^{prefix}(?P<text>.*)$"

    return re.compile(pattern)

COMMENT_LINE = build_comment_regex(SYNTAX["comment"])

def build_embedded_start_regex(spec):
    open_tok = re.escape(SYNTAX["embedded"]["open"])
    return re.compile(rf".*{open_tok}.*")

EMBEDDED_START = build_embedded_start_regex(SYNTAX["embedded"])

def build_embedded_end_regex(spec):
    prefix = re.escape(spec["prefix"])
    close_tok = re.escape(spec["close"])

    pattern = rf"^{prefix}*\s*{close_tok}\s*$"
    return re.compile(pattern)

EMBEDDED_END = build_embedded_end_regex(SYNTAX["embedded"])



def refresh():
    global BLOCK_HEADER, KEY_VALUE, COMMENT_LINE, CALC_COMMENT_LINE, NESTED_START, LOOP_KEY, EMBEDDED_START, EMBEDDED_END

    BLOCK_HEADER = build_block_header_regex(SYNTAX["block_header"])
    KEY_VALUE = build_key_value_regex(SYNTAX["key_value"])
    COMMENT_LINE = build_comment_regex(SYNTAX["comment"])
    CALC_COMMENT_LINE = build_calc_comment_regex(SYNTAX["calc_comment"])
    NESTED_START = build_nested_start_regex(SYNTAX["nested"])
    LOOP_KEY = build_loop_key_regex(SYNTAX["key_value"])
    COMMENT_LINE = build_comment_regex(SYNTAX["comment"])
    EMBEDDED_START = build_embedded_start_regex(SYNTAX["embedded"])
    EMBEDDED_END = build_embedded_end_regex(SYNTAX["embedded"])






