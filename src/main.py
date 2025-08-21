import customtkinter as ctk
import os
import subprocess
import threading
import json
import re
import sys
from tkinter import messagebox

# Configure CustomTkinter appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SoftwareUpdater:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("DFIR Software Updater")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Try to set icon if it exists
        try:
            icon_path = self.get_resource_path("assets/icon.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Could not set icon: {e}")
        
        # Load program data from JSON file
        self.programs_data = self.load_programs()
        
        self.setup_ui()
        self.check_installations()
        
    def get_resource_path(self, relative_path):
        """Get absolute path to resource, works for dev and for PyInstaller"""
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        
        return os.path.join(base_path, relative_path)
        
    def load_programs(self):
        """Load program data from JSON file"""
        try:
            # Get the path to programs.json
            config_path = self.get_resource_path("programs.json")
            
            # Check if programs.json exists, if not create from template
            if not os.path.exists(config_path):
                template_path = self.get_resource_path("programs_template.json")
                if os.path.exists(template_path):
                    import shutil
                    # For packaged version, we need to copy to the current working directory
                    cwd_config_path = os.path.join(os.getcwd(), "programs.json")
                    shutil.copy(template_path, cwd_config_path)
                    messagebox.showinfo("Info", "Created programs.json from template in the current directory. Please configure your programs and restart the application.")
                    return []
                else:
                    messagebox.showerror("Error", "programs.json file not found and template not available.")
                    return self.get_default_programs()
            
            # Load programs from JSON file
            with open(config_path, "r") as f:
                programs = json.load(f)
                
            return programs
        except FileNotFoundError:
            messagebox.showerror("Error", "programs.json file not found. Using default programs.")
            return self.get_default_programs()
        except json.JSONDecodeError as e:
            messagebox.showerror("Error", f"Error parsing programs.json: {str(e)}")
            return self.get_default_programs()
        except Exception as e:
            messagebox.showerror("Error", f"Error loading programs: {str(e)}")
            return self.get_default_programs()
            
    def get_default_programs(self):
        """Return default program data if JSON file cannot be loaded"""
        return [
            {
                "name": "Wireshark",
                "install_path": r"C:\Program Files\Wireshark",
                "installer_path": r"C:\Installers\Wireshark-win64-4.2.5.exe",
                "silent_args": "/S"
            },
            {
                "name": "Sysinternals",
                "install_path": r"C:\Tools\Sysinternals",
                "installer_path": r"C:\Installers\sysinternals-suite.zip",
                "silent_args": ""
            }
        ]
        
    def get_program_version(self, program):
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
            print(f"Error getting version for {program.get('name', 'Unknown')}: {str(e)}")
            return "Error"
            
    def setup_ui(self):
        # Main frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            self.main_frame, 
            text="DFIR Software Updater", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        # Description
        desc_label = ctk.CTkLabel(
            self.main_frame,
            text="Update software on offline workstations",
            font=ctk.CTkFont(size=14)
        )
        desc_label.pack(pady=(0, 20))
        
        # Programs frame
        self.programs_frame = ctk.CTkScrollableFrame(self.main_frame, height=300)
        self.programs_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Create program widgets
        self.program_widgets = []
        for program in self.programs_data:
            self.create_program_widget(program)
        
        # Log frame
        log_frame = ctk.CTkFrame(self.main_frame)
        log_frame.pack(fill="both", expand=False, padx=20, pady=(0, 20))
        
        log_label = ctk.CTkLabel(log_frame, text="Update Log", font=ctk.CTkFont(weight="bold"))
        log_label.pack(pady=(10, 5))
        
        self.log_text = ctk.CTkTextbox(log_frame, height=100)
        self.log_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.log_text.configure(state="disabled")
        
        # Status bar
        self.status_bar = ctk.CTkFrame(self.root, height=30)
        self.status_bar.pack(fill="x", side="bottom")
        
        self.status_label = ctk.CTkLabel(
            self.status_bar, 
            text="Ready",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=5)
        
    def create_program_widget(self, program):
        # Frame for each program
        frame = ctk.CTkFrame(self.programs_frame)
        frame.pack(fill="x", padx=10, pady=5)
        
        # Program name
        name_label = ctk.CTkLabel(frame, text=program["name"], font=ctk.CTkFont(size=16, weight="bold"))
        name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Installation path (smaller font)
        path_label = ctk.CTkLabel(frame, text=program["install_path"], font=ctk.CTkFont(size=12))
        path_label.grid(row=1, column=0, padx=10, pady=(0, 5), sticky="w")
        
        # Version information
        version_label = ctk.CTkLabel(frame, text="Checking...", font=ctk.CTkFont(size=12))
        version_label.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="w")
        
        # Status label
        status_label = ctk.CTkLabel(frame, text="Checking...", font=ctk.CTkFont(size=12))
        status_label.grid(row=0, column=1, padx=10, pady=10)
        
        # Update button
        update_btn = ctk.CTkButton(
            frame, 
            text="Update", 
            command=lambda p=program: self.start_update(p),
            width=80
        )
        update_btn.grid(row=0, column=2, padx=10, pady=10)
        
        # Progress bar (hidden by default)
        progress_bar = ctk.CTkProgressBar(frame)
        progress_bar.set(0)
        progress_bar.grid(row=3, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="ew")
        progress_bar.grid_forget()  # Hide initially
        
        # Store widget references
        widget_data = {
            "frame": frame,
            "status_label": status_label,
            "version_label": version_label,
            "update_btn": update_btn,
            "progress_bar": progress_bar
        }
        self.program_widgets.append(widget_data)
        
    def check_installations(self):
        """Check which programs are installed and their versions"""
        # For packaged version, check if programs.json exists in current directory
        try:
            if hasattr(sys, '_MEIPASS'):
                # Running as packaged executable
                cwd_config_path = os.path.join(os.getcwd(), "programs.json")
                if os.path.exists(cwd_config_path):
                    # Load programs from current working directory
                    with open(cwd_config_path, "r") as f:
                        self.programs_data = json.load(f)
        except Exception as e:
            print(f"Error loading programs from current directory: {e}")
        
        for i, program in enumerate(self.programs_data):
            widget_data = self.program_widgets[i]
            status_label = widget_data["status_label"]
            version_label = widget_data["version_label"]
            
            # Check if installed
            if os.path.exists(program["install_path"]):
                # Get current version
                current_version = self.get_program_version(program)
                new_version = program.get("new_version", "Unknown")
                
                # Update version label
                if current_version != "Unknown" and current_version != "Error":
                    version_text = f"Current: {current_version}"
                    if new_version != "Unknown" and new_version != "N/A":
                        version_text += f" → New: {new_version}"
                    version_label.configure(text=version_text)
                    
                    # Check if update is available
                    if (new_version != "Unknown" and new_version != "N/A" and 
                        current_version != new_version):
                        status_label.configure(text="Update Available", text_color="orange")
                    else:
                        status_label.configure(text="Installed", text_color="green")
                else:
                    version_label.configure(text="Version: Unknown")
                    status_label.configure(text="Installed", text_color="green")
            else:
                status_label.configure(text="Not Installed", text_color="red")
                new_version = program.get("new_version", "Unknown")
                if new_version != "Unknown" and new_version != "N/A":
                    version_label.configure(text=f"New: {new_version}")
                else:
                    version_label.configure(text="Not Installed")
                    
    def start_update(self, program):
        """Start the update process for a program"""
        # Find the widget data for this program
        widget_data = None
        for wd in self.program_widgets:
            name_label = wd["frame"].winfo_children()[0]  # First label is the name
            if name_label.cget("text") == program["name"]:
                widget_data = wd
                break
                
        if not widget_data:
            self.log_message(f"Error: Could not find widget for {program['name']}")
            return
            
        # Disable update button
        widget_data["update_btn"].configure(state="disabled", text="Updating...")
        
        # Show progress bar
        widget_data["progress_bar"].grid()
        
        # Start update in separate thread
        thread = threading.Thread(target=self.run_update, args=(program, widget_data))
        thread.daemon = True
        thread.start()
        
    def run_update(self, program, widget_data):
        """Run the actual update process using PowerShell"""
        self.log_message(f"Starting update for {program['name']}...")
        
        # Check if installer exists
        if not os.path.exists(program["installer_path"]):
            self.root.after(0, lambda: self.finish_update(
                program, widget_data, f"Installer not found: {program['installer_path']}", False))
            return
            
        try:
            # Handle different file types
            installer_path = program["installer_path"]
            file_ext = os.path.splitext(installer_path)[1].lower()
            
            if file_ext == ".zip":
                # Special handling for zip files (extract instead of execute)
                ps_command = (
                    f"Expand-Archive -Path '{installer_path}' "
                    f"-DestinationPath '{program['install_path']}' -Force"
                )
                self.log_message(f"Extracting: {ps_command}")
            else:
                # Construct PowerShell command for executables
                ps_command = (
                    f"Start-Process -FilePath '{installer_path}' "
                    f"-ArgumentList '{program['silent_args']}' -Wait"
                )
                self.log_message(f"Executing: {ps_command}")
            
            # Run PowerShell with the command
            result = subprocess.run(
                ["powershell", "-Command", ps_command],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            # Check result
            if result.returncode == 0:
                self.root.after(0, lambda: self.finish_update(
                    program, widget_data, f"{program['name']} updated successfully!", True))
            else:
                error_msg = result.stderr if result.stderr else "Unknown error occurred"
                self.root.after(0, lambda: self.finish_update(
                    program, widget_data, f"Update failed: {error_msg}", False))
                
        except subprocess.TimeoutExpired:
            self.root.after(0, lambda: self.finish_update(
                program, widget_data, "Update timed out after 5 minutes", False))
        except Exception as e:
            self.root.after(0, lambda: self.finish_update(
                program, widget_data, f"Update error: {str(e)}", False))
                
    def finish_update(self, program, widget_data, message, success):
        """Finish the update process and update UI"""
        # Hide progress bar
        widget_data["progress_bar"].grid_forget()
        
        # Re-enable update button
        widget_data["update_btn"].configure(state="normal", text="Update")
        
        # Update status
        status_text = "Installed" if success else "Error"
        status_color = "green" if success else "red"
        widget_data["status_label"].configure(text=status_text, text_color=status_color)
        
        # Log message
        self.log_message(message)
        
        # Update status bar
        self.status_label.configure(text=message)
        
        # Show completion message if needed
        if success:
            messagebox.showinfo("Update Complete", message)
            
    def log_message(self, message):
        """Add a message to the log"""
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"{message}\n")
        self.log_text.configure(state="disabled")
        self.log_text.see("end")  # Scroll to end
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SoftwareUpdater()
    app.run()