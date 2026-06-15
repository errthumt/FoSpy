from ....config import values as full_cfg
from ....ui._utils import _round_spec


def assemble_sliders(specs, cfg_name, cfg):
    digits_default = full_cfg.get("slider_digits.default")
    digit_cfg = full_cfg.get(f"slider_digits.{cfg_name}")
    for name, spec in specs.items():
        if spec.get("int", False):
            digits = 0
        else:
            digits = digit_cfg.get(name, None) or digits_default
        spec["digits"] = digits

        spec["default"] = cfg.get(name)

        for key in ["min", "max", "default", "None"]:
            if key not in spec:
                continue
            spec[key] = _round_spec(spec[key], digits, key)
    return specs

def get_find_sliders(find_cfg, intensity_col):
    sliders = {
        "height": {
            "type": "range",
            "label": "Peak Height",
            "min": 0,
            "max": max(intensity_col),
        },
        "threshold": {
            "type": "range",
            "label": "Threshold",
            "min": 0,
            "max": 1
        },
        "distance": {
            "type": "scalar",
            "label": "Min Distance (samples)",
            "min": 1,
            "max": len(intensity_col),
            "int": True,
            "None": 1
        },
        "prominence": {
            "type": "range",
            "label": "Prominence",
            "min": 0,
            "max": max(intensity_col),
        },
        "width": {
            "type": "range",
            "label": "Width (samples)",
            "min": 0,
            "max": len(intensity_col),
            "int": True
        },
        "wlen": {
            "type": "scalar",
            "label": "Window Length",
            "min": 2,
            "max": len(intensity_col),
            "int": True,
            "None": len(intensity_col)
        },
        "rel_height": {
            "type": "scalar",
            "label": "Relative Height",
            "min": 0,
            "max": 1,
            "None": 1
        },
        "plateau_size": {
            "type": "range",
            "label": "Plateau Size",
            "min": 0,
            "max": len(intensity_col),
            "int": True
        }
    }

    sliders = assemble_sliders(sliders, "find_peaks", find_cfg)
    
    return sliders


def get_baseline_sliders(baseline_cfg):
    sliders = {
        "lam": {
            "type": "scalar",
            "label": "Logarithmic Lambda",
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