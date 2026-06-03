@echo off
cd /d "%~dp0user_files"
start "" "%~dp0FoSpy\venv\Scripts\python.exe" -i -c "from FoSpy.blocks.synthesis import Synthesis; from FoSpy.blocks.template import TemplateSet"