def get_find_sliders(find_cfg, intensity_col):
    return {
    "height": {
        "type": "range", "label": "Peak Height", "min": 0, "max": 1, "default": find_cfg["height"]
    },
    "threshold": {
        "type": "range", "label": "Threshold", "min": 0, "max": 1, "default": find_cfg["threshold"]
    },
    "distance": {
        "type": "scalar", "label": "Min Distance (samples)", "min": 1, "max": 200, "default": find_cfg["distance"], "digits": 0
    },
    "prominence": {
        "type": "range", "label": "Prominence", "min": 0, "max": 1, "default": find_cfg["prominence"]
    },
    "width": {
        "type": "range", "label": "Width (samples)", "min": 0, "max": 200, "default": find_cfg["width"], "digits": 0
    },
    "wlen": {
        "type": "scalar", "label": "Window Length", "min": 2, "max": len(intensity_col), "default": find_cfg["wlen"], "digits": 0
    },
    "rel_height": {
        "type": "scalar", "label": "Relative Height", "min": 0, "max": 1, "default": find_cfg["rel_height"]
    },
    "plateau_size": {
        "type": "range", "label": "Plateau Size", "min": 0, "max": 200, "default": find_cfg["plateau_size"], "digits": 0
    },
}