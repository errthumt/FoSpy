@echo off
cd /d "%~dp0user_files"
start "" "%~dp0FoSpy\venv\Scripts\python.exe" -i -c "fos-dev-test"