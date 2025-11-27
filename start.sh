#!/bin/bash
# ARC Raiders Event Timers Main Launcher
# This is the main entry point for the application

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== ARC Raiders Event Timers ==="
echo ""

# Check if dependencies are installed (quick check)
if ! python3 -c "import requests, bs4, PIL" 2>/dev/null; then
    echo "⚠ Dependencies not installed!"
    echo ""
    echo "Please install dependencies first:"
    echo "  Option 1 (GUI):     ./launch-installer.sh"
    echo "  Option 2 (CLI):     ./installers/install.sh"
    echo "  Option 3 (AppImage): ./installers/build-appimage.sh"
    echo ""
    read -p "Would you like to run the GUI installer now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ./launch-installer.sh
        echo ""
        echo "After installation completes, run this script again."
        exit 0
    else
        exit 1
    fi
fi

# Check if virtual environment exists and use it if available
if [ -d "venv" ]; then
    echo "Using virtual environment..."
    source venv/bin/activate
fi

# Run the application from core directory
echo "Launching application..."
echo ""
python3 core/arc_timers.py
