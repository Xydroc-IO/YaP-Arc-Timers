#!/bin/bash
# Launcher for ARC Raiders Event Timers Dependency Installer (GUI)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "=== ARC Raiders Event Timers - Dependency Installer ==="
echo ""

# Check if Python 3 is available
if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: Python 3 is required but not installed."
    echo "Please install Python 3 first:"
    echo "  Ubuntu/Debian: sudo apt install python3"
    echo "  Fedora/RHEL:   sudo dnf install python3"
    echo "  Arch/Manjaro:  sudo pacman -S python"
    echo "  openSUSE:      sudo zypper install python3"
    exit 1
fi

# Check if tkinter is available (required for GUI)
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo "Warning: tkinter is not installed."
    echo "The installer GUI requires tkinter. Installing now..."
    echo ""
    
    # Try to detect distro and install tkinter
    if command -v apt >/dev/null 2>&1; then
        echo "Detected Debian/Ubuntu system..."
        sudo apt update && sudo apt install -y python3-tk
    elif command -v dnf >/dev/null 2>&1; then
        echo "Detected Fedora/RHEL system..."
        sudo dnf install -y python3-tkinter
    elif command -v pacman >/dev/null 2>&1; then
        echo "Detected Arch/Manjaro system..."
        sudo pacman -S --noconfirm tk
    elif command -v zypper >/dev/null 2>&1; then
        echo "Detected openSUSE system..."
        sudo zypper install -y python3-tk
    else
        echo "Could not detect package manager."
        echo "Please install python3-tkinter manually and run this script again."
        exit 1
    fi
    
    echo ""
fi

# Launch the GUI installer
cd "$PROJECT_ROOT"
python3 core/install-dependencies-gui.py

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo ""
    echo "You can now run the application with:"
    echo "  ./start.sh"
    echo "or"
    echo "  python3 core/arc_timers.py"
fi

exit $exit_code

