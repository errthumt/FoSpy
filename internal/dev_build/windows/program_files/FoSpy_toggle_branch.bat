@echo off
setlocal enabledelayedexpansion

REM --- Navigate to repo ---
cd /d "%~dp0FoSpy"

REM --- Detect current branch ---
for /f "usebackq delims=" %%b in (`git rev-parse --abbrev-ref HEAD`) do set "CURRENT_BRANCH=%%b"


echo Current branch: %CURRENT_BRANCH%
echo.

REM --- Determine target branch ---
if /i "%CURRENT_BRANCH%"=="main" (
    set TARGET_BRANCH=dev
) else (
    if /i "%CURRENT_BRANCH%"=="dev" (
        set TARGET_BRANCH=main
    ) else (
        echo You are on branch "%CURRENT_BRANCH%", which is not main or dev.
        echo Aborting to avoid accidental switching.
        pause
        exit /b 1
    )
)

echo Switching from %CURRENT_BRANCH% to %TARGET_BRANCH%
echo.

REM --- Confirm ---
choice /m "Proceed with branch toggle"
if errorlevel 2 (
    echo Aborted by user.
    exit /b 1
)

echo.
echo Restoring working directory...
git restore .

echo Switching branches...
git switch %TARGET_BRANCH%
if errorlevel 1 (
    echo Failed to switch branches.
    pause
    exit /b 1
)

echo Pulling latest changes...
git pull

echo.
echo Branch toggle complete.
pause
