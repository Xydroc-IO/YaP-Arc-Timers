<div align="center">
  <img src="timers250.png" alt="ARC Raiders Event Timers Logo" width="250"/>
  
  # ARC Raiders Event Timers
  
  **Real-time event countdown timers from MetaForge**
  
  [![Linux](https://img.shields.io/badge/Linux-Compatible-green.svg)](https://www.linux.org/)
  [![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)
  [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
  
</div>

---

## 📋 Overview

ARC Raiders Event Timers is a GUI application that pulls and displays real-time event information from [MetaForge](https://metaforge.app/arc-raiders/event-timers). Track all ARC Raiders events with live countdowns, automatic timezone conversion, and a beautiful dark-themed interface.

### ✨ Features

- 🔄 **Real-time Countdown Timers** - Live updates for all events
- 🌍 **Automatic Timezone Conversion** - Shows times in your local timezone
- 📊 **3×3 Responsive Grid Layout** - Clean, organized event display
- 🎨 **Dark Theme UI** - Easy on the eyes
- 🔁 **Auto-refresh** - Updates when events expire
- 📍 **Event Locations** - Shows all active locations
- ⏰ **Upcoming Windows** - View next event times
- 🖼️ **Custom Logo** - Branded interface with taskbar icon
- 🔒 **Secure Installation** - GUI installer with password protection

---

## 🚀 Quick Start

### 1️⃣ Install Dependencies (First Time Only)
```bash
./launch-installer.sh
```
- Opens a beautiful GUI installer
- Auto-detects your Linux distribution
- Enter your sudo password securely
- Installs everything automatically

### 2️⃣ Run the Application
```bash
./start.sh
```
That's it! The app will launch and show all ARC Raiders events with live countdowns.

---

## 📂 Project Structure

```
YaP-Arc-Timers/
├── core/                                    # Core application files
│   ├── arc_timers.py                       # Main application
│   └── install-dependencies-gui.py         # GUI dependency installer
├── installers/                              # Installation scripts
│   ├── launch-dependency-installer.sh      # Launch GUI installer
│   └── build-appimage.sh                   # AppImage builder
├── launchers/                               # Launcher scripts
│   └── start-app.sh                        # Direct app launcher
├── launch-installer.sh                      # Quick launcher for GUI installer
├── start.sh                                 # Main application launcher ⭐
├── requirements.txt                         # Python dependencies
├── timers250.png                           # Application logo
├── QUICK_START.md                          # Quick reference guide
└── README.md                                # This file
```

---

## 💾 Installation

### Option 1: GUI Dependency Installer (Recommended!)
Run the graphical installer that works on all Linux distributions:
```bash
./launch-installer.sh
```

**GUI Installer Features:**
- ✅ **Universal Compatibility** - Works on all major Linux distributions:
  - 🐧 Ubuntu, Debian, Linux Mint, Pop!_OS
  - 🎩 Fedora, RHEL, CentOS, Rocky Linux
  - 🏔️ Arch Linux, Manjaro, EndeavourOS
  - 🦎 openSUSE Leap, Tumbleweed
- ✅ **All Desktop Environments** - GNOME, KDE Plasma, XFCE, Cinnamon, MATE, LXQt, etc.
- ✅ **Auto-detection** - Automatically detects your distro and package manager
- ✅ **Secure Password Input** - Password field with show/hide toggle
- ✅ **Real-time Progress** - Live installation log with color-coded output
- ✅ **Smart Installation** - Automatically uses `--break-system-packages` flag when needed
- ✅ **Multiple Fallback Strategies** - Tries multiple installation methods
- ✅ **Beautiful Interface** - Modern dark-themed GUI
- ✅ **Primary Monitor Support** - Opens on your main display

### Option 2: AppImage (No Installation Needed!)
Build a fully portable AppImage:
```bash
./installers/build-appimage.sh
./ARC-Raiders-Event-Timers-x86_64.AppImage
```

The AppImage is completely self-contained and works on all major Linux distributions!

### Option 3: Manual Install
```bash
pip3 install --break-system-packages -r requirements.txt
```

Or without the flag if your system allows:
```bash
pip3 install -r requirements.txt
```

---

## 🎮 Usage

### Quick Start (Recommended)
```bash
./start.sh
```

The main launcher will automatically:
- ✅ Check if dependencies are installed
- ✅ Offer to run the GUI installer if needed
- ✅ Launch the application

### All Launch Options

#### Option 1: Main Launcher ⭐
```bash
./start.sh
```
Smart launcher with dependency checking

#### Option 2: Direct Launcher
```bash
./launchers/start-app.sh
```
Checks dependencies and launches app

#### Option 3: Direct Execution
```bash
python3 core/arc_timers.py
```
Requires dependencies pre-installed

#### Option 4: AppImage (Portable)
```bash
./ARC-Raiders-Event-Timers-x86_64.AppImage
```
No dependencies needed, fully self-contained!

---

## 🐧 Supported Systems

### Linux Distributions

✅ **Debian-based**: Ubuntu, Debian, Linux Mint, Pop!_OS, Elementary OS  
✅ **Fedora-based**: Fedora, RHEL, CentOS, Rocky Linux, AlmaLinux  
✅ **Arch-based**: Arch Linux, Manjaro, EndeavourOS, Garuda  
✅ **SUSE-based**: openSUSE Leap, openSUSE Tumbleweed

### Desktop Environments

✅ GNOME • KDE Plasma • XFCE • Cinnamon • MATE • LXQt • Budgie • Deepin • Pantheon

---

## 🔧 Building AppImage

To build a portable AppImage:

```bash
./installers/build-appimage.sh
```

This creates `ARC-Raiders-Event-Timers-x86_64.AppImage` which:
- ✅ Works on **all** Linux distributions
- ✅ Requires **no installation** or dependencies
- ✅ Fully **self-contained** and portable
- ✅ Includes all Python dependencies and the logo
- ✅ Can be run directly or distributed

**Build Requirements:**
- Python 3.6+
- pip (for installing PyInstaller)
- Internet connection (for downloading tools)

The build script automatically:
- Installs PyInstaller (with `--break-system-packages` on Arch/Manjaro)
- Downloads appimagetool if needed
- Bundles all dependencies
- Creates the final AppImage

---

## 📦 Dependencies

### System Packages
- `python3` (3.6 or higher)
- `python3-pip`
- `python3-tk` (tkinter for GUI)
- `python3-pil` (Pillow/PIL for image handling)

### Python Packages
- `requests` - HTTP library for fetching event data from MetaForge
- `beautifulsoup4` - HTML parsing for extracting event information
- `lxml` - Fast XML/HTML parser
- `Pillow` - Image handling for logo display

All dependencies are listed in `requirements.txt` and automatically installed by the GUI installer.

---

## 🎯 How It Works

1. **Fetches Data** - Scrapes event information from MetaForge website
2. **Parses Events** - Extracts event names, times, locations, and countdowns
3. **Converts Timezones** - Automatically converts UTC times to your local timezone
4. **Displays GUI** - Shows events in a responsive 3×3 grid with live countdowns
5. **Auto-refreshes** - Updates events when countdowns reach zero
6. **Manual Refresh** - Click the Refresh button anytime (60-second cooldown)

---

## 🎨 GUI Features

### Header
- 🖼️ Custom logo display
- 🌍 Timezone indicator (e.g., "EST", "PST", "UTC")
- 🔄 Refresh button with cooldown
- 📊 Status indicator

### Event Cards
- 🎯 Event name and status (Active/Upcoming)
- 📍 Event locations
- ⏰ Time windows (converted to your timezone)
- ⏱️ Live countdown timers (hours, minutes, seconds)
- 📅 Upcoming event windows

### Layout
- 📐 3×3 responsive grid
- 🔲 Auto-resizing (horizontal and vertical)
- 🎨 Dark theme with color-coded statuses
- 📜 Scrollable when needed

---

## ❓ Troubleshooting

### Dependencies not installed
Run the GUI installer:
```bash
./launch-installer.sh
```

Enter your sudo password and click **🚀 START INSTALLATION**

### "Unable to Fetch Events" error
The app couldn't parse the MetaForge website. Possible causes:
- Website structure changed
- Network connectivity issues
- Website temporarily unavailable

**Debug Mode**: The app saves the HTML response to `debug_response.html`. Check this file to see the raw content.

### App won't start
1. Install dependencies: `./launch-installer.sh`
2. Check Python version: `python3 --version` (requires 3.6+)
3. Try direct execution: `python3 core/arc_timers.py`
4. Check for errors in terminal output

### No events showing / Blank screen
1. Check your internet connection
2. Click the **Refresh** button
3. Verify [MetaForge website](https://metaforge.app/arc-raiders/event-timers) is accessible
4. Check `debug_response.html` for raw HTML content

### Timezone is wrong
The app auto-detects your system timezone. Check the header to see which timezone is displayed. To change your system timezone:
```bash
# List available timezones
timedatectl list-timezones

# Set timezone (example)
sudo timedatectl set-timezone America/New_York
```

### GUI Installer: Password not working
- Make sure you have sudo privileges
- Check if password is correct (use show/hide toggle)
- Try running with sudo manually: `sudo -v`

### GUI Installer: Window on wrong monitor
The installer tries to open on your primary monitor. If it opens on the wrong screen, you can drag it or resize the window.

### AppImage build fails
**Error**: `externally-managed-environment` (Arch/Manjaro)  
**Solution**: The build script automatically handles this with `--break-system-packages`

**Error**: Missing dependencies  
**Solution**: Install system packages first via GUI installer

### Grid layout issues
- The grid auto-resizes horizontally and vertically
- Minimum window size: 1200×700
- Try maximizing the window for best view

---

## 🛠️ Development

### Project Organization

The project follows a clean, organized structure:

- **`core/`** - Core application code and installers
- **`installers/`** - Installation and build scripts
- **`launchers/`** - Launcher utilities
- **Root** - Main entry points and resources

### Debug Mode

Set `DEBUG_MODE = True` in `core/arc_timers.py` to enable debug features:
- Saves raw HTML to `debug_response.html`
- Prints detailed error messages
- Shows parsing information

### Adding Features

The code is well-structured for adding features:
- Event parsing: `fetch_events()` method
- GUI layout: `display_events()` method
- Countdown updates: `update_countdowns()` method
- Timezone conversion: `convert_time_range_to_local()` method

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- 🐛 Report bugs
- 💡 Suggest features
- 🔧 Submit pull requests
- 📖 Improve documentation

---

## 📄 License

This project is licensed under the GNU General Public License v3.0. See LICENSE file for details.

---

## 🎮 About ARC Raiders

ARC Raiders is an upcoming free-to-play cooperative PvPvE action survival shooter developed by Embark Studios. This tool helps players track in-game events in real-time using data from MetaForge.

### Useful Links
- [ARC Raiders Official Website](https://www.arcraiders.com/)
- [MetaForge Event Timers](https://metaforge.app/arc-raiders/event-timers)
- [Embark Studios](https://www.embark-studios.com/)

---

## 🙏 Credits

- **MetaForge** - For providing the event timer data
- **Embark Studios** - For creating ARC Raiders
- **Python Community** - For the excellent libraries used in this project

---

<div align="center">
  
  **Made with ❤️ for the ARC Raiders community**
  
  ---
  
  If you find this tool useful, please ⭐ star the repository!

  [Virus Total](https://www.virustotal.com/gui/file/51912ad2fb9a17c6b5e23a0b15ac428fc4b9cd69a275bd86b34569b3a4dad3f1/detection)
  
</div>
