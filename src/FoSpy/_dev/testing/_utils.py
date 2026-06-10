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

# def run_interactive_batch(path=None):
#     if path is None or not os.path.exists(path):
#         print("No batch file provided.")
#         return

#     if not platform.system() == "Windows":
#         print("Only Windows is supported for batch file execution.")
#         return
#     # Start the batch file with pipes
#     proc = subprocess.Popen(
#         [path],
#         stdin=subprocess.PIPE,
#         stdout=subprocess.PIPE,
#         stderr=subprocess.STDOUT,
#         text=True,
#         bufsize=1
#     )

#     # Thread to stream output live
#     def stream_output():
#         for line in proc.stdout:
#             print(line, end="")  # forward to Python CLI

#     t = threading.Thread(target=stream_output, daemon=True)
#     t.start()

#     # Main loop: read user input and send to batch file
#     try:
#         while proc.poll() is None:
#             try:
#                 user_input = input()
#                 proc.stdin.write(user_input + "\n")
#             except OSError:
#                 raise KeyboardInterrupt
#     except KeyboardInterrupt:
#         proc.terminate()
    
import subprocess
import sys
import os
import msvcrt  # Windows-only for single-key input

from ...config import values as cfg

REPO_PATH = os.path.abspath(cfg.DEV.repo)

def run_git(*args):
    """Run a git command and stream output live."""
    cmd = ["git"] + list(args)
    proc = subprocess.Popen(
        cmd,
        cwd=REPO_PATH,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    for line in proc.stdout:
        print(line, end="")
    proc.wait()
    return proc.returncode


def get_current_branch():
    return subprocess.check_output(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=REPO_PATH,
        text=True
    ).strip()


def choice_prompt(message):
    """Replicates `choice /m` behavior: Y/N single keypress."""
    print(f"{message} [Y,N]? ", end="", flush=True)
    while True:
        ch = msvcrt.getch().decode("utf-8").lower()
        if ch in ("y", "n"):
            print(ch.upper())
            return ch == "y"


def toggle_branches():
    from ...config import values as cfg, save as cfg_save

    # Detect current branch
    current = get_current_branch()
    print(f"Current branch: {current}\n")

    # Determine target branch
    if current.lower() == "main":
        target = "dev"
    elif current.lower() == "dev":
        target = "main"
    else:
        print(f'You are on branch "{current}", which is not main or dev.')
        print("Aborting to avoid accidental switching.")
        input("Press any key to continue...")
        return True

    print(f"Switching from {current} to {target}\n")

    # Confirm
    if not choice_prompt("Proceed with branch toggle"):
        print("Aborted by user.")
        return True

    print("\nRestoring working directory...")
    run_git("restore", ".")

    print("Switching branches...")
    if run_git("switch", target) != 0:
        print("Failed to switch branches.")
        input("Press any key to continue...")
        return True

    print("Pulling latest changes...")
    run_git("pull")

    cfg.DEV.branch = target
    cfg_save(prompt=False)

    print("\nBranch toggle complete.")
    input("Press any key to continue...")

    return True

LOGO = """
        %@@@@@@@@.             .@@@@@@@@%                
     @@@@  @@@@@@@@@@@@@@@@@@@@@@@@@@@  @@@@             
     @@ @@@@%#######*@@@@@@@*#######%@@@@ @@             
      @@@%###########@=   :@############@@@              
       @%###########@@     @@############@               
       @@@########@@@       @@@########@@@               
         @@@@@@@@@@*         *@@@@@@@@@@                 
                                                         
               @                                         
               @                                         
     @         @           #                             
     @         @           @                             
     @         @           @                             
     @         @           @         %-                  
     @         @=     =   =@         @@                  
    @@         %@     @   @@    %@   @@    @             
 ::    :::::::    ::.   :    ::    :    ::   :::         
                                                         
 @@@@@@@@@          @@@@@@@@@+                           
 @@        @@@@@@@# @@         @@@@@@@@  @@   @@:        
 @@@@@@@#  @*    @+ @@@@@@@@@  @@    @@  @@   @@         
 @@        @*    @* -       @- @@    @@  @@   -@         
 @@        @@@@@@@  @@@@@@@@@  @@@@@@@@  @@@@@@@         
                               @@             *@         
                               @@        @@@@@@          
"""

PREAMBLE = """
----------------------------------------------
FoSpy Development Testing Suite
----------------------------------------------
"""

def print_logo():
    print(LOGO)
    print(PREAMBLE)


