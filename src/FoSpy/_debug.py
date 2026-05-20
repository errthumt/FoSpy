from pprint import pprint
import sys
import inspect
import io

DEBUG_WIDTH = 120

class Debug:
    def __init__(self):
        self.on = False

        frame = inspect.currentframe().f_back
        self.module_name = frame.f_globals.get("__name__", "<unknown>")
        self.label = f"|(Debug message from {self.module_name})"
        self.label_width = len(self.label)

    def msg(self,msg):
        self.pmsg(str(msg))

    def pmsg(self,msg,**kwargs):
        if self.on:
            text_width = DEBUG_WIDTH - self.label_width

            buf = io.StringIO()
            pprint(msg,stream=buf, width=text_width,**kwargs)
            txt = buf.getvalue()
            for line in txt.splitlines():
                print(f'{line:<{text_width}}{self.label:>{self.label_width}}')

def _find_debugs():
    results = []
    for name, module in sys.modules.items():
        # Some entries in sys.modules are None (partially imported modules)
        if module is None:
            continue

        if hasattr(module, "_debug"):
            results.append((name, module._debug))
    return results

def debug_status():
    results = []
    for module, debug_obj in _find_debugs():
        if hasattr(debug_obj,"on"):
            results.append((module, 'ON' if debug_obj.on else "OFF"))
    return results


def all_debugs_on(soundoff=True):
    for module, debug_obj in _find_debugs():
        if hasattr(debug_obj,"on"):
            debug_obj.on = True
            if soundoff:
                debug_obj.msg("Turning Debug On")

def all_debugs_off(soundoff=True):
    all_debugs_on(soundoff=False)
    for module, debug_obj in _find_debugs():
        if hasattr(debug_obj,"on"):
            if soundoff:
                debug_obj.msg("Turning Debug Off")
            debug_obj.on = False         
    
def deep_diff(d1, d2, path=""):
    """
    Recursively diff two nested dict/list structures.
    Ignores:
      - calculated comments (strings starting with SYNTAX["calc_comment"]["prefix"])
      - whitespace-only differences in strings
      - empty _fos_comments entries
    """
    from .parsing.syntax import SYNTAX, meta_keys
    calc_prefix = SYNTAX["calc_comment"]["prefix"]
    diffs = []

    # -----------------------------
    # Helpers
    # -----------------------------

    def is_calc_comment(x):
        return isinstance(x, str) and x.strip().startswith(calc_prefix)

    def normalize_ws(x):
        """Normalize whitespace for comparison."""
        if isinstance(x, str):
            return x.strip()        # remove leading/trailing whitespace
        return x

    def is_ws_only_diff(a, b):
        """True if a and b differ only by whitespace."""
        if not isinstance(a, str) or not isinstance(b, str):
            return False
        return a.strip() == b.strip()

    def is_empty_comment_list(path, d1, d2):
        """
        Suppress differences like:
            /foo/_fos_comments/bar: missing in d1
        when both sides are empty or missing.
        """
        if meta_keys["comments"] not in path:
            return False

        # Missing on one side
        if d1 is None or d2 is None:
            return True

        # Both lists but empty
        if isinstance(d1, list) and isinstance(d2, list):
            return len(d1) == 0 and len(d2) == 0

        return False

    # -----------------------------
    # Case 1 — both dicts
    # -----------------------------
    if isinstance(d1, dict) and isinstance(d2, dict):

        # keys only in d1
        for k in d1.keys() - d2.keys():
            p = f"{path}/{k}"
            if not is_empty_comment_list(p, d1.get(k), None):
                diffs.append(f"{p}: missing in d2")

        # keys only in d2
        for k in d2.keys() - d1.keys():
            p = f"{path}/{k}"
            if not is_empty_comment_list(p, None, d2.get(k)):
                diffs.append(f"{p}: missing in d1")

        # keys in both
        for k in d1.keys() & d2.keys():
            diffs.extend(deep_diff(d1[k], d2[k], f"{path}/{k}"))

        return diffs

    # -----------------------------
    # Case 2 — both lists
    # -----------------------------
    if isinstance(d1, list) and isinstance(d2, list):
        # Filter out calculated comments
        f1 = [x for x in d1 if not is_calc_comment(x)]
        f2 = [x for x in d2 if not is_calc_comment(x)]

        # length mismatch
        if len(f1) != len(f2):
            diffs.append(f"{path}: list length {len(f1)} != {len(f2)}")
            min_len = min(len(f1), len(f2))
        else:
            min_len = len(f1)

        # compare element‑wise
        for i in range(min_len):
            diffs.extend(deep_diff(f1[i], f2[i], f"{path}[{i}]"))

        return diffs

    # -----------------------------
    # Case 3 — scalar mismatch
    # -----------------------------
    if d1 != d2:

        # Ignore calculated comments entirely
        if is_calc_comment(d1) or is_calc_comment(d2):
            return diffs

        # Ignore whitespace-only differences
        if is_ws_only_diff(d1, d2):
            return diffs

        # Compare normalized whitespace versions
        if normalize_ws(d1) == normalize_ws(d2):
            return diffs

        diffs.append(f"{path}: {d1!r} != {d2!r}")

    return diffs



if __name__ == "__main__":
    from pprint import pp
    from FoSpy import *
    pp(debug_status())




