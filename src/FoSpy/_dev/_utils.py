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


def run_batch(path=None):
    if path is None or not os.path.exists(path):
        print("No batch file provided.")
        return

    if not platform.system() == "Windows":
        print("Only Windows is supported for batch file execution.")
        return
    # Ensure Windows uses cmd.exe to run the batch file
    subprocess.run([os.environ["COMSPEC"], "/c", path], shell=True)

import subprocess
import threading
import sys

def run_interactive_batch(path=None):
    if path is None or not os.path.exists(path):
        print("No batch file provided.")
        return

    if not platform.system() == "Windows":
        print("Only Windows is supported for batch file execution.")
        return
    # Start the batch file with pipes
    proc = subprocess.Popen(
        [path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    # Thread to stream output live
    def stream_output():
        for line in proc.stdout:
            print(line, end="")  # forward to Python CLI

    t = threading.Thread(target=stream_output, daemon=True)
    t.start()

    # Main loop: read user input and send to batch file
    try:
        while proc.poll() is None:
            user_input = input()
            proc.stdin.write(user_input + "\n")
            proc.stdin.flush()
    except KeyboardInterrupt:
        proc.terminate()


