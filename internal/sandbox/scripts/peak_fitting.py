from numpy import loadtxt
from scipy.signal import find_peaks
import os
from pathlib import Path
from pprint import pp
import Dans_Diffraction as ddf
from cif2xrd.pattern import simPattern
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.colors import TABLEAU_COLORS as colors

SANDBOX = Path(os.path.dirname(os.path.realpath(__file__))) / ".."
EXP_DATA = SANDBOX / "assets/As_experimental.xy"
CIF = SANDBOX / "assets/As.cif"

SCATTER_SETUP = {
    'scattering_type':'xray',
    'min_twotheta':3.0,
    'max_twotheta':90.0,
    'wavelength_a':1.5406,
    'powder_lorentz':0.5
}

def main(patterns):
    # compare = compare_peaks(
    #     ("experimental",EXP_DATA, get_xy_pattern),
    #     ("dans-diffraction",CIF, get_ddf_pattern),
    #     ("cif2xrd",CIF, get_cif2xrd_pattern),
    #     normalize=True, prominence=0.01,
    #     rel_height=1.0,
    #     width=0.01,round_to=2)
    # pp(compare)

    # for name, (peak_list, properties, df) in compare.items():
    #     fig, ax = plt.subplots()
    #     df.plot(title=name, x="two_theta", y="intensity", ax=ax)

    # plt.show()

    frames = {
        name: setup["get_pattern"](setup["filepath"])
        for name, setup in patterns.items()
    }

    merged = merge_frames("two_theta", **frames)



    matches = match_peaks(merged["intensity_experimental"], merged["intensity_dans-diffraction"], prominence=0.01)

    fig, ax = plt.subplots()
    merged.plot(y="intensity_experimental", ax=ax)
    color = next_color()
    for exp_peak, matching in matches["matches"]:

        plot_rows_as_sticks(merged, matching, "intensity_dans-diffraction", ax=ax, colors=next(color), linewidth=1)

    plt.show()
    pass

def next_color():
    while True:
        yield 'r'
        yield 'g'
        yield 'b'

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

def merge_frames(x_name="two_theta",normalize=True,**frames:pd.DataFrame):
    # frames = {name1: frame1, name2: frame2}
    # assume all non x_name columns are "y" columns, but column names are unknown and not necessarily shared
    # output: df with columns x_name, name1_y1, name1_y2, name2_y1, name2_y2
    
    x_cols = [df[x_name] for df in frames.values()]
    x_min = max(min(x) for x in x_cols)
    x_max = min(max(x) for x in x_cols)
    x_step = max(np.mean(np.diff(x)) for x in x_cols)

    x_common = np.arange(x_min, x_max, x_step)
    base = pd.DataFrame({x_name:x_common})
    out = base.copy()
    for name, df in frames.items():
        merged = pd.merge(base, df, how="outer", on=x_name)
        merged = (merged
            .set_index(x_name)
            .interpolate(method="linear")
            .reindex(base[x_name])
            .reset_index()
        )
        for col in merged.columns:
            if col != x_name:
                out[f"{col}_{name}"] = merged[col]
    out.set_index(x_name, inplace=True)

    if normalize:
        out /= out.max()

    return out

def unpack_peaks(data,*props, unwrap=True, **kwargs):
    if isinstance(data, tuple):
        x_list, properties = data
    else:
        x_list, properties = find_peaks(data, **kwargs)

    out = [x_list]
    for prop in props:
        out.append(properties[prop])

    return out[0] if unwrap and len(out) == 1 else out


def match_peaks(exp_data, sim_data, **kwargs):
    kwargs.setdefault("prominence", (None, None))
    kwargs.setdefault("width", (None, None))

    exp, l_bases, r_bases = unpack_peaks(exp_data, "left_bases", "right_bases", **kwargs)
    sim = unpack_peaks(sim_data, **kwargs)
    

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

    



def get_xy_pattern(filepath):
    two_theta, intensity = loadtxt(filepath, unpack=True)
    return pd.DataFrame({'two_theta':two_theta, 'intensity':intensity})

def get_cif2xrd_pattern(filepath):
    sim = simPattern(filepath)
    return pd.DataFrame({'two_theta':sim.two_theta, 'intensity':sim.intensity})

def get_ddf_pattern(filepath):
    xtl = ddf.Crystal(filepath)
    xtl.Scatter.setup_scatter(**SCATTER_SETUP)
    two_theta, intensity, reflections = xtl.Scatter.powder()
    return pd.DataFrame({'two_theta':two_theta, 'intensity':intensity})

if __name__ == '__main__':

    PATTERNS = {
        "experimental": {
            "filepath": EXP_DATA,
            "get_pattern": get_xy_pattern
        },
        "dans-diffraction": {
            "filepath": CIF,
            "get_pattern": get_ddf_pattern
        },
        "cif2xrd": {
            "filepath": CIF,
            "get_pattern": get_cif2xrd_pattern
        }
    }

    main(PATTERNS)

    pass