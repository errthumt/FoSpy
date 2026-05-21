import os

from .._debug import Debug
_debug = Debug()

from . import syntax as snt
from .syntax import meta_keys as mk
from .format import *

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
        
        template_keys = []
        for key in loop_keys:
            for comment in key_comments[key]:
                lines.append(format_comment(comment,indent))

            #scan for template fields

            for block in blocklist:
                val = block.get(key, None)
                if val == format_field("template"):
                    template_keys.append(key)
                    key = f"-{key}"
            lines.append(format_loop_key(key,indent))

        # all blocks in a list block must have the same template fields.
        for temp_key in template_keys:
            for block in blocklist:
                block[temp_key] = format_field("template")

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
    for remaining_key in mk.values():
        block.pop(remaining_key, None)
    lines = []

    if typ == "explicit":
        for key, val in block.items():
            key_comments = comments.get(key)
            if key_comments:
                for comment in key_comments:
                    lines.append(format_comment(comment, indent))
            for line in expand_lists(key, val, indent):
                lines.append(line)
    elif typ == "looped":
        for key in loop_keys:
            val = block.pop(key)
            key_comments = comments.get(key)
            if key_comments:
                for comment in key_comments:
                    lines.append(format_comment(comment, indent))
            for line in expand_lists(key, val, indent, looped=True):
                lines.append(line)
        for key,val in block.items():
            key_comments = comments.get(key)
            if key_comments:
                for comment in key_comments:
                    lines.append(format_comment(comment, indent))
            for line in expand_lists(key, val, indent, looped=False):
                lines.append(line)
    else:
        raise ValueError(f"Unexpected list type: '{typ}'. Expected 'explicit' or 'looped'.")
    
    lines.append("")
    
    return lines

def expand_lists(key, val, indent, looped=False):
    lines = []
    key = f"-{key}" if val == format_field("template") else key

    if key == "embedded":
        lines.append(format_embed_start(key, indent, looped))
        for line in val:
            lines.append(line.rstrip())
        lines.append(f'{SYNTAX["embedded"]["prefix"]*20} {SYNTAX["embedded"]["close"]}')
    elif type(val) == list:
        if len(val) == 0:
            lines.append(format_key_value(key, empty_nested(False), indent, looped))
        else:
            lines.append(format_nested_start(key,len(val)>1, looped,indent))
            for line in block_list_to_lines(val, indent=indent+1):
                lines.append(line)
            lines.pop()
            lines.append(format_nested_end(len(val)>1,indent))
    elif type(val) == dict:
        return expand_lists(key, [val], indent, looped)
    else:
        lines.append(format_key_value(key, val, indent, looped))

    return lines



def write_dict_to_file(blocks, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    blocks = blocks.copy()
    block_comments = blocks.pop(mk["comments"])

    meta = [blocks.pop("metadata",{})]

    with open(filepath, "w") as f:
        for line in block_list_to_lines(meta):
            f.write(f'{line}\n')
        for name, block in blocks.items():
            if isinstance(block,dict):
                block = [block]
            if name in mk.values():
                continue
            if name != "metadata":
                comments = block_comments.get(name,[])
                for comment in comments:
                    f.write(f'{format_comment(comment)}\n')

                f.write(f'{format_block_header(name, "list" if len(block)>1 else "single")}\n')           
            
            for line in block_list_to_lines(block):
                f.write(f'{line}\n')
