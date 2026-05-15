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

import re

def build_key_value_regex(spec):
    delim = re.escape(spec["delimiter"])
    prefix = spec.get("prefix")

    # If prefix is a real string (not False), require it before the key
    if prefix:
        prefix = re.escape(prefix)
        key_pattern = rf"{prefix}(?P<key>[^:]+)"
    else:
        key_pattern = r"(?P<key>[^:]+)"

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

import re

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

def refresh():
    global BLOCK_HEADER, KEY_VALUE, COMMENT_LINE, NESTED_START, LOOP_KEY

    BLOCK_HEADER = build_block_header_regex(SYNTAX["block_header"])
    KEY_VALUE = build_key_value_regex(SYNTAX["key_value"])
    COMMENT_LINE = build_comment_regex(SYNTAX["comment"])
    NESTED_START = build_nested_start_regex(SYNTAX["nested"])
    LOOP_KEY = build_loop_key_regex(SYNTAX["key_value"])
    COMMENT_LINE = build_comment_regex(SYNTAX["comment"])






