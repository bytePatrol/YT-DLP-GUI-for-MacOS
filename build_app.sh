#!/bin/bash
#
# build_app.sh - Complete build system for YouTube 4K Downloader
# 
# This script handles:
#   - Auto-detecting the best Python version (prefers 3.13, avoids 3.14)
#   - Auto-installing Python 3.13 via Homebrew if needed
#   - Auto-fixing missing Tkinter support
#   - Generating setup.py configuration
#   - Updating yt-dlp to the latest version
#   - Building the macOS app with py2app
#   - Bundling ffmpeg and deno for a self-contained app
#   - Creating DMG installer with background and icons
#   - Installing to Applications folder
#
# Python Detection (fully automatic):
#   1. Searches for Python 3.13/3.12/3.11/3.10 with working Tkinter
#   2. If Tkinter is broken, automatically installs python-tk via Homebrew
#   3. If no suitable Python exists, offers to install Python 3.13
#   4. Supports both Apple Silicon (/opt/homebrew/) and Intel (/usr/local/)
#
# Usage:
#   ./build_app.sh                      # Build with current .py file
#   ./build_app.sh yt_dlp_gui_v18.py    # Build with a new version
#   ./build_app.sh --update-ytdlp       # Just update yt-dlp, no build
#   ./build_app.sh --dmg                # Just create DMG (skip build)
#   ./build_app.sh --help               # Show help
#
# Author: bytePatrol
#

# ============================================================================
# CONFIGURATION
# ============================================================================

# Auto-detect project directory (where this script is located)
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$PROJECT_DIR/venv"
# Auto-detect latest yt_dlp_gui script or use default
_detect_main_script() {
    # Find the highest version yt_dlp_gui_v*.py file
    local latest=$(ls -1 "$PROJECT_DIR"/yt_dlp_gui_v*.py 2>/dev/null | sort -V | tail -1)
    if [ -n "$latest" ]; then
        echo "$(basename "$latest")"
    else
        echo "yt_dlp_gui_v18_0_8.py"
    fi
}

MAIN_SCRIPT="$(_detect_main_script)"  # Auto-detect latest script
APP_NAME="YouTube 4K Downloader"
BUNDLE_ID="com.bytepatrol.youtube4kdownloader"
INSTALL_DIR="/Applications"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Global variable to store built app path
BUILT_APP_PATH=""

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

print_header() {
    echo ""
    echo -e "${CYAN}==========================================${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}==========================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}[OK] $1${NC}"
}

print_error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}[WARN] $1${NC}"
}

print_info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

show_help() {
    echo ""
    echo "YouTube 4K Downloader Build Script"
    echo ""
    echo "Usage:"
    echo "  ./build_app.sh                      Build with current .py file"
    echo "  ./build_app.sh <file.py>            Build with a new Python file"
    echo "  ./build_app.sh --update-ytdlp       Just update yt-dlp (no build)"
    echo "  ./build_app.sh --check-updates      Check for yt-dlp updates"
    echo "  ./build_app.sh --dmg                Just create DMG (skip build)"
    echo "  ./build_app.sh --clean              Clean build artifacts"
    echo "  ./build_app.sh --help               Show this help"
    echo ""
    echo "Examples:"
    echo "  ./build_app.sh yt_dlp_gui_v18.py    Build new version"
    echo "  ./build_app.sh --update-ytdlp       Update yt-dlp before building"
    echo "  ./build_app.sh --dmg                Create DMG from existing build"
    echo ""
    echo "Python Detection:"
    echo "  The script automatically finds the best Python version:"
    echo "  - Prefers Python 3.13, 3.12, 3.11, 3.10 (in that order)"
    echo "  - Avoids Python 3.14 (Tcl/Tk threading issues)"
    echo "  - Checks Homebrew locations (Apple Silicon and Intel)"
    echo "  - Falls back to system python3 if needed"
    echo ""
}

# ============================================================================
# PYTHON DETECTION & AUTO-INSTALLATION
# ============================================================================

# Global variable to store the detected Python path
DETECTED_PYTHON=""

test_python_tkinter() {
    # Test if a Python interpreter has working Tkinter
    # Returns 0 if Tkinter works, 1 if it doesn't
    local python_path="$1"
    "$python_path" -c "import tkinter" 2>/dev/null
    return $?
}

check_homebrew() {
    # Check if Homebrew is installed
    if command -v brew &> /dev/null; then
        return 0
    else
        return 1
    fi
}

auto_install_python() {
    # Attempt to automatically install Python 3.13 with Tkinter via Homebrew
    # Returns 0 on success, 1 on failure
    
    echo ""
    print_info "This build requires Python with Tkinter (GUI) support."
    print_info "No suitable Python installation was found on your system."
    echo ""
    
    if ! check_homebrew; then
        print_error "Homebrew is not installed."
        echo ""
        echo "  To install Homebrew, run:"
        echo ""
        echo '    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        echo ""
        echo "  Then re-run this build script."
        echo ""
        return 1
    fi
    
    echo "┌─────────────────────────────────────────────────────────────────┐"
    echo "│  AUTOMATIC SETUP                                                │"
    echo "├─────────────────────────────────────────────────────────────────┤"
    echo "│  This script can automatically install the required Python      │"
    echo "│  version (3.13) with GUI support via Homebrew.                  │"
    echo "│                                                                 │"
    echo "│  The following will be installed:                               │"
    echo "│    • python@3.13      (Python interpreter)                      │"
    echo "│    • python-tk@3.13   (Tkinter GUI support)                     │"
    echo "└─────────────────────────────────────────────────────────────────┘"
    echo ""
    
    # Check if running interactively
    if [ -t 0 ]; then
        # Interactive mode - ask for confirmation
        read -p "Would you like to install Python 3.13 now? [Y/n] " -n 1 -r
        echo ""
        
        if [[ ! $REPLY =~ ^[Yy]$ ]] && [[ ! -z $REPLY ]]; then
            print_info "Installation cancelled."
            print_info "You can manually install with: brew install python@3.13 python-tk@3.13"
            return 1
        fi
    else
        # Non-interactive mode - proceed with installation
        print_info "Non-interactive mode detected. Proceeding with automatic installation..."
    fi
    
    echo ""
    print_info "Installing Python 3.13 with Tkinter support..."
    echo ""
    
    # Install python-tk first (it's a dependency for GUI apps)
    if ! brew install python-tk@3.13 2>&1; then
        print_warning "python-tk@3.13 installation had issues, continuing..."
    fi
    
    # Install Python 3.13
    if ! brew install python@3.13 2>&1; then
        print_error "Failed to install Python 3.13"
        return 1
    fi
    
    echo ""
    print_success "Python 3.13 installed successfully!"
    echo ""
    
    # Verify the installation
    local new_python="/opt/homebrew/opt/python@3.13/bin/python3"
    if [ ! -x "$new_python" ]; then
        # Try Intel location
        new_python="/usr/local/opt/python@3.13/bin/python3"
    fi
    
    if [ -x "$new_python" ] && test_python_tkinter "$new_python"; then
        DETECTED_PYTHON="$new_python"
        return 0
    else
        print_error "Python was installed but Tkinter still isn't working."
        print_info "Try running: brew reinstall python-tk@3.13 python@3.13"
        return 1
    fi
}

try_fix_tkinter() {
    # Attempt to fix Tkinter for a specific Python version
    # $1 = Python version (e.g., "3.14")
    local version="$1"
    
    if ! check_homebrew; then
        return 1
    fi
    
    print_info "Attempting to install Tkinter support for Python $version..."
    
    if brew install "python-tk@$version" 2>&1; then
        print_success "python-tk@$version installed"
        return 0
    else
        return 1
    fi
}

find_python() {
    # Find the best available Python 3 interpreter with working Tkinter
    # Priority: Python 3.13 > 3.12 > 3.11 > 3.10 (avoiding 3.14 due to Tcl/Tk threading issues)
    # Will attempt to auto-install if no suitable Python is found
    # Sets DETECTED_PYTHON global variable
    
    DETECTED_PYTHON=""
    
    # Preferred versions in order (3.13 is ideal, avoid 3.14)
    local PREFERRED_VERSIONS=("3.13" "3.12" "3.11" "3.10")
    
    # Fallback versions (we'll use these if nothing else works, but warn about issues)
    local FALLBACK_VERSIONS=("3.14" "3.9")
    
    # Locations to check for each version
    local HOMEBREW_APPLE="/opt/homebrew/opt/python@VERSION/bin/python3"
    local HOMEBREW_INTEL="/usr/local/opt/python@VERSION/bin/python3"
    local HOMEBREW_GENERIC_APPLE="/opt/homebrew/bin/python3"
    local HOMEBREW_GENERIC_INTEL="/usr/local/bin/python3"
    
    # Track Python installations with broken Tkinter (we might try to fix them)
    local BROKEN_TKINTER_VERSIONS=()
    
    # First, try to find preferred versions in Homebrew
    for version in "${PREFERRED_VERSIONS[@]}"; do
        # Check Apple Silicon Homebrew
        local apple_path="${HOMEBREW_APPLE/VERSION/$version}"
        if [ -x "$apple_path" ]; then
            if test_python_tkinter "$apple_path"; then
                DETECTED_PYTHON="$apple_path"
                print_info "Found Python $version at: $apple_path"
                break
            else
                BROKEN_TKINTER_VERSIONS+=("$version")
            fi
        fi
        
        # Check Intel Homebrew
        local intel_path="${HOMEBREW_INTEL/VERSION/$version}"
        if [ -x "$intel_path" ]; then
            if test_python_tkinter "$intel_path"; then
                DETECTED_PYTHON="$intel_path"
                print_info "Found Python $version at: $intel_path"
                break
            else
                BROKEN_TKINTER_VERSIONS+=("$version")
            fi
        fi
    done
    
    # If no preferred version found, check fallback versions
    if [ -z "$DETECTED_PYTHON" ]; then
        for version in "${FALLBACK_VERSIONS[@]}"; do
            local apple_path="${HOMEBREW_APPLE/VERSION/$version}"
            local intel_path="${HOMEBREW_INTEL/VERSION/$version}"
            
            if [ -x "$apple_path" ]; then
                if test_python_tkinter "$apple_path"; then
                    DETECTED_PYTHON="$apple_path"
                    print_info "Found Python $version at: $apple_path"
                    break
                else
                    BROKEN_TKINTER_VERSIONS+=("$version")
                fi
            elif [ -x "$intel_path" ]; then
                if test_python_tkinter "$intel_path"; then
                    DETECTED_PYTHON="$intel_path"
                    print_info "Found Python $version at: $intel_path"
                    break
                else
                    BROKEN_TKINTER_VERSIONS+=("$version")
                fi
            fi
        done
    fi
    
    # If still nothing, try generic Homebrew python3
    if [ -z "$DETECTED_PYTHON" ]; then
        if [ -x "$HOMEBREW_GENERIC_APPLE" ]; then
            if test_python_tkinter "$HOMEBREW_GENERIC_APPLE"; then
                DETECTED_PYTHON="$HOMEBREW_GENERIC_APPLE"
                print_info "Found Python at: $HOMEBREW_GENERIC_APPLE"
            fi
        fi
        
        if [ -z "$DETECTED_PYTHON" ] && [ -x "$HOMEBREW_GENERIC_INTEL" ]; then
            if test_python_tkinter "$HOMEBREW_GENERIC_INTEL"; then
                DETECTED_PYTHON="$HOMEBREW_GENERIC_INTEL"
                print_info "Found Python at: $HOMEBREW_GENERIC_INTEL"
            fi
        fi
    fi
    
    # Last resort: system python3
    if [ -z "$DETECTED_PYTHON" ]; then
        if command -v python3 &> /dev/null; then
            local sys_python=$(command -v python3)
            if test_python_tkinter "$sys_python"; then
                DETECTED_PYTHON="$sys_python"
                print_info "Using system Python: $DETECTED_PYTHON"
            fi
        fi
    fi
    
    # If we found Python installations with broken Tkinter, try to fix them
    if [ -z "$DETECTED_PYTHON" ] && [ ${#BROKEN_TKINTER_VERSIONS[@]} -gt 0 ]; then
        echo ""
        print_warning "Found Python installations but Tkinter (GUI support) is missing."
        
        # Try to fix the first broken version
        local version_to_fix="${BROKEN_TKINTER_VERSIONS[0]}"
        
        if check_homebrew; then
            echo ""
            print_info "Attempting to install Tkinter support for Python $version_to_fix..."
            echo ""
            
            if brew install "python-tk@$version_to_fix" 2>&1; then
                # Re-check if it works now
                local apple_path="${HOMEBREW_APPLE/VERSION/$version_to_fix}"
                local intel_path="${HOMEBREW_INTEL/VERSION/$version_to_fix}"
                
                if [ -x "$apple_path" ] && test_python_tkinter "$apple_path"; then
                    DETECTED_PYTHON="$apple_path"
                    echo ""
                    print_success "Tkinter support installed successfully!"
                    print_info "Found Python $version_to_fix at: $apple_path"
                elif [ -x "$intel_path" ] && test_python_tkinter "$intel_path"; then
                    DETECTED_PYTHON="$intel_path"
                    echo ""
                    print_success "Tkinter support installed successfully!"
                    print_info "Found Python $version_to_fix at: $intel_path"
                fi
            fi
        fi
    fi
    
    # If still no working Python, offer to install one
    if [ -z "$DETECTED_PYTHON" ]; then
        if auto_install_python; then
            # DETECTED_PYTHON is set by auto_install_python on success
            # Delete any existing venv since we have a new Python
            if [ -d "$VENV_DIR" ]; then
                print_info "Removing old virtual environment..."
                rm -rf "$VENV_DIR"
            fi
        else
            echo ""
            print_error "Unable to find or install a suitable Python environment."
            echo ""
            echo "  Manual installation options:"
            echo ""
            echo "  1. Install Python 3.13 (recommended):"
            echo "     brew install python@3.13 python-tk@3.13"
            echo ""
            echo "  2. Fix Tkinter for your existing Python:"
            echo "     brew install python-tk@3.14"
            echo "     brew reinstall python@3.14"
            echo ""
            echo "  After installing, delete the 'venv' folder and re-run this script."
            echo ""
            exit 1
        fi
    fi
    
    # Check Python version for warnings
    local PY_VERSION=$("$DETECTED_PYTHON" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null)
    
    if [ -z "$PY_VERSION" ]; then
        print_error "Could not determine Python version from: $DETECTED_PYTHON"
        exit 1
    fi
    
    # Warn about Python 3.14 (Tcl/Tk threading issues in some cases)
    if [[ "$PY_VERSION" == "3.14" ]]; then
        print_warning "Python 3.14 in use - if you experience GUI issues, consider Python 3.13"
    fi
    
    # Warn about old versions
    local MINOR_VERSION="${PY_VERSION#3.}"
    if [ "$MINOR_VERSION" -lt 10 ] 2>/dev/null; then
        print_warning "Python $PY_VERSION detected - version 3.10+ recommended"
    fi
    
    print_success "Using Python $PY_VERSION ($DETECTED_PYTHON)"
}

activate_venv() {
    if [ ! -f "$VENV_DIR/bin/activate" ]; then
        print_warning "Virtual environment not found at $VENV_DIR"
        print_info "Creating virtual environment..."
        
        # Find the best Python interpreter (sets DETECTED_PYTHON)
        find_python
        
        if [ -z "$DETECTED_PYTHON" ]; then
            print_error "Failed to find Python interpreter"
            exit 1
        fi
        
        # Create virtual environment
        "$DETECTED_PYTHON" -m venv "$VENV_DIR"
        
        if [ $? -ne 0 ]; then
            print_error "Failed to create virtual environment"
            print_info "Python used: $DETECTED_PYTHON"
            exit 1
        fi
        
        print_success "Virtual environment created"
        
        # Activate and install dependencies
        source "$VENV_DIR/bin/activate"
        
        print_info "Installing required packages..."
        pip install --upgrade pip
        pip install py2app customtkinter pillow requests yt-dlp darkdetect idna urllib3 charset-normalizer certifi psutil
        
        if [ $? -ne 0 ]; then
            print_error "Failed to install dependencies"
            exit 1
        fi
        
        print_success "All dependencies installed"
    else
        source "$VENV_DIR/bin/activate"
        
        # CRITICAL: Verify Tkinter works in this venv
        if ! python -c "import tkinter" 2>/dev/null; then
            print_warning "Existing virtual environment has broken Tkinter!"
            print_info "Rebuilding virtual environment..."
            
            # Deactivate and remove the broken venv
            deactivate 2>/dev/null || true
            rm -rf "$VENV_DIR"
            
            # Find a working Python (sets DETECTED_PYTHON)
            find_python
            
            if [ -z "$DETECTED_PYTHON" ]; then
                print_error "Failed to find Python interpreter with working Tkinter"
                exit 1
            fi
            
            # Create new virtual environment
            print_info "Creating new virtual environment..."
            "$DETECTED_PYTHON" -m venv "$VENV_DIR"
            
            if [ $? -ne 0 ]; then
                print_error "Failed to create virtual environment"
                print_info "Python used: $DETECTED_PYTHON"
                exit 1
            fi
            
            print_success "Virtual environment created"
            
            # Activate and install dependencies
            source "$VENV_DIR/bin/activate"
            
            print_info "Installing required packages..."
            pip install --upgrade pip
            pip install py2app customtkinter pillow requests yt-dlp darkdetect idna urllib3 charset-normalizer certifi psutil
            
            if [ $? -ne 0 ]; then
                print_error "Failed to install dependencies"
                exit 1
            fi
            
            print_success "All dependencies installed"
        else
            print_success "Virtual environment activated"
            
            # Check if psutil is installed (required for v18.0.0+)
            if ! python -c "import psutil" 2>/dev/null; then
                print_warning "psutil not found in existing venv, installing..."
                pip install psutil
                if [ $? -ne 0 ]; then
                    print_error "Failed to install psutil"
                    exit 1
                fi
                print_success "psutil installed"
            fi
        fi
    fi
}

deactivate_venv() {
    if command -v deactivate &> /dev/null; then
        deactivate 2>/dev/null || true
    fi
}

# ============================================================================
# GENERATE SETUP.PY
# ============================================================================

generate_setup_py() {
    local PY_FILE="$1"
    local VERSION="$2"
    
    print_info "Generating setup.py for $PY_FILE (v$VERSION)"
    
    cat > "$PROJECT_DIR/setup.py" << 'SETUP_EOF'
"""
Setup script for creating a macOS .app bundle for YouTube 4K Downloader
Auto-generated by build_app.sh
"""

from setuptools import setup
import os
import sys
import tkinter
import shutil

# Path to your app icon (in assets folder)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(SCRIPT_DIR, 'assets', 'icon.icns')

# Verify icon exists
if os.path.isfile(ICON_PATH):
    print(f"[OK] Found icon at: {ICON_PATH}")
else:
    print(f"[WARN] Icon not found at: {ICON_PATH}")
    ICON_PATH = None

# Find Tcl/Tk library paths for bundling
def find_tcl_tk():
    """Find Tcl/Tk frameworks/libraries to bundle."""
    tcl_paths = []
    
    # Get the Tcl/Tk library that Python is actually using
    try:
        tcl_lib = tkinter.Tcl().eval('info library')
        if tcl_lib and os.path.exists(tcl_lib):
            # Get parent directories to find the framework
            tcl_root = os.path.dirname(os.path.dirname(tcl_lib))
            if os.path.exists(tcl_root):
                print(f"[OK] Found Tcl at: {tcl_root}")
                tcl_paths.append(tcl_root)
    except Exception as e:
        print(f"[WARN] Could not detect Tcl/Tk path: {e}")
    
    # Also check common Homebrew locations
    homebrew_paths = [
        '/opt/homebrew/opt/tcl-tk/lib',  # Apple Silicon
        '/usr/local/opt/tcl-tk/lib',      # Intel
    ]
    for path in homebrew_paths:
        if os.path.isdir(path):
            print(f"[OK] Found Homebrew Tcl/Tk at: {path}")
            tcl_paths.append(path)
            break
    
    return tcl_paths

tcl_tk_paths = find_tcl_tk()

SETUP_EOF

    # Now append the rest with variable substitution
    cat >> "$PROJECT_DIR/setup.py" << SETUP_EOF

APP = ['$PY_FILE']
DATA_FILES = []

# Build frameworks list for Tcl/Tk
frameworks_to_include = []
for tcl_path in tcl_tk_paths:
    tcl_fw = os.path.join(tcl_path, 'Tcl.framework')
    tk_fw = os.path.join(tcl_path, 'Tk.framework')
    if os.path.isdir(tcl_fw):
        frameworks_to_include.append(tcl_fw)
    if os.path.isdir(tk_fw):
        frameworks_to_include.append(tk_fw)

if frameworks_to_include:
    print(f"[OK] Will bundle frameworks: {frameworks_to_include}")

OPTIONS = {
    'argv_emulation': False,
    'iconfile': ICON_PATH,
    'plist': {
        'CFBundleName': '$APP_NAME',
        'CFBundleDisplayName': '$APP_NAME',
        'CFBundleGetInfoString': "Modern YouTube downloader for macOS - 100% Standalone",
        'CFBundleIdentifier': "$BUNDLE_ID",
        'CFBundleVersion': "$VERSION",
        'CFBundleShortVersionString': "$VERSION",
        'NSHumanReadableCopyright': "Copyright 2025 bytePatrol. All rights reserved.",
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.13',
    },
    'frameworks': [],  # Don't bundle Tcl/Tk - let system handle it
    'packages': [
        'customtkinter',
        'tkinter',
        'PIL',
        'requests',
        'certifi',
        'charset_normalizer',
        'yt_dlp',
        'idna',
        'urllib3',
        'darkdetect',
        'psutil',
    ],
    'includes': [
        'subprocess',
        'json',
        'threading',
        'queue',
        'pathlib',
        'dataclasses',
        'typing',
        'enum',
        'hashlib',
        'tempfile',
        'shlex',
        'urllib.request',
        '_tkinter',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'PIL.Image',
        'PIL.ImageTk',
    ],
    'excludes': [
        'numpy',
        'scipy',
        'matplotlib',
        'pandas',
        'IPython',
        'jupyter',
        'notebook',
        'test',
        'tests',
    ],
    'semi_standalone': False,
    'site_packages': True,
    'strip': False,
}

setup(
    name='$APP_NAME',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
SETUP_EOF

    print_success "setup.py generated"
}

# ============================================================================
# UPDATE YT-DLP
# ============================================================================

check_ytdlp_updates() {
    print_header "Checking for yt-dlp Updates"
    
    activate_venv
    
    CURRENT_VERSION=$(pip show yt-dlp 2>/dev/null | grep "Version:" | awk '{print $2}')
    echo "Current version: $CURRENT_VERSION"
    
    # Check PyPI for latest version
    LATEST_VERSION=$(pip index versions yt-dlp 2>/dev/null | grep -oE '[0-9]{4}\.[0-9]{1,2}\.[0-9]{1,2}' | head -1)
    
    if [ -z "$LATEST_VERSION" ]; then
        # Fallback method
        LATEST_VERSION=$(pip install yt-dlp== 2>&1 | grep -oE '[0-9]{4}\.[0-9]{1,2}\.[0-9]{1,2}' | tail -1)
    fi
    
    echo "Latest version:  $LATEST_VERSION"
    
    deactivate_venv
    
    if [ "$CURRENT_VERSION" = "$LATEST_VERSION" ]; then
        print_success "yt-dlp is up to date!"
        return 1  # No update needed
    else
        print_warning "Update available: $CURRENT_VERSION -> $LATEST_VERSION"
        return 0  # Update available
    fi
}

update_ytdlp() {
    print_header "Updating yt-dlp"
    
    activate_venv
    
    BEFORE_VERSION=$(pip show yt-dlp 2>/dev/null | grep "Version:" | awk '{print $2}')
    print_info "Current version: $BEFORE_VERSION"
    
    echo ""
    echo "Updating yt-dlp..."
    pip install --upgrade yt-dlp
    
    AFTER_VERSION=$(pip show yt-dlp 2>/dev/null | grep "Version:" | awk '{print $2}')
    
    echo ""
    if [ "$BEFORE_VERSION" = "$AFTER_VERSION" ]; then
        print_success "yt-dlp is already at the latest version: $AFTER_VERSION"
    else
        print_success "yt-dlp updated: $BEFORE_VERSION -> $AFTER_VERSION"
    fi
    
    deactivate_venv
}

# ============================================================================
# CLEAN BUILD
# ============================================================================

clean_build() {
    print_header "Cleaning Build Artifacts"
    
    cd "$PROJECT_DIR"
    
    if [ -d "build" ]; then
        rm -rf build
        print_success "Removed build/"
    fi
    
    if [ -d "dist" ]; then
        rm -rf dist
        print_success "Removed dist/"
    fi
    
    # Remove .pyc files
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    
    print_success "Clean complete"
}

# ============================================================================
# BUNDLE DEPENDENCIES (ffmpeg + deno + Tcl/Tk)
# ============================================================================

bundle_dependencies() {
    local APP_PATH="$1"
    local RESOURCES_DIR="$APP_PATH/Contents/Resources"
    local FRAMEWORKS_DIR="$APP_PATH/Contents/Frameworks"
    
    print_header "Bundling Dependencies (ffmpeg + deno)"
    
    echo "App path: $APP_PATH"
    echo "Resources dir: $RESOURCES_DIR"
    
    if [ ! -d "$APP_PATH" ]; then
        print_error "App not found at: $APP_PATH"
        echo "Contents of dist/:"
        ls -la "$PROJECT_DIR/dist/" 2>/dev/null || echo "dist/ not found"
        return 1
    fi
    
    if [ ! -d "$RESOURCES_DIR" ]; then
        print_error "Resources directory not found at: $RESOURCES_DIR"
        return 1
    fi
    
    # Create Frameworks directory if it doesn't exist
    mkdir -p "$FRAMEWORKS_DIR"
    
    TEMP_DIR=$(mktemp -d)
    cd "$TEMP_DIR"
    
    # --- Bundle Tcl/Tk ---
    # This is CRITICAL for standalone apps - without this, the app will fail
    # on systems that don't have Homebrew's Tcl/Tk installed
    print_info "Bundling Tcl/Tk libraries..."
    
    # Find where Python's tkinter expects Tcl/Tk
    TCL_VERSION=""
    TCL_LIB_DIR=""
    
    # Check Homebrew locations (Apple Silicon and Intel)
    if [ -d "/opt/homebrew/opt/tcl-tk/lib" ]; then
        TCL_LIB_DIR="/opt/homebrew/opt/tcl-tk/lib"
        # Detect version (tcl9.0, tcl8.6, etc.)
        if [ -d "$TCL_LIB_DIR/tcl9.0" ]; then
            TCL_VERSION="9.0"
        elif [ -d "$TCL_LIB_DIR/tcl8.6" ]; then
            TCL_VERSION="8.6"
        fi
    elif [ -d "/usr/local/opt/tcl-tk/lib" ]; then
        TCL_LIB_DIR="/usr/local/opt/tcl-tk/lib"
        if [ -d "$TCL_LIB_DIR/tcl9.0" ]; then
            TCL_VERSION="9.0"
        elif [ -d "$TCL_LIB_DIR/tcl8.6" ]; then
            TCL_VERSION="8.6"
        fi
    fi
    
    if [ -n "$TCL_VERSION" ] && [ -n "$TCL_LIB_DIR" ]; then
        print_info "Found Tcl/Tk $TCL_VERSION at $TCL_LIB_DIR"
        
        # Create lib directory in app bundle
        mkdir -p "$APP_PATH/Contents/lib"
        
        # Copy Tcl library folder
        if [ -d "$TCL_LIB_DIR/tcl$TCL_VERSION" ]; then
            cp -R "$TCL_LIB_DIR/tcl$TCL_VERSION" "$APP_PATH/Contents/lib/"
            print_success "Copied tcl$TCL_VERSION library"
        fi
        
        # Copy Tk library folder
        if [ -d "$TCL_LIB_DIR/tk$TCL_VERSION" ]; then
            cp -R "$TCL_LIB_DIR/tk$TCL_VERSION" "$APP_PATH/Contents/lib/"
            print_success "Copied tk$TCL_VERSION library"
        fi
        
        # Copy dynamic libraries (.dylib files)
        mkdir -p "$FRAMEWORKS_DIR"
        
        # Copy Tcl dylib
        for tcl_dylib in "$TCL_LIB_DIR"/libtcl*.dylib; do
            if [ -f "$tcl_dylib" ]; then
                cp "$tcl_dylib" "$FRAMEWORKS_DIR/"
                print_success "Copied $(basename "$tcl_dylib")"
            fi
        done
        
        # Copy Tk dylib
        for tk_dylib in "$TCL_LIB_DIR"/libtk*.dylib; do
            if [ -f "$tk_dylib" ]; then
                cp "$tk_dylib" "$FRAMEWORKS_DIR/"
                print_success "Copied $(basename "$tk_dylib")"
            fi
        done
        
        # Also check for tcl9 and tk9 specific dylibs (Tcl 9.0 naming)
        if [ -f "$TCL_LIB_DIR/libtcl9.0.dylib" ]; then
            cp "$TCL_LIB_DIR/libtcl9.0.dylib" "$FRAMEWORKS_DIR/"
        fi
        if [ -f "$TCL_LIB_DIR/libtk9.0.dylib" ]; then
            cp "$TCL_LIB_DIR/libtk9.0.dylib" "$FRAMEWORKS_DIR/"
        fi
        
        # --- Bundle Tcl/Tk dependencies (libtommath, etc.) ---
        # Tcl 9.0 depends on libtommath for big number support
        print_info "Bundling Tcl/Tk dependencies..."
        
        # Find and copy libtommath
        LIBTOMMATH_PATHS=(
            "/opt/homebrew/opt/libtommath/lib/libtommath.1.dylib"
            "/opt/homebrew/lib/libtommath.1.dylib"
            "/usr/local/opt/libtommath/lib/libtommath.1.dylib"
            "/usr/local/lib/libtommath.1.dylib"
        )
        
        LIBTOMMATH_FOUND=false
        for tommath_path in "${LIBTOMMATH_PATHS[@]}"; do
            if [ -f "$tommath_path" ]; then
                cp "$tommath_path" "$FRAMEWORKS_DIR/"
                print_success "Copied libtommath.1.dylib"
                LIBTOMMATH_FOUND=true
                
                # Also copy the unversioned symlink target if it exists
                tommath_dir=$(dirname "$tommath_path")
                if [ -f "$tommath_dir/libtommath.dylib" ]; then
                    cp "$tommath_dir/libtommath.dylib" "$FRAMEWORKS_DIR/" 2>/dev/null || true
                fi
                break
            fi
        done
        
        if [ "$LIBTOMMATH_FOUND" = false ]; then
            print_warning "libtommath not found - Tcl 9.0 may not work!"
            print_info "Install with: brew install libtommath"
        fi
        
        # Use otool to find ALL dependencies of bundled dylibs and copy them
        print_info "Checking for additional Tcl/Tk dependencies..."
        
        for dylib in "$FRAMEWORKS_DIR"/*.dylib; do
            if [ -f "$dylib" ]; then
                # Get all dependencies
                deps=$(otool -L "$dylib" 2>/dev/null | grep -E "^\s+/opt/homebrew|^\s+/usr/local" | awk '{print $1}')
                
                for dep in $deps; do
                    dep_name=$(basename "$dep")
                    
                    # Skip if already copied
                    if [ -f "$FRAMEWORKS_DIR/$dep_name" ]; then
                        continue
                    fi
                    
                    # Copy the dependency
                    if [ -f "$dep" ]; then
                        cp "$dep" "$FRAMEWORKS_DIR/"
                        print_success "Copied dependency: $dep_name"
                    fi
                done
            fi
        done
        
        # --- Fix library paths using install_name_tool ---
        # Change hardcoded Homebrew paths to use @executable_path/../Frameworks
        print_info "Fixing library paths for standalone use..."
        
        for dylib in "$FRAMEWORKS_DIR"/*.dylib; do
            if [ -f "$dylib" ]; then
                dylib_name=$(basename "$dylib")
                
                # Change the install name of this library to use @rpath
                install_name_tool -id "@rpath/$dylib_name" "$dylib" 2>/dev/null || true
                
                # Find and fix references to Homebrew paths
                deps=$(otool -L "$dylib" 2>/dev/null | grep -E "^\s+/opt/homebrew|^\s+/usr/local" | awk '{print $1}')
                
                for dep in $deps; do
                    dep_name=$(basename "$dep")
                    # Change the path to use @rpath
                    install_name_tool -change "$dep" "@rpath/$dep_name" "$dylib" 2>/dev/null || true
                done
            fi
        done
        
        print_success "Library paths fixed for standalone deployment"
        
        # --- Also fix _tkinter.so in the app bundle ---
        # The _tkinter Python module also has hardcoded paths
        print_info "Fixing _tkinter.so library paths..."
        
        TKINTER_SO=$(find "$APP_PATH/Contents/Resources" -name "_tkinter*.so" -o -name "_tkinter*.dylib" 2>/dev/null | head -1)
        
        if [ -n "$TKINTER_SO" ] && [ -f "$TKINTER_SO" ]; then
            print_info "Found _tkinter at: $TKINTER_SO"
            
            # Get dependencies and fix them
            deps=$(otool -L "$TKINTER_SO" 2>/dev/null | grep -E "^\s+/opt/homebrew|^\s+/usr/local" | awk '{print $1}')
            
            for dep in $deps; do
                dep_name=$(basename "$dep")
                
                # Make sure the dependency is in Frameworks
                if [ ! -f "$FRAMEWORKS_DIR/$dep_name" ] && [ -f "$dep" ]; then
                    cp "$dep" "$FRAMEWORKS_DIR/"
                    print_success "Copied missing dependency: $dep_name"
                fi
                
                # Fix the path in _tkinter.so
                install_name_tool -change "$dep" "@rpath/$dep_name" "$TKINTER_SO" 2>/dev/null || true
            done
            
            # Add rpath to _tkinter.so so it can find Frameworks
            install_name_tool -add_rpath "@executable_path/../Frameworks" "$TKINTER_SO" 2>/dev/null || true
            install_name_tool -add_rpath "@loader_path/../../Frameworks" "$TKINTER_SO" 2>/dev/null || true
            
            print_success "_tkinter.so paths fixed"
        else
            print_warning "_tkinter.so not found - may need manual fixing"
        fi
        
        # --- Fix all .so files in lib-dynload ---
        print_info "Fixing all Python extension modules..."
        
        LIB_DYNLOAD=$(find "$APP_PATH/Contents/Resources" -type d -name "lib-dynload" 2>/dev/null | head -1)
        
        if [ -n "$LIB_DYNLOAD" ] && [ -d "$LIB_DYNLOAD" ]; then
            for so_file in "$LIB_DYNLOAD"/*.so; do
                if [ -f "$so_file" ]; then
                    # Add rpath
                    install_name_tool -add_rpath "@executable_path/../Frameworks" "$so_file" 2>/dev/null || true
                    
                    # Fix any Homebrew dependencies
                    deps=$(otool -L "$so_file" 2>/dev/null | grep -E "^\s+/opt/homebrew|^\s+/usr/local" | awk '{print $1}')
                    
                    for dep in $deps; do
                        dep_name=$(basename "$dep")
                        
                        # Copy if not already in Frameworks
                        if [ ! -f "$FRAMEWORKS_DIR/$dep_name" ] && [ -f "$dep" ]; then
                            cp "$dep" "$FRAMEWORKS_DIR/"
                            print_success "Copied: $dep_name"
                        fi
                        
                        # Fix the reference
                        install_name_tool -change "$dep" "@rpath/$dep_name" "$so_file" 2>/dev/null || true
                    done
                fi
            done
            print_success "All extension modules fixed"
        fi
        
        print_info "Tcl/Tk bundled successfully"
    else
        print_warning "Could not find Homebrew Tcl/Tk installation"
        print_warning "The app may not work on systems without Tcl/Tk installed"
        print_info "Install with: brew install tcl-tk"
    fi
    
    # --- Install FFmpeg ---
    echo ""
    echo "Downloading static ffmpeg..."
    if curl -L --progress-bar "https://evermeet.cx/ffmpeg/getrelease/ffmpeg/zip" -o ffmpeg.zip; then
        unzip -q ffmpeg.zip
        
        if [ -f "ffmpeg" ]; then
            cp ffmpeg "$RESOURCES_DIR/ffmpeg"
            chmod +x "$RESOURCES_DIR/ffmpeg"
            print_success "FFmpeg installed ($(ls -lh "$RESOURCES_DIR/ffmpeg" | awk '{print $5}'))"
        else
            print_error "FFmpeg not found in zip"
            cd /
            rm -rf "$TEMP_DIR"
            return 1
        fi
    else
        print_error "FFmpeg download failed"
        cd /
        rm -rf "$TEMP_DIR"
        return 1
    fi
    
    # --- Install Deno ---
    ARCH=$(uname -m)
    if [ "$ARCH" = "arm64" ]; then
        DENO_ARCH="aarch64"
    else
        DENO_ARCH="x86_64"
    fi
    
    echo ""
    echo "Downloading deno for $DENO_ARCH..."
    if curl -L --progress-bar "https://github.com/denoland/deno/releases/latest/download/deno-${DENO_ARCH}-apple-darwin.zip" -o deno.zip; then
        unzip -q -o deno.zip
        
        if [ -f "deno" ]; then
            cp deno "$RESOURCES_DIR/deno"
            chmod +x "$RESOURCES_DIR/deno"
            print_success "Deno installed ($(ls -lh "$RESOURCES_DIR/deno" | awk '{print $5}'))"
        else
            print_error "Deno not found in zip"
            cd /
            rm -rf "$TEMP_DIR"
            return 1
        fi
    else
        print_error "Deno download failed"
        cd /
        rm -rf "$TEMP_DIR"
        return 1
    fi
    
    # Cleanup
    cd /
    rm -rf "$TEMP_DIR"
    
    echo ""
    print_success "All dependencies bundled successfully!"
    return 0
}

# ============================================================================
# VERIFY APP
# ============================================================================

verify_app() {
    local APP_PATH="$1"
    
    print_header "Verifying Built App"
    
    if [ ! -d "$APP_PATH" ]; then
        print_error "App not found at: $APP_PATH"
        return 1
    fi
    
    local RESOURCES_DIR="$APP_PATH/Contents/Resources"
    local FRAMEWORKS_DIR="$APP_PATH/Contents/Frameworks"
    local ERRORS=0
    
    # Check bundled executables
    echo "Checking bundled executables..."
    if [ -f "$RESOURCES_DIR/ffmpeg" ]; then
        print_success "ffmpeg present"
    else
        print_error "ffmpeg missing!"
        ERRORS=$((ERRORS + 1))
    fi
    
    if [ -f "$RESOURCES_DIR/deno" ]; then
        print_success "deno present"
    else
        print_error "deno missing!"
        ERRORS=$((ERRORS + 1))
    fi
    
    # Check for Tcl/Tk libraries
    echo ""
    echo "Checking Tcl/Tk libraries..."
    if [ -d "$APP_PATH/Contents/lib/tcl9.0" ] || [ -d "$APP_PATH/Contents/lib/tcl8.6" ]; then
        print_success "Tcl library present"
    else
        print_warning "Tcl library not found in Contents/lib/"
    fi
    
    if [ -d "$APP_PATH/Contents/lib/tk9.0" ] || [ -d "$APP_PATH/Contents/lib/tk8.6" ]; then
        print_success "Tk library present"
    else
        print_warning "Tk library not found in Contents/lib/"
    fi
    
    if ls "$FRAMEWORKS_DIR"/libtcl*.dylib 1> /dev/null 2>&1; then
        print_success "Tcl dylib present"
    else
        print_warning "Tcl dylib not found in Frameworks/"
    fi
    
    if ls "$FRAMEWORKS_DIR"/libtk*.dylib 1> /dev/null 2>&1; then
        print_success "Tk dylib present"
    else
        print_warning "Tk dylib not found in Frameworks/"
    fi
    
    # Check for Python packages in site-packages
    echo ""
    echo "Checking Python packages..."
    local SITE_PACKAGES=$(find "$APP_PATH/Contents/Resources/lib" -name "site-packages" -type d 2>/dev/null | head -1)
    
    if [ -n "$SITE_PACKAGES" ]; then
        local PACKAGES=("customtkinter" "PIL" "requests" "yt_dlp" "certifi")
        
        for pkg in "${PACKAGES[@]}"; do
            if [ -d "$SITE_PACKAGES/$pkg" ] || ls "$SITE_PACKAGES" | grep -qi "^${pkg}" 2>/dev/null; then
                print_success "$pkg"
            else
                print_error "$pkg missing!"
                ERRORS=$((ERRORS + 1))
            fi
        done
    else
        print_warning "Could not locate site-packages directory"
    fi
    
    # Check main executable
    echo ""
    echo "Checking main executable..."
    local EXECUTABLE="$APP_PATH/Contents/MacOS/$APP_NAME"
    if [ -f "$EXECUTABLE" ]; then
        local ARCH=$(file "$EXECUTABLE" | grep -o 'arm64\|x86_64' | head -1)
        local CURRENT_ARCH=$(uname -m)
        print_success "Executable found (architecture: $ARCH)"
        
        if [ "$ARCH" != "$CURRENT_ARCH" ]; then
            print_warning "Built for $ARCH but running on $CURRENT_ARCH"
        fi
    else
        print_error "Main executable not found!"
        ERRORS=$((ERRORS + 1))
    fi
    
    echo ""
    if [ $ERRORS -eq 0 ]; then
        print_success "All checks passed!"
        return 0
    else
        print_error "$ERRORS error(s) found - app may not launch correctly"
        return 1
    fi
}

# ============================================================================
# CODE SIGN APP (Ad-hoc signing to prevent "damaged" errors)
# ============================================================================

codesign_app() {
    local APP_PATH="$1"
    
    print_header "Code Signing App (Ad-hoc)"
    
    if [ ! -d "$APP_PATH" ]; then
        print_error "App not found: $APP_PATH"
        return 1
    fi
    
    echo "Signing with ad-hoc signature..."
    echo "(This prevents 'app is damaged' errors on other Macs)"
    echo ""
    
    # Remove any existing signatures and quarantine attributes
    xattr -cr "$APP_PATH" 2>/dev/null || true
    
    # Sign all nested components first (frameworks, dylibs, etc.)
    find "$APP_PATH" -type f \( -name "*.dylib" -o -name "*.so" -o -name "*.framework" \) -exec codesign --force --sign - {} \; 2>/dev/null || true
    
    # Sign the main executable
    codesign --force --deep --sign - "$APP_PATH" 2>&1
    
    if [ $? -eq 0 ]; then
        print_success "App signed successfully"
        
        # Verify signature
        if codesign --verify --verbose "$APP_PATH" 2>&1 | grep -q "valid"; then
            print_success "Signature verified"
        fi
    else
        print_warning "Code signing had issues (app may still work)"
    fi
    
    # Remove quarantine attribute (in case it got re-added)
    xattr -dr com.apple.quarantine "$APP_PATH" 2>/dev/null || true
    
    return 0
}

# ============================================================================
# SETUP TCL/TK ENVIRONMENT
# ============================================================================

setup_tcltk_environment() {
    local APP_PATH="$1"
    local RESOURCES_DIR="$APP_PATH/Contents/Resources"
    local MACOS_DIR="$APP_PATH/Contents/MacOS"
    
    print_header "Setting up Tcl/Tk Environment"
    
    # Detect which Tcl/Tk version was bundled
    TCL_VERSION=""
    if [ -d "$APP_PATH/Contents/lib/tcl9.0" ]; then
        TCL_VERSION="9.0"
    elif [ -d "$APP_PATH/Contents/lib/tcl8.6" ]; then
        TCL_VERSION="8.6"
    fi
    
    if [ -z "$TCL_VERSION" ]; then
        print_warning "No bundled Tcl/Tk found - skipping environment setup"
        return 0
    fi
    
    print_info "Found bundled Tcl/Tk $TCL_VERSION"
    
    # Find the main executable
    MAIN_EXECUTABLE=$(find "$MACOS_DIR" -type f -perm +111 ! -name "*.dylib" | head -1)
    
    if [ -z "$MAIN_EXECUTABLE" ]; then
        print_error "Could not find main executable in $MACOS_DIR"
        return 1
    fi
    
    EXECUTABLE_NAME=$(basename "$MAIN_EXECUTABLE")
    print_info "Main executable: $EXECUTABLE_NAME"
    
    # Rename original executable
    mv "$MAIN_EXECUTABLE" "${MAIN_EXECUTABLE}_real"
    
    # Create wrapper script that sets environment variables
    cat > "$MAIN_EXECUTABLE" << 'WRAPPER_SCRIPT'
#!/bin/bash
# Wrapper script to set Tcl/Tk environment variables
# Auto-generated by build_app.sh

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_DIR="$(dirname "$SCRIPT_DIR")"

# Set Tcl/Tk library paths to the bundled versions
WRAPPER_SCRIPT

    # Add version-specific paths
    cat >> "$MAIN_EXECUTABLE" << WRAPPER_VARS
export TCL_LIBRARY="\$APP_DIR/lib/tcl$TCL_VERSION"
export TK_LIBRARY="\$APP_DIR/lib/tk$TCL_VERSION"
WRAPPER_VARS

    # Add the rest of the wrapper
    cat >> "$MAIN_EXECUTABLE" << 'WRAPPER_END'

# Set library paths for bundled dylibs (libtommath, etc.)
export DYLD_LIBRARY_PATH="$APP_DIR/Frameworks:$DYLD_LIBRARY_PATH"
export DYLD_FRAMEWORK_PATH="$APP_DIR/Frameworks:$DYLD_FRAMEWORK_PATH"

# Also set DYLD_FALLBACK_LIBRARY_PATH as a backup
export DYLD_FALLBACK_LIBRARY_PATH="$APP_DIR/Frameworks:/usr/lib:/usr/local/lib"

# Execute the real application
exec "$SCRIPT_DIR/$(basename "$0")_real" "$@"
WRAPPER_END

    # Make wrapper executable
    chmod +x "$MAIN_EXECUTABLE"
    
    print_success "Created launcher wrapper with Tcl/Tk environment"
    print_info "TCL_LIBRARY will be set to: Contents/lib/tcl$TCL_VERSION"
    print_info "TK_LIBRARY will be set to: Contents/lib/tk$TCL_VERSION"
    
    return 0
}

# ============================================================================
# BUILD APP
# ============================================================================

build_app() {
    local PY_FILE="$1"
    
    print_header "Building $APP_NAME"
    
    cd "$PROJECT_DIR"
    
    # Check if Python file exists
    if [ ! -f "$PY_FILE" ]; then
        print_error "Python file not found: $PY_FILE"
        exit 1
    fi
    
    print_info "Source: $PY_FILE"
    
    # Extract version from the Python file
    VERSION=$(grep -E "^APP_VERSION\s*=" "$PY_FILE" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
    if [ -z "$VERSION" ]; then
        VERSION="1.0.0"
    fi
    print_info "Version: $VERSION"
    
    # Generate setup.py with current settings
    generate_setup_py "$PY_FILE" "$VERSION"
    
    # Clean previous build
    clean_build
    
    # Activate venv and build
    activate_venv
    
    # Ensure psutil is installed (v18.0.0 requirement)
    if ! python -c "import psutil" 2>/dev/null; then
        print_info "Installing psutil (required for v18.0.0)..."
        pip install psutil
        if [ $? -ne 0 ]; then
            print_error "Failed to install psutil"
            exit 1
        fi
        print_success "psutil installed"
    fi
    
    echo ""
    echo "Running py2app..."
    echo ""
    python setup.py py2app
    
    BUILD_RESULT=$?
    
    deactivate_venv
    
    if [ $BUILD_RESULT -ne 0 ]; then
        print_error "py2app build failed"
        exit 1
    fi
    
    # Find the built app - handle spaces in name properly
    echo ""
    echo "Looking for built app in dist/..."
    ls -la "$PROJECT_DIR/dist/"
    
    # Use find with -print0 and read to handle spaces
    BUILT_APP_PATH=""
    while IFS= read -r -d '' app; do
        BUILT_APP_PATH="$app"
        break
    done < <(find "$PROJECT_DIR/dist" -maxdepth 1 -name "*.app" -type d -print0 2>/dev/null)
    
    if [ -z "$BUILT_APP_PATH" ]; then
        print_error "No .app found in dist/"
        exit 1
    fi
    
    print_success "App built: $BUILT_APP_PATH"
    
    # Bundle dependencies
    if ! bundle_dependencies "$BUILT_APP_PATH"; then
        print_error "Failed to bundle dependencies"
        exit 1
    fi
    
    # Setup Tcl/Tk environment for the bundled libraries
    if ! setup_tcltk_environment "$BUILT_APP_PATH"; then
        print_warning "Tcl/Tk environment setup had issues"
    fi
    
    # Verify the built app
    verify_app "$BUILT_APP_PATH"
    
    # Code sign the app (prevents "damaged" errors)
    codesign_app "$BUILT_APP_PATH"
    
    # Show final app size
    echo ""
    APP_SIZE=$(du -sh "$BUILT_APP_PATH" | cut -f1)
    print_success "Build complete! App size: $APP_SIZE"
}

# ============================================================================
# INSTALL APP
# ============================================================================

install_app() {
    local SOURCE_APP="$1"
    
    print_header "Installing to $INSTALL_DIR"
    
    if [ ! -d "$SOURCE_APP" ]; then
        print_error "Source app not found: $SOURCE_APP"
        return 1
    fi
    
    # Get the app name from the source
    APP_BASENAME=$(basename "$SOURCE_APP")
    INSTALL_PATH="$INSTALL_DIR/$APP_BASENAME"
    
    print_info "Installing: $APP_BASENAME"
    
    # Remove old installation if exists
    if [ -d "$INSTALL_PATH" ]; then
        print_warning "Removing existing installation..."
        rm -rf "$INSTALL_PATH"
    fi
    
    # Copy new app
    cp -R "$SOURCE_APP" "$INSTALL_DIR/"
    
    if [ -d "$INSTALL_PATH" ]; then
        print_success "Installed to: $INSTALL_PATH"
        
        # Verify ffmpeg and deno are present
        if [ -f "$INSTALL_PATH/Contents/Resources/ffmpeg" ]; then
            print_success "ffmpeg verified"
        else
            print_warning "ffmpeg not found in installed app!"
        fi
        
        if [ -f "$INSTALL_PATH/Contents/Resources/deno" ]; then
            print_success "deno verified"
        else
            print_warning "deno not found in installed app!"
        fi
    else
        print_error "Installation failed"
        return 1
    fi
}

# ============================================================================
# CREATE DMG INSTALLER
# ============================================================================

create_dmg() {
    local SOURCE_APP="$1"
    local VERSION="$2"
    
    print_header "Creating DMG Installer"
    
    if [ ! -d "$SOURCE_APP" ]; then
        print_error "App not found: $SOURCE_APP"
        return 1
    fi
    
    local DMG_NAME="${APP_NAME// /_}_v${VERSION}.dmg"
    local VOLUME_NAME="$APP_NAME"
    local ICON_PATH="$PROJECT_DIR/assets/icon.icns"
    local BG_IMAGE="$PROJECT_DIR/assets/dmg_background.png"
    
    print_info "Creating: $DMG_NAME"
    
    # Install fileicon if needed
    if ! command -v fileicon &> /dev/null; then
        print_info "Installing fileicon..."
        brew install fileicon --quiet
    fi
    
    # Get Applications folder icon path
    local APPS_ICON="/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/ApplicationsFolderIcon.icns"
    if [ ! -f "$APPS_ICON" ]; then
        print_warning "System Applications icon not found, trying alternatives..."
        for alt in \
            "/System/Library/CoreServices/Finder.app/Contents/Resources/ApplicationsFolderIcon.icns" \
            "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/GenericFolderIcon.icns"
        do
            if [ -f "$alt" ]; then
                APPS_ICON="$alt"
                print_info "Found: $APPS_ICON"
                break
            fi
        done
    fi
    
    # Cleanup previous attempts
    print_info "Cleaning up previous DMG files..."
    rm -f "$PROJECT_DIR/$DMG_NAME" "$PROJECT_DIR/temp_rw.dmg"
    rm -rf "$PROJECT_DIR/dmg_staging"
    
    # Unmount any existing volume with same name
    hdiutil detach "/Volumes/$VOLUME_NAME" 2>/dev/null || true
    
    # Create staging directory
    print_info "Creating staging directory..."
    mkdir -p "$PROJECT_DIR/dmg_staging"
    
    # Copy app
    print_info "Copying app to staging..."
    cp -R "$SOURCE_APP" "$PROJECT_DIR/dmg_staging/$APP_NAME.app"
    
    # Create README
    cat > "$PROJECT_DIR/dmg_staging/README.txt" << 'READMEEOF'
Installation: Drag app to Applications folder.

First Launch (macOS Security):
  System Settings â†’ Privacy & Security â†’ Open Anyway
  
Or run in Terminal:
  xattr -cr /Applications/YouTube\ 4K\ Downloader.app

github.com/bytePatrol/YT-DLP-GUI-for-MacOS
READMEEOF
    
    # Calculate size
    local APP_SIZE=$(du -sm "$PROJECT_DIR/dmg_staging" | cut -f1)
    local DMG_SIZE=$((APP_SIZE + 60))
    print_info "Staging size: ${APP_SIZE}MB, DMG size: ${DMG_SIZE}MB"
    
    # Create read-write DMG
    print_info "Creating read-write DMG..."
    hdiutil create -size "${DMG_SIZE}m" -fs HFS+ -volname "$VOLUME_NAME" -type UDIF -layout SPUD "$PROJECT_DIR/temp_rw.dmg"
    
    # Mount it read-write
    print_info "Mounting read-write..."
    local MOUNT_OUTPUT=$(hdiutil attach -readwrite -noverify -noautoopen "$PROJECT_DIR/temp_rw.dmg")
    local MOUNT_DIR=$(echo "$MOUNT_OUTPUT" | grep "/Volumes/" | sed 's/.*\(\/Volumes\/.*\)/\1/' | head -1)
    print_info "Mounted at: $MOUNT_DIR"
    
    if [ -z "$MOUNT_DIR" ] || [ ! -d "$MOUNT_DIR" ]; then
        print_error "Failed to mount DMG"
        return 1
    fi
    
    sleep 2
    
    # Copy contents to mounted DMG
    print_info "Copying contents to DMG..."
    cp -R "$PROJECT_DIR/dmg_staging/$APP_NAME.app" "$MOUNT_DIR/"
    cp "$PROJECT_DIR/dmg_staging/README.txt" "$MOUNT_DIR/"
    
    # Create Applications symlink (CRITICAL: must be actual symlink, not folder)
    print_info "Creating Applications symlink..."
    
    # Remove any existing Applications item first
    rm -rf "$MOUNT_DIR/Applications" 2>/dev/null || true
    
    # Create the symlink
    ln -s /Applications "$MOUNT_DIR/Applications"
    
    # Verify it's actually a symlink
    if [ -L "$MOUNT_DIR/Applications" ]; then
        print_success "Applications symlink created"
        print_info "  -> $(readlink "$MOUNT_DIR/Applications")"
    else
        print_error "Failed to create symlink - it's a $(file "$MOUNT_DIR/Applications")"
        # Try again with explicit removal
        rm -rf "$MOUNT_DIR/Applications"
        ln -s /Applications "$MOUNT_DIR/Applications"
    fi
    
    # Set icon on symlink while DMG is read-write
    print_info "Setting Applications folder icon..."
    if [ -f "$APPS_ICON" ]; then
        if fileicon set "$MOUNT_DIR/Applications" "$APPS_ICON" 2>/dev/null; then
            print_success "Icon set with fileicon"
        else
            print_warning "fileicon failed, trying SetFile..."
            if command -v SetFile &> /dev/null; then
                cp "$APPS_ICON" "$MOUNT_DIR/Applications/Icon"$'\r' 2>/dev/null || true
                SetFile -a C "$MOUNT_DIR/Applications" 2>/dev/null || true
            fi
        fi
    fi
    
    # Create .background folder and copy background image
    mkdir -p "$MOUNT_DIR/.background"
    if [ -f "$BG_IMAGE" ]; then
        cp "$BG_IMAGE" "$MOUNT_DIR/.background/background.png"
        print_success "Background image copied"
    else
        print_warning "No background image found at $BG_IMAGE"
        print_info "Creating default background..."
        _create_default_dmg_background "$MOUNT_DIR/.background/background.png"
    fi
    
    # Set volume icon
    if [ -f "$ICON_PATH" ]; then
        print_info "Setting volume icon..."
        cp "$ICON_PATH" "$MOUNT_DIR/.VolumeIcon.icns"
        SetFile -a C "$MOUNT_DIR"
    fi
    
    # Configure Finder window appearance
    print_info "Configuring Finder window..."
    osascript << ENDSCRIPT
tell application "Finder"
    tell disk "$VOLUME_NAME"
        open
        delay 2
        
        -- Window settings (600x400 - compact to avoid cutoff issues)
        set current view of container window to icon view
        set toolbar visible of container window to false
        set statusbar visible of container window to false
        set the bounds of container window to {300, 100, 900, 500}
        
        -- Icon view settings
        set viewOptions to the icon view options of container window
        set arrangement of viewOptions to not arranged
        set icon size of viewOptions to 100
        
        -- Set background image
        try
            set background picture of viewOptions to file ".background:background.png"
        end try
        
        -- Position icons (compact layout)
        set position of item "$APP_NAME.app" of container window to {140, 140}
        set position of item "Applications" of container window to {460, 140}
        set position of item "README.txt" of container window to {300, 260}
        
        -- Refresh to ensure settings take effect
        close
        delay 1
        open
        delay 2
        close
    end tell
end tell
ENDSCRIPT
    
    print_success "Finder window configured"
    
    # Sync and unmount
    print_info "Syncing and unmounting..."
    sync
    sleep 2
    hdiutil detach "$MOUNT_DIR" -force
    
    # Convert to compressed read-only DMG
    print_info "Converting to compressed DMG..."
    hdiutil convert "$PROJECT_DIR/temp_rw.dmg" -format UDZO -imagekey zlib-level=9 -o "$PROJECT_DIR/$DMG_NAME"
    
    # Cleanup temp DMG
    rm -f "$PROJECT_DIR/temp_rw.dmg"
    
    # Set icon on the DMG file itself (AFTER conversion)
    if [ -f "$ICON_PATH" ]; then
        print_info "Setting DMG file icon..."
        fileicon set "$PROJECT_DIR/$DMG_NAME" "$ICON_PATH"
    fi
    
    # Cleanup staging
    rm -rf "$PROJECT_DIR/dmg_staging"
    
    # Final output
    local DMG_SIZE_FINAL=$(du -h "$PROJECT_DIR/$DMG_NAME" | cut -f1)
    print_success "DMG created: $DMG_NAME ($DMG_SIZE_FINAL)"
    
    # Store path for later use
    BUILT_DMG_PATH="$PROJECT_DIR/$DMG_NAME"
}

_create_default_dmg_background() {
    # Create a background image for the DMG
    # Try PIL first, fall back to sips/ImageMagick, or create minimal PNG
    local OUTPUT_PATH="$1"
    
    # Method 1: Try PIL (best quality)
    if python3 -c "from PIL import Image" 2>/dev/null; then
        print_info "Creating background with PIL..."
        python3 << PYEOF
from PIL import Image, ImageDraw, ImageFont

width, height = 600, 400
img = Image.new('RGB', (width, height), color='#4a4a4a')
draw = ImageDraw.Draw(img)

# Arrow at y=130 (between icons)
arrow_y = 130
draw.line([(230, arrow_y), (350, arrow_y)], fill='#2a2a2a', width=5)
draw.polygon([(350, arrow_y - 14), (370, arrow_y), (350, arrow_y + 14)], fill='#2a2a2a')

# Text below arrow
try:
    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
except:
    font = ImageFont.load_default()

text = "Drag to Install"
bbox = draw.textbbox((0, 0), text, font=font)
text_x = (width - (bbox[2] - bbox[0])) // 2
draw.text((text_x, arrow_y + 35), text, fill='#1a1a1a', font=font)

img.save("$OUTPUT_PATH", 'PNG')
print("Created background with PIL")
PYEOF
        if [ -f "$OUTPUT_PATH" ]; then
            print_success "Background created with PIL"
            return 0
        fi
    fi
    
    # Method 2: Try ImageMagick (if installed)
    if command -v convert &> /dev/null; then
        print_info "Creating background with ImageMagick..."
        convert -size 600x400 xc:'#4a4a4a' \
            -fill '#2a2a2a' -draw "line 230,130 350,130" \
            -fill '#2a2a2a' -draw "polygon 350,116 370,130 350,144" \
            -font Helvetica -pointsize 16 -fill '#1a1a1a' \
            -gravity center -annotate +0+35 "Drag to Install" \
            "$OUTPUT_PATH" 2>/dev/null
        if [ -f "$OUTPUT_PATH" ]; then
            print_success "Background created with ImageMagick"
            return 0
        fi
    fi
    
    # Method 3: Create a minimal solid color PNG using base64
    # This is a 600x400 gray (#4a4a4a) PNG encoded in base64
    print_info "Creating minimal background (no PIL/ImageMagick)..."
    python3 << PYEOF
import zlib
import struct

def create_png(width, height, r, g, b, filename):
    def png_chunk(chunk_type, data):
        chunk_len = struct.pack('>I', len(data))
        chunk_crc = struct.pack('>I', zlib.crc32(chunk_type + data) & 0xffffffff)
        return chunk_len + chunk_type + data + chunk_crc
    
    # PNG signature
    signature = b'\x89PNG\r\n\x1a\n'
    
    # IHDR chunk
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr = png_chunk(b'IHDR', ihdr_data)
    
    # IDAT chunk (image data)
    raw_data = b''
    for y in range(height):
        raw_data += b'\x00'  # filter byte
        for x in range(width):
            raw_data += bytes([r, g, b])
    
    compressed = zlib.compress(raw_data, 9)
    idat = png_chunk(b'IDAT', compressed)
    
    # IEND chunk
    iend = png_chunk(b'IEND', b'')
    
    with open(filename, 'wb') as f:
        f.write(signature + ihdr + idat + iend)

# Create 600x400 gray background (#4a4a4a = 74, 74, 74)
create_png(600, 400, 74, 74, 74, "$OUTPUT_PATH")
print("Created minimal gray background")
PYEOF
    
    if [ -f "$OUTPUT_PATH" ]; then
        print_success "Minimal background created"
        return 0
    fi
    
    print_warning "Could not create background image"
    return 1
}

# ============================================================================
# MAIN
# ============================================================================

main() {
    echo ""
    echo -e "${CYAN}+------------------------------------------+${NC}"
    echo -e "${CYAN}|   YouTube 4K Downloader Build System     |${NC}"
    echo -e "${CYAN}+------------------------------------------+${NC}"
    
    # Global variable for version (extracted during build)
    VERSION=""
    BUILT_DMG_PATH=""
    
    # Parse arguments
    case "${1:-}" in
        --help|-h)
            show_help
            exit 0
            ;;
        --update-ytdlp)
            update_ytdlp
            exit 0
            ;;
        --check-updates)
            check_ytdlp_updates
            exit 0
            ;;
        --clean)
            clean_build
            exit 0
            ;;
        --dmg)
            # Just create DMG from existing build
            print_info "Creating DMG from existing build..."
            
            # Find the app in dist/
            BUILT_APP_PATH=$(find "$PROJECT_DIR/dist" -maxdepth 1 -name "*.app" -type d 2>/dev/null | head -1)
            
            if [ -z "$BUILT_APP_PATH" ]; then
                print_error "No .app found in dist/. Run a build first."
                exit 1
            fi
            
            # Extract version from the Python file
            VERSION=$(grep -E "^APP_VERSION\s*=" "$PROJECT_DIR/$MAIN_SCRIPT" 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
            if [ -z "$VERSION" ]; then
                VERSION="1.0.0"
            fi
            
            print_info "Found app: $BUILT_APP_PATH"
            print_info "Version: $VERSION"
            
            create_dmg "$BUILT_APP_PATH" "$VERSION"
            
            print_header "DMG Creation Complete!"
            echo "  DMG: $BUILT_DMG_PATH"
            echo ""
            
            # Ask to mount and verify
            read -p "Mount DMG to verify? (y/n) " -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                hdiutil attach "$BUILT_DMG_PATH"
                open "/Volumes/$APP_NAME"
            fi
            
            exit 0
            ;;
        *.py)
            # New Python file provided
            if [ -f "$1" ]; then
                print_info "Using Python file: $1"
                MAIN_SCRIPT=$(basename "$1")
                # Copy if source is different from destination
                SOURCE_PATH="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
                DEST_PATH="$PROJECT_DIR/$MAIN_SCRIPT"
                if [ "$SOURCE_PATH" != "$DEST_PATH" ]; then
                    cp "$1" "$PROJECT_DIR/"
                    print_success "Copied to project folder"
                else
                    print_info "File already in project folder"
                fi
            else
                print_error "File not found: $1"
                exit 1
            fi
            ;;
        "")
            # No arguments - use default/existing script
            print_info "Using existing script: $MAIN_SCRIPT"
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
    
    # Check for yt-dlp updates
    echo ""
    if check_ytdlp_updates; then
        echo ""
        read -p "Update yt-dlp before building? (y/n) " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            update_ytdlp
        fi
    fi
    
    # Build the app
    cd "$PROJECT_DIR"
    build_app "$MAIN_SCRIPT"
    
    # Extract version for DMG naming
    VERSION=$(grep -E "^APP_VERSION\s*=" "$PROJECT_DIR/$MAIN_SCRIPT" 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
    if [ -z "$VERSION" ]; then
        VERSION="1.0.0"
    fi
    
    # Ask to create DMG
    echo ""
    read -p "Create DMG installer? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        create_dmg "$BUILT_APP_PATH" "$VERSION"
    fi
    
    # Ask to install
    echo ""
    read -p "Install to $INSTALL_DIR? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        install_app "$BUILT_APP_PATH"
    fi
    
    # Done!
    print_header "Build Complete!"
    
    echo "Your app is ready:"
    echo ""
    echo "  Built app:  $BUILT_APP_PATH"
    
    if [ -n "$BUILT_DMG_PATH" ] && [ -f "$BUILT_DMG_PATH" ]; then
        echo "  DMG:        $BUILT_DMG_PATH"
    fi
    
    APP_BASENAME=$(basename "$BUILT_APP_PATH")
    if [ -d "$INSTALL_DIR/$APP_BASENAME" ]; then
        echo "  Installed:  $INSTALL_DIR/$APP_BASENAME"
    fi
    echo ""
    print_success "Done!"
}

# Run main
main "$@"
