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
    

if __name__ == "__main__":
    from pprint import pp
    from FoSpy import *
    pp(debug_status())




