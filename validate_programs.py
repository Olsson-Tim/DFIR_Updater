import json
import os
import subprocess
import re

def get_program_version(program):
    """Get the currently installed version of a program"""
    try:
        # Check if program has version checking configuration
        if "version_check" not in program:
            return "Unknown"
            
        version_check = program["version_check"]
        check_type = version_check.get("type", "none")
        
        if check_type == "none":
            return "N/A"
            
        elif check_type == "exe_version":
            # Get version from executable file properties
            exe_path = version_check.get("path", "")
            if not os.path.exists(exe_path):
                return "Not Installed"
                
            # Use PowerShell to get file version
            ps_command = f"(Get-Item '{exe_path}').VersionInfo.ProductVersion"
            result = subprocess.run(
                ["powershell", "-Command", ps_command],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
            else:
                return "Unknown"
                
        elif check_type == "cmd_output":
            # Get version from command output
            command = version_check.get("command", "")
            regex_pattern = version_check.get("regex", "")
            
            if not command:
                return "Unknown"
                
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0 and result.stdout:
                if regex_pattern:
                    match = re.search(regex_pattern, result.stdout)
                    if match:
                        return match.group(1)
                return result.stdout.strip()
            elif result.stderr:
                match = re.search(regex_pattern, result.stderr)
                if match:
                    return match.group(1)
                return "Unknown"
            else:
                return "Unknown"
                
        elif check_type == "file_content":
            # Get version from file content
            file_path = version_check.get("path", "")
            regex_pattern = version_check.get("regex", "")
            
            if not os.path.exists(file_path):
                return "Not Installed"
                
            with open(file_path, "r") as f:
                content = f.read()
                
            if regex_pattern:
                match = re.search(regex_pattern, content)
                if match:
                    return match.group(1)
            return "Unknown"
            
        else:
            return "Unknown"
            
    except subprocess.TimeoutExpired:
        return "Timeout"
    except Exception as e:
        print(f"Error getting version: {str(e)}")
        return "Error"

def validate_programs():
    """Validate the programs.json file"""
    try:
        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, "programs.json")
        
        # Load programs from JSON file
        with open(config_path, "r") as f:
            programs = json.load(f)
            
        print(f"Found {len(programs)} programs in programs.json")
        print("-" * 50)
        
        # Validate each program
        for i, program in enumerate(programs):
            print(f"Program {i+1}: {program['name']}")
            
            # Check required fields
            required_fields = ["name", "install_path", "installer_path", "silent_args"]
            for field in required_fields:
                if field not in program:
                    print(f"  ERROR: Missing field '{field}'")
                    continue
                    
            # Check if installer exists
            if os.path.exists(program["installer_path"]):
                print(f"  Installer: Found")
            else:
                print(f"  Installer: NOT FOUND ({program['installer_path']})")
                
            # Check if currently installed
            if os.path.exists(program["install_path"]):
                print(f"  Status: Installed")
            else:
                print(f"  Status: Not Installed")
                
            # Check version information
            current_version = get_program_version(program)
            new_version = program.get("new_version", "Unknown")
            
            print(f"  Current Version: {current_version}")
            if new_version != "Unknown" and new_version != "N/A":
                print(f"  New Version: {new_version}")
                
                # Check if update is available
                if (new_version != "Unknown" and new_version != "N/A" and 
                    current_version != new_version and 
                    current_version != "Not Installed" and
                    current_version != "Unknown"):
                    print(f"  Update Available: YES")
                elif current_version == "Not Installed":
                    print(f"  Update Available: Not Installed")
                else:
                    print(f"  Update Available: NO")
            else:
                print(f"  New Version: N/A")
                
            print()
            
        print("Validation complete.")
        return True
        
    except FileNotFoundError:
        print("ERROR: programs.json file not found")
        return False
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in programs.json: {str(e)}")
        return False
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    validate_programs()