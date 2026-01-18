"""
Setup script for creating a macOS .app bundle for YouTube 4K Downloader

Usage:
    python setup.py py2app

This will create a standalone .app in the dist/ folder that can be
moved to your Applications folder.

Note: ffmpeg and deno are bundled separately by build_app.sh
"""

from setuptools import setup
import os

# Path to your app icon
ICON_PATH = '/Users/ryan/Downloads/YT_DLP_Master/icon.icns'

# Verify icon exists
if os.path.isfile(ICON_PATH):
    print(f"✅ Found icon at: {ICON_PATH}")
else:
    print(f"⚠️  Icon not found at: {ICON_PATH}")
    ICON_PATH = None

APP = ['yt_dlp_gui_v17.7.3.py']
DATA_FILES = []  # ffmpeg and deno are bundled by build_app.sh

OPTIONS = {
    'argv_emulation': False,
    'iconfile': ICON_PATH,  # Your custom app icon
    'plist': {
        'CFBundleName': 'YouTube 4K Downloader',
        'CFBundleDisplayName': 'YouTube 4K Downloader',
        'CFBundleGetInfoString': "Modern YouTube downloader for macOS - 100% Standalone",
        'CFBundleIdentifier': "com.bytepatrol.youtube4kdownloader",
        'CFBundleVersion': "17.7.3",
        'CFBundleShortVersionString': "17.7.3",
        'NSHumanReadableCopyright': "Copyright © 2025 bytePatrol. All rights reserved.",
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.13',
    },
    'packages': [
        'customtkinter',
        'tkinter',
        'PIL',
        'requests',
        'certifi',
        'charset_normalizer',
        'yt_dlp',
    ],
    'includes': [
        'subprocess',
        'json',
        'threading',
        'queue',
        'pathlib',
    ],
    'excludes': [
        'numpy',
        'scipy',
        'matplotlib',
        'pandas',
    ],
    'semi_standalone': False,
    'site_packages': True,
}

setup(
    name='YouTube 4K Downloader',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
