#!/bin/bash
# ARC Raiders Event Timers AppImage Builder
# Creates a fully self-contained AppImage with PyInstaller

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$PROJECT_ROOT/build"
APPDIR="$BUILD_DIR/AppDir"
APPIMAGE_NAME="ARC-Raiders-Event-Timers-x86_64.AppImage"

echo "=== ARC Raiders Event Timers AppImage Builder ==="
echo "Creating fully self-contained AppImage with PyInstaller..."

# Check for required tools
if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: Python 3 is required!"
    exit 1
fi

# Clean previous build
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

# Copy application files to build directory
echo "Copying application files..."
cp "$PROJECT_ROOT/core/arc_timers.py" "$BUILD_DIR/"
cp "$PROJECT_ROOT/requirements.txt" "$BUILD_DIR/"
cp "$PROJECT_ROOT/timers250.png" "$BUILD_DIR/"

# Create PyInstaller spec file
echo "Creating PyInstaller spec..."
cat > "$BUILD_DIR/arc_timers.spec" << 'SPECFILE'
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['arc_timers.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('timers250.png', '.'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'PIL._tkinter_finder',
        'PIL.Image',
        'PIL.ImageTk',
        'requests',
        'bs4',
        'lxml',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'numpy', 'pandas', 'scipy', 'IPython', 'jupyter'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='arc-timers',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='timers250.png' if os.path.exists('timers250.png') else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=True,
    upx=True,
    upx_exclude=[],
    name='arc-timers',
)
SPECFILE

# Build with PyInstaller
if command -v pyinstaller >/dev/null 2>&1 || python3 -m pip show pyinstaller >/dev/null 2>&1; then
    echo "Building with PyInstaller..."
    cd "$BUILD_DIR"
    
    # Install PyInstaller if not available
    if ! command -v pyinstaller >/dev/null 2>&1; then
        echo "Installing PyInstaller..."
        python3 -m pip install --break-system-packages pyinstaller 2>/dev/null || \
        python3 -m pip install --user pyinstaller 2>/dev/null || \
        pip3 install --break-system-packages pyinstaller 2>/dev/null || \
        pip3 install --user pyinstaller
    fi
    
    # Install dependencies
    echo "Installing dependencies..."
    python3 -m pip install --break-system-packages -r requirements.txt 2>/dev/null || \
    python3 -m pip install --user -r requirements.txt 2>/dev/null || \
    pip3 install --break-system-packages -r requirements.txt 2>/dev/null || \
    pip3 install --user -r requirements.txt
    
    # Build executable
    echo "Building with PyInstaller..."
    python3 -m PyInstaller --clean --noconfirm arc_timers.spec || \
    pyinstaller --clean --noconfirm arc_timers.spec
    
    # Create AppDir structure
    mkdir -p "$APPDIR/usr/bin"
    mkdir -p "$APPDIR/usr/share/applications"
    mkdir -p "$APPDIR/usr/share/icons/hicolor/256x256/apps"
    mkdir -p "$APPDIR/usr/share/pixmaps"
    
    # Copy built executable (onedir mode)
    if [ -d "dist/arc-timers" ]; then
        cp -r "dist/arc-timers"/* "$APPDIR/usr/bin/"
        chmod +x "$APPDIR/usr/bin/arc-timers"
        echo "✓ Using onedir mode"
    elif [ -f "dist/arc-timers" ]; then
        cp "dist/arc-timers" "$APPDIR/usr/bin/"
        chmod +x "$APPDIR/usr/bin/arc-timers"
        echo "✓ Using onefile mode"
    else
        echo "PyInstaller build failed!"
        exit 1
    fi
else
    echo "Error: PyInstaller is required for building AppImage"
    echo "Install with: pip3 install --user pyinstaller"
    exit 1
fi

# Copy icon (from project root, not script dir)
cp "$PROJECT_ROOT/timers250.png" "$APPDIR/usr/share/pixmaps/arc-timers.png"
cp "$PROJECT_ROOT/timers250.png" "$APPDIR/usr/share/icons/hicolor/256x256/apps/arc-timers.png"

# Create .desktop file
cat > "$APPDIR/usr/share/applications/arc-timers.desktop" << 'EOF'
[Desktop Entry]
Type=Application
Name=ARC Raiders Event Timers
GenericName=Event Timer
Comment=Real-time ARC Raiders event countdown timers from MetaForge
Exec=arc-timers
Icon=arc-timers
Categories=Game;Utility;
Terminal=false
StartupNotify=true
Keywords=arc;raiders;events;timers;gaming;
EOF

# Create AppRun
cat > "$APPDIR/AppRun" << 'APPRUN'
#!/bin/bash
HERE="$(dirname "$(readlink -f "${0}")")"
export PATH="${HERE}/usr/bin:${PATH}"
export LD_LIBRARY_PATH="${HERE}/usr/lib:${LD_LIBRARY_PATH}"
cd "${HERE}/usr/bin"
exec ./arc-timers "$@"
APPRUN

chmod +x "$APPDIR/AppRun"

# Create symlinks
ln -sf usr/share/applications/arc-timers.desktop "$APPDIR/arc-timers.desktop"
ln -sf usr/share/pixmaps/arc-timers.png "$APPDIR/arc-timers.png"

# Download appimagetool if needed
if ! command -v appimagetool >/dev/null 2>&1; then
    echo "Downloading appimagetool..."
    mkdir -p "$BUILD_DIR/tools"
    cd "$BUILD_DIR/tools"
    if [ ! -f appimagetool-x86_64.AppImage ]; then
        wget -q https://github.com/AppImage/AppImageKit/releases/download/13/appimagetool-x86_64.AppImage || \
        wget -q https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
        chmod +x appimagetool-x86_64.AppImage
    fi
    APPIMAGETOOL="$BUILD_DIR/tools/appimagetool-x86_64.AppImage"
else
    APPIMAGETOOL="appimagetool"
fi

# Build AppImage
echo "Building AppImage..."
cd "$BUILD_DIR"
ARCH=x86_64 "$APPIMAGETOOL" "$APPDIR" "$APPIMAGE_NAME"

# Move to project root
mv "$APPIMAGE_NAME" "$PROJECT_ROOT/$APPIMAGE_NAME"
chmod +x "$PROJECT_ROOT/$APPIMAGE_NAME"

echo ""
echo "=== Build Complete ==="
echo "AppImage: $PROJECT_ROOT/$APPIMAGE_NAME"
echo ""
echo "The AppImage is compatible with all major Linux distributions"
echo ""
echo "To run: ./$APPIMAGE_NAME"

