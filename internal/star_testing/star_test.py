import os
import starfile, json
from pandas import DataFrame
from pathlib import Path

from dict2star.blocks import encode_blocks


TEST_ROOT = Path(__file__).parent

JSON_IN = TEST_ROOT / "start_synthesis.json"
STAR_OUT = TEST_ROOT / "test.star"

def dict_as_star(d:dict):
    if isinstance(d, dict):
        out = {}
        for k,v in d.items():
            if isinstance(v, list) and all(isinstance(x, dict) for x in v):
                for i in range(len(v)):
                    out[f"{k}_{i}"] = dict_as_star(v[i])
            else:
                out[k] = dict_as_star(v)
        return out
    elif isinstance(d, list):
        return DataFrame(d)
    else:
        return d

with open(JSON_IN, "r") as f:
    d = dict(json.load(f))

d = dict_as_star(d)

starfile.write(data=d, filename=STAR_OUT)
