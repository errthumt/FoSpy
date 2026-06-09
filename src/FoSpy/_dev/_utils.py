from tkinter import Tk, filedialog

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