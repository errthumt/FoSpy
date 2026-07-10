from .syntax import meta_keys as mk
from .syntax import meta_defaults as md
from .syntax import SYNTAX
from . import regex as rx
from .format_fos import format_key_value, empty_nested, format_field, format_comment

from .._debug import Debug
_debug = Debug()

def dict_from_file(filepath):
    block = None
    blocks = {}
    comments = {}
    current_block = "metadata"
    current_type = "single"
    embedding = False
    multiline = False
    break_line = None
    break_num = 0
    with open(filepath, "r", encoding="utf-8") as f:
        endComments = []
        for line in f:
            break_num += 1
            if rx.EMBEDDED_END.match(line):
                embedding = False
                block.append(line)
                continue

            if embedding:
                if rx.EMBEDDED_START.match(line):
                    break_line = line
                    break
                block.append(line)
                continue

            txt = line.strip()     
            if rx.CALC_COMMENT_LINE.match(txt) or (
                txt == "" and not multiline
            ):
                continue

            if txt.endswith(";;;"):
                multiline = True

            if multiline and SYNTAX["nested"]["close"] in txt:
                multiline = False

            if rx.EMBEDDED_START.match(txt):
                _debug.msg(f"Starting Embedding on line: {txt}")
                embedding = True

            # block = blocks.get(current_block)
            # if block is None:
            #     blocks[current_block] = (current_type,[])
            #     block = blocks[current_block][1]
            # else:
            #     block = block[1]

            blocks.setdefault(current_block, (current_type,[]))
            block = blocks[current_block][1]
            
            m = rx.BLOCK_HEADER.match(txt)
            if m:
                name_found = False
                for regex_name, typ in zip(("list_name", "single_name"),("list","single")):
                    if m.group(regex_name) is not None:
                        current_block = m.group(regex_name).lower()
                        current_type = typ
                        name_found = True
                        break
                if not name_found:
                    raise SyntaxError(f"Line: '{txt}' was identified as a block header but no header name could be identified")

                #_debug.msg(f"Identified {current_type} block header in line: {txt}")
                #_debug.msg(f"Block name: {current_block}")

                comments[current_block] = [rx.COMMENT_LINE.match(ln).group("text").lstrip() for ln in endComments]
                endComments = []
                continue

            if rx.COMMENT_LINE.match(txt):
                endComments.append(txt)
                continue

            for ln in [*endComments,txt]:
                block.append(ln.strip())
            endComments = []
    if embedding:
        raise SyntaxError(
            "An embedded document was never closed before the end of the file or starting a new embed.\n"
            + f"Current Line (line #{break_num}): "
            + ("<end of FOS file>\n" if not break_line else break_line)
            + "Ensure that there are spaces between '#', 'END FOS EMBED', and '}}}' when ending an "
            + "embedded document."
        )

    for block, (typ, lines) in blocks.items():
        if typ == "single":
            blockDict = create_single_block_dict(lines)
            if blockDict == {}:
                blocks[block] = []
            else:
                blocks[block] = [blockDict]
        elif typ == "list":
            blocks[block] = create_list_block_dict(lines)
        else:
            raise ValueError(f"Unrecognized block type: '{typ}', expected either single or list")
    blocks[mk["comments"]] = comments

    for meta_key in mk.values():
        if meta_key not in blocks:
            try:
                blocks[meta_key] = md[meta_key].copy()
            except AttributeError:
                blocks[meta_key] = md[meta_key]

    return blocks

def _create_multiline_str(lines):
    out = ""

    for i, ln in enumerate(lines):
        stripped = ln.strip()
        if stripped == "":
            out += "\n\n"
        else:
            out += stripped + " "

    return out.strip()


def create_single_block_dict(lines, _list_type="explicit"):
    """"""

    """ _debug.msg('Processing the following lines as a single block:')
    for line in lines:
        _debug.msg(line)
    _debug.msg('-----') """
    if len(lines)==0:
        return {}
    
    # Single string mode, process block as a multiline string instead of key: value pairs
    if lines[0].strip() == ";;;":
        return _create_multiline_str(lines[1:])

    open_br = SYNTAX["nested"]["open"]
    close_br = SYNTAX["nested"]["close"]

    nested_lines = []
    nested_type = None
    out_dict = {mk["list_type"]:_list_type, mk["comments"]:{}}
    nested = 0
    nested_key = None
    comments = []
    embedding = False
    for line in lines:
        # _debug.msg(f'processing: {line}')
        is_comment = rx.COMMENT_LINE.match(line)
        if is_comment:
            if nested > 0:
                nested_lines.append(line)
            else:
                comments.append(is_comment.group("text").lstrip())
        elif embedding:
            if rx.EMBEDDED_END.match(line):
                embedding = False
                out_dict[nested_key] = "".join(nested_lines)
                nested_lines = []
                nested_key = None
                nested_type = None
                _debug.msg("Ending Embedding")
            else:
                nested_lines.append(line)
        elif nested==0:
            if line.strip() == "" and not embedding:
                continue
            m = rx.KEY_VALUE.match(line)
            if m:
                key, val = m.group("key"), m.group("val")
            else:
                raise SyntaxError(f"Failed to parse key: value pair from line: '{line}'")
            # _debug.msg(f"processed: key:'{key}', val:'{val}'")
            if key.startswith("-"):
                key = key[1:]
                val = format_field("template")
            if key in out_dict:
                raise ValueError(f"Duplicate key found: '{key}' Each key can only appear once within a block.")
            
            emb = rx.EMBEDDED_START.match(line)
            m = rx.NESTED_START.match(val) or emb
            if val in (empty_nested(True),empty_nested(False)):
                out_dict[key] = []
                out_dict[mk["comments"]][key]=comments
                comments = []
            
            elif m:
                # _debug.msg(f'{key} is nested')
                
                nested_key = key
                if rx.EMBEDDED_START.match(line):
                    embedding = True
                    _debug.msg("Starting embedding")

                elif m.group("list"):
                    nested_type = "list"
                    nested += 2
                
                else:
                    nested_type = "single"
                    nested += 1

                out_dict[mk["comments"]][nested_key] = comments
                comments = []

                remainder = m.group("rest") if not emb else None
                if remainder:
                    nested_lines.append(remainder)
                continue
            else:
                out_dict[key] = val
                out_dict[mk["comments"]][key] = comments
                comments = []
        else:
            nested += line.count(open_br)
            nested -= line.count(close_br)

            if nested < 0:
                raise ValueError("Mismatched brackets when trying to parse blocks.")
            elif nested == 0:
                # _debug.msg(f'ended nesting on line: {line}')
                stripped = line.rstrip(close_br)
                if stripped:
                    nested_lines.append(stripped)
                val = [create_single_block_dict(nested_lines)] if nested_type == "single" else create_list_block_dict(nested_lines)
                if isinstance(val[0], str):
                    val = val[0]
                out_dict[nested_key] = val
                nested_lines = []
                nested_key = None
                nested_type = None
            else:
                nested_lines.append(line)
    for meta_key in mk.values():
        if meta_key not in out_dict:
            out_dict[meta_key] = md[meta_key]
    
    if nested != 0:
        raise ValueError("Mismatched brackets when trying to parse blocks.")

    return out_dict


            

def create_list_block_dict(lines):

    open_br = SYNTAX["nested"]["open"]
    close_br = SYNTAX["nested"]["close"]

    block_list = []
    current_lines = []
    keys = []

    nested = 0
    m = False
    for ln in lines:
        if rx.COMMENT_LINE.match(ln):
            continue
        m = rx.LOOP_KEY.match(ln)
        if m:
            break

    if m: # loop_key mode
        getting_keys = True
        comments = []
        key_comments = {}

        key_idx = 0
        embedding = False
        for line in lines:
            # _debug.msg(f'processing list line: {line}')

            if embedding:
                if rx.EMBEDDED_END.match(line):
                    embedding = False
                current_lines.append(line)
                continue

            is_loop_key = rx.LOOP_KEY.match(line)
            is_key_val = rx.KEY_VALUE.match(line)
            is_comment = rx.COMMENT_LINE.match(line)
            is_embed_start = rx.EMBEDDED_START.match(line)
            if getting_keys and is_comment:
                comments.append(is_comment.group("text").lstrip())
            elif nested>0 or is_comment:
                current_lines.append(line)
            elif is_loop_key:
                if not getting_keys:
                    raise SyntaxError(f"Error on line: '{line}'. You cannot declare more loop keys after starting values.")
                key = is_loop_key.group("key")
                if key in keys:
                    raise ValueError(f"Duplicate key found: '{key}'. Each key can only be specified once at the beginning of a looped list block.")
                key_comments[key.lstrip("-")] = comments
                comments = []
                keys.append(key)
                # _debug.msg(f'added key: {key}')
            
            elif is_key_val:
                if getting_keys:
                    getting_keys = False
                    for ln in comments:
                        current_lines.append(format_comment(ln))
                embedding = is_embed_start
                current_lines.append(line)

            else:
                if getting_keys:
                    getting_keys = False
                    for ln in comments:
                        current_lines.append(format_comment(ln))
                if key_idx == len(keys):
                    block_list.append(create_single_block_dict(current_lines, _list_type="looped"))
                    trailing_comments = []
                    for ln in reversed(current_lines):
                        if rx.COMMENT_LINE.match(ln):
                            trailing_comments.append(ln)
                        else:
                            break
                    
                    trailing_comments.reverse()
                    current_lines = trailing_comments
                    key_idx = 0
                embedding = rx.EMBEDDED_START.match(line)
                key = keys[key_idx]
                current_lines.append(format_key_value(key, line))
                key_idx += 1
                

            nested += line.count(open_br)
            nested -= line.count(close_br)
            if nested<0:
                raise ValueError("Mismatched brackets when trying to parse blocks.")

        if current_lines:
            # _debug.msg("sending lines to single block:")
            for ln in current_lines:
                # _debug.msg(l)
                pass
            # _debug.msg("---")
            block_list.append(create_single_block_dict(current_lines, _list_type="looped"))

        block_list[0][mk["key_comments"]] = key_comments
    else:
        embedding = False
        for line in lines:
            is_key_val, is_comment = rx.KEY_VALUE.match(line), rx.COMMENT_LINE.match(line)
            if embedding or rx.EMBEDDED_START.match(line):
                if rx.EMBEDDED_END.match(line):
                    embedding = False
                elif rx.EMBEDDED_START.match(line):
                    embedding = True
                current_lines.append(line)
                continue

            if not (is_key_val or is_comment or nested>0):
                raise SyntaxError(f"Failed to parse key: value pair from line: '{line}'")
            key = is_key_val.group("key") if is_key_val else None
            if nested > 0:
                current_lines.append(line)
            elif key in keys:
                block_list.append(create_single_block_dict(current_lines))
                trailing_comments = []
                for ln in reversed(current_lines):
                    if rx.COMMENT_LINE.match(ln):
                        trailing_comments.append(ln)
                    else:
                        break
                
                trailing_comments.reverse()
                current_lines = [*trailing_comments, line]
                keys = [key]
            else:
                if key is not None:
                    keys.append(key)
                #_debug.pmsg(keys)
                current_lines.append(line)
            nested += line.count(open_br)
            nested -= line.count(close_br)
            _debug.msg(f"Current nested: {nested} | Current line: {line}")
            if nested<0:
                raise ValueError("Mismatched brackets when trying to parse blocks.")

        block_list.append(create_single_block_dict(current_lines))
    if nested != 0:
        raise ValueError("Mismatched brackets when trying to parse blocks.")
    return block_list