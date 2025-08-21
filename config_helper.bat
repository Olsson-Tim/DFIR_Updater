@echo off
title DFIR Software Updater - Configuration Helper
echo DFIR Software Updater Configuration Helper
echo ========================================
echo.

if exist programs.json (
    echo programs.json already exists.
    echo Checking if it's valid...
    python -c "import json; f=open('programs.json'); json.load(f); f.close(); print('File is valid JSON')"
    if errorlevel 1 (
        echo.
        echo ERROR: programs.json is not valid JSON
        echo Please check the file format or delete it to recreate from template
    ) else (
        echo File is valid.
        echo You can edit programs.json to configure your software list
    )
) else (
    if exist programs_template.json (
        echo Creating programs.json from template...
        copy programs_template.json programs.json
        echo.
        echo Created programs.json
        echo Edit this file to configure your software list
    ) else (
        echo ERROR: programs_template.json not found
        echo Cannot create configuration file
    )
)

echo.
echo Configuration files:
dir programs*.json
echo.
pause