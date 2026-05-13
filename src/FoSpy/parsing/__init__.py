import os
from pprint import pprint

from .._debug import Debug
_debug = Debug()

from . import syntax as st
from .syntax import meta_keys as mk


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

            if txt.startswith("[") and txt.endswith("]") and txt != "[]":
                if txt.startswith("[["):
                    current_type = "list"
                else:
                    current_type = "single"

                current_block = txt.strip("[]")
                comments[current_block] = endComments
                endComments = []
                continue

            if txt.startswith(st.line_comment):
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
        if line.startswith(st.line_comment):
            if nested > 0:
                nested_lines.append(line)
            else:
                comments.append(line)
        elif nested==0:
            split = line.split(st.key_delimiter)
            key, val = split[0], st.key_delimiter.join(split[1:]).strip()
            # _debug.msg(f"processed: key:'{key}', val:'{val}'")
            if key in out_dict:
                raise ValueError(f"Duplicate key found: '{key}' Each key can only appear once within a block.")
            
            if val in ("[]","[[]]"):
                out_dict[key] = []
                out_dict[mk["comments"]][key]=comments
                comments = []
            
            elif val.startswith("["):
                # _debug.msg(f'{key} is nested')
                nested += 1
                nested_key = key
                out_dict[mk["comments"]][nested_key] = comments
                comments = []
                if val.startswith("[["):
                    nested_type = "list"
                    nested += 1
                else:
                    nested_type = "single"
                val = val.lstrip("[")
                if len(val) > 0:
                    nested_lines.append(val)
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

    if lines[0].startswith(st.key_delimiter):
        getting_keys = True
        comments = []
        key_comments = {}

        key_idx = 0
        for line in lines:
            # _debug.msg(f'processing list line: {line}')

            if getting_keys and line.startswith(st.line_comment):
                comments.append(line)
            elif nested>0 or line.startswith(st.line_comment):
                current_lines.append(line)
            elif line.startswith(st.key_delimiter):
                key = line[1:]
                if key in keys:
                    raise ValueError(f"Duplicate key found: '{key}'. Each key can only be specified once at the beginning of a looped list block.")
                key_comments[key] = comments
                comments = []
                keys.append(key)
                # _debug.msg(f'added key: {key}')
            
            elif st.key_delimiter in line:
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
                        if l.startswith(st.line_comment):
                            trailing_comments.append(l)
                        else:
                            break
                    
                    trailing_comments.reverse()
                    current_lines = trailing_comments
                    key_idx = 0

                key = keys[key_idx]
                current_lines.append(f'{key}:{line}')
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
            key = line.split(st.key_delimiter)[0].strip()
            if nested > 0:
                current_lines.append(line)
            elif key in keys:
                block_list.append(create_single_block_dict(current_lines))
                trailing_comments = []
                for l in reversed(current_lines):
                    if l.startswith(st.line_comment):
                        trailing_comments.append(l)
                    else:
                        break
                
                trailing_comments.reverse()
                current_lines = [*trailing_comments, line]
                keys = []
            else:
                keys.append(key)
                current_lines.append(line)

            if "[" in line:
                    nested += 1
            if "]" in line:
                nested -= 1
            if nested<0:
                raise ValueError("Mismatched brackets when trying to parse blocks.")

        block_list.append(create_single_block_dict(current_lines))

    return block_list

def block_list_to_lines(blocklist:list, indent=0):
    lines = []
    intersect = set.intersection(*(set(d.keys()) for d in blocklist))
    loop_keys = [k for k in blocklist[0] if k in intersect]

    for meta_key in mk.values():
        if meta_key in loop_keys:
            loop_keys.remove(meta_key)

    typ = blocklist[0][mk["list_type"]]
    for block in blocklist[1:]:
        new_typ = block[mk["list_type"]]
        if new_typ != typ:
            raise ValueError(f"All blocks in a multi-block section must have the same {mk["list_type"]}, either 'explicit' or 'looped'.")
        
    if typ == "looped":
        key_comments = {}
        for key in loop_keys:
            key_comments[key] = []

        for block in blocklist:
            comments = block.get(mk["key_comments"])
            if not comments: continue
            for key in loop_keys:
                for comment in comments[key]:
                    key_comments[key].append(comment)

        for key in loop_keys:
            for comment in key_comments[key]:
                lines.append(f"{indent*st.indent}{comment}")
            lines.append(f"{indent*st.indent}{st.key_delimiter}{key}")
        lines.append("")

    for block in blocklist: 
        for line in block_to_lines(block, indent=indent+1 if typ=="looped" else indent, loop_keys=loop_keys):
            lines.append(line)

    return lines
    

def block_to_lines(block, indent=0, loop_keys=[]):
    block = block.copy()
    typ = block.pop(mk["list_type"])
    comments = block.pop(mk["comments"])
    key_comments = block.pop(mk["key_comments"], None)
    lines = []

    if typ == "explicit":
        for key, val in block.items():
            key_comments = comments.get(key)
            if key_comments:
                for comment in key_comments:
                    lines.append(f"{indent*st.indent}{comment}")
            
            for line in expand_lists(key, val, indent):
                lines.append(line)
    elif typ == "looped":
        for key in loop_keys:
            val = block.pop(key)
            key_comments = comments.get(key)
            if key_comments:
                for comment in key_comments:
                    lines.append(f"{indent*st.indent}{comment}")
            for line in expand_lists(key, val, indent, looped=True):
                lines.append(line)
        for key,val in block.items():
            key_comments = comments.get(key)
            if key_comments:
                for comment in key_comments:
                    lines.append(f"{indent*st.indent}{comment}")
            for line in expand_lists(key, val, indent, looped=False):
                lines.append(line)
    else:
        raise ValueError(f"Unexpected list type: '{typ}'. Expected 'explicit' or 'looped'.")
    
    lines.append("")
    
    return lines

def expand_lists(key, val, indent, looped=False):
    lines = []
    if type(val) == list:
        if len(val) == 0:
            lines.append(f'{indent*st.indent}{f"{key}{st.key_delimiter} " if not looped else ""}[]')
        else:
            bracket_num = 1 if len(val) == 1 else 2
            lines.append(f'{indent*st.indent}{f"{key}{st.key_delimiter} " if not looped else ""}{"["*bracket_num}')
            for line in block_list_to_lines(val, indent=indent):
                lines.append(line)
            lines.pop()
            lines.append(f"{indent*st.indent}{"]"*bracket_num}")
    else:
        lines.append(f'{indent*st.indent}{f"{key}{st.key_delimiter} " if not looped else ""}{val}')

    return lines



def write_dict_to_file(blocks, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    blocks = blocks.copy()
    block_comments = blocks.pop(mk["comments"])

    with open(filepath, "w") as f:
        for name, blocklist in blocks.items():
            if name != "metadata":
                comments = block_comments[name]
                for comment in comments:
                    f.write(f'{comment}\n')
                if len(blocklist) > 1:
                    f.write(f'[[{name}]]\n')
                else:
                    f.write(f'[{name}]\n')           
            
            for line in block_list_to_lines(blocklist):
                f.write(f'{line}\n')
