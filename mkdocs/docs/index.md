# FoSpy
An API for opening, editing, and saving Files of Synthesis (*.fos)

## GitHub
[FoSpy @ errthumt](https://www.github.com/errthumt/FoSpy)

## Survey: Try Making Your Own FOS

We are looking for as much input as possible from other scientists about what types of information should be in the FOS format. Create your own file of synthesis that precisely describes your synthetic approach to a material. *Don't worry about strict syntax guidelines or how long it might take to make these files in bulk* (GUI and LLM automation are right around the corner). Only worry about capturing all the relevant information so that we can make sure our format standards will work for you.

1. Check out some [example synthesis files](./examples/synthesis/index.md)
2. Download [the empty FOS File](mkdocs/docs/file_download/empty_fos.txt)
3. Add details about your synthesis
   1. Edit and save the file as a `.txt` file to skip security filters.
4. Attach the file to a [Github Issue](https://www.github.com/errthumt/FoSpy/issues/new) or email to [errthumt@iastate.edu](mailto:errthumt@iastate.edu)


## Grammar Extension for IDE
[VSCode Grammar Extension for FOS Files](https://github.com/errthumt/fos-grammar)

## Proof of Concept: CyFoS-alpha
There is a fully-packaged app as a proof-of-concept with a gui for opening and editing FOS files.
* [Github](https://www.github.com/errthumt/CyFoS-alpha)
* [Installer download](https://github.com/errthumt/CyFoS-alpha/raw/refs/heads/main/installer/windows_release/CyFoS_Setup_1.2.5.exe)


## For Devs

### Setting Up A Dev Environment
Windows batch script for setting up a dev environment: [windows_new_clone.bat](./windows_new_clone.bat)(requires python and git installed)
* Clones the repo under C:\users\your-username\FoSpy
* Creates virtual python environment under ...\FoSpy\venv
* Installs the current FoSpy package as a live editable package to your venv.
