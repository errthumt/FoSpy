@echo off
cd /d "%~dp0user_files"
call %~dp0FoSpy\venv\Scripts\activate
fos-dev-test