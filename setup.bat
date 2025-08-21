@echo off
title DFIR Software Updater Setup
echo Installing required dependencies...
pip install -r requirements.txt
echo.
echo Setup complete!
echo.
echo To configure programs:
echo 1. Run 'config_helper.bat' to create/check programs.json
echo 2. Edit 'programs.json' to add/remove programs
echo 3. Ensure installer files exist at the specified paths
echo.
echo Run 'run_updater.bat' to start the application
pause