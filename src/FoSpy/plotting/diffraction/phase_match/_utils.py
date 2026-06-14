def rows_to_2th(two_theta, row_structure):
    if isinstance(row_structure, int):
        return two_theta[row_structure]
    
    if isinstance(row_structure, dict):
        return {k: rows_to_2th(two_theta, v) for k, v in row_structure.items()}
    
    if isinstance(row_structure, list):
        return [rows_to_2th(two_theta, v) for v in row_structure]
    
    if isinstance(row_structure, tuple):
        return tuple(rows_to_2th(two_theta, v) for v in row_structure)
    
    return row_structure

def plot_rows_as_sticks(df, row_indices, intensity_col, ax=None, **vline_kwargs):
    # Create an axis if one wasn't provided
    if ax is None:
        import matplotlib.pyplot as plt
        ax = plt.gca()

    xs = [df.index[i] for i in row_indices]
    col = df[intensity_col]
    ys = [col.iloc[i] for i in row_indices]

    ax.vlines(xs, 0, ys, **vline_kwargs)
    return ax

def plot_stick_at_x(x, x_array, y_array, ax=None, **vline_kwargs):
    import numpy as np
    # Create an axis if one wasn't provided
    if ax is None:
        import matplotlib.pyplot as plt
        ax = plt.gca()

    idx = np.searchsorted(x_array, x)
    idx = np.clip(idx, 1, len(x_array)-1)

    left = idx -1
    right = idx
    choose_right = (x - x_array[left]) > (x_array[right] - x)

    nearest = np.where(choose_right, right, left)
    
    y = y_array[nearest]

    line = ax.vlines(x, 0, y, **vline_kwargs)
    return line


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

from matplotlib.widgets import Slider, Button, CheckButtons

START_Y = 0.1
SLIDER_START_X = 0.70
PADDING = 0.01
CHECK_X      = SLIDER_START_X+PADDING
CHECK_W      = 0.03
SLIDER_X     = CHECK_X + CHECK_W + PADDING
SLIDER_W     = 1.0 - SLIDER_X - PADDING
LABEL_LSHIFT = (CHECK_W + 2*PADDING) / SLIDER_W
ROW_H        = 0.03
ROW_SPACING  = 0.05
OK_BTN_CENTER= 0.85
OK_BTN_W     = 0.20
OK_BTN_H     = 0.05
OK_BTN_X     = OK_BTN_CENTER - OK_BTN_W/2

def new_slider(label, fig, spec, ypos, min_val, max_val, default, typ):
    ax_check = fig.add_axes([CHECK_X, ypos, CHECK_W, ROW_H])
    check = CheckButtons(ax_check, [""], default is not None)

    ax_slider = fig.add_axes([SLIDER_X, ypos, SLIDER_W, ROW_H])
    slider = Slider(ax_slider, label, min_val, max_val, valinit=max_val)

    text_width = slider.valtext.get_window_extent().width
    fig_width = fig.get_window_extent().width
    text_width = text_width / fig_width

    slider.ax.set_position([SLIDER_X, ypos, SLIDER_W-text_width, ROW_H])

    if default is not None:
        slider.set_val(default)
    elif typ in ("min", "scalar"):
        slider.set_val(min_val)
    else:
        slider.set_val(max_val)

    return slider, check


