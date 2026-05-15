from .syntax import meta_keys as mk
from . import _debug
from .regex import *
from .format import format_key_value

def dict_from_file(filepath):
    _debug.msg("Parsing Debug Mode is On")
    blocks = {}
    comments = {}
    current_block = "metadata"
    current_type = "single"
    with open(filepath, "r", encoding="utf-8") as f:
        endComments = []
        for line in f:
            txt = line.strip()     
            if txt == "":
                continue

            block = blocks.get(current_block)
            if block is None:
                blocks[current_block] = (current_type,[])
                block = blocks[current_block][1]
            else:
                block = block[1]

            
            '''
            if txt.startswith("[") and txt.endswith("]") and txt not in ("[]","[[]]"):
                if txt.startswith("[["):
                    current_type = "list"
                else:
                    current_type = "single"

                current_block = txt.strip("[]").lower()'''
            m = BLOCK_HEADER.match(txt)
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

                comments[current_block] = [COMMENT_LINE.match(l).group("text").lstrip() for l in endComments]
                endComments = []
                continue

            if COMMENT_LINE.match(txt):
                endComments.append(txt)
                continue

            for l in [*endComments,txt]:
                block.append(l.strip())
            endComments = []

    for block, (typ, lines) in blocks.items():
        if typ == "single":
            blocks[block] = [create_single_block_dict(lines)]
        elif typ == "list":
            blocks[block] = create_list_block_dict(lines)
        else:
            raise ValueError(f"Unrecognized block type: '{typ}', expected either single or list")
    blocks[mk["comments"]] = comments

    return blocks

def create_single_block_dict(lines, _list_type="explicit"):
    """"""

    """ _debug.msg('Processing the following lines as a single block:')
    for line in lines:
        _debug.msg(line)
    _debug.msg('-----') """
    nested_lines = []
    nested_type = None
    out_dict = {mk["list_type"]:_list_type, mk["comments"]:{}}
    nested = 0
    nested_key = None
    comments = []
    for line in lines:
        # _debug.msg(f'processing: {line}')
        is_comment = COMMENT_LINE.match(line)
        if is_comment:
            if nested > 0:
                nested_lines.append(line)
            else:
                comments.append(is_comment.group("text").lstrip())
        elif nested==0:
            m = KEY_VALUE.match(line)
            if m:
                key, val = m.group("key"), m.group("val")
            else:
                raise SyntaxError(f"Failed to parse key: value pair from line: '{line}'")
            # _debug.msg(f"processed: key:'{key}', val:'{val}'")
            if key in out_dict:
                raise ValueError(f"Duplicate key found: '{key}' Each key can only appear once within a block.")
            
            m = NESTED_START.match(val)
            if val in ("[]","[[]]"):
                out_dict[key] = []
                out_dict[mk["comments"]][key]=comments
                comments = []
            
            elif m:
                # _debug.msg(f'{key} is nested')
                nested_key = key
                if m.group("list"):
                    nested_type = "list"
                    nested += 2
                else:
                    nested_type = "single"
                    nested += 1

                out_dict[mk["comments"]][nested_key] = comments
                comments = []

                remainder = m.group("rest")
                if remainder:
                    nested_lines.append(remainder)
                continue
            else:
                out_dict[key] = val
                out_dict[mk["comments"]][key] = comments
                comments = []
        else:
            nested += line.count("[")
            nested -= line.count("]")

            if nested < 0:
                raise ValueError("Mismatched brackets when trying to parse blocks.")
            elif nested == 0:
                # _debug.msg(f'ended nesting on line: {line}')
                stripped = line.rstrip("]")
                if stripped:
                    nested_lines.append(stripped)
                out_dict[nested_key] = [create_single_block_dict(nested_lines)] if nested_type == "single" else create_list_block_dict(nested_lines)
                nested_lines = []
                nested_key = None
                nested_type = None
            else:
                nested_lines.append(line)
    return out_dict


            

def create_list_block_dict(lines):
    for line in lines:
        # _debug.msg(line)
        pass
    block_list = []
    current_lines = []
    keys = []

    nested = 0

    m = LOOP_KEY.match(lines[0])
    if m: # loop_key mode
        getting_keys = True
        comments = []
        key_comments = {}

        key_idx = 0
        for line in lines:
            # _debug.msg(f'processing list line: {line}')

            is_loop_key = LOOP_KEY.match(line)
            is_key_val = KEY_VALUE.match(line)
            is_comment = COMMENT_LINE.match(line)
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
                key_comments[key] = comments
                comments = []
                keys.append(key)
                # _debug.msg(f'added key: {key}')
            
            elif is_key_val:
                if getting_keys:
                    getting_keys = False
                    for l in comments:
                        current_lines.append(l)
                current_lines.append(line)

            else:
                if getting_keys:
                    getting_keys = False
                    for l in comments:
                        current_lines.append(l)
                if key_idx == len(keys):
                    block_list.append(create_single_block_dict(current_lines, _list_type="looped"))
                    trailing_comments = []
                    for l in reversed(current_lines):
                        if COMMENT_LINE.match(l):
                            trailing_comments.append(l)
                        else:
                            break
                    
                    trailing_comments.reverse()
                    current_lines = trailing_comments
                    key_idx = 0

                key = keys[key_idx]
                current_lines.append(format_key_value(key, line))
                key_idx += 1
                

            if "[" in line:
                # _debug.msg(f'found [ in line: {line}')
                nested += 1
            if "]" in line:
                nested -= 1
            if nested<0:
                raise ValueError("Mismatched brackets when trying to parse blocks.")

        if current_lines:
            # _debug.msg("sending lines to single block:")
            for l in current_lines:
                # _debug.msg(l)
                pass
            # _debug.msg("---")
            block_list.append(create_single_block_dict(current_lines, _list_type="looped"))

        block_list[0][mk["key_comments"]] = key_comments
    else:
        for line in lines:
            is_key_val, is_comment = KEY_VALUE.match(line), COMMENT_LINE.match(line)
            if not (is_key_val or is_comment):
                raise SyntaxError(f"Failed to parse key: value pair from line: '{line}'")
            key = is_key_val.group("key") if is_key_val else None
            if nested > 0:
                current_lines.append(line)
            elif key in keys:
                block_list.append(create_single_block_dict(current_lines))
                trailing_comments = []
                for l in reversed(current_lines):
                    if COMMENT_LINE.match(l):
                        trailing_comments.append(l)
                    else:
                        break
                
                trailing_comments.reverse()
                current_lines = [*trailing_comments, line]
                keys = []
            else:
                keys.append(key)
                #_debug.pmsg(keys)
                current_lines.append(line)

            if "[" in line:
                nested += 1
            if "]" in line:
                nested -= 1
            if nested<0:
                raise ValueError("Mismatched brackets when trying to parse blocks.")

        block_list.append(create_single_block_dict(current_lines))

    return block_list