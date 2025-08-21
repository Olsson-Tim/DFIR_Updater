@echo off
title DFIR Software Updater - Build Script
echo Building DFIR Software Updater executable...
echo ==========================================

REM Check if PyInstaller is installed
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
    if errorlevel 1 (
        echo Failed to install PyInstaller
        pause
        exit /b 1
    )
)

REM Check if Pillow is installed
python -c "import PIL" >nul 2>&1
if errorlevel 1 (
    echo Pillow not found. Installing...
    pip install pillow
    if errorlevel 1 (
        echo Failed to install Pillow
        pause
        exit /b 1
    )
)

REM Create the icon if it doesn't exist
if not exist "assets\icon.ico" (
    echo Creating application icon...
    python scripts/create_icon.py
    if errorlevel 1 (
        echo Failed to create icon
        pause
        exit /b 1
    )
)

REM Create the executable with all necessary files
echo.
echo Building executable...
pyinstaller --noconfirm --onedir --windowed ^
    --hidden-import=customtkinter ^
    --add-data "programs.json;." ^
    --add-data "programs_template.json;." ^
    --add-data "assets;assets" ^
    --icon "assets/icon.ico" ^
    --name "DFIR_Software_Updater" ^
    src/main.py

if errorlevel 1 (
    echo.
    echo Build failed!
    pause
    exit /b 1
)

REM Copy necessary files to the distribution directory
echo.
echo Copying additional files to distribution directory...
copy /Y "programs.json" "dist\DFIR_Software_Updater\"
copy /Y "programs_template.json" "dist\DFIR_Software_Updater\"

echo.
echo Build complete!
echo.
echo To run the application:
echo 1. Run 'run_packaged.bat'
echo 2. Or navigate to 'dist\DFIR_Software_Updater' and run 'DFIR_Software_Updater.exe'
echo.
echo Note: Make sure the 'assets' folder and 'programs.json' file are in the same directory as the executable
pause