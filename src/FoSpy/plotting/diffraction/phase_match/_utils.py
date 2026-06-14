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
        "type": "scalar", "label": "Min Distance (samples)", "min": 1, "max": 200, "default": find_cfg["distance"]
    },
    "prominence": {
        "type": "range", "label": "Prominence", "min": 0, "max": 1, "default": find_cfg["prominence"]
    },
    "width": {
        "type": "range", "label": "Width (samples)", "min": 0, "max": 200, "default": find_cfg["width"]
    },
    "wlen": {
        "type": "scalar", "label": "Window Length", "min": 2, "max": len(intensity_col), "default": find_cfg["wlen"]
    },
    "rel_height": {
        "type": "scalar", "label": "Relative Height", "min": 0, "max": 1, "default": find_cfg["rel_height"]
    },
    "plateau_size": {
        "type": "range", "label": "Plateau Size", "min": 0, "max": 200, "default": find_cfg["plateau_size"]
    },
}
