import os
import shutil
import traceback
from datetime import datetime
from tkinter import Tk, filedialog

from .. import Synthesis
from ._utils import file_prompt


def run(filepath=None):
    print(filepath)
    if filepath is None:
        print("No file selected.")
        filepath = file_prompt()

    # --- Build output directory ---
    filename = os.path.splitext(os.path.basename(filepath))[0]
    extension = os.path.splitext(filepath)[1]
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    outdir = os.path.join("user_files","testing", f"{filename}_{timestamp}")
    outdir = os.path.abspath(outdir)
    os.makedirs(outdir, exist_ok=True)

    original_copy = os.path.join(outdir, f"{filename}_original{extension}")
    fos_out = os.path.join(outdir, f"{filename}_saved.fos")
    json_out = os.path.join(outdir, f"{filename}_saved.json")
    error_log = os.path.join(outdir, "error_log.txt")

    # --- Copy original file BEFORE loading ---
    shutil.copy2(filepath, original_copy)

    # --- Processing ---
    try:
        my_synthesis = Synthesis.fromFile(filepath)
        my_synthesis.save(fos_out)
        my_synthesis.save(json_out)

        print("Processing complete.")
        print(f"Original copied to: {original_copy}")
        print(f"Saved: {fos_out}")
        print(f"Saved: {json_out}")

    except Exception:
        with open(error_log, "w", encoding="utf-8") as f:
            f.write(traceback.format_exc())
        print(f"An error occurred. See log:\n  {error_log}")