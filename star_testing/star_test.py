import os
import starfile, json
from pathlib import Path

from dict2star.blocks import encode_blocks



TEST_ROOT = Path(__file__).parent

JSON_IN = TEST_ROOT / "start_synthesis.json"
STAR_OUT = TEST_ROOT / "test.star"

def dict_as_star(d:dict):
    out = {}
    if not isinstance(d, dict):
        return d
    for k,v in d.items():
        if isinstance(v, dict):
            out[k] = dict_as_star(v)
        elif isinstance(v, list):
            for i in range(len(v)):
                out[tuple([k])] = [[dict_as_star(obj)] for obj in v]
        else:
            out[k] = v
    return out

with open(JSON_IN, "r") as f:
    d = dict(json.load(f))



def dict_to_lines(d:dict):
    lines = []
    

#starfile.write(data=d, filename=STAR_OUT)

blocks = encode_blocks({"synthesis":d})

with open(STAR_OUT, "w") as f:
    f.write(blocks)