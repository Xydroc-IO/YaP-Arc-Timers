#!/bin/bash
# Direct launcher for ARC Raiders Event Timers application

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# Check if dependencies are installed
if ! python3 -c "import requests, bs4, PIL" 2>/dev/null; then
    echo "Error: Dependencies not installed!"
    echo "Please run the installer first:"
    echo "  ./launch-installer.sh"
    echo ""
    read -p "Would you like to run the installer now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ./launch-installer.sh
        exit $?
    else
        exit 1
    fi
fi

# Launch the application
echo "Launching ARC Raiders Event Timers..."
python3 core/arc_timers.py

