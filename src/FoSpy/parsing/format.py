from .syntax import SYNTAX

def _indent(st:str, ind):
    return f"{' '*ind*SYNTAX["indent_size"]}{st}"

def format_block_header(name: str, list_type: str):
    spec = SYNTAX["block_header"]
    if list_type == "list":
        return f"{spec['list']['open']}{name.capitalize()}{spec['list']['close']}"
    else:
        return f"{spec['single']['open']}{name.capitalize()}{spec['single']['close']}"


def format_key_value(key: str, val: str, ind=0, looped=False):
    spec = SYNTAX["key_value"]
    delim = spec["delimiter"]
    prefix = spec.get("prefix")
    if looped:
        return _indent(val, ind)

    if prefix:
        key = f"{prefix}{key}"

    return _indent(f"{key}{delim}{"" if " " in delim else " "}{val}",ind)


def format_comment(text: str, ind: int = 0):
    spec = SYNTAX["comment"]
    prefix = spec["prefix"]
    return _indent(f"{prefix} {text}", ind)

def format_calc_comment(text:str):
    spec = SYNTAX["calc_comment"]
    prefix = spec["prefix"]
    return f"{prefix} {text}"

def format_nested_start(key, is_list: bool, looped=False, ind=0):
    spec = SYNTAX["nested"]
    open_br = spec["open"]

    val = open_br * (2 if is_list else 1)

    return format_key_value(key, val, ind, looped)

def format_nested_end(is_list, ind=0):
    spec = SYNTAX["nested"]
    close_br = spec["close"]
    close = close_br *(2 if is_list else 1)
    return _indent(close, ind)

def empty_nested(is_list):
    spec = SYNTAX["nested"]
    open_br = spec["open"]
    opn = open_br * (2 if is_list else 1)
    close_br = spec["close"]
    close = close_br *(2 if is_list else 1)

    return f"{opn}{close}"

def format_loop_key(key: str, ind=0):
    spec = SYNTAX["key_value"]
    prefix = spec.get("prefix")
    delim  = spec["delimiter"]

    if prefix:
        # key_
        return _indent(f"{key}{prefix}",ind)
    else:
        # :key
        return _indent(f"{delim}{key}",ind)


