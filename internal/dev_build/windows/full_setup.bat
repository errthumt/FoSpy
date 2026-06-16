@echo off
setlocal

REM --- Ensure working directory is the batch file's directory ---
cd /d "%~dp0"

echo Creating user folder FoSpy_DEV_ENV...
set "TARGET_DIR=%USERPROFILE%\FoSpy_DEV_ENV"
if not exist "%TARGET_DIR%" (
    mkdir "%TARGET_DIR%"
)

echo Copying shortcut files...
xcopy /e /i /y "%~dp0program_files\*" "%TARGET_DIR%"

echo Creating Start Menu shortcuts...

REM --- Start Menu folder for this user ---
set "START_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs\FoSpy_DEV"

if not exist "%START_MENU%" (
    mkdir "%START_MENU%"
)

REM --- Shortcut: FoSpy Live ---
powershell -NoProfile -Command ^
  "$s=(New-Object -ComObject WScript.Shell).CreateShortcut('%START_MENU%\FoSpy - Live Session.lnk');" ^
  "$s.TargetPath='%TARGET_DIR%\FoSpy_live.bat';" ^
  "$s.WorkingDirectory='%TARGET_DIR%';" ^
  "$s.Save()"

REM --- Shortcut: Toggle Branch ---
powershell -NoProfile -Command ^
  "$s=(New-Object -ComObject WScript.Shell).CreateShortcut('%START_MENU%\FoSpy - Dev Testing.lnk');" ^
  "$s.TargetPath='%TARGET_DIR%\FoSpy_dev_test.bat';" ^
  "$s.WorkingDirectory='%TARGET_DIR%';" ^
  "$s.Save()"


echo Shortcuts created.


echo Checking for Git Installation...
where git >nul 2>&1
if %errorlevel%==0 (
    echo Git already installed.
) else (
    echo Git not found. Installing...
    start /wait "" installers\Git-2.54.0-64-bit.exe /SILENT /LOADINF=installers\git_options.ini
)

echo Checking for Python Install Manager...
where pymanager >nul 2>&1
if %errorlevel%==0 (
    echo Py Manager already installed.
) else (
    echo Py Manager no found. Installing...
    start /wait "" msiexec /i installers\python-manager-26.2.msi /passive /norestart
)

echo Switching to new user folder...
cd /d %TARGET_DIR%

echo Installing standalone Python3.14
pymanager install 3.14 --target=python314

echo Cloning FoSpy repo from GitHub
git clone https://www.github.com/errthumt/fospy.git/ FoSpy

echo Creating virtual Python environment....
python314\python -m venv FoSpy\venv

echo Installing FoSpy to virtual environment...
cd FoSpy
call venv\Scripts\activate
pip install --force-reinstall -e .[DEV-TEST]

git checkout main

echo Done.
