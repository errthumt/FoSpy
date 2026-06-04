import os
import starfile, json
from pathlib import Path

TEST_ROOT = Path(__file__).parent

JSON_IN = TEST_ROOT / "start_synthesis.json"
STAR_OUT = TEST_ROOT / "test.star"

def dict_as_star(d:dict):
    out = {}
    for k,v in d.items():
        if isinstance(v, dict):
            out[k] = dict_as_star(v)
        elif isinstance(v, list):
            for i in range(len(v)):
                out[f"{k}_{i}"] = dict_as_star(v[i])
        else:
            out[k] = v
    return out

with open(JSON_IN, "r") as f:
    d = dict(json.load(f))

d = dict_as_star(d)

starfile.write(data=d, filename=STAR_OUT)