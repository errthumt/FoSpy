# Setting Up a Dev Environment for FoSpy

This page is a guide on how to set up a python environment for in-progress testing of the FOS API. This can either be for code collaborators, or if you want the most recent changes in the package to be reflected whenever you are testing your FOS files.

## Easy Install for Windows

All of the steps below can be automated with the windows setup package [downloaded here](../file_download/fos_dev_setup_win.zip)

1. Extract the folder
2. Run full_setup.bat

## Required Software

There are only two required software to be installed before running this guide:

### Git
 
Git is the version-control system used by GitHub and many other hosts to track individual changes to files, manage multiple "branches" of the same project, and many other capabilities. With Git, you can synchronize your local install of the project with the full Github project at any time with a few simple commands. You can also easily switch between the development branch and the main branch just as easily.

- [Git Installer Downloads](https://git-scm.com/install/windows)

### Python

A stable runtime of Python \>= 3.10 is required for install. Since many scientists have off-market versions of python packaged with programs like GSAS-II or Anaconda, it is recommended to start with a fresh 3.14 runtime of Python using the new [Python install manager](https://www.python.org/downloads/release/pymanager-262/). The install manager also has commands for checking current installed runtimes.

It is also recommended to use a python virtual environment. This is a private instance of Python that you can install whatever packages you need to without cluttering the parent Python install.

## Usage After Setup

After following the instructions below, you can start any FoSpy editing session by activating the virtual environment and calling `python`, or by executing the python.exe created in your venv\Scripts folder. You usually want to start by importing whatever `FileBlock` you'll be creating.

Installing with the [easy install package](#easy-install-for-windows) should create some windows shortcuts to do this:

- Live Session: An interactive python session with `Synthesis` and `TemplateSet` already imported.
- Toggle Branch: Toggle between the stable "Main" branch and the "Dev" branch with staged features.
  - This is only for users who aren't editing branch files; it discards all your changes.
- Test Load: Attempt to read a synthesis file and either save a copy, or print the error log to a text file.

```cmd
C:\Users\travi>cd FOS_DEV\FoSpy
C:\Users\travi\FOS_DEV\FoSpy> venv\Scripts\activate
(venv) C:\Users\travi\FOS_DEV\FoSpy>python
Python 3.14.5 (tags/v3.14.5:5607950, May 10 2026, 10:43:50) [MSC v.1944 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
Ctrl click to launch VS Code Native REPL
>>> from FoSpy.blocks.synthesis import Synthesis
>>> my_synthesis = Synthesis.fromFile("my_synthesis.fos")
```

## Setup Instructions

### Start: Create or navigate to a safe directory for building your dev environment
The user directory is usually a good place to start (`$HOME` in Powershell, `%USERPROFILE%` in CMD)

```cmd
C:\>cd /d %USERPROFILE%
C:\Users\travi>mkdir FOS_DEV
C:\Users\travi>cd FOS_DEV
C:\Users\travi\FOS_DEV>
```

### Optional: Install a standalone python runtime using the install manager
This installs a separate runtime in FOS_DEV/python314, even if an existing 3.14 runtime is on your device

```cmd
C:\Users\travi\FOS_DEV> pymanager install 3.14 --target=python314
```

### Clone the GitHub repository
This downloads the full build directly from the GitHub and sets it up for version tracking.

```cmd
C:\Users\travi\FOS_DEV>git clone https://www.github.com/errthumt/fospy.git FoSpy
```

### Setup and activate Python Virtual Environment
Python virtual environments are contained within their own folder. Putting the folder inside the cloned repo folder is helpful so that you can put any extra files that the build is expecting inside the \venv folder, like access tokens for uploading to PyPI or pushing back to the repository.

**This repository is set up to "hide" files contained inside FoSpy\venv from being uploaded back to the GitHub. If you anticipate contributing to the project, make sure your environment is named placed at that location so you don't accidentally commit secret files back to the public site.**

I'm using my standalone python install here, but if your system default Python is stable, you can use the simple `python` command instead of `python314\python`

```cmd
C:\Users\travi\FOS_DEV>python314\python -m venv FoSpy\venv
C:\Users\travi\FOS_DEV>cd FoSpy
C:\Users\travi\FOS_DEV\FoSpy>venv\Scripts\activate
```


### Install FoSpy as an editable package
Installing with the `-e` tag means that any time the files are updated, the change is automatically reflected in your scripts.

```cmd
(venv) C:\Users\travi\FOS_DEV\FoSpy>pip install -e .
```
