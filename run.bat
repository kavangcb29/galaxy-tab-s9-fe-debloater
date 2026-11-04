@echo off
title Samsung Galaxy Tab S9 FE Debloater Toolkit
cd /d "%~dp0"

echo ========================================================
echo       SAMSUNG GALAXY TAB S9 FE DEBLOATER TOOLKIT
echo ========================================================
echo.

where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed or not in your PATH.
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)

echo Launching Graphical User Interface (GUI)...
start "" python debloater.py --gui

exit /b 0
