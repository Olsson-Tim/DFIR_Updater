# DFIR Software Updater

A Python GUI application for updating software on offline Windows workstations. This tool uses CustomTkinter for the interface and PowerShell to execute installers silently.

## Features

- Modern dark-themed GUI using CustomTkinter
- Lists software with installation status and version information
- Updates software using PowerShell commands
- Progress tracking for updates
- Detailed logging of update activities
- Silent installation support
- External configuration file for easy customization

## Requirements

- Windows OS
- Python 3.7 or higher (for running from source)
- CustomTkinter library

## Directory Structure

```
DFIR_Updater/
├── assets/                 # Icons and other resources
├── dist/                   # Packaged executables (created during build)
├── build/                  # Build artifacts (created during build)
├── src/                    # Source code
├── scripts/                # Utility scripts
├── programs.json           # Configuration file
├── programs_template.json  # Configuration template
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── build.bat               # Build script
├── run_updater.bat         # Run script for source version
├── run_packaged.bat        # Run script for packaged version
├── setup.bat               # Setup script
└── config_helper.bat       # Configuration helper script
```

## Installation

1. Install Python from https://www.python.org/downloads/
2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```
   Or run `setup.bat` which will do this automatically.

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
            "path": "C:\\Program Files\\Software\\software.exe"
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

### Running from Source

1. Ensure installers are available at the specified paths
2. Run the application using one of these methods:
   - Double-click `run_updater.bat`
   - Run from command line:
     ```
     python src/main.py
     ```

### Running Packaged Version

1. Run `build.bat` to create the executable
2. Run the application using one of these methods:
   - Double-click `run_packaged.bat`
   - Navigate to `dist/DFIR_Software_Updater` and run `DFIR_Software_Updater.exe`

## Packaging as Executable

To package the application as a standalone executable:

1. Run `build.bat` to create the executable
2. The executable will be created in the `dist/DFIR_Software_Updater` directory
3. Run `run_packaged.bat` to launch the packaged application

### Build Requirements

- Python 3.7 or higher
- PyInstaller
- Pillow (for icon handling)

These dependencies will be automatically installed when running `build.bat`.

### Distribution

To distribute the application, copy the entire `dist/DFIR_Software_Updater` directory to the target system. The directory contains:
- `DFIR_Software_Updater.exe` - The main executable
- `programs.json` - Configuration file (can be modified after packaging)
- `programs_template.json` - Template for creating new configurations
- `assets/` - Icon and other resource files

### Creating a Single File Executable

To create a single-file executable instead of a directory, use the `--onefile` option:
```
pyinstaller --noconfirm --onefile --windowed --hidden-import=customtkinter --add-data "programs.json;." --add-data "programs_template.json;." --add-data "assets;assets" --icon "assets/icon.ico" --name "DFIR_Software_Updater" src/main.py
```

Note: Single-file executables are slower to start as they need to extract files to a temporary directory on each run. When using the single-file option, the `programs.json` file will be created in the same directory as the executable when the application is first run.

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