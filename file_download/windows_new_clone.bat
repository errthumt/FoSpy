@echo off

cd /d %USERPROFILE%

git clone https://github.com/errthumt/FoSpy.git FoSpy

cd FoSpy
git switch dev

python -m venv venv
call venv\Scripts\activate.bat
pip install --upgrade build twine
pip install -e .
