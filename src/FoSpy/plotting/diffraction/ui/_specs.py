from ....config import values as full_cfg
from ....ui.sliders._utils import _round_spec
import numpy as np


def assemble_sliders(specs, cfg_name, cfg):
    # TODO: move to ui utils
    digits_default = full_cfg.get("slider_digits.default")
    digit_cfg = full_cfg.get(f"slider_digits.{cfg_name}")
    for name, spec in specs.items():
        if spec["type"] == "group":
            grp_specs = assemble_sliders(spec["specs"], cfg_name, cfg)
            spec["specs"] = grp_specs
            continue
        if spec.get("int", False):
            digits = 0
        else:
            digits = digit_cfg.get(name, None) or digits_default
        spec["digits"] = digits

        spec["default"] = cfg.get(name)

        for key in ["min", "max", "default", "None"]:
            if key not in spec:
                continue
            include = spec.get("include_"+key, True)
            spec[key] = _round_spec(spec[key], digits, key, include)
    return specs

def get_find_sliders(find_cfg, intensity_col):
    sliders = {
        "height_group": {
            "type": "group",
            "label": "Height Parameters",
            "specs": {
                "height": {
                    "type": "range",
                    "label": "Allowed Height (Y units)",
                    "min": 0,
                    "max": max(intensity_col),
                },
                "threshold": {
                    "type": "range",
                    "label": "Allowed Threshold (Y units)",
                    "min": 0,
                    "max": np.max(np.abs(np.diff(intensity_col))),
                },
                "prominence": {
                    "type": "range",
                    "label": "Allowed Prominence (Y units)",
                    "min": 0,
                    "max": max(intensity_col),
                },
            }
        },
        "width_group": {
            "type": "group",
            "label": "Width Parameters",
            "specs": {
                "distance": {
                    "type": "scalar",
                    "label": "Allowed Neighbor Distance (points)",
                    "min": 1,
                    "max": len(intensity_col),
                    "int": True,
                    "None": 1
                },
                "width": {
                    "type": "range",
                    "label": "Allowed Width (points)",
                    "min": 0,
                    "max": len(intensity_col),
                    "int": True
                },
                "wlen": {
                    "type": "scalar",
                    "label": "Window Length (points)",
                    "min": 2,
                    "max": len(intensity_col),
                    "int": True,
                    "None": len(intensity_col)
                },
                "rel_height": {
                    "type": "scalar",
                    "label": "Width @ Height (Height-Relative, top-down)",
                    "include_min": False,
                    "min": 0,
                    "max": 1,
                    "None": 1
                },
                "plateau_size": {
                    "type": "range",
                    "label": "Plateau Size (points)",
                    "min": 0,
                    "max": len(intensity_col),
                    "int": True
                } 
            }
        } 
    }

    sliders = assemble_sliders(sliders, "find_peaks", find_cfg)
    
    return sliders


def get_baseline_sliders(baseline_cfg):
    sliders = {
        "lam": {
            "type": "scalar",
            "label": "Baseline Smoothing",
            "min": 0,
            "max": 10
        },
        "diff_order": {
            "type": "scalar",
            "label": "Differential Order",
            "min": 1,
            "max": 3,
            "int": True
        },
        "max_iter": {
            "type": "scalar",
            "label": "Maximum Iterations",
            "min": 1,
            "max": 100,
            "int": True
        },
        "tol": {
            "type": "scalar",
            "label": "Tolerance",
            "min": 0,
            "max": 1
        }
    }

    sliders = assemble_sliders(sliders, "baseline", baseline_cfg)
    return sliders

