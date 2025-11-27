#!/usr/bin/env python3
"""
ARC Raiders Event Timers - Dependency Installer (GUI)
Compatible with all major Linux distributions and desktop environments
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import os
import sys
import threading
import time

class DependencyInstallerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ARC Raiders Event Timers - Dependency Installer")
        self.root.geometry("750x700")
        self.root.configure(bg="#1a1a1a")
        self.root.resizable(True, True)  # Allow resizing both horizontally and vertically
        self.root.minsize(750, 650)  # Set minimum size
        
        # Center window
        self.center_window()
        
        self.sudo_password = None
        self.distro_info = self.detect_distro()
        self.installation_complete = False
        
        self.setup_ui()
        
    def center_window(self):
        """Center the window on primary monitor"""
        self.root.update_idletasks()
        width = 750
        height = 700
        
        # For multi-monitor setups, get the pointer position to determine active monitor
        # Or default to positioning near 0,0 (primary monitor)
        try:
            # Get the root window position (usually on primary monitor)
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            # Try to get primary monitor dimensions (usually the first monitor)
            # In multi-monitor setups, position relative to primary monitor at origin
            pointer_x = self.root.winfo_pointerx()
            pointer_y = self.root.winfo_pointery()
            
            # If pointer is far from origin, assume multi-monitor and center on primary
            # Primary monitor typically starts at 0,0
            if pointer_x > screen_width * 0.6 or pointer_x < 0:
                # Position on primary monitor (left-most, starting at 0)
                # Assume primary monitor is 1920x1080 or get reasonable defaults
                primary_width = min(1920, screen_width)
                primary_height = min(1080, screen_height)
                x = (primary_width // 2) - (width // 2)
                y = (primary_height // 2) - (height // 2)
            else:
                # Center on total screen space (single monitor or pointer is on primary)
                x = (screen_width // 2) - (width // 2)
                y = (screen_height // 2) - (height // 2)
            
            # Ensure window is not off-screen
            x = max(0, min(x, screen_width - width))
            y = max(0, min(y, screen_height - height))
            
        except:
            # Fallback to simple centering on primary monitor
            x = 100
            y = 100
        
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def detect_distro(self):
        """Detect Linux distribution and package manager"""
        distro = {
            'name': 'Unknown',
            'package_manager': None,
            'install_cmd': None,
            'update_cmd': None,
            'python_packages': []
        }
        
        # Try to read /etc/os-release
        try:
            with open('/etc/os-release', 'r') as f:
                os_release = f.read().lower()
                
                if 'ubuntu' in os_release or 'debian' in os_release or 'mint' in os_release:
                    distro['name'] = 'Debian/Ubuntu'
                    distro['package_manager'] = 'apt'
                    distro['install_cmd'] = ['sudo', 'apt', 'install', '-y']
                    distro['update_cmd'] = ['sudo', 'apt', 'update']
                    distro['python_packages'] = ['python3', 'python3-pip', 'python3-tk', 'python3-pil', 'python3-pil.imagetk']
                    
                elif 'fedora' in os_release or 'rhel' in os_release or 'centos' in os_release:
                    distro['name'] = 'Fedora/RHEL'
                    distro['package_manager'] = 'dnf'
                    distro['install_cmd'] = ['sudo', 'dnf', 'install', '-y']
                    distro['update_cmd'] = ['sudo', 'dnf', 'check-update']
                    distro['python_packages'] = ['python3', 'python3-pip', 'python3-tkinter', 'python3-pillow', 'python3-pillow-tk']
                    
                elif 'arch' in os_release or 'manjaro' in os_release:
                    distro['name'] = 'Arch/Manjaro'
                    distro['package_manager'] = 'pacman'
                    distro['install_cmd'] = ['sudo', 'pacman', '-S', '--noconfirm']
                    distro['update_cmd'] = ['sudo', 'pacman', '-Sy']
                    distro['python_packages'] = ['python', 'python-pip', 'tk', 'python-pillow']
                    
                elif 'opensuse' in os_release or 'suse' in os_release:
                    distro['name'] = 'openSUSE'
                    distro['package_manager'] = 'zypper'
                    distro['install_cmd'] = ['sudo', 'zypper', 'install', '-y']
                    distro['update_cmd'] = ['sudo', 'zypper', 'refresh']
                    distro['python_packages'] = ['python3', 'python3-pip', 'python3-tk', 'python3-Pillow', 'python3-Pillow-tk']
                    
        except Exception as e:
            print(f"Could not detect distro: {e}")
        
        return distro
    
    def setup_ui(self):
        """Setup the GUI"""
        # Header - more compact
        header_frame = tk.Frame(self.root, bg="#2d2d2d", height=70)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="ARC Raiders Event Timers",
            font=("Arial", 18, "bold"),
            bg="#2d2d2d",
            fg="#ffffff"
        )
        title_label.pack(pady=(8, 2))
        
        subtitle_label = tk.Label(
            header_frame,
            text="Dependency Installer",
            font=("Arial", 11),
            bg="#2d2d2d",
            fg="#888888"
        )
        subtitle_label.pack(pady=(0, 8))
        
        # Main content (allow it to expand) - reduced padding
        content_frame = tk.Frame(self.root, bg="#1a1a1a")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=12)
        
        # Configure content frame to expand properly
        content_frame.grid_rowconfigure(2, weight=1)  # Log frame row gets priority
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Distribution info - more compact
        info_frame = tk.Frame(content_frame, bg="#2d2d2d", relief=tk.RAISED, borderwidth=2)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            info_frame,
            text="System Information",
            font=("Arial", 11, "bold"),
            bg="#2d2d2d",
            fg="#ffffff"
        ).pack(anchor="w", padx=12, pady=(8, 4))
        
        tk.Label(
            info_frame,
            text=f"Distribution: {self.distro_info['name']}",
            font=("Arial", 9),
            bg="#2d2d2d",
            fg="#aaaaaa"
        ).pack(anchor="w", padx=12, pady=2)
        
        tk.Label(
            info_frame,
            text=f"Package Manager: {self.distro_info['package_manager'] or 'Unknown'}",
            font=("Arial", 9),
            bg="#2d2d2d",
            fg="#aaaaaa"
        ).pack(anchor="w", padx=12, pady=(2, 8))
        
        # Password frame - more compact
        password_frame = tk.Frame(content_frame, bg="#2d2d2d", relief=tk.RAISED, borderwidth=2)
        password_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            password_frame,
            text="Administrator Password",
            font=("Arial", 11, "bold"),
            bg="#2d2d2d",
            fg="#ffffff"
        ).pack(anchor="w", padx=12, pady=(8, 4))
        
        tk.Label(
            password_frame,
            text="Enter your sudo password to install system packages:",
            font=("Arial", 9),
            bg="#2d2d2d",
            fg="#aaaaaa"
        ).pack(anchor="w", padx=12, pady=(0, 4))
        
        password_entry_frame = tk.Frame(password_frame, bg="#2d2d2d")
        password_entry_frame.pack(fill=tk.X, padx=12, pady=(0, 8))
        
        self.password_entry = tk.Entry(
            password_entry_frame,
            show="●",
            font=("Arial", 11),
            bg="#1a1a1a",
            fg="#ffffff",
            insertbackground="#ffffff",
            relief=tk.FLAT,
            borderwidth=0
        )
        self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 10))
        
        self.show_password_var = tk.BooleanVar()
        show_password_check = tk.Checkbutton(
            password_entry_frame,
            text="Show",
            variable=self.show_password_var,
            command=self.toggle_password_visibility,
            font=("Arial", 9),
            bg="#2d2d2d",
            fg="#aaaaaa",
            selectcolor="#1a1a1a",
            activebackground="#2d2d2d",
            activeforeground="#ffffff"
        )
        show_password_check.pack(side=tk.LEFT)
        
        # Log output - more compact
        log_frame = tk.Frame(content_frame, bg="#2d2d2d", relief=tk.RAISED, borderwidth=2)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        tk.Label(
            log_frame,
            text="Installation Log",
            font=("Arial", 11, "bold"),
            bg="#2d2d2d",
            fg="#ffffff"
        ).pack(anchor="w", padx=12, pady=(8, 4))
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            font=("Courier", 9),
            bg="#1a1a1a",
            fg="#00ff00",
            insertbackground="#00ff00",
            relief=tk.FLAT,
            state=tk.DISABLED,
            height=10
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 8))
        
        # Progress bar - more compact
        self.progress = ttk.Progressbar(
            content_frame,
            mode='indeterminate',
            length=300
        )
        self.progress.pack(pady=(0, 8))
        
        # Buttons - more compact but still visible
        button_frame = tk.Frame(content_frame, bg="#1a1a1a")
        button_frame.pack(fill=tk.X, pady=(0, 0))
        
        self.install_btn = tk.Button(
            button_frame,
            text="🚀 START INSTALLATION",
            command=self.start_installation,
            bg="#22c55e",
            fg="#ffffff",
            font=("Arial", 14, "bold"),
            padx=40,
            pady=12,
            relief=tk.RAISED,
            borderwidth=3,
            cursor="hand2",
            activebackground="#16a34a",
            activeforeground="#ffffff",
            highlightthickness=2,
            highlightbackground="#16a34a"
        )
        self.install_btn.pack(side=tk.LEFT, expand=True, padx=(0, 6), fill=tk.X)
        
        self.close_btn = tk.Button(
            button_frame,
            text="✕ Close",
            command=self.close_window,
            bg="#666666",
            fg="#ffffff",
            font=("Arial", 12, "bold"),
            padx=25,
            pady=12,
            relief=tk.FLAT,
            cursor="hand2",
            activebackground="#555555"
        )
        self.close_btn.pack(side=tk.LEFT, padx=(6, 0))
        
        self.log("✓ Ready to install dependencies!")
        self.log(f"✓ Detected: {self.distro_info['name']}")
        self.log("")
        self.log("👉 Enter your sudo password above and click 'START INSTALLATION'")
        
    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="●")
    
    def log(self, message):
        """Add message to log"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update()
    
    def run_command(self, cmd, use_sudo=False, stdin_password=None):
        """Run a command and return success status"""
        try:
            if use_sudo and stdin_password:
                # Modify command to add -S flag to sudo for reading password from stdin
                full_cmd = cmd.copy()
                
                # Find 'sudo' in the command and add -S flag after it
                if full_cmd and full_cmd[0] == 'sudo':
                    # Insert -S flag after sudo
                    full_cmd.insert(1, '-S')
                
                process = subprocess.Popen(
                    full_cmd,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                stdout, stderr = process.communicate(input=f"{stdin_password}\n", timeout=300)
                
                if process.returncode != 0:
                    # Filter out the sudo password prompt from stderr
                    error_lines = [line for line in stderr.strip().split('\n') 
                                 if line.strip() and '[sudo]' not in line.lower() and 'password' not in line.lower()]
                    if error_lines:
                        self.log(f"Error: {' '.join(error_lines)}")
                    return False
                
                if stdout.strip():
                    for line in stdout.strip().split('\n'):
                        if line.strip() and '[sudo]' not in line.lower():
                            self.log(f"  {line.strip()}")
                            
            else:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                if result.returncode != 0:
                    self.log(f"Error: {result.stderr.strip()}")
                    return False
                    
                if result.stdout.strip():
                    for line in result.stdout.strip().split('\n')[:5]:  # Show first 5 lines
                        if line.strip():
                            self.log(f"  {line.strip()}")
            
            return True
            
        except subprocess.TimeoutExpired:
            self.log("Error: Command timed out")
            return False
        except Exception as e:
            self.log(f"Error: {str(e)}")
            return False
    
    def start_installation(self):
        """Start installation in a separate thread"""
        password = self.password_entry.get()
        
        if not password:
            messagebox.showerror("Error", "Please enter your sudo password")
            return
        
        if not self.distro_info['package_manager']:
            messagebox.showerror(
                "Error", 
                "Could not detect your distribution's package manager.\n"
                "Please install dependencies manually."
            )
            return
        
        self.sudo_password = password
        self.install_btn.config(state=tk.DISABLED)
        self.password_entry.config(state=tk.DISABLED)
        self.progress.start()
        
        # Run installation in separate thread
        thread = threading.Thread(target=self.install_dependencies, daemon=True)
        thread.start()
    
    def install_dependencies(self):
        """Install all dependencies"""
        try:
            self.log("\n=== Starting Installation ===\n")
            
            # Step 1: Update package manager
            self.log("Step 1/3: Updating package manager...")
            if self.distro_info['update_cmd']:
                cmd = self.distro_info['update_cmd'].copy()
                if self.run_command(cmd, use_sudo=True, stdin_password=self.sudo_password):
                    self.log("✓ Package manager updated successfully")
                else:
                    self.log("⚠ Package manager update had issues (continuing anyway)")
            
            time.sleep(0.5)
            
            # Step 2: Install system packages
            self.log("\nStep 2/3: Installing system packages...")
            if self.distro_info['python_packages']:
                cmd = self.distro_info['install_cmd'].copy()
                cmd.extend(self.distro_info['python_packages'])
                
                self.log(f"Installing: {', '.join(self.distro_info['python_packages'])}")
                
                if self.run_command(cmd, use_sudo=True, stdin_password=self.sudo_password):
                    self.log("✓ System packages installed successfully")
                else:
                    self.log("✗ Failed to install some system packages")
                    self.root.after(0, self.installation_failed)
                    return
            
            time.sleep(0.5)
            
            # Step 3: Install Python packages
            self.log("\nStep 3/3: Installing Python packages with pip...")
            
            # Read requirements.txt (in parent directory)
            script_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(script_dir)
            req_file = os.path.join(parent_dir, 'requirements.txt')
            if os.path.exists(req_file):
                self.log("Installing from requirements.txt...")
                
                # Try with --break-system-packages first
                cmd = ['python3', '-m', 'pip', 'install', '--break-system-packages', '-r', req_file]
                
                if self.run_command(cmd):
                    self.log("✓ Python packages installed successfully (with --break-system-packages)")
                else:
                    # Try without --break-system-packages
                    self.log("Retrying without --break-system-packages...")
                    cmd = ['python3', '-m', 'pip', 'install', '-r', req_file]
                    
                    if self.run_command(cmd):
                        self.log("✓ Python packages installed successfully")
                    else:
                        # Try with --user flag as last resort
                        self.log("Retrying with --user flag...")
                        cmd = ['python3', '-m', 'pip', 'install', '--user', '-r', req_file]
                        
                        if self.run_command(cmd):
                            self.log("✓ Python packages installed successfully (user installation)")
                        else:
                            self.log("✗ Failed to install Python packages")
                            self.root.after(0, self.installation_failed)
                            return
            else:
                self.log("⚠ requirements.txt not found, skipping pip installation")
            
            time.sleep(0.5)
            
            # Installation complete
            self.log("\n=== Installation Complete ===")
            self.log("All dependencies have been installed successfully!")
            self.log("You can now run: python3 arc_timers.py")
            
            self.root.after(0, self.installation_success)
            
        except Exception as e:
            self.log(f"\n✗ Installation failed: {str(e)}")
            self.root.after(0, self.installation_failed)
    
    def installation_success(self):
        """Handle successful installation"""
        self.progress.stop()
        self.install_btn.config(
            state=tk.DISABLED, 
            text="✓ INSTALLATION COMPLETE", 
            bg="#22c55e",
            relief=tk.FLAT
        )
        self.installation_complete = True
        messagebox.showinfo(
            "Success",
            "All dependencies have been installed successfully!\n\n"
            "You can now run the application with:\n"
            "./start.sh\n\nor\n\n"
            "python3 core/arc_timers.py"
        )
    
    def installation_failed(self):
        """Handle failed installation"""
        self.progress.stop()
        self.install_btn.config(state=tk.NORMAL)
        self.password_entry.config(state=tk.NORMAL)
        messagebox.showerror(
            "Installation Failed",
            "Some dependencies could not be installed.\n"
            "Please check the log for details."
        )
    
    def close_window(self):
        """Close the window"""
        self.root.destroy()


def main():
    # Check if running on Linux
    if sys.platform != 'linux':
        print("This installer is designed for Linux systems only.")
        sys.exit(1)
    
    root = tk.Tk()
    app = DependencyInstallerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

