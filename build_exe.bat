@echo off
title Building Samsung Galaxy Tab S9 FE Debloater Portable EXE
echo ========================================================
echo  Samsung Galaxy Tab S9 FE Debloater - Executable Builder
echo ========================================================
echo.

echo [1/3] Ensuring PyInstaller is installed...
python -m pip install --upgrade pyinstaller

echo.
echo [2/3] Compiling standalone Windows executable...
pyinstaller --noconfirm --onedir --windowed ^
    --name "Samsung-Tab-S9FE-Debloater" ^
    --add-data "presets.json;." ^
    --add-data "database.py;." ^
    --add-data "adb_manager.py;." ^
    --add-data "utils.py;." ^
    gui.py

echo.
echo [3/3] Bundling runtime dependencies and tools...
if exist "bin" xcopy /E /I /Y "bin" "dist\Samsung-Tab-S9FE-Debloater\bin"
if not exist "dist\Samsung-Tab-S9FE-Debloater\backups" mkdir "dist\Samsung-Tab-S9FE-Debloater\backups"

echo.
echo ========================================================
echo [SUCCESS] Portable build created at:
echo dist\Samsung-Tab-S9FE-Debloater\Samsung-Tab-S9FE-Debloater.exe
echo ========================================================
pause
