@echo off
title DFIR Software Updater
echo Starting DFIR Software Updater...
echo ================================
echo.

REM Check if the executable exists
if exist "dist\DFIR_Software_Updater\DFIR_Software_Updater.exe" (
    echo Launching the application...
    echo.
    cd dist\DFIR_Software_Updater
    "DFIR_Software_Updater.exe"
    cd ..\..
) else (
    echo ERROR: Application executable not found!
    echo Please run 'build.bat' to create the executable first.
    echo.
    pause
    exit /b 1
)