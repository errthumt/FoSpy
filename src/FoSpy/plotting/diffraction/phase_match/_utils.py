from ....config import values as cfg
from ...._debug import Debug

from scipy.signal import find_peaks
_debug = Debug()

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

def convert_baseline_cfg(baseline_cfg):
    out = baseline_cfg.copy()

    out['lam'] = 10**out['lam']

    for int_cfg in ("max_iter", "diff_order"):
        out[int_cfg] = int(out[int_cfg])

    return out

# def plot_rows_as_sticks(df, row_indices, intensity_col, ax=None, **vline_kwargs):
#     # Create an axis if one wasn't provided
#     if ax is None:
#         import matplotlib.pyplot as plt
#         ax = plt.gca()

#     xs = [df.index[i] for i in row_indices]
#     col = df[intensity_col]
#     ys = [col.iloc[i] for i in row_indices]

#     ax.vlines(xs, 0, ys, **vline_kwargs)
#     return ax

# def plot_stick_at_x(x, x_array, y_array, ax=None, **vline_kwargs):
#     import numpy as np
#     # Create an axis if one wasn't provided
#     if ax is None:
#         import matplotlib.pyplot as plt
#         ax = plt.gca()

#     idx = np.searchsorted(x_array, x)
#     idx = np.clip(idx, 1, len(x_array)-1)

#     left = idx -1
#     right = idx
#     choose_right = (x - x_array[left]) > (x_array[right] - x)

#     nearest = np.where(choose_right, right, left)
    
#     y = y_array[nearest]

#     line = ax.vlines(x, 0, y, **vline_kwargs)
#     return line


def check_for_interactive(interactive, kw):
    if isinstance(interactive, bool):
        return interactive
    elif isinstance(interactive, str):
        return interactive == kw
    elif isinstance(interactive, list):
        return kw in interactive


def unpack_peaks(data,*props, unwrap=True, **peak_parameters):
    _debug.msg("Peak Parameters")
    _debug.pmsg(peak_parameters)
    if isinstance(data, tuple):
        x_list, properties = data
    else:
        x_list, properties = find_peaks(data, **peak_parameters)

    out = [x_list]
    for prop in props:
        out.append(properties[prop])

    return out[0] if unwrap and len(out) == 1 else out


def match_peaks(exp_data, sim_peaks, match_width:float=None):
    if match_width is None:
        match_width = cfg.get("diffraction.match_peaks.match_width")

    exp, widths = unpack_peaks(exp_data, "widths")
    sim = sim_peaks

    l_bases = [x - (width * match_width/2) for x, width in zip(exp, widths)]
    r_bases = [x + (width * match_width/2) for x, width in zip(exp, widths)]

    matches = []
    found = []
    missing = []
    for exp_x, l_base, r_base in zip(exp, l_bases, r_bases):
        exp_x = int(exp_x)
        l_base = int(l_base)
        r_base = int(r_base)
        matches.append((exp_x, {}))
        for sim_x in sim:
            sim_x = int(sim_x)
            if sim_x < l_base:
                if sim_x not in found and sim_x not in missing:
                    missing.append(sim_x)
                continue
            elif sim_x > r_base:
                if exp_x == exp[-1]:
                    missing.append(sim_x)
                else:
                    break

            if l_base <= sim_x <= r_base:
                delta = abs(exp_x - sim_x)

                if len(matches) > 1 and sim_x in matches[-2][1]:
                    old_delta = matches[-2][1][sim_x]
                    if delta < old_delta:
                        matches[-2][1].pop(sim_x)
                    else:
                        continue

                matches[-1][1][sim_x] = delta
                if sim_x not in found:
                    found.append(sim_x)
    matches = tuple(
        (exp_x, tuple(matched.keys()))
        for exp_x, matched in matches
    )
    return {"matches": matches, "missing": missing}



