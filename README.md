# DFIR Software Updater

A Python GUI application for updating software on offline Windows workstations. This tool uses CustomTkinter for the interface and PowerShell to execute installers silently.

## Features

- Modern dark-themed GUI using CustomTkinter
- Lists software with installation status
- Updates software using PowerShell commands
- Progress tracking for updates
- Detailed logging of update activities
- Silent installation support

## Requirements

- Windows OS
- Python 3.7 or higher
- CustomTkinter library

## Installation

1. Install Python from https://www.python.org/downloads/
2. Install CustomTkinter:
   ```
   pip install customtkinter
   ```

## Configuration

Software programs are configured in the `programs.json` file. Edit this file to add, remove, or modify programs:

```json
[
    {
        "name": "Software Name",
        "install_path": "C:\\Program Files\\Software",
        "installer_path": "C:\\Installers\\software-installer.exe",
        "silent_args": "/S",
        "version_check": {
            "type": "exe_version",
            "path": "C:\\Path\\To\\Executable.exe"
        },
        "new_version": "1.2.3"
    }
]
```

### Configuration Fields
- `name`: Display name for the software
- `install_path`: Path where the software is installed (used to check if already installed)
- `installer_path`: Full path to the installer executable or archive
- `silent_args`: Arguments for silent/unattended installation
- `version_check`: Configuration for checking the current version (see below)
- `new_version`: The version available for update

### Version Checking
The `version_check` object supports several methods for checking the current version:

1. **Executable File Version**:
   ```json
   "version_check": {
       "type": "exe_version",
       "path": "C:\\Path\\To\\Executable.exe"
   }
   ```

2. **Command Output**:
   ```json
   "version_check": {
       "type": "cmd_output",
       "command": "C:\\Path\\To\\executable.exe --version",
       "regex": "Version ([0-9.]+)"
   }
   ```

3. **File Content**:
   ```json
   "version_check": {
       "type": "file_content",
       "path": "C:\\Path\\To\\version.txt",
       "regex": "([0-9.]+)"
   }
   ```

4. **No Version Check**:
   ```json
   "version_check": {
       "type": "none"
   }
   ```

If `programs.json` doesn't exist, the application will create it from `programs_template.json` on first run.

### Assets Directory

The `assets` directory contains icons and other resources for the application. To use a custom icon:
1. Create a .ico file (recommended size: 256x256 pixels)
2. Place it in the `assets` directory as `icon.ico`

## Usage

1. Ensure installers are available at the specified paths
2. Run the application using one of these methods:
   - Double-click `run_updater.bat`
   - Run from command line:
     ```
     python main.py
     ```
3. Click "Update" buttons to install/update software

## Silent Installation Arguments

Common silent installation arguments:
- `/S` - Silent installation (NSIS installers)
- `/quiet` - Quiet installation (MSI installers)
- `/silent` - Silent installation (Inno Setup)
- `/qn` - No UI (Windows Installer)

## How It Works

1. The application checks if software is installed by verifying the installation path exists
2. When you click "Update", it runs PowerShell to execute the installer with silent arguments
3. PowerShell waits for the installation to complete before continuing
4. Progress and status are updated in the GUI

## Troubleshooting

- Ensure installer paths are correct and files exist
- Check silent installation arguments for each installer type
- Review the log output for error messages
- Some installers may require administrator privileges