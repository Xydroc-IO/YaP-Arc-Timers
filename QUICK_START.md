# ARC Raiders Event Timers - Quick Start Guide

## 🚀 Fastest Way to Get Started

### 1️⃣ Install Dependencies (First Time Only)
```bash
./launch-installer.sh
```
- Opens a GUI installer
- Auto-detects your Linux distribution
- Enter your sudo password when prompted
- Installs everything automatically

### 2️⃣ Run the Application
```bash
./start.sh
```
That's it! The app will launch and show all ARC Raiders events.

---

## 📂 Project Structure

```
ArcTimers/
├── core/                     # Application code
├── installers/               # Installation scripts
├── launchers/                # Launcher utilities
├── launch-installer.sh       # → Run installer GUI
├── start.sh                  # → Run the app
├── timers250.png            # Logo
└── requirements.txt         # Dependencies
```

---

## 🎯 Common Tasks

### Install Dependencies
```bash
./launch-installer.sh           # GUI installer (recommended)
./installers/install.sh         # Command-line installer
```

### Run Application
```bash
./start.sh                      # Main launcher (recommended)
./launchers/start-app.sh        # Alternative launcher
python3 core/arc_timers.py      # Direct execution
```

### Build AppImage
```bash
./installers/build-appimage.sh
./ARC-Raiders-Event-Timers-x86_64.AppImage
```

---

## 🐧 Supported Linux Distributions

✅ **Debian-based**: Ubuntu, Debian, Linux Mint, Pop!_OS, Elementary OS  
✅ **Fedora-based**: Fedora, RHEL, CentOS, Rocky Linux, AlmaLinux  
✅ **Arch-based**: Arch Linux, Manjaro, EndeavourOS, Garuda  
✅ **SUSE-based**: openSUSE Leap, openSUSE Tumbleweed

## 🖥️ Supported Desktop Environments

✅ GNOME, KDE Plasma, XFCE, Cinnamon, MATE, LXQt, Budgie, Deepin, Pantheon

---

## ❓ Need Help?

**Dependencies won't install?**  
→ Run: `./launch-installer.sh` and check the installation log

**App won't start?**  
→ Make sure dependencies are installed first

**No events showing?**  
→ Check your internet connection and click Refresh

**More help?**  
→ See `README.md` for detailed troubleshooting

---

## ⚡ Features at a Glance

- 🔄 Real-time countdown timers
- 🌍 Automatic timezone conversion
- 📊 3×3 responsive grid layout
- 🎨 Dark theme UI
- 🔁 Auto-refresh when events expire
- 📍 Shows all event locations
- ⏰ Upcoming event windows

Enjoy tracking ARC Raiders events! 🎮

