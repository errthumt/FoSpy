import os

from . import syntax as snt
from .syntax import meta_keys as mk

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
                lines.append(f"{indent*snt.indent}{snt.line_comment} {comment}")
            lines.append(f"{indent*snt.indent}{snt.key_delimiter}{key}")
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
                    lines.append(f"{indent*snt.indent}{snt.line_comment} {comment}")
            
            for line in expand_lists(key, val, indent):
                lines.append(line)
    elif typ == "looped":
        for key in loop_keys:
            val = block.pop(key)
            key_comments = comments.get(key)
            if key_comments:
                for comment in key_comments:
                    lines.append(f"{indent*snt.indent}{snt.line_comment} {comment}")
            for line in expand_lists(key, val, indent, looped=True):
                lines.append(line)
        for key,val in block.items():
            key_comments = comments.get(key)
            if key_comments:
                for comment in key_comments:
                    lines.append(f"{indent*snt.indent}{snt.line_comment} {comment}")
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
            lines.append(f'{indent*snt.indent}{f"{key}{snt.key_delimiter} " if not looped else ""}[]')
        else:
            bracket_num = 1 if len(val) == 1 else 2
            lines.append(f'{indent*snt.indent}{f"{key}{snt.key_delimiter} " if not looped else ""}{"["*bracket_num}')
            for line in block_list_to_lines(val, indent=indent):
                lines.append(line)
            lines.pop()
            lines.append(f"{indent*snt.indent}{"]"*bracket_num}")
    else:
        lines.append(f'{indent*snt.indent}{f"{key}{snt.key_delimiter} " if not looped else ""}{val}')

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
                    f.write(f'{snt.line_comment} {comment}\n')
                if len(blocklist) > 1:
                    f.write(f'[[{name.capitalize()}]]\n')
                else:
                    f.write(f'[{name.capitalize()}]\n')           
            
            for line in block_list_to_lines(blocklist):
                f.write(f'{line}\n')
