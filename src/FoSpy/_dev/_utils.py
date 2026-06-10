from tkinter import Tk, filedialog

import os, platform, subprocess

def file_prompt(title="Select an input file", filetypes=[("FOS files", "*.fos"), ("JSON files", "*.json"), ("All files", "*.*")]):
    root = Tk()
    root.withdraw()  # hide root window
    filepath = filedialog.askopenfilename(
        title=title,
        filetypes=filetypes
    )
    if not filepath:
        raise Exception("No file selected.")
    return filepath

def open_file(path):
    system = platform.system()
    if system == "Windows":
        os.startfile(path)
    elif system == "Darwin":
        subprocess.call(["open", path])
    else:
        subprocess.call(["xdg-open", path])
