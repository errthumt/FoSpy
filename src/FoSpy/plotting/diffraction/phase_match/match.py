from scipy.signal import find_peaks
import pandas as pd
import numpy as np

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

def merge_frames(x_name="two_theta",normalize=True,interpolate=True,**frames:pd.DataFrame):
    # frames = {name1: frame1, name2: frame2}
    # assume all non x_name columns are "y" columns, but column names are unknown and not necessarily shared
    # output: df with columns x_name, name1_y1, name1_y2, name2_y1, name2_y2
    
    x_cols = [df[x_name] for df in frames.values()]
    x_min = max(min(x) for x in x_cols)
    x_max = min(max(x) for x in x_cols)
    x_step = max(np.mean(np.diff(x)) for x in x_cols) if interpolate else np.mean(np.diff(x_cols[0]))

    x_common = np.arange(x_min, x_max, x_step)
    base = pd.DataFrame({x_name:x_common})
    out = base.copy()
    for i, (name, df) in enumerate(frames.items()):
        merged = pd.merge(base, df, how="outer", on=x_name)
        merged = merged.set_index(x_name)
        if interpolate or i == 0:
            merged = merged.interpolate(method="linear")

        merged = merged.reindex(base[x_name],method=None if interpolate else "nearest").reset_index()
        for col in merged.columns:
            if col != x_name:
                out[f"{col}_{name}"] = merged[col]
    out.set_index(x_name, inplace=True)

    if normalize:
        out /= out.max()

    return out