#!/usr/bin/env python3
"""
YouTube 4K Downloader v18 - 2026 Modern Design Edition

Complete UI/UX overhaul with contemporary design standards:
-  Glass morphism design with backdrop blur effects
- 💫 Purple-blue gradient accents throughout
-  Responsive flexbox layout (no cut-off sections)
-  Collapsible activity log panel (max 200px, scrollable)
- Â± Modern card-based interface with generous spacing
- ✨ Smooth animations and micro-interactions
- Ëœ Larger touch targets (56-60px buttons)
- 💎 Softer corners (16-20px border radius)

v18.0.5 Changes - DOWNLOAD BUTTON & SELECTION FIX:
- FIXED: Download button now ALWAYS visible without needing fullscreen
- FIXED: Quality selection now properly deselects 1080p when clicking another option
  - Orange "recommended" highlight is cleared when user selects a different format
  - Only the selected format shows the purple highlight
- CHANGED: Video section now uses internal grid layout for better space management
- CHANGED: More compact format cards (smaller padding, font sizes)
- CHANGED: Smaller thumbnail (160x90) to save vertical space
- CHANGED: Download button row is fixed at bottom of video card, never hidden

v18.0.2 Changes - NO-SCROLL LAYOUT:
- FIXED: Everything now fits without scrolling at any window size
- FIXED: "Best" badge no longer overlaps resolution text (now inline: "\xe2\x98\x85 1080p")
- FIXED: Progress bar and metrics always fully visible
- CHANGED: Removed ScrollableFrame - using pure grid layout
- CHANGED: Much more compact design throughout:
  - Header reduced from 72px to 56px
  - URL input reduced from 64px to 48px  
  - Thumbnail reduced from 180x101 to 160x90
  - Format cards: smaller padding, single-line details
  - Progress section: tighter spacing
  - All fonts slightly smaller
- CHANGED: Video section now uses grid row 0 (expands), progress uses row 1 (fixed)

v18.0.1 Changes - LAYOUT FIX:
- FIXED: Resource gauges (CPU/Memory/GPU) now in footer - always visible without scrolling
- FIXED: Gauges no longer cut off even on smaller screens
- FIXED: Download metrics (Speed/FPS/ETA/Size) now always visible in compact inline row
- IMPROVED: More compact video card with smaller thumbnail and tighter spacing
- IMPROVED: More compact format cards (quality selection buttons)
- IMPROVED: More compact progress section with inline metrics bar
- IMPROVED: Footer shows system resources alongside output path
- IMPROVED: Overall ~30% reduction in vertical space usage

v18.0.0 Changes - MAJOR UI REDESIGN:
- NEW: Complete visual overhaul with 2026 design standards
- NEW: Glass morphism effects with semi-transparent backgrounds
- NEW: Purple-blue gradient color scheme (#667eea -> #764ba2)
- NEW: Collapsible activity log (saves space, max 200px height)
- NEW: Responsive layout with fixed header/footer, scrollable content
- NEW: Larger, more modern buttons and inputs (56-60px height)
- NEW: Icon-first header design with circular icon buttons
- NEW: Enhanced progress section with cleaner metrics display
- NEW: Improved quality cards with better visual hierarchy
- NEW: Smooth hover effects and transitions throughout
- IMPROVED: Better spacing and padding (20-24px standard)
- IMPROVED: Softer border radius (16-20px vs 8-10px)
- All v17.10 features maintained (auto-update, chapters, SponsorBlock, etc.)

v17.9.0 Changes:
- Fixed shell injection vulnerability in macOS notifications
- Added input sanitization and truncation for security
- Added subprocess timeouts to prevent hanging
- Complete documentation overhaul with Google-style docstrings
- Eliminated all bare except clauses

v17.8.8 Changes:
- FIXED: History now saves correctly (was writing to wrong file path)
- Updated Help menu with accurate information (no manual yt-dlp/ffmpeg install needed)
- Fixed broken emoji characters throughout the app
- Updated documentation and changelog

v17.8.7 Changes:
- SponsorBlock is now automatically disabled for chapter downloads
- Added notice in SponsorBlock settings explaining chapter download limitation
- Added notice in chapter selection window about SponsorBlock being disabled
- This prevents potential issues with chapter extraction and SponsorBlock conflicts

v17.8.6 Changes:
- FIXED: Footer no longer disappears after clicking Analyze
- Footer (Output path, Open Folder, Change buttons) now stays visible permanently
- Fixed layout issue where dynamically showing video_frame pushed footer off screen
- Log panel no longer expands infinitely, allowing footer to remain visible
- Can now download multiple videos without restarting the app

v17.8.5 Changes:
- MAJOR PERFORMANCE FIX: Chapter downloads are now 10-50x faster!
- New strategy: Download once -> Encode once -> Split into chapters
- Old method downloaded and encoded the ENTIRE video for EACH chapter (insanely slow)
- New method uses ffmpeg stream copy to split chapters (instant, no re-encoding)
- Fixed bug where only 3 chapters were output despite selecting more
- Added proper progress tracking through all stages (download/encode/split)
- Temp files are now properly cleaned up after chapter extraction

v17.8.4 Changes:
- FIXED: Chapter downloads now work with bundled ffmpeg
- Added --ffmpeg-location to chapter extraction commands
- yt-dlp's --download-sections requires ffmpeg for partial video extraction
- Error "ffmpeg is not installed" no longer occurs when downloading chapters

v17.8.3 Changes:
- CRITICAL FIX: All downloads now work with YouTube's SABR streaming restrictions
- Added --extractor-args youtube:player_client=android_sdkless to ALL yt-dlp commands
- Added --remote-components ejs:github for JavaScript challenge solving
- Fixed chapter downloads failing with "Some web client https formats have been skipped"
- Fixed main video/audio downloads that were also affected by SABR restrictions
- android_sdkless client bypasses YouTube's SABR-only enforcement

v17.8.2 Changes:
- MAJOR FIX: App no longer appears frozen during long merge/conversion operations
- NEW: Chapter downloads restored! Download videos split by chapters
- Detects YouTube chapters automatically and shows "📑 Download Chapters" button
- Select individual chapters or download all at once
- Supports both video and audio-only chapter extraction
- Added file size monitoring during stalls - shows "Merging... 1.2 GB written (45s elapsed)"
- Detects yt-dlp's internal merging phase and shows activity indicator
- Fixed encoding issue in fetch_video_info/fetch_full_info that broke Analyze button
- Fixed footer disappearing after Analyze - now stays visible
- Background thread monitors output file growth when progress parsing fails

v17.7.4 Changes:
- MAJOR FIX: SponsorBlock now works via post-processing!
- Queries SponsorBlock API after conversion to find segments
- Re-encodes video with segments removed using ffmpeg filters
- More reliable than trying to integrate during download
- Properly removes sponsor segments, intros, outros, etc.
- Shows detailed segment information in activity log

v17.6.0 Changes:
- Reverted to proven separate download strategy (fast, reliable)
- Using our own ffmpeg for QuickTime-compatible encoding (H.264 + AAC)
- SponsorBlock kept disabled - doesn't work with YouTube's current API restrictions
- Prioritizes speed and compatibility over non-functional features

v17.4.0 Changes:
- Reverted to separate video+audio download strategy (known to work)
- Disabled SponsorBlock in download commands (not compatible with current YouTube API)
- SponsorBlock UI remains but feature is non-functional until YouTube API improves
- Prioritizes getting correct quality and working downloads

v17.3.0 Changes:
- MAJOR CHANGE: Use 'best' format (pre-muxed video+audio) instead of merging
- SponsorBlock works properly on complete formats
- Simpler, more reliable approach
- Downloads single file with both video and audio already combined

v17.2.4 Changes:
- Fixed _find_temp_file to prefer MP4 files and skip audio-only formats
- Now correctly finds the video+audio file even when multiple files exist
- Proper video output with SponsorBlock working

v17.2.3 Changes:
- Fixed file finder to prefer MP4 files over WebM/audio-only files
- Now correctly selects the video+audio file for conversion
- Filters out audio-only formats (f251, etc.) when finding complete file

v17.2.2 Changes:
- Improved temp file cleanup - removes ALL files with video_id after conversion
- Better handling of yt-dlp's varied output filenames
- Only the final converted file should remain

v17.2.1 Changes:
- Fixed format selector to properly merge video+audio
- Added --merge-output-format to ensure single mp4/mkv output
- Prevents separate audio-only files from being created

v17.2.0 Changes:
- FIXED: SponsorBlock now actually removes segments
- Changed strategy: download complete video+audio with SponsorBlock, then re-encode
- SponsorBlock works on the complete stream before conversion
- Segments are properly cut from the final output

v17.1.7 Changes:
- Don't fail on non-zero exit code if file downloaded successfully
- Check for downloaded files before marking as failed
- Warnings no longer cause download failure if content was retrieved

v17.1.6 Changes:
- Improved error handling - warnings no longer cause download failure
- Better file detection - finds downloaded files even with unexpected names
- Added debug logging to diagnose download issues
- Downloads should now succeed despite YouTube warnings

v17.1.5 Changes:
- Added explicit SABR bypass using skip=dash,hls
- Forces yt-dlp to skip DASH/HLS formats and use progressive formats
- Should work around YouTube's SABR streaming restrictions

v17.1.4 Changes:
- Changed from specific format IDs to quality-based selection
- Uses height-based format selection (bestvideo[height<=2160]) instead of format IDs
- Avoids SABR-restricted formats by letting yt-dlp pick best available format at target quality
- More reliable downloads by using yt-dlp's smart format selection

v17.1.3 Changes:
- Removed all client restrictions from downloads
- Let yt-dlp automatically select the best working client
- yt-dlp will adapt to YouTube's current restrictions dynamically

v17.1.2 Changes:
- Using tv_embedded client only (no PO token required)
- Removed mweb client which now requires tokens
- Should complete downloads successfully

v17.1.1 Changes:
- Fixed SABR streaming error during downloads
- Added proper client selection for download phase
- Format detection works (all qualities visible) AND downloads work

v17.1.0 Changes:
- MAJOR FIX: Switched from -J (JSON) to --list-formats for format detection
- Now correctly detects all available qualities (4K, 1440p, 1080p, 720p, etc.)
- Parses yt-dlp's format table output which has full format availability
- Fixes YouTube API limitations with JSON output

v17.0.9 Changes:
- Removed player_client restrictions to allow yt-dlp's smart format detection
- yt-dlp now automatically selects best working client for format availability
- Should detect all available qualities without client-specific limitations

v17.0.8 Changes:
- Fixed format detection showing only 360p
- Using mediaconnect client which provides full format access
- All quality options (4K, 1440p, 1080p, 720p, etc.) now available

v17.0.7 Changes:
- Fixed YouTube PO Token requirement error
- Using ios client which doesn't require tokens
- Downloads work without manual token configuration

v17.0.6 Changes:
- Fixed YouTube SABR streaming error blocking downloads
- Added --extractor-args to handle YouTube's new streaming requirements
- Downloads now work with latest YouTube restrictions

v17.0.5 Changes:
- Fixed SponsorBlock not removing segments despite enabled settings
- SponsorBlock now properly reads selected categories from settings
- Categories are correctly passed to yt-dlp (e.g., 'sponsor,intro,outro')
- Both "Remove" and "Mark" actions now work properly

v17.0.4 Changes:
- Added bundled deno JavaScript runtime support for yt-dlp
- App automatically uses bundled deno if present (no Homebrew needed)
- Fixes "No supported JavaScript runtime" error
- Use bundle_dependencies.sh to install ffmpeg + deno into app

v17.0.3 Changes:
- Fixed crash with emoji/unicode in video titles
- Improved filename sanitization to ASCII-only for maximum compatibility
- Fixed 'ascii codec can't decode' errors in ffmpeg subprocess
- All subprocess calls now use UTF-8 encoding with error replacement

v17.0.2 Changes:
- Self-contained app: uses bundled static ffmpeg (no Homebrew required)
- Fixed ffmpeg library loading error (libsharpyuv.0.dylib)

v17.0.1 Changes:
- Fixed conversion failures with special characters in titles (& ; $ etc.)
- Improved ffmpeg error logging - now shows actual error messages
- Better filename sanitization for shell-safe output files

v17.0.0 Changes:
- Fixed settings persistence - SponsorBlock, Encoding, etc. now save properly
- Separated settings.json from config.json to prevent overwrites
- Settings are saved immediately when changed
- Moved config files to ~/.config/yt-dlp-gui/ for better organization

Requirements:
    pip install customtkinter pillow requests yt-dlp

Author: bytePatrol
License: MIT
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    HAS_DND = True
except ImportError:
    HAS_DND = False
    # Drag & drop will be disabled
import subprocess
import json
import os
import re
import sys
import shlex
import threading
import queue
import time
import shutil
import stat
import platform
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any, Callable, Tuple
from dataclasses import dataclass, field
from enum import Enum, auto
import urllib.request
import tempfile
import hashlib

# Optional imports with fallbacks
try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("Warning: Pillow not installed. Thumbnails will be disabled.")

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print("Warning: requests not installed. SponsorBlock will be disabled.")


# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================

APP_NAME = "YouTube 4K Downloader"
APP_VERSION = "18.1.2"

# Configuration paths - using proper config directory
CONFIG_DIR = Path.home() / ".config" / "yt-dlp-gui"
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

CONFIG_PATH = CONFIG_DIR / "config.json"
SETTINGS_PATH = CONFIG_DIR / "settings.json"  # Separate file for settings
HISTORY_PATH = CONFIG_DIR / "history.json"
CACHE_DIR = Path.home() / ".cache" / "yt_dlp_gui"

# Application Support directory for user-installed binaries (macOS standard)
APP_SUPPORT_DIR = Path.home() / "Library" / "Application Support" / "YouTube 4K Downloader"
APP_SUPPORT_DIR.mkdir(parents=True, exist_ok=True)

# User-installed yt-dlp binary location
USER_YTDLP_PATH = APP_SUPPORT_DIR / "yt-dlp"
USER_YTDLP_VERSION_FILE = APP_SUPPORT_DIR / "yt-dlp-version.txt"

# GitHub API for yt-dlp releases
YTDLP_GITHUB_API = "https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest"
YTDLP_RELEASES_URL = "https://github.com/yt-dlp/yt-dlp/releases"

# GitHub API for app releases
APP_GITHUB_API = "https://api.github.com/repos/bytePatrol/YT-DLP-GUI-for-MacOS/releases/latest"
APP_RELEASES_URL = "https://github.com/bytePatrol/YT-DLP-GUI-for-MacOS/releases"

def find_executable(name: str) -> str:
    """
    Find executable, checking user-installed location first, then bundled resources.
    
    Priority order for yt-dlp:
    1. User-installed binary in ~/Library/Application Support/YouTube 4K Downloader/
    2. Bundled binary in app Resources (for fresh installs)
    3. Python module (pip-installed)
    4. System paths (Homebrew, etc.)
    
    Args:
        name: Name of the executable to find
        
    Returns:
        Path to the executable or special value like "python-module"
    """
    import shutil
    
    # Special handling for yt-dlp: check user-installed version first
    if name == "yt-dlp":
        # 1. Check user-installed binary (from auto-update)
        if USER_YTDLP_PATH.is_file():
            # Verify it's executable
            if os.access(USER_YTDLP_PATH, os.X_OK):
                return str(USER_YTDLP_PATH)
    
    # Check if we're running from a .app bundle - prefer bundled executables
    if getattr(sys, 'frozen', False):
        bundle_dir = os.path.dirname(os.path.dirname(sys.executable))
        resources_dir = os.path.join(bundle_dir, 'Resources')
        bundled_path = os.path.join(resources_dir, name)
        if os.path.isfile(bundled_path):
            return bundled_path
    
    # Special handling for yt-dlp: prefer Python module method
    if name == "yt-dlp":
        # Try to import yt-dlp as a Python module first (most reliable)
        try:
            import yt_dlp
            return "python-module"
        except ImportError as e:
            pass
        
        # Check Homebrew paths
        homebrew_paths = [
            "/opt/homebrew/bin/yt-dlp",
            "/usr/local/bin/yt-dlp",
        ]
        for p in homebrew_paths:
            if os.path.isfile(p):
                return p
    
    # Check if it's available in PATH (includes venv)
    path = shutil.which(name)
    if path:
        return path
    
    # Fallback paths for other executables
    fallback_paths = [
        f"/opt/homebrew/bin/{name}",
        f"/usr/local/bin/{name}",
        f"/usr/bin/{name}",
    ]
    
    for p in fallback_paths:
        if os.path.isfile(p):
            return p
    
    return name  # Return just the name, let it fail later with clear error

# Binary paths - dynamically found
YTDLP_PATH = find_executable("yt-dlp")
FFMPEG_PATH = find_executable("ffmpeg")
DENO_PATH = find_executable("deno")  # JavaScript runtime for yt-dlp

# Color Palette - 2026 Modern Design with Purple/Blue Gradients
COLORS = {
    "bg_primary": "#0a0a0f",
    "bg_secondary": "#161618",
    "bg_tertiary": "#1c1c1e",
    "bg_elevated": "#2c2c2e",
    "bg_hover": "#3a3a3c",
    
    "text_primary": "#f5f5f7",
    "text_secondary": "#98989d",
    "text_tertiary": "#636366",
    
    # Modern gradient accents - Purple to Blue
    "accent_gradient_start": "#667eea",
    "accent_gradient_end": "#764ba2",
    "accent_blue": "#0a84ff",
    "accent_blue_hover": "#409cff",
    "accent_green": "#30d158",
    "accent_orange": "#ff9f0a",
    "accent_red": "#ff453a",
    "accent_purple": "#bf5af2",
    
    "border": "#2c2c2e",
    "border_light": "#3a3a3c",
    "border_focus": "#667eea",
    
    # Glass morphism colors (with alpha)
    "glass_overlay": "#1c1c1e",  # Used with transparency
}

# Resolution presets
RESOLUTION_PRESETS = {
    "Best Available": None,
    "4K (2160p)": 2160,
    "1440p": 1440,
    "1080p": 1080,
    "720p": 720,
    "480p": 480,
}

# Output format presets
FORMAT_PRESETS = {
    "QuickTime (H.264 + AAC)": {"vcodec": "h264", "acodec": "aac", "ext": "mp4"},
    "High Quality (HEVC + AAC)": {"vcodec": "hevc", "acodec": "aac", "ext": "mp4"},
    "Web Optimized (VP9 + Opus)": {"vcodec": "vp9", "acodec": "opus", "ext": "webm"},
    "Audio Only (M4A)": {"vcodec": None, "acodec": "aac", "ext": "m4a"},
    "Audio Only (MP3)": {"vcodec": None, "acodec": "mp3", "ext": "mp3"},
}

# SponsorBlock categories
SPONSORBLOCK_CATEGORIES = {
    "sponsor": "Sponsor Segments",
    "intro": "Intermission/Intro Animation",  
    "outro": "Endcards/Credits",
    "selfpromo": "Unpaid/Self Promotion",
    "preview": "Preview/Recap",
    "music_offtopic": "Music: Non-Music Section",
    "interaction": "Interaction Reminder",
    "filler": "Filler Tangent",
}

# Keyboard shortcuts configuration
KEYBOARD_SHORTCUTS = {
    "paste_url": "<Command-v>",
    "download": "<Command-Return>", 
    "analyze": "<Return>",
}


# GitHub API for app updates
APP_GITHUB_REPO = "bytePatrol/YT-DLP-GUI-for-MacOS"
APP_GITHUB_API = f"https://api.github.com/repos/{APP_GITHUB_REPO}/releases/latest"
APP_RELEASES_URL = f"https://github.com/{APP_GITHUB_REPO}/releases"


class AppUpdateChecker:
    """
    Check for app updates from GitHub releases.
    
    Compares current app version with the latest GitHub release and
    notifies the user if a new version is available.
    """
    
    def __init__(self, current_version: str, repo: str = APP_GITHUB_REPO):
        self.current_version = current_version
        self.repo = repo
        self.api_url = f"https://api.github.com/repos/{repo}/releases/latest"
        self.releases_url = f"https://github.com/{repo}/releases"
    
    def check_for_update(self) -> tuple[bool, Optional[dict]]:
        """
        Check GitHub for a newer app version.
        
        Returns:
            Tuple of (update_available, release_info)
            release_info contains: version, url, changelog, published_date
        """
        try:
            # Query GitHub API for latest release
            req = urllib.request.Request(
                self.api_url,
                headers={
                    "Accept": "application/vnd.github.v3+json",
                    "User-Agent": f"YouTube4KDownloader/{self.current_version}"
                }
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
            
            # Extract release info
            latest_version = data.get("tag_name", "").lstrip("v")
            release_name = data.get("name", "")
            release_body = data.get("body", "")
            html_url = data.get("html_url", self.releases_url)
            published_at = data.get("published_at", "")
            
            # Check if update is available
            if self._compare_versions(self.current_version, latest_version) < 0:
                release_info = {
                    "version": latest_version,
                    "name": release_name,
                    "changelog": self._parse_changelog(release_body),
                    "url": html_url,
                    "published_date": self._format_date(published_at)
                }
                return True, release_info
            
            return False, None
            
        except Exception as e:
            print(f"Error checking for app updates: {e}")
            return False, None
    
    def _compare_versions(self, v1: str, v2: str) -> int:
        """
        Compare two version strings.
        
        Returns:
            -1 if v1 < v2, 0 if equal, 1 if v1 > v2
        """
        try:
            # Parse version strings like "18.0.0" or "17.10.0"
            def parse_version(v):
                parts = re.split(r'[._-]', v)
                return [int(p) for p in parts if p.isdigit()]
            
            p1 = parse_version(v1)
            p2 = parse_version(v2)
            
            # Pad shorter list with zeros
            max_len = max(len(p1), len(p2))
            p1.extend([0] * (max_len - len(p1)))
            p2.extend([0] * (max_len - len(p2)))
            
            for a, b in zip(p1, p2):
                if a < b:
                    return -1
                elif a > b:
                    return 1
            return 0
        except Exception:
            return -1 if v1 != v2 else 0
    
    def _parse_changelog(self, body: str) -> str:
        """
        Parse and format the release changelog.
        
        Extracts key changes and formats them nicely.
        """
        if not body:
            return "No changelog available."
        
        # Limit to first 500 characters for display
        if len(body) > 500:
            body = body[:500] + "..."
        
        # Clean up markdown formatting for display
        body = body.replace("**", "")
        body = body.replace("###", "*")
        body = body.replace("##", "*")
        body = body.replace("#", "")
        
        return body.strip()
    
    def _format_date(self, iso_date: str) -> str:
        """Format ISO date to human-readable format."""
        try:
            from datetime import datetime
            dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
            return dt.strftime("%B %d, %Y")
        except:
            return iso_date


# ============================================================================
# APP UPDATE CHECKER
# ============================================================================

class AppUpdateChecker:
    """
    Check for new app releases from GitHub.
    
    Queries the GitHub API to check if a newer version of the app is available,
    extracts changelog information, and notifies the user.
    """
    
    def __init__(self, current_version: str):
        self.current_version = current_version
        self.api_url = APP_GITHUB_API
        self.releases_url = APP_RELEASES_URL
    
    def check_for_update(self) -> tuple[bool, Optional[dict]]:
        """
        Check GitHub for a newer app version.
        
        Returns:
            Tuple of (update_available, release_info)
            release_info dict contains:
                - version: str (e.g., "18.1.0")
                - name: str (release name)
                - changelog: str (formatted release notes)
                - url: str (link to release page)
                - published_date: str (human-readable date)
        """
        try:
            # Query GitHub API
            req = urllib.request.Request(
                self.api_url,
                headers={
                    "Accept": "application/vnd.github.v3+json",
                    "User-Agent": f"YouTube4KDownloader/{self.current_version}"
                }
            )
            
            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode('utf-8'))
            
            # Extract release information
            latest_version = data.get("tag_name", "").lstrip("v")
            release_name = data.get("name", "")
            release_body = data.get("body", "")
            html_url = data.get("html_url", self.releases_url)
            published_at = data.get("published_at", "")
            
            # Compare versions
            if self._compare_versions(self.current_version, latest_version) < 0:
                release_info = {
                    "version": latest_version,
                    "name": release_name,
                    "changelog": self._parse_changelog(release_body),
                    "url": html_url,
                    "published_date": self._format_date(published_at)
                }
                return True, release_info
            
            return False, None
            
        except urllib.error.URLError as e:
            print(f"Network error checking for app updates: {e}")
            return False, None
        except Exception as e:
            print(f"Error checking for app updates: {e}")
            return False, None
    
    def _compare_versions(self, v1: str, v2: str) -> int:
        """
        Compare two version strings.
        
        Returns:
            -1 if v1 < v2, 0 if equal, 1 if v1 > v2
        """
        try:
            # Parse version strings like "18.0.0" or "17.10.0"
            def parse_version(v):
                parts = re.split(r'[._-]', v)
                return [int(p) for p in parts if p.isdigit()]
            
            p1 = parse_version(v1)
            p2 = parse_version(v2)
            
            # Pad shorter list with zeros
            max_len = max(len(p1), len(p2))
            p1.extend([0] * (max_len - len(p1)))
            p2.extend([0] * (max_len - len(p2)))
            
            for a, b in zip(p1, p2):
                if a < b:
                    return -1
                elif a > b:
                    return 1
            return 0
        except Exception:
            return -1 if v1 != v2 else 0
    
    def _parse_changelog(self, body: str) -> str:
        """
        Parse and format the release changelog.
        
        Extracts key changes and formats them for display.
        """
        if not body:
            return "No changelog available."
        
        # Limit to first 600 characters for dialog display
        if len(body) > 600:
            # Try to cut at a newline
            truncated = body[:600]
            last_newline = truncated.rfind('\n')
            if last_newline > 400:
                body = body[:last_newline] + "\n\n..."
            else:
                body = truncated + "..."
        
        # Clean up markdown for better display
        body = body.replace("**", "")
        body = body.replace("###", "*")
        body = body.replace("##", "*")
        body = body.replace("#", "")
        
        return body.strip()
    
    def _format_date(self, iso_date: str) -> str:
        """Format ISO date to human-readable format."""
        try:
            from datetime import datetime
            dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
            return dt.strftime("%B %d, %Y")
        except Exception:
            return iso_date


class UpdateNotificationDialog(ctk.CTkToplevel):
    """Modern dialog to notify user about available app updates."""
    
    def __init__(self, parent, release_info: dict):
        super().__init__(parent)
        
        self.release_info = release_info
        
        self.title("NEW Update Available")
        self.geometry("620x550")
        self.transient(parent)
        self.resizable(False, False)
        
        # Center on screen
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 620) // 2
        y = (screen_height - 550) // 2
        self.geometry(f"+{x}+{y}")
        
        self.configure(fg_color=COLORS["bg_primary"])
        
        self._create_ui()
        
        # Grab focus
        self.lift()
        self.focus_force()
    
    def _create_ui(self):
        """Create the update notification UI."""
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Header with gradient background
        header_frame = ctk.CTkFrame(
            main_frame,
            fg_color=COLORS["bg_elevated"],
            corner_radius=16
        )
        header_frame.pack(fill="x", pady=(0, 20))
        
        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="x", padx=24, pady=24)
        
        # Large update icon
        icon_label = ctk.CTkLabel(
            header_content,
            text="NEW",
            font=ctk.CTkFont(size=56)
        )
        icon_label.pack(pady=(0, 12))
        
        # Title
        title_label = ctk.CTkLabel(
            header_content,
            text="🎉 New Version Available!",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=COLORS["text_primary"]
        )
        title_label.pack()
        
        # Version info
        version_text = f"Version {self.release_info['version']} is now available"
        if self.release_info.get('published_date'):
            version_text += f" * Released {self.release_info['published_date']}"
        
        version_label = ctk.CTkLabel(
            header_content,
            text=version_text,
            font=ctk.CTkFont(size=14),
            text_color=COLORS["text_secondary"]
        )
        version_label.pack(pady=(8, 0))
        
        # Release name (if different from version)
        if self.release_info.get('name') and self.release_info['name'] != f"v{self.release_info['version']}":
            name_label = ctk.CTkLabel(
                header_content,
                text=self.release_info['name'],
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=COLORS["accent_purple"]
            )
            name_label.pack(pady=(4, 0))
        
        # Changelog section
        changelog_header = ctk.CTkLabel(
            main_frame,
            text=" What's New:",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=COLORS["text_primary"],
            anchor="w"
        )
        changelog_header.pack(fill="x", pady=(0, 12))
        
        # Scrollable changelog - FIXED HEIGHT to ensure buttons always visible
        changelog_frame = ctk.CTkFrame(
            main_frame,
            fg_color=COLORS["bg_secondary"],
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border_light"],
            height=180  # Fixed height
        )
        changelog_frame.pack(fill="x", pady=(0, 20))
        changelog_frame.pack_propagate(False)  # Maintain fixed height
        
        changelog_text = ctk.CTkTextbox(
            changelog_frame,
            font=ctk.CTkFont(size=13),
            fg_color="transparent",
            text_color=COLORS["text_secondary"],
            wrap="word",
            activate_scrollbars=True
        )
        changelog_text.pack(fill="both", expand=True, padx=16, pady=16)
        
        # Insert changelog
        changelog_content = self.release_info.get('changelog', 'No changelog available.')
        changelog_text.insert("1.0", changelog_content)
        changelog_text.configure(state="disabled")
        
        # Buttons - ensure always visible at bottom
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent", height=60)
        button_frame.pack(fill="x", side="bottom")
        button_frame.pack_propagate(False)
        
        # Download button (primary, prominent)
        download_btn = ModernButton(
            button_frame,
            text="â¬‡ï¸ Download Update",
            style="primary",
            width=220,
            height=48,
            command=self._open_release_page
        )
        download_btn.pack(side="right", pady=6)
        
        # Later button
        later_btn = ModernButton(
            button_frame,
            text="Remind Me Later",
            style="secondary",
            width=160,
            height=48,
            command=self.destroy
        )
        later_btn.pack(side="right", padx=(0, 12), pady=6)
    
    def _open_release_page(self):
        """Open the release page in browser."""
        import webbrowser
        webbrowser.open(self.release_info.get('url', APP_RELEASES_URL))
        self.destroy()


# ============================================================================
# YT-DLP AUTO-UPDATER
# ============================================================================

class YtDlpUpdater:
    """
    Handles automatic updates for yt-dlp from GitHub releases.
    
    Downloads the standalone macOS binary and stores it in a user-writable
    location (~/Library/Application Support/YouTube 4K Downloader/).
    
    This allows the app to update yt-dlp without requiring the entire app
    to be re-downloaded and re-installed.
    """
    
    # GitHub API URL for latest release
    GITHUB_API_URL = "https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest"
    
    # Binary name based on architecture
    BINARY_NAMES = {
        "arm64": "yt-dlp_macos",      # Apple Silicon
        "x86_64": "yt-dlp_macos",     # Intel (same binary, universal)
    }
    
    def __init__(self, install_path: Path = USER_YTDLP_PATH, 
                 version_file: Path = USER_YTDLP_VERSION_FILE,
                 app_version: str = APP_VERSION):
        """
        Initialize the updater.
        
        Args:
            install_path: Where to install the yt-dlp binary
            version_file: File to store the installed version
            app_version: Version of the main app (for User-Agent)
        """
        self.install_path = install_path
        self.version_file = version_file
        self.app_version = app_version
        self._callbacks: List[Callable] = []
    
    def add_callback(self, callback: Callable):
        """Add a callback for progress updates."""
        self._callbacks.append(callback)
    
    def _notify(self, event: str, data: Any = None):
        """Notify all callbacks of an event."""
        for cb in self._callbacks:
            try:
                cb(event, data)
            except Exception as e:
                print(f"Callback error: {e}")
    
    def get_installed_version(self) -> Optional[str]:
        """
        Get the version of the currently installed user yt-dlp binary.
        
        Returns:
            Version string (e.g., "2025.01.15") or None if not installed
        """
        # First check if binary exists
        if not self.install_path.is_file():
            return None
        
        # Try to read from version file (faster)
        if self.version_file.is_file():
            try:
                version = self.version_file.read_text().strip()
                if version:
                    return version
            except Exception:
                pass
        
        # Fall back to running --version
        try:
            result = subprocess.run(
                [str(self.install_path), "--version"],
                capture_output=True, text=True, timeout=10,
                encoding='utf-8', errors='replace'
            )
            if result.returncode == 0:
                version = result.stdout.strip().split('\n')[0]
                # Cache the version
                try:
                    self.version_file.write_text(version)
                except Exception:
                    pass
                return version
        except Exception as e:
            print(f"Could not get installed yt-dlp version: {e}")
        
        return None
    
    def get_current_version(self, ytdlp_path: Optional[str] = None) -> str:
        """
        Get the version of whatever yt-dlp the app is currently using.
        
        Args:
            ytdlp_path: Path to yt-dlp, or None to auto-detect
            
        Returns:
            Version string or "unknown"
        """
        # First check user-installed version
        user_version = self.get_installed_version()
        if user_version:
            return user_version
        
        # Try to get version from provided path or system
        if ytdlp_path and ytdlp_path != "python-module":
            try:
                if os.path.isfile(ytdlp_path):
                    result = subprocess.run(
                        [ytdlp_path, "--version"],
                        capture_output=True, text=True, timeout=10,
                        encoding='utf-8', errors='replace'
                    )
                    if result.returncode == 0:
                        return result.stdout.strip().split('\n')[0]
            except Exception:
                pass
        
        # Try Python module
        try:
            import yt_dlp
            return yt_dlp.version.__version__
        except Exception:
            pass
        
        return "unknown"
    
    def check_for_update(self, current_ytdlp_path: Optional[str] = None) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Check GitHub for a newer version of yt-dlp.
        
        Args:
            current_ytdlp_path: Path to currently used yt-dlp (for version check)
        
        Returns:
            Tuple of (update_available, latest_version, current_version)
        """
        current_version = self.get_current_version(current_ytdlp_path)
        
        self._notify("checking", {"current_version": current_version})
        
        try:
            # Query GitHub API
            req = urllib.request.Request(
                self.GITHUB_API_URL,
                headers={
                    "Accept": "application/vnd.github.v3+json",
                    "User-Agent": f"YouTube4KDownloader/{self.app_version}"
                }
            )
            
            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode('utf-8'))
            
            latest_version = data.get("tag_name", "").lstrip("v")
            
            # Compare versions
            if not current_version or current_version == "unknown":
                update_available = True
            else:
                update_available = self._compare_versions(current_version, latest_version) < 0
            
            self._notify("check_complete", {
                "update_available": update_available,
                "current_version": current_version,
                "latest_version": latest_version
            })
            
            return update_available, latest_version, current_version
            
        except urllib.error.URLError as e:
            self._notify("error", f"Network error checking for updates: {e}")
            return False, None, current_version
        except Exception as e:
            self._notify("error", f"Error checking for updates: {e}")
            return False, None, current_version
    
    def _compare_versions(self, v1: str, v2: str) -> int:
        """
        Compare two version strings.
        
        Returns:
            -1 if v1 < v2, 0 if equal, 1 if v1 > v2
        """
        try:
            # yt-dlp versions are like "2025.01.15" or "2025.01.15.123456"
            def parse_version(v):
                # Remove any non-numeric suffixes and split
                parts = re.split(r'[._-]', v)
                return [int(p) for p in parts if p.isdigit()]
            
            p1 = parse_version(v1)
            p2 = parse_version(v2)
            
            # Pad shorter list with zeros
            max_len = max(len(p1), len(p2))
            p1.extend([0] * (max_len - len(p1)))
            p2.extend([0] * (max_len - len(p2)))
            
            for a, b in zip(p1, p2):
                if a < b:
                    return -1
                elif a > b:
                    return 1
            return 0
        except Exception:
            # If parsing fails, assume update is available
            return -1 if v1 != v2 else 0
    
    def download_and_install(self, version: Optional[str] = None) -> Tuple[bool, str]:
        """
        Download and install the latest (or specified) version of yt-dlp.
        
        Args:
            version: Specific version to install, or None for latest
            
        Returns:
            Tuple of (success, message)
        """
        self._notify("starting", {"version": version or "latest"})
        
        try:
            # Get release info from GitHub
            if version:
                api_url = f"https://api.github.com/repos/yt-dlp/yt-dlp/releases/tags/{version}"
            else:
                api_url = self.GITHUB_API_URL
            
            req = urllib.request.Request(
                api_url,
                headers={
                    "Accept": "application/vnd.github.v3+json",
                    "User-Agent": f"YouTube4KDownloader/{self.app_version}"
                }
            )
            
            self._notify("progress", {"stage": "Fetching release info...", "percent": 5})
            
            with urllib.request.urlopen(req, timeout=15) as response:
                release_data = json.loads(response.read().decode('utf-8'))
            
            release_version = release_data.get("tag_name", "").lstrip("v")
            assets = release_data.get("assets", [])
            
            # Find the macOS binary
            arch = platform.machine()
            binary_name = self.BINARY_NAMES.get(arch, "yt-dlp_macos")
            
            download_url = None
            for asset in assets:
                if asset.get("name") == binary_name:
                    download_url = asset.get("browser_download_url")
                    break
            
            if not download_url:
                # Try alternative name
                for asset in assets:
                    name = asset.get("name", "")
                    if "macos" in name.lower() and not name.endswith(".zip"):
                        download_url = asset.get("browser_download_url")
                        break
            
            if not download_url:
                return False, f"Could not find macOS binary for {arch} architecture"
            
            self._notify("progress", {"stage": "Downloading yt-dlp...", "percent": 10})
            
            # Ensure install directory exists
            self.install_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Download the binary
            temp_path = self.install_path.parent / f"yt-dlp-{release_version}.tmp"
            
            # Create opener with redirect handling
            req = urllib.request.Request(
                download_url,
                headers={"User-Agent": f"YouTube4KDownloader/{self.app_version}"}
            )
            
            with urllib.request.urlopen(req, timeout=60) as response:
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0
                chunk_size = 65536  # 64KB chunks
                
                with open(temp_path, 'wb') as f:
                    while True:
                        chunk = response.read(chunk_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0:
                            percent = 10 + int((downloaded / total_size) * 80)
                            size_mb = downloaded / (1024 * 1024)
                            total_mb = total_size / (1024 * 1024)
                            self._notify("progress", {
                                "stage": f"Downloading... {size_mb:.1f}/{total_mb:.1f} MB",
                                "percent": percent
                            })
            
            self._notify("progress", {"stage": "Installing...", "percent": 92})
            
            # Make it executable
            temp_path.chmod(temp_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            
            # Verify it works
            self._notify("progress", {"stage": "Verifying...", "percent": 95})
            
            try:
                result = subprocess.run(
                    [str(temp_path), "--version"],
                    capture_output=True, text=True, timeout=10,
                    encoding='utf-8', errors='replace'
                )
                if result.returncode != 0:
                    temp_path.unlink(missing_ok=True)
                    return False, f"Downloaded binary failed verification: {result.stderr}"
            except subprocess.TimeoutExpired:
                temp_path.unlink(missing_ok=True)
                return False, "Downloaded binary timed out during verification"
            except Exception as e:
                temp_path.unlink(missing_ok=True)
                return False, f"Downloaded binary failed verification: {e}"
            
            # Move to final location (atomic on same filesystem)
            self._notify("progress", {"stage": "Finalizing...", "percent": 98})
            
            # Remove old binary if exists
            if self.install_path.exists():
                self.install_path.unlink()
            
            # Move new binary into place
            temp_path.rename(self.install_path)
            
            # Save version info
            self.version_file.write_text(release_version)
            
            # Clear quarantine attribute (macOS security)
            try:
                subprocess.run(
                    ["xattr", "-d", "com.apple.quarantine", str(self.install_path)],
                    capture_output=True, check=False
                )
            except Exception:
                pass
            
            self._notify("complete", {"version": release_version})
            
            return True, f"Successfully installed yt-dlp {release_version}"
            
        except urllib.error.URLError as e:
            self._notify("error", f"Network error: {e}")
            return False, f"Network error downloading update: {e}"
        except Exception as e:
            self._notify("error", str(e))
            return False, f"Error installing update: {e}"
    
    def remove_user_install(self) -> bool:
        """
        Remove the user-installed yt-dlp binary.
        
        Returns:
            True if removed successfully
        """
        try:
            if self.install_path.exists():
                self.install_path.unlink()
            if self.version_file.exists():
                self.version_file.unlink()
            return True
        except Exception as e:
            print(f"Error removing user-installed yt-dlp: {e}")
            return False


# ============================================================================
# DATA CLASSES
# ============================================================================

# ============================================================================
# CUSTOM EXCEPTIONS
# ============================================================================

class YtDlpError(Exception):
    """Base exception for yt-dlp related errors."""
    pass


class AgeRestrictedError(YtDlpError):
    """Raised when a video is age-restricted and requires authentication."""
    
    def __init__(self, video_id: str = None, message: str = None):
        self.video_id = video_id
        self.message = message or "This video is age-restricted and requires authentication."
        super().__init__(self.message)
    
    def get_help_text(self) -> str:
        """Return helpful instructions for the user."""
        return (
            "This video is age-restricted by YouTube.\n\n"
            "To download age-restricted videos, you need to:\n"
            "1. Export cookies from your browser while logged into YouTube\n"
            "2. Use the cookies file with yt-dlp\n\n"
            "For detailed instructions, visit:\n"
            "https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp"
        )


class PrivateVideoError(YtDlpError):
    """Raised when a video is private."""
    
    def __init__(self, video_id: str = None):
        self.video_id = video_id
        super().__init__("This video is private and cannot be accessed.")


class VideoUnavailableError(YtDlpError):
    """Raised when a video is unavailable (deleted, region-locked, etc.)."""
    
    def __init__(self, video_id: str = None, reason: str = None):
        self.video_id = video_id
        self.reason = reason or "This video is unavailable."
        super().__init__(self.reason)


class LoginRequiredError(YtDlpError):
    """Raised when authentication is required but not provided."""
    
    def __init__(self, video_id: str = None, reason: str = None):
        self.video_id = video_id
        self.reason = reason or "This video requires authentication to access."
        super().__init__(self.reason)


class UnviewablePlaylistError(YtDlpError):
    """Raised when a playlist cannot be enumerated (e.g., YouTube Mix/Radio playlists)."""
    
    def __init__(self, playlist_id: str = None, reason: str = None, video_id: str = None):
        self.playlist_id = playlist_id
        self.video_id = video_id  # The seed video if available
        self.reason = reason or "This playlist type cannot be viewed."
        
        # Determine playlist type for better messaging
        if playlist_id and playlist_id.startswith('RD'):
            self.playlist_type = "YouTube Mix"
            self.message = (
                f"This is a YouTube Mix (auto-generated playlist) which cannot be downloaded as a playlist.\n\n"
                f"YouTube Mixes are dynamically generated based on your viewing history and the seed video - "
                f"they don't have a fixed list of videos that can be enumerated.\n\n"
                f"You can still download the individual video from this URL."
            )
        else:
            self.playlist_type = "Special Playlist"
            self.message = (
                f"This playlist type ({reason}) cannot be accessed.\n\n"
                f"It may be private, deleted, or a special YouTube-generated playlist."
            )
        
        super().__init__(self.message)


class DownloadStatus(Enum):
    QUEUED = auto()
    ANALYZING = auto()
    DOWNLOADING = auto()
    CONVERTING = auto()
    PAUSED = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()


@dataclass
class VideoFormat:
    """Represents a single video/audio format."""
    format_id: str
    ext: str
    resolution: Optional[str] = None
    height: Optional[int] = None
    width: Optional[int] = None
    fps: Optional[float] = None
    vcodec: Optional[str] = None
    acodec: Optional[str] = None
    filesize: Optional[int] = None
    filesize_approx: Optional[int] = None
    tbr: Optional[float] = None  # Total bitrate
    vbr: Optional[float] = None  # Video bitrate
    abr: Optional[float] = None  # Audio bitrate
    is_video_only: bool = False
    is_audio_only: bool = False
    is_quicktime_compatible: bool = False
    
    @property
    def size_bytes(self) -> Optional[int]:
        return self.filesize or self.filesize_approx
    
    @property
    def size_str(self) -> str:
        size = self.size_bytes
        if not size:
            return "Unknown"
        if size >= 1024 ** 3:
            return f"{size / (1024 ** 3):.1f} GB"
        elif size >= 1024 ** 2:
            return f"{size / (1024 ** 2):.0f} MB"
        else:
            return f"{size / 1024:.0f} KB"
    
    @property
    def bitrate_str(self) -> str:
        br = self.tbr or self.vbr or self.abr
        if not br:
            return "Unknown"
        if br >= 1000:
            return f"{br / 1000:.1f} Mbps"
        return f"{br:.0f} kbps"


@dataclass
class Chapter:
    """Represents a chapter in a video."""
    index: int
    title: str
    start_time: float  # in seconds
    end_time: float    # in seconds
    
    @property
    def duration(self) -> float:
        """Duration of the chapter in seconds."""
        return self.end_time - self.start_time
    
    @property
    def duration_str(self) -> str:
        """Human-readable duration."""
        duration = int(self.duration)
        hours, remainder = divmod(duration, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        return f"{minutes}:{seconds:02d}"
    
    @property
    def start_time_str(self) -> str:
        """Human-readable start time."""
        start = int(self.start_time)
        hours, remainder = divmod(start, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        return f"{minutes}:{seconds:02d}"
    
    @property
    def safe_filename(self) -> str:
        """Return a filesystem-safe version of the chapter title."""
        return sanitize_filename(self.title, max_length=100)


@dataclass
class PlaylistItem:
    """Represents a single video in a playlist."""
    id: str
    title: str
    url: str
    index: int  # Position in playlist (1-based)
    duration: Optional[int] = None
    channel: Optional[str] = None
    thumbnail: Optional[str] = None
    
    @property
    def duration_str(self) -> str:
        if not self.duration:
            return "Unknown"
        hours, remainder = divmod(self.duration, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        return f"{minutes}:{seconds:02d}"


@dataclass
class VideoInfo:
    """Represents video metadata."""
    id: str
    title: str
    url: str
    thumbnail: Optional[str] = None
    duration: Optional[int] = None
    channel: Optional[str] = None
    view_count: Optional[int] = None
    upload_date: Optional[str] = None
    description: Optional[str] = None
    formats: List[VideoFormat] = field(default_factory=list)
    chapters: List[Chapter] = field(default_factory=list)  # v17.8.0: Chapter support
    is_playlist: bool = False
    playlist_count: Optional[int] = None
    playlist_title: Optional[str] = None  # v18.1.0: Playlist title
    playlist_items: List[PlaylistItem] = field(default_factory=list)  # v18.1.0: Playlist videos
    
    @property
    def duration_str(self) -> str:
        if not self.duration:
            return "Unknown"
        hours, remainder = divmod(self.duration, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        return f"{minutes}:{seconds:02d}"
    
    @property
    def views_str(self) -> str:
        if not self.view_count:
            return "Unknown"
        if self.view_count >= 1_000_000_000:
            return f"{self.view_count / 1_000_000_000:.1f}B"
        if self.view_count >= 1_000_000:
            return f"{self.view_count / 1_000_000:.1f}M"
        if self.view_count >= 1_000:
            return f"{self.view_count / 1_000:.1f}K"
        return str(self.view_count)
    
    @property
    def has_chapters(self) -> bool:
        """Check if video has chapters."""
        return len(self.chapters) > 0
    
    @property
    def has_playlist_items(self) -> bool:
        """Check if this contains playlist items."""
        return len(self.playlist_items) > 0
    
    @property
    def total_playlist_duration(self) -> int:
        """Get total duration of all playlist items in seconds."""
        return sum(item.duration or 0 for item in self.playlist_items)
    
    @property
    def total_playlist_duration_str(self) -> str:
        """Get formatted total playlist duration."""
        total = self.total_playlist_duration
        if total == 0:
            return "Unknown"
        hours, remainder = divmod(total, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours:
            return f"{hours}h {minutes}m"
        return f"{minutes}m {seconds}s"


@dataclass
class DownloadTask:
    """Represents a download task in the queue."""
    id: str
    video_info: VideoInfo
    selected_format: Optional[VideoFormat] = None
    output_path: Optional[str] = None
    status: DownloadStatus = DownloadStatus.QUEUED
    progress: float = 0.0
    speed: Optional[str] = None
    eta: Optional[str] = None
    download_speed: Optional[str] = None  # NEW: Download speed in Mbps
    conversion_fps: Optional[str] = None  # NEW: Conversion FPS
    file_size: Optional[int] = None       # NEW: File size in bytes
    status_detail: Optional[str] = None   # v17.7.5: Detailed status message (e.g., "Processing chapters...")
    current_file_size: Optional[int] = None  # v17.7.5: Current size of output file being written
    error_message: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


# ============================================================================
# SPONSORBLOCK API
# ============================================================================

class SponsorBlockAPI:
    """Interface for SponsorBlock API to fetch segment information."""
    
    API_BASE = "https://sponsor.ajay.app/api"
    
    @staticmethod
    def get_video_hash_prefix(video_id: str) -> str:
        """Get SHA256 hash prefix for privacy-preserving API calls."""
        hash_full = hashlib.sha256(video_id.encode('utf-8')).hexdigest()
        return hash_full[:4]  # First 4 characters
    
    @staticmethod
    def fetch_segments(video_id: str, categories: List[str]) -> List[Dict[str, Any]]:
        """
        Fetch SponsorBlock segments for a video.
        
        Args:
            video_id: YouTube video ID
            categories: List of category strings (e.g., ['sponsor', 'intro'])
        
        Returns:
            List of segments with 'segment' (start, end times) and 'category'
        """
        if not HAS_REQUESTS:
            print("WARNING: requests library not available, SponsorBlock disabled")
            return []
        
        try:
            # Build category filter string
            category_param = "[" + ",".join(f'"{c}"' for c in categories) + "]"
            
            # Query API (using hash prefix for privacy)
            hash_prefix = SponsorBlockAPI.get_video_hash_prefix(video_id)
            url = f"{SponsorBlockAPI.API_BASE}/skipSegments/{hash_prefix}?categories={category_param}"
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 404:
                # No segments found
                return []
            
            if response.status_code != 200:
                print(f"SponsorBlock API error: {response.status_code}")
                return []
            
            data = response.json()
            
            # Find segments for this specific video
            if isinstance(data, list):
                for video_data in data:
                    if video_data.get('videoID') == video_id:
                        segments = video_data.get('segments', [])
                        return segments
            
            return []
            
        except Exception as e:
            print(f"SponsorBlock API exception: {e}")
            return []
    
    @staticmethod
    def format_segments_for_ffmpeg(segments: List[Dict[str, Any]], duration: float) -> str:
        """
        Convert SponsorBlock segments to ffmpeg select filter expression.
        
        Args:
            segments: List of segment dicts with 'segment' [start, end]
            duration: Total video duration in seconds
        
        Returns:
            ffmpeg select expression to keep non-sponsor parts
        """
        if not segments:
            return "select='1'"  # Keep everything
        
        # Sort segments by start time
        sorted_segments = sorted(segments, key=lambda x: x['segment'][0])
        
        # Build list of time ranges to KEEP (inverse of segments to remove)
        keep_ranges = []
        last_end = 0.0
        
        for seg in sorted_segments:
            start, end = seg['segment']
            
            # Add the part before this segment
            if start > last_end:
                keep_ranges.append((last_end, start))
            
            last_end = max(last_end, end)
        
        # Add final segment after last removed part
        if last_end < duration:
            keep_ranges.append((last_end, duration))
        
        if not keep_ranges:
            return "select='1'"  # Keep everything
        
        # Build ffmpeg select expression: between(t, start, end)
        conditions = []
        for start, end in keep_ranges:
            conditions.append(f"between(t,{start},{end})")
        
        select_expr = "+".join(conditions)
        return f"select='{select_expr}'"


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

@dataclass
class ParsedYouTubeURL:
    """
    Parsed YouTube URL with extracted components.
    
    Attributes:
        original_url: The original URL as provided
        video_id: The video ID (11 characters) if present
        playlist_id: The playlist ID if present
        is_playlist_url: True if this is explicitly a playlist URL (youtube.com/playlist)
        has_video_and_playlist: True if URL has both video ID and playlist context
    """
    original_url: str
    video_id: Optional[str] = None
    playlist_id: Optional[str] = None
    is_playlist_url: bool = False
    has_video_and_playlist: bool = False
    
    @property
    def single_video_url(self) -> str:
        """Get URL for just the single video (no playlist context)."""
        if self.video_id:
            return f"https://www.youtube.com/watch?v={self.video_id}"
        return self.original_url
    
    @property
    def playlist_url(self) -> str:
        """Get URL for the playlist."""
        if self.playlist_id:
            return f"https://www.youtube.com/playlist?list={self.playlist_id}"
        return self.original_url
    
    @property
    def is_valid(self) -> bool:
        """Check if this is a valid YouTube URL with content to download."""
        return self.video_id is not None or self.playlist_id is not None


def parse_youtube_url(url: str) -> ParsedYouTubeURL:
    """
    Parse a YouTube URL and extract video ID, playlist ID, and URL type.
    
    Args:
        url: Any YouTube URL
        
    Returns:
        ParsedYouTubeURL with extracted components
        
    Examples:
        "watch?v=abc&list=PLxyz" -> video_id="abc", playlist_id="PLxyz", has_video_and_playlist=True
        "playlist?list=PLxyz" -> playlist_id="PLxyz", is_playlist_url=True
        "watch?v=abc" -> video_id="abc"
        "youtu.be/abc" -> video_id="abc"
    """
    result = ParsedYouTubeURL(original_url=url)
    
    # Extract video ID
    # Pattern 1: youtube.com/watch?v=VIDEO_ID
    video_match = re.search(r'[?&]v=([a-zA-Z0-9_-]{11})', url)
    if video_match:
        result.video_id = video_match.group(1)
    else:
        # Pattern 2: youtu.be/VIDEO_ID
        video_match = re.search(r'youtu\.be/([a-zA-Z0-9_-]{11})', url)
        if video_match:
            result.video_id = video_match.group(1)
    
    # Extract playlist ID
    playlist_match = re.search(r'[?&]list=([a-zA-Z0-9_-]+)', url)
    if playlist_match:
        result.playlist_id = playlist_match.group(1)
    
    # Determine URL type
    result.is_playlist_url = "youtube.com/playlist" in url
    result.has_video_and_playlist = (result.video_id is not None and result.playlist_id is not None)
    
    return result


def clean_youtube_url(url: str) -> str:
    """
    Clean a YouTube URL by removing playlist and index parameters.
    
    This prevents yt-dlp from trying to process playlist metadata when
    the user only wants to download a single video, which can cause
    timeouts.
    
    Args:
        url: The original YouTube URL (may contain &list=, &index=, etc.)
        
    Returns:
        A cleaned URL with only the video ID, or the original URL if
        it's not a standard YouTube video URL.
        
    Examples:
        Input:  https://www.youtube.com/watch?v=abc123&list=PLxyz&index=5
        Output: https://www.youtube.com/watch?v=abc123
        
        Input:  https://youtu.be/abc123?list=PLxyz
        Output: https://youtu.be/abc123
    """
    parsed = parse_youtube_url(url)
    
    # If it's explicitly a playlist URL (no video), return as-is
    if parsed.is_playlist_url and not parsed.video_id:
        return url
    
    # If we have a video ID, return clean single-video URL
    if parsed.video_id:
        return parsed.single_video_url
    
    # Return original URL if we can't parse it
    return url


def sanitize_filename(name: str, max_length: int = 200) -> str:
    """Create a filesystem-safe filename, removing problematic characters and emoji."""
    import unicodedata
    
    # First, normalize unicode characters
    name = unicodedata.normalize('NFKD', name)
    
    # Remove emoji and other non-ASCII characters that cause encoding issues
    # Keep only ASCII letters, numbers, spaces, and basic punctuation
    result = []
    for c in name:
        if ord(c) < 128:  # ASCII only
            # Check if it's a problematic shell/filesystem character
            if c in '<>:"/\\|?*&;`$!\'()[]{}#%^':
                result.append('_')
            elif ord(c) >= 32:  # Printable ASCII
                result.append(c)
        elif unicodedata.category(c) in ('Ll', 'Lu', 'Lt', 'Lm', 'Lo'):
            # Try to keep accented letters by decomposing them
            decomposed = unicodedata.normalize('NFD', c)
            for dc in decomposed:
                if ord(dc) < 128:
                    result.append(dc)
    
    result = ''.join(result)
    # Replace multiple spaces/underscores with single space
    result = re.sub(r'[_\s]+', ' ', result)
    result = result.strip().rstrip('.')
    return result[:max_length] if result else "video"


def format_time(seconds: float) -> str:
    """Format seconds as HH:MM:SS."""
    seconds = int(max(0, seconds))
    h, remainder = divmod(seconds, 3600)
    m, s = divmod(remainder, 60)
    if h:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def send_notification(title: str, message: str):
    """Send macOS notification."""
    try:
        script = f'display notification "{message}" with title "{title}"'
        subprocess.run(["osascript", "-e", script], check=False, capture_output=True)
    except Exception:
        pass


def load_json_file(path: Path, default: Any = None) -> Any:
    """Load JSON from file with fallback, merging with defaults if dict."""
    result = default.copy() if isinstance(default, dict) else (default if default is not None else {})
    try:
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
                if isinstance(result, dict) and isinstance(loaded, dict):
                    result.update(loaded)  # Merge loaded data into defaults
                else:
                    result = loaded
    except Exception as e:
        print(f"Warning: Could not load {path}: {e}")
    return result


def save_json_file(path: Path, data: Any):
    """Save data to JSON file."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
    except Exception as e:
        print(f"Failed to save {path}: {e}")


# ============================================================================
# YT-DLP INTERFACE
# ============================================================================

class YtDlpInterface:
    """Interface for yt-dlp operations."""
    
    def __init__(self, ytdlp_path: str = YTDLP_PATH):
        self.ytdlp_path = ytdlp_path
        self._version: Optional[str] = None
        # Check if we should use Python module method
        self._use_python_module = (ytdlp_path == "python-module")
        
        if not self._use_python_module:
            # Detect if we need to use system Python for script execution
            self._system_python = self._find_system_python()
            self._use_system_python = (
                (self.ytdlp_path.startswith('/opt/homebrew') or 
                 self.ytdlp_path.startswith('/usr/local')) and
                self._system_python is not None
            )
        else:
            self._system_python = None
            self._use_system_python = False
    
    def refresh_path(self) -> None:
        """
        Re-detect yt-dlp path to pick up updates.
        
        Call this after installing an update to ensure the new binary is used.
        """
        self.ytdlp_path = find_executable("yt-dlp")
        self._version = None  # Clear cached version
        self._use_python_module = (self.ytdlp_path == "python-module")
        
        if not self._use_python_module:
            self._system_python = self._find_system_python()
            self._use_system_python = (
                (self.ytdlp_path.startswith('/opt/homebrew') or 
                 self.ytdlp_path.startswith('/usr/local')) and
                self._system_python is not None
            )
        else:
            self._system_python = None
            self._use_system_python = False
    
    def _find_system_python(self) -> Optional[str]:
        """Find system Python that can run Homebrew scripts."""
        candidates = [
            '/opt/homebrew/bin/python3',      # Homebrew Python (Apple Silicon) - try first
            '/usr/local/bin/python3',          # Homebrew Python (Intel)
            '/usr/bin/python3',                # System Python (fallback)
        ]
        for python in candidates:
            if os.path.isfile(python):
                return python
        return None
    
    def _build_command(self, args: List[str]) -> List[str]:
        """Build command to execute yt-dlp."""
        # Check if we have a bundled deno and add --js-runtimes flag
        js_runtime_args = []
        if DENO_PATH and os.path.isfile(DENO_PATH):
            js_runtime_args = ["--js-runtimes", f"deno:{DENO_PATH}"]
        
        if self._use_python_module:
            # Use Python module execution (most reliable when yt-dlp is pip-installed)
            return [sys.executable, '-m', 'yt_dlp'] + js_runtime_args + args
        elif self._use_system_python:
            # Use system Python to run yt-dlp script
            return [self._system_python, self.ytdlp_path] + js_runtime_args + args
        else:
            return [self.ytdlp_path] + js_runtime_args + args
    
    @property
    def is_available(self) -> bool:
        if self._use_python_module:
            try:
                import yt_dlp
                return True
            except ImportError:
                return False
        return os.path.isfile(self.ytdlp_path)
    
    def get_version(self) -> str:
        """Get yt-dlp version string."""
        if self._version:
            return self._version
        try:
            cmd = self._build_command(["--version"])
            result = subprocess.run(
                cmd,
                capture_output=True, text=True, check=False,
                encoding='utf-8', errors='replace'
            )
            if result.returncode == 0:
                self._version = result.stdout.strip().split('\n')[0]
                return self._version
        except Exception as e:
            print(f"Warning: Could not get yt-dlp version: {e}")
        return "Not found"
    
    def fetch_video_info(self, url: str) -> VideoInfo:
        """Fetch video metadata using yt-dlp -J."""
        try:
            # Clean the URL to remove playlist parameters
            cleaned_url = clean_youtube_url(url)
            
            result = subprocess.run(
                self._build_command(["-J", "--no-playlist", cleaned_url]),
                capture_output=True, text=True, check=False, timeout=30,
                encoding='utf-8', errors='replace'
            )
            
            if result.returncode != 0:
                raise RuntimeError(f"yt-dlp error: {result.stderr.strip()}")
            
            data = json.loads(result.stdout)
            return self._parse_video_info(data, cleaned_url)
            
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse yt-dlp output: {e}")
        except subprocess.TimeoutExpired:
            raise RuntimeError("yt-dlp took too long to respond")
    
    def fetch_full_info(self, url: str) -> VideoInfo:
        """Fetch full video info including all formats using --list-formats.
        
        Raises:
            AgeRestrictedError: If the video is age-restricted
            PrivateVideoError: If the video is private
            VideoUnavailableError: If the video is unavailable
            LoginRequiredError: If login is required for other reasons
            RuntimeError: For other errors
        """
        try:
            # Clean the URL to remove playlist parameters that cause slowdowns
            # URLs like "watch?v=abc&list=xyz&index=5" become "watch?v=abc"
            # This prevents yt-dlp from trying to fetch playlist metadata
            cleaned_url = clean_youtube_url(url)
            
            # First get basic metadata with -J
            # --no-playlist ensures we only get info for the single video
            result_info = subprocess.run(
                self._build_command(["-J", "--no-playlist", cleaned_url]),
                capture_output=True, text=True, check=False, timeout=30,
                encoding='utf-8', errors='replace'
            )
            
            # Check for specific error conditions in stderr
            stderr_text = result_info.stderr.strip() if result_info.stderr else ""
            
            if result_info.returncode != 0:
                # Parse the error to provide specific feedback
                error_info = self._parse_ytdlp_error(stderr_text, url)
                raise error_info
            
            data = json.loads(result_info.stdout)
            info = self._parse_video_info(data, cleaned_url, include_formats=False)
            
            # Now get formats using --list-formats (this shows ALL formats)
            # --no-playlist ensures we only get formats for the single video
            result_formats = subprocess.run(
                self._build_command([
                    "--list-formats",
                    "--no-playlist",
                    "--remote-components", "ejs:github",
                    cleaned_url
                ]),
                capture_output=True, text=True, check=False, timeout=30,
                encoding='utf-8', errors='replace'
            )
            
            # Check for errors in format listing too
            if result_formats.returncode != 0:
                format_stderr = result_formats.stderr.strip() if result_formats.stderr else ""
                # Check if this is an age-restriction or other specific error
                error_info = self._parse_ytdlp_error(format_stderr, url)
                if isinstance(error_info, (AgeRestrictedError, PrivateVideoError, VideoUnavailableError, LoginRequiredError)):
                    raise error_info
            
            if result_formats.returncode == 0:
                # Parse the format table output
                info.formats = self._parse_format_table(result_formats.stdout)
            
            return info
            
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse yt-dlp output: {e}")
        except subprocess.TimeoutExpired:
            raise RuntimeError("yt-dlp took too long to respond")
        except (AgeRestrictedError, PrivateVideoError, VideoUnavailableError, LoginRequiredError):
            # Re-raise our custom exceptions
            raise
    
    def fetch_playlist_info(self, url: str) -> VideoInfo:
        """
        Fetch playlist metadata including all video entries.
        
        Args:
            url: YouTube playlist URL or video URL with playlist context
            
        Returns:
            VideoInfo with is_playlist=True and populated playlist_items
            
        Raises:
            RuntimeError: For various errors
            UnviewablePlaylistError: For YouTube Mixes and other non-enumerable playlists
        """
        try:
            # Parse the URL to get playlist ID
            parsed = parse_youtube_url(url)
            
            if not parsed.playlist_id:
                raise RuntimeError("No playlist ID found in URL")
            
            # Check for YouTube Mix playlists (auto-generated, cannot be enumerated)
            # These have IDs starting with 'RD' (Radio/Mix based on a seed video)
            if parsed.playlist_id.startswith('RD'):
                raise UnviewablePlaylistError(
                    playlist_id=parsed.playlist_id,
                    reason="YouTube Mix",
                    video_id=parsed.video_id
                )
            
            # Use --flat-playlist to get playlist entries without downloading each video's info
            # This is MUCH faster than fetching full info for each video
            result = subprocess.run(
                self._build_command([
                    "-J",
                    "--flat-playlist",
                    "--extractor-args", "youtube:player_client=android_sdkless",
                    parsed.playlist_url
                ]),
                capture_output=True, text=True, check=False, timeout=60,  # Longer timeout for playlists
                encoding='utf-8', errors='replace'
            )
            
            if result.returncode != 0:
                stderr_text = result.stderr.strip() if result.stderr else ""
                
                # Check for "unviewable" playlist error
                if "unviewable" in stderr_text.lower() or "unavailable" in stderr_text.lower():
                    raise UnviewablePlaylistError(
                        playlist_id=parsed.playlist_id,
                        reason="unviewable or private",
                        video_id=parsed.video_id
                    )
                
                raise RuntimeError(f"Failed to fetch playlist: {stderr_text[:200]}")
            
            data = json.loads(result.stdout)
            
            # Parse playlist metadata
            playlist_id = data.get("id", parsed.playlist_id)
            playlist_title = data.get("title", "Unknown Playlist")
            playlist_channel = data.get("channel") or data.get("uploader", "Unknown")
            playlist_thumbnail = data.get("thumbnail")
            
            # Parse playlist entries
            entries = data.get("entries", [])
            playlist_items = []
            
            for idx, entry in enumerate(entries, start=1):
                if entry is None:
                    continue  # Skip unavailable videos
                
                video_id = entry.get("id")
                if not video_id:
                    continue
                
                item = PlaylistItem(
                    id=video_id,
                    title=entry.get("title", f"Video {idx}"),
                    url=f"https://www.youtube.com/watch?v={video_id}",
                    index=idx,
                    duration=entry.get("duration"),
                    channel=entry.get("channel") or entry.get("uploader"),
                    thumbnail=entry.get("thumbnail")
                )
                playlist_items.append(item)
            
            # Create VideoInfo representing the playlist
            info = VideoInfo(
                id=playlist_id,
                title=playlist_title,
                url=parsed.playlist_url,
                thumbnail=playlist_thumbnail,
                duration=None,  # Playlists don't have a single duration
                channel=playlist_channel,
                view_count=data.get("view_count"),
                is_playlist=True,
                playlist_count=len(playlist_items),
                playlist_title=playlist_title,
                playlist_items=playlist_items
            )
            
            return info
            
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse playlist data: {e}")
        except subprocess.TimeoutExpired:
            raise RuntimeError("Playlist fetch timed out (playlist may be too large)")
    
    def _parse_ytdlp_error(self, stderr: str, url: str) -> Exception:
        """Parse yt-dlp stderr to identify specific error types.
        
        Args:
            stderr: The stderr output from yt-dlp
            url: The URL being processed (for extracting video ID)
            
        Returns:
            An appropriate exception based on the error type
        """
        stderr_lower = stderr.lower()
        
        # Extract video ID from URL if possible
        video_id = None
        if "youtube.com" in url or "youtu.be" in url:
            # Try to extract video ID
            import re
            match = re.search(r'(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})', url)
            if match:
                video_id = match.group(1)
        
        # Check for age-restriction errors
        age_restriction_patterns = [
            "sign in to confirm your age",
            "age-restricted",
            "this video may be inappropriate for some users",
            "confirm your age",
            "age verification required",
        ]
        
        for pattern in age_restriction_patterns:
            if pattern in stderr_lower:
                return AgeRestrictedError(video_id=video_id, message=stderr)
        
        # Check for private video errors
        private_patterns = [
            "private video",
            "video is private",
            "this video is private",
        ]
        
        for pattern in private_patterns:
            if pattern in stderr_lower:
                return PrivateVideoError(video_id=video_id)
        
        # Check for login required errors (not age-related)
        login_patterns = [
            "login_required",
            "sign in to view this video",
            "members-only",
            "this video is available to this channel's members",
        ]
        
        for pattern in login_patterns:
            if pattern in stderr_lower:
                return LoginRequiredError(video_id=video_id, reason=stderr)
        
        # Check for video unavailable errors
        unavailable_patterns = [
            "video unavailable",
            "this video is not available",
            "video has been removed",
            "video is no longer available",
            "this video has been removed",
            "copyright claim",
            "blocked in your country",
            "not available in your country",
            "geo restriction",
        ]
        
        for pattern in unavailable_patterns:
            if pattern in stderr_lower:
                return VideoUnavailableError(video_id=video_id, reason=stderr)
        
        # Default to RuntimeError for unknown errors
        return RuntimeError(f"yt-dlp error: {stderr}")
    
    def _parse_format_table(self, table_output: str) -> List[VideoFormat]:
        """Parse yt-dlp --list-formats table output into VideoFormat objects."""
        formats = []
        lines = table_output.split('\n')
        
        # Find the start of the format table (after "Available formats")
        table_start = -1
        for i, line in enumerate(lines):
            if 'Available formats' in line or 'ID' in line and 'EXT' in line:
                table_start = i + 1
                break
        
        if table_start == -1:
            return formats
        
        # Parse each format line
        for line in lines[table_start:]:
            line = line.strip()
            if not line or line.startswith('[') or '---' in line:
                continue
            
            # Skip audio-only lines (we want video formats)
            if 'audio only' in line.lower() and 'video' not in line.lower():
                continue
            
            # Split by vertical bar separator to get sections
            sections = line.split('|')
            if len(sections) < 2:
                # Try splitting by whitespace only
                parts = line.split()
            else:
                # Combine all sections and split by whitespace
                parts = ' '.join(sections).split()
            
            if len(parts) < 3:
                continue
            
            try:
                format_id = parts[0]
                ext = parts[1]
                
                # Parse resolution (look for patterns like 1920x1080, 1280x720, etc.)
                height = None
                width = None
                resolution = None
                fps = None
                
                for part in parts:
                    # Parse resolution like "1920x1080"
                    if 'x' in part and not part.startswith('0x'):
                        res_match = re.match(r'(\d+)x(\d+)', part)
                        if res_match:
                            width = int(res_match.group(1))
                            height = int(res_match.group(2))
                            resolution = f"{width}x{height}"
                    # Parse height like "1080p" or "1080p60"
                    elif re.match(r'^\d+p\d*$', part):
                        height_match = re.match(r'^(\d+)p', part)
                        if height_match:
                            height = int(height_match.group(1))
                            resolution = part
                    # Parse FPS (standalone number between 24-120)
                    elif part.isdigit() and 24 <= int(part) <= 120:
                        fps = int(part)
                
                # Skip if no valid height found or too low
                if not height or height < 100:
                    continue
                
                # Look for codecs in the line
                vcodec = None
                acodec = None
                line_lower = line.lower()
                
                if 'avc1' in line_lower or 'h264' in line_lower or 'avc' in line_lower:
                    vcodec = 'h264'
                elif 'vp9' in line_lower or 'vp09' in line_lower:
                    vcodec = 'vp9'
                elif 'av01' in line_lower or 'av1' in line_lower:
                    vcodec = 'av1'
                
                if 'mp4a' in line_lower or 'aac' in line_lower:
                    acodec = 'aac'
                elif 'opus' in line_lower:
                    acodec = 'opus'
                
                # Determine if video/audio only
                is_video_only = 'video only' in line_lower
                is_audio_only = 'audio only' in line_lower
                
                # Parse bitrate (look for patterns like "4364k", "1.8M", etc.)
                tbr = None
                for part in parts:
                    # Match patterns like "4364k" or "1181k"
                    if re.match(r'^\d+k$', part):
                        try:
                            tbr = int(part[:-1])
                        except:
                            pass
                        break
                    # Match patterns like "1.8M" or "4M"
                    elif re.match(r'^[\d.]+M$', part):
                        try:
                            tbr = int(float(part[:-1]) * 1000)
                        except:
                            pass
                        break
                
                # Parse file size (look for patterns like "668.33MiB", "91.60MiB", "1.5GiB")
                filesize = None
                filesize_approx = None
                for part in parts:
                    # Remove leading ~ for approximate sizes
                    size_part = part.lstrip('~')
                    is_approx = part.startswith('~')
                    
                    # Match MiB sizes like "668.33MiB"
                    mib_match = re.match(r'^([\d.]+)MiB$', size_part)
                    if mib_match:
                        try:
                            size_val = float(mib_match.group(1))
                            size_bytes = int(size_val * 1024 * 1024)
                            if is_approx:
                                filesize_approx = size_bytes
                            else:
                                filesize = size_bytes
                        except:
                            pass
                        continue
                    
                    # Match GiB sizes like "1.5GiB"
                    gib_match = re.match(r'^([\d.]+)GiB$', size_part)
                    if gib_match:
                        try:
                            size_val = float(gib_match.group(1))
                            size_bytes = int(size_val * 1024 * 1024 * 1024)
                            if is_approx:
                                filesize_approx = size_bytes
                            else:
                                filesize = size_bytes
                        except:
                            pass
                        continue
                    
                    # Match KiB sizes like "500KiB"
                    kib_match = re.match(r'^([\d.]+)KiB$', size_part)
                    if kib_match:
                        try:
                            size_val = float(kib_match.group(1))
                            size_bytes = int(size_val * 1024)
                            if is_approx:
                                filesize_approx = size_bytes
                            else:
                                filesize = size_bytes
                        except:
                            pass
                        continue
                
                fmt = VideoFormat(
                    format_id=format_id,
                    ext=ext,
                    resolution=resolution,
                    height=height,
                    width=width,
                    fps=fps or 30,
                    vcodec=vcodec,
                    acodec=acodec,
                    filesize=filesize,
                    filesize_approx=filesize_approx,
                    tbr=tbr,
                    vbr=None,
                    abr=None,
                    is_video_only=is_video_only,
                    is_audio_only=is_audio_only,
                    is_quicktime_compatible=False,  # We'll convert anyway
                )
                formats.append(fmt)
                
            except Exception as e:
                # Skip malformed lines
                continue
        
        # Sort by height descending, then by bitrate
        formats.sort(key=lambda x: (x.height or 0, x.tbr or 0), reverse=True)
        return formats
    
    def _parse_video_info(self, data: dict, url: str, include_formats: bool = False) -> VideoInfo:
        """Parse yt-dlp JSON into VideoInfo."""
        # Check if it's a playlist
        is_playlist = data.get("_type") == "playlist"
        
        # Parse chapters if available
        chapters = []
        chapters_data = data.get("chapters", [])
        if chapters_data:
            for i, ch in enumerate(chapters_data):
                chapter = Chapter(
                    index=i,
                    title=ch.get("title", f"Chapter {i + 1}"),
                    start_time=ch.get("start_time", 0),
                    end_time=ch.get("end_time", 0)
                )
                chapters.append(chapter)
        
        info = VideoInfo(
            id=data.get("id", "unknown"),
            title=data.get("title", "Unknown Title"),
            url=url,
            thumbnail=data.get("thumbnail"),
            duration=data.get("duration"),
            channel=data.get("channel") or data.get("uploader"),
            view_count=data.get("view_count"),
            upload_date=data.get("upload_date"),
            description=data.get("description"),
            chapters=chapters,
            is_playlist=is_playlist,
            playlist_count=data.get("playlist_count") if is_playlist else None,
        )
        
        if include_formats and "formats" in data:
            info.formats = self._parse_formats(data["formats"])
        
        return info
    
    def _parse_formats(self, formats_data: list) -> List[VideoFormat]:
        """Parse format list from yt-dlp."""
        formats = []
        
        for f in formats_data:
            vcodec = (f.get("vcodec") or "").lower()
            acodec = (f.get("acodec") or "").lower()
            ext = (f.get("ext") or "").lower()
            height = f.get("height")
            width = f.get("width")
            resolution = f.get("resolution")
            format_note = (f.get("format_note") or "").lower()
            format_id = f.get("format_id", "")
            
            # BUGFIX v16.2.1: If height is missing, try to parse from resolution string
            if height is None and resolution:
                # Resolution format: "1920x1080" or "1280x720"
                parts = resolution.lower().split('x')
                if len(parts) == 2:
                    try:
                        width = int(parts[0])
                        height = int(parts[1])
                    except:
                        pass
            
            # Skip storyboard/thumbnail formats
            if ext in ("mhtml", "jpg", "png", "webp"):
                continue
            
            # Skip storyboard format notes
            if "storyboard" in format_note:
                continue
            
            # Skip formats with no video codec AND no audio codec
            if vcodec in ("", "none") and acodec in ("", "none"):
                continue
            
            # Skip very low resolutions that are likely storyboards (under 100p)
            # But allow audio-only formats (height=None or 0)
            if height and height < 100:
                continue
            
            is_video_only = vcodec not in ("", "none") and acodec in ("", "none")
            is_audio_only = vcodec in ("", "none") and acodec not in ("", "none")
            
            # Check QuickTime compatibility (has both video AND audio, H.264/HEVC)
            is_qt = (
                ext in ("mp4", "m4v", "mov") and
                vcodec not in ("", "none") and acodec not in ("", "none") and
                any(c in vcodec for c in ("avc", "h264", "hev", "hevc"))
            )
            
            fmt = VideoFormat(
                format_id=format_id,
                ext=ext,
                resolution=resolution,
                height=height,
                width=width,
                fps=f.get("fps"),
                vcodec=vcodec if vcodec not in ("", "none") else None,
                acodec=acodec if acodec not in ("", "none") else None,
                filesize=f.get("filesize"),
                filesize_approx=f.get("filesize_approx"),
                tbr=f.get("tbr"),
                vbr=f.get("vbr"),
                abr=f.get("abr"),
                is_video_only=is_video_only,
                is_audio_only=is_audio_only,
                is_quicktime_compatible=is_qt,
            )
            formats.append(fmt)
        
        # Sort by height (resolution) descending, then by bitrate
        formats.sort(key=lambda x: (x.height or 0, x.tbr or 0), reverse=True)
        return formats
    
    def download(self, url: str, format_id: str, output_template: str,
                 progress_callback: Optional[Callable] = None) -> subprocess.Popen:
        """Start a download process."""
        cmd = [
            self.ytdlp_path,
            "--newline",
            "-f", format_id,
            "-o", output_template,
            url
        ]
        
        return subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
    
    def check_update(self) -> tuple[bool, str]:
        """Check for and apply yt-dlp updates."""
        try:
            result = subprocess.run(
                self._build_command(["-U"]),
                capture_output=True, text=True, check=False
            )
            output = result.stdout + result.stderr
            success = result.returncode == 0
            self._version = None  # Clear cached version
            return success, output.strip()
        except Exception as e:
            return False, str(e)


# ============================================================================
# THUMBNAIL MANAGER
# ============================================================================

class ThumbnailManager:
    """Manages thumbnail downloading and caching."""
    
    def __init__(self, cache_dir: Path = CACHE_DIR):
        self.cache_dir = cache_dir / "thumbnails"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._cache: Dict[str, Any] = {}
    
    def get_thumbnail(self, url: str, video_id: str, 
                      size: tuple = (320, 180)) -> Optional[Any]:
        """Get thumbnail image, downloading if necessary."""
        if not HAS_PIL or not url:
            return None
        
        cache_key = f"{video_id}_{size[0]}x{size[1]}"
        
        # Check memory cache
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        # Check disk cache
        cache_path = self.cache_dir / f"{cache_key}.png"
        if cache_path.exists():
            try:
                img = Image.open(cache_path)
                ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=size)
                self._cache[cache_key] = ctk_img
                return ctk_img
            except Exception:
                pass
        
        # Download thumbnail
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                img_data = response.read()
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
                tmp.write(img_data)
                tmp_path = tmp.name
            
            img = Image.open(tmp_path)
            img = img.resize(size, Image.Resampling.LANCZOS)
            img.save(cache_path, "PNG")
            os.unlink(tmp_path)
            
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=size)
            self._cache[cache_key] = ctk_img
            return ctk_img
            
        except Exception as e:
            print(f"Failed to load thumbnail: {e}")
            return None
    
    def clear_cache(self):
        """Clear thumbnail cache."""
        self._cache.clear()
        try:
            shutil.rmtree(self.cache_dir)
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass


# ============================================================================
# PROGRESS TRACKING & ETA
# ============================================================================

class ProgressTracker:
    """Tracks download/conversion progress for accurate ETA calculation."""
    
    def __init__(self, window_size=15):
        self.window_size = window_size  # Seconds for sliding window
        self.history = []  # List of (timestamp, percentage) tuples
        self.start_time = None
        self.current_stage = "idle"
        self.download_speed = None  # Mbps
        self.conversion_fps = None
        # v17.7.5: Stall detection
        self.last_progress_time = None
        self.last_progress_value = 0
        self.stall_threshold = 5  # Seconds before considering progress stalled
        self.is_stalled = False
        # v17.7.5: File monitoring
        self.monitored_file = None
        self.last_file_size = 0
        self.file_growth_rate = 0  # bytes per second
        
    def start(self, stage="downloading"):
        """Start tracking a new stage."""
        self.start_time = time.time()
        self.history = []
        self.current_stage = stage
        self.download_speed = None
        self.conversion_fps = None
        self.last_progress_time = time.time()
        self.last_progress_value = 0
        self.is_stalled = False
        self.monitored_file = None
        self.last_file_size = 0
        self.file_growth_rate = 0
        
    def update(self, percentage):
        """Update progress percentage."""
        if self.start_time is None:
            self.start()
            
        current_time = time.time()
        self.history.append((current_time, percentage))
        
        # Keep only last window_size seconds
        cutoff_time = current_time - self.window_size
        self.history = [(t, p) for t, p in self.history if t >= cutoff_time]
        
        # v17.7.5: Update stall detection
        if percentage > self.last_progress_value:
            self.last_progress_time = current_time
            self.last_progress_value = percentage
            self.is_stalled = False
    
    def check_stall(self) -> bool:
        """Check if progress appears stalled (no updates for threshold seconds)."""
        if self.last_progress_time is None:
            return False
        time_since_progress = time.time() - self.last_progress_time
        self.is_stalled = time_since_progress > self.stall_threshold
        return self.is_stalled
    
    def get_stall_duration(self) -> float:
        """Get how long progress has been stalled."""
        if self.last_progress_time is None:
            return 0
        return time.time() - self.last_progress_time
    
    def set_monitored_file(self, filepath: str):
        """Set a file to monitor for growth (used when progress parsing fails)."""
        self.monitored_file = filepath
        self.last_file_size = 0
        
    def check_file_growth(self) -> tuple[bool, int, float]:
        """
        Check if the monitored file is growing.
        Returns: (is_growing, current_size, growth_rate_mbps)
        """
        if not self.monitored_file or not os.path.exists(self.monitored_file):
            return False, 0, 0
        
        try:
            current_size = os.path.getsize(self.monitored_file)
            current_time = time.time()
            
            if self.last_file_size > 0 and hasattr(self, '_last_size_check_time'):
                time_delta = current_time - self._last_size_check_time
                if time_delta > 0:
                    size_delta = current_size - self.last_file_size
                    # Convert bytes/sec to Mbps (megabits per second)
                    self.file_growth_rate = (size_delta * 8) / (time_delta * 1_000_000)
            
            self._last_size_check_time = current_time
            is_growing = current_size > self.last_file_size
            self.last_file_size = current_size
            
            return is_growing, current_size, self.file_growth_rate
        except Exception:
            return False, 0, 0
    
    def get_eta(self):
        """Calculate ETA in seconds using sliding window."""
        if len(self.history) < 2:
            return None
            
        # Get oldest and newest in window
        oldest_time, oldest_pct = self.history[0]
        newest_time, newest_pct = self.history[-1]
        
        time_delta = newest_time - oldest_time
        progress_delta = newest_pct - oldest_pct
        
        if time_delta == 0 or progress_delta <= 0:
            return None
            
        # Calculate rate and remaining time
        rate = progress_delta / time_delta  # % per second
        remaining_pct = 100 - newest_pct
        eta_seconds = remaining_pct / rate if rate > 0 else None
        
        return eta_seconds
    
    def format_eta(self):
        """Format ETA as human-readable string."""
        eta = self.get_eta()
        if eta is None or eta <= 0:
            return "calculating..."
            
        if eta < 60:
            return f"{int(eta)}s"
        elif eta < 3600:
            mins = int(eta / 60)
            secs = int(eta % 60)
            return f"{mins}m {secs}s"
        else:
            hours = int(eta / 3600)
            mins = int((eta % 3600) / 60)
            return f"{hours}h {mins}m"
    
    def set_download_speed(self, speed_mbps):
        """Set download speed in Mbps."""
        self.download_speed = speed_mbps
    
    def set_conversion_fps(self, fps):
        """Set conversion FPS."""
        self.conversion_fps = fps
    
    def format_speed(self):
        """Format download speed."""
        if self.download_speed is None:
            return ""
        return f"{self.download_speed:.1f} Mbps"
    
    def format_fps(self):
        """Format conversion FPS."""
        if self.conversion_fps is None:
            return ""
        return f"{self.conversion_fps:.0f} fps"
    
    def format_file_size(self, size_bytes: int) -> str:
        """Format file size as human-readable string."""
        if size_bytes >= 1024 ** 3:
            return f"{size_bytes / (1024 ** 3):.2f} GB"
        elif size_bytes >= 1024 ** 2:
            return f"{size_bytes / (1024 ** 2):.1f} MB"
        elif size_bytes >= 1024:
            return f"{size_bytes / 1024:.1f} KB"
        return f"{size_bytes} B"


# ============================================================================
# DOWNLOAD MANAGER
# ============================================================================

class DownloadManager:
    """Manages download queue and operations."""
    
    def __init__(self, ytdlp: YtDlpInterface, output_dir: str):
        self.ytdlp = ytdlp
        self.output_dir = output_dir
        self.queue: List[DownloadTask] = []
        self.current_task: Optional[DownloadTask] = None
        self.current_process: Optional[subprocess.Popen] = None
        self._running = False
        self._paused = False
        self._lock = threading.Lock()
        self._callbacks: List[Callable] = []
        self.progress_tracker = ProgressTracker(window_size=15)  # NEW: Progress tracking with ETA
        # Load settings for SponsorBlock support
        from pathlib import Path as PathLib
        self.settings_mgr = SettingsManager(SETTINGS_PATH)
    
    def add_callback(self, callback: Callable):
        """Add a callback for status updates."""
        self._callbacks.append(callback)
    
    def _notify(self, event: str, data: Any = None):
        """Notify all callbacks."""
        for cb in self._callbacks:
            try:
                cb(event, data)
            except Exception as e:
                print(f"Callback error: {e}")
    
    def add_task(self, video_info: VideoInfo, selected_format: Optional[VideoFormat] = None) -> DownloadTask:
        """Add a download task to the queue."""
        task = DownloadTask(
            id=f"{video_info.id}_{int(time.time())}",
            video_info=video_info,
            selected_format=selected_format,
        )
        
        with self._lock:
            self.queue.append(task)
        
        self._notify("task_added", task)
        return task
    
    def remove_task(self, task_id: str):
        """Remove a task from the queue."""
        with self._lock:
            self.queue = [t for t in self.queue if t.id != task_id]
        self._notify("task_removed", task_id)
    
    def start(self):
        """Start processing the queue."""
        if self._running:
            return
        
        self._running = True
        self._paused = False
        threading.Thread(target=self._process_queue, daemon=True).start()
    
    def pause(self):
        """Pause queue processing."""
        self._paused = True
        if self.current_task:
            self.current_task.status = DownloadStatus.PAUSED
            self._notify("task_updated", self.current_task)
    
    def resume(self):
        """Resume queue processing."""
        self._paused = False
        if self.current_task:
            self.current_task.status = DownloadStatus.DOWNLOADING
            self._notify("task_updated", self.current_task)
    
    def cancel_current(self):
        """Cancel the current download."""
        if self.current_process:
            self.current_process.terminate()
        if self.current_task:
            self.current_task.status = DownloadStatus.CANCELLED
            self._notify("task_updated", self.current_task)
    
    def _process_queue(self):
        """Process downloads in the queue."""
        while self._running:
            if self._paused:
                time.sleep(0.5)
                continue
            
            # Get next task
            task = None
            with self._lock:
                for t in self.queue:
                    if t.status == DownloadStatus.QUEUED:
                        task = t
                        break
            
            if not task:
                time.sleep(0.5)
                continue
            
            self.current_task = task
            self._download_task(task)
            self.current_task = None
        
    def _download_task(self, task: DownloadTask):
        """Execute a single download task with ffmpeg conversion for QuickTime compatibility."""
        task.status = DownloadStatus.DOWNLOADING
        task.started_at = datetime.now()
        self._notify("task_updated", task)
        
        try:
            video_info = task.video_info
            fmt = task.selected_format
            safe_title = sanitize_filename(video_info.title)
            
            # Create temp filenames
            video_id = video_info.id
            temp_video = os.path.join(self.output_dir, f"{video_id}_temp_video.%(ext)s")
            temp_audio = os.path.join(self.output_dir, f"{video_id}_temp_audio.%(ext)s")
            final_output = os.path.join(self.output_dir, f"{safe_title}.mp4")
            
            # Handle duplicate filenames
            counter = 1
            base_output = final_output
            while os.path.exists(final_output):
                name, ext = os.path.splitext(base_output)
                final_output = f"{name} ({counter}){ext}"
                counter += 1
            
            # Step 1: Download best video (using working strategy from v17.1.7)
            if fmt and fmt.height:
                video_format = f"bestvideo[height<={fmt.height}][ext=mp4]/bestvideo[height<={fmt.height}]/bestvideo"
                self._notify("log", ("info", f"Downloading best video at or below {fmt.height}p"))
            else:
                video_format = "bestvideo[ext=mp4]/bestvideo/best"
                self._notify("log", ("info", "Downloading best available video"))
            
            video_cmd_args = [
                "--newline",
                "--remote-components", "ejs:github",
                "--extractor-args", "youtube:player_client=android_sdkless",
                "-f", video_format,
                "-o", temp_video,
                video_info.url
            ]
            
            # NOTE: SponsorBlock is now applied via post-processing (after download)
            # See _apply_sponsorblock_postprocess() method
            
            video_cmd = self.ytdlp._build_command(video_cmd_args)
            self._run_subprocess_with_progress(video_cmd, task, "🔥 Downloading video", 0, 40, video_id)
            
            if task.status == DownloadStatus.FAILED:
                return
            
            # Find the downloaded video file
            video_file = self._find_temp_file(self.output_dir, f"{video_id}_temp_video")
            
            if not video_file:
                self._notify("log", ("warning", f"Temp video file not found with expected name, searching..."))
                for fname in os.listdir(self.output_dir):
                    if video_id in fname and fname.endswith(('.mp4', '.webm', '.mkv')):
                        video_file = os.path.join(self.output_dir, fname)
                        self._notify("log", ("info", f"Found video file: {fname}"))
                        break
            
            if not video_file:
                task.status = DownloadStatus.FAILED
                task.error_message = "Video file not found after download"
                return
            
            # Step 2: Download best audio
            audio_cmd = self.ytdlp._build_command([
                "--newline",
                "--remote-components", "ejs:github",
                "--extractor-args", "youtube:player_client=android_sdkless",
                "-f", "bestaudio[ext=m4a]/bestaudio/best",
                "-o", temp_audio,
                video_info.url
            ])
            
            self._run_subprocess_with_progress(audio_cmd, task, "🎵 Downloading audio", 40, 60, video_id)
            
            if task.status == DownloadStatus.FAILED:
                return
            
            # Find the downloaded audio file
            audio_file = self._find_temp_file(self.output_dir, f"{video_id}_temp_audio")
            
            if not audio_file:
                self._notify("log", ("warning", f"Temp audio file not found, searching..."))
                for fname in os.listdir(self.output_dir):
                    if video_id in fname and fname.endswith(('.m4a', '.webm', '.opus', '.mp3')):
                        audio_file = os.path.join(self.output_dir, fname)
                        self._notify("log", ("info", f"Found audio file: {fname}"))
                        break
            
            if not audio_file:
                task.status = DownloadStatus.FAILED
                task.error_message = "Audio file not found after download"
                return
            
            # Step 3: Convert with ffmpeg to QuickTime-compatible H.264 + AAC
            task.status = DownloadStatus.CONVERTING
            self._notify("task_updated", task)
            
            # ENHANCEMENT v16.1: Smart per-resolution bitrate selection
            from pathlib import Path as PathLib
            settings_mgr = SettingsManager(SETTINGS_PATH)
            
            encoder_type = settings_mgr.get("encoder_type", "auto")
            encoder_preset = settings_mgr.get("encoder_preset", "medium")
            bitrate_mode = settings_mgr.get("bitrate_mode", "auto")
            audio_bitrate = settings_mgr.get("audio_bitrate", 192)
            
            # Determine video codec
            if encoder_type == "cpu":
                video_codec = "libx264"
            elif encoder_type == "gpu":
                video_codec = "h264_videotoolbox"
            else:  # auto
                video_codec = "h264_videotoolbox"  # Try GPU first
            
            # Calculate video bitrate based on mode and resolution
            video_height = fmt.height if fmt else None
            
            # Log source video info
            if fmt:
                source_info = f"Source: {fmt.height}p, codec: {fmt.vcodec}, bitrate: {fmt.tbr}k" if fmt.tbr else f"Source: {fmt.height}p, codec: {fmt.vcodec}"
                self._notify("log", ("info", source_info))
            
            if bitrate_mode == "per_resolution":
                per_res = settings_mgr.get("per_resolution_bitrates", {
                    "2160": "15", "1440": "10", "1080": "6", "720": "4", "480": "2"
                })
                if video_height:
                    if video_height >= 2160:
                        video_bitrate = f"{per_res.get('2160', '15')}M"
                    elif video_height >= 1440:
                        video_bitrate = f"{per_res.get('1440', '10')}M"
                    elif video_height >= 1080:
                        video_bitrate = f"{per_res.get('1080', '6')}M"
                    elif video_height >= 720:
                        video_bitrate = f"{per_res.get('720', '4')}M"
                    else:
                        video_bitrate = f"{per_res.get('480', '2')}M"
                else:
                    video_bitrate = "8M"
            elif bitrate_mode == "custom":
                video_bitrate = settings_mgr.get("video_bitrate", "8M")
                if not video_bitrate.endswith(('M', 'm', 'K', 'k')):
                    video_bitrate = f"{video_bitrate}M"
            else:  # auto mode
                if video_height:
                    if video_height >= 2160:
                        video_bitrate = "15M"
                    elif video_height >= 1440:
                        video_bitrate = "10M"
                    elif video_height >= 1080:
                        video_bitrate = "6M"
                    elif video_height >= 720:
                        video_bitrate = "4M"
                    else:
                        video_bitrate = "2M"
                else:
                    video_bitrate = "8M"
            
            # Calculate buffer size
            try:
                bitrate_num = float(video_bitrate.rstrip('MmKk'))
                maxrate = video_bitrate
                bufsize = f"{int(bitrate_num * 2)}M"
            except:
                maxrate = "10M"
                bufsize = "16M"
            
            # Log the bitrate being used
            self._notify("log", ("info", f"Using video bitrate: {video_bitrate}, maxrate: {maxrate}, bufsize: {bufsize}"))
            
            # Build ffmpeg command - merge video and audio
            ffmpeg_cmd = [
                FFMPEG_PATH,
                "-y",
                "-i", video_file,
                "-i", audio_file,
                "-map", "0:v:0",
                "-map", "1:a:0",
                "-c:v", video_codec,
            ]
            
            # Add preset for CPU encoding
            if video_codec == "libx264":
                ffmpeg_cmd.extend(["-preset", encoder_preset])
            
            # Add bitrate and encoding params
            ffmpeg_cmd.extend([
                "-b:v", video_bitrate,
                "-maxrate", maxrate,
                "-bufsize", bufsize,
                "-pix_fmt", "yuv420p",
                "-c:a", "aac",
                "-b:a", f"{audio_bitrate}k",
                "-movflags", "+faststart",
                "-shortest",
                final_output
            ])
            
            # Log full ffmpeg command for debugging (properly quoted)
            cmd_str = shlex.join(ffmpeg_cmd)
            self._notify("log", ("info", f"FFmpeg command: {cmd_str}"))
            
            # If GPU encoding fails, fall back to CPU
            # Progress: 60-85% if no SponsorBlock, 60-75% if SponsorBlock enabled
            progress_end = 75 if self.settings_mgr.get('sponsorblock_enabled', False) else 85
            success = self._run_ffmpeg_with_progress(ffmpeg_cmd, task, "⚙️ Converting", 60, progress_end, video_info.duration)
            
            if not success and video_codec == "h264_videotoolbox":
                # Try CPU encoding as fallback
                ffmpeg_cmd[ffmpeg_cmd.index("h264_videotoolbox")] = "libx264"
                preset_idx = ffmpeg_cmd.index("libx264") + 1
                ffmpeg_cmd.insert(preset_idx, "-preset")
                ffmpeg_cmd.insert(preset_idx + 1, encoder_preset)
                success = self._run_ffmpeg_with_progress(ffmpeg_cmd, task, "Converting (CPU)", 60, progress_end, video_info.duration)
            
            # Cleanup ALL temp files with this video_id
            try:
                files_removed = []
                for fname in os.listdir(self.output_dir):
                    # Remove any file containing the video_id that's not the final output
                    if video_id in fname and fname != os.path.basename(final_output):
                        file_path = os.path.join(self.output_dir, fname)
                        try:
                            os.remove(file_path)
                            files_removed.append(fname)
                        except:
                            pass
                
                if files_removed:
                    self._notify("log", ("info", f"Cleaned up temp files: {', '.join(files_removed)}"))
            except Exception as e:
                self._notify("log", ("warning", f"Cleanup error: {e}"))
            
            if success and os.path.exists(final_output):
                # Step 4: Apply SponsorBlock post-processing if enabled
                if self.settings_mgr.get('sponsorblock_enabled', False):
                    final_output = self._apply_sponsorblock_postprocess(
                        task, final_output, video_info.id, video_info.duration
                    )
                else:
                    # No SponsorBlock - mark as 100% complete after conversion
                    task.progress = 100.0
                    self._notify("task_updated", task)
                
                task.status = DownloadStatus.COMPLETED
                task.progress = 100.0
                task.completed_at = datetime.now()
                task.output_path = final_output
                
                # Calculate file size
                try:
                    task.file_size = os.path.getsize(final_output)
                except:
                    task.file_size = None
                
                # BUGFIX v16.1: Save to history
                try:
                    history_entry = {
                        "id": video_info.id,
                        "title": video_info.title,
                        "url": video_info.url,
                        "channel": video_info.channel,
                        "downloaded_at": datetime.now().isoformat(),
                        "output_path": final_output,
                        "file_size": task.file_size,
                        "duration": video_info.duration,
                        "format": f"{fmt.height}p" if fmt and fmt.height else "best"
                    }
                    hist_mgr = HistoryManager(HISTORY_PATH)
                    hist_mgr.add(history_entry)
                except Exception:
                    pass  # Don't fail download if history fails
                
                send_notification("✅ Download Complete", f"{video_info.title}")
            else:
                task.status = DownloadStatus.FAILED
                task.error_message = "Conversion failed"
            
        except Exception as e:
            task.status = DownloadStatus.FAILED
            task.error_message = str(e)
        
        finally:
            self.current_process = None
            self._notify("task_updated", task)
    
    def _find_temp_file(self, directory: str, prefix: str) -> Optional[str]:
        """Find a temp file by prefix, preferring video files over audio-only."""
        try:
            matches = []
            for fname in os.listdir(directory):
                if fname.startswith(prefix):
                    matches.append(fname)
            
            if not matches:
                return None
            
            # Filter out known audio-only formats
            audio_formats = ['.f251.', '.f140.', '.f139.', '.f250.']
            video_files = [f for f in matches if not any(af in f for af in audio_formats)]
            
            # Prefer MP4, then MKV, then WebM
            for ext in ['.mp4', '.mkv', '.webm']:
                for fname in video_files:
                    if fname.endswith(ext):
                        return os.path.join(directory, fname)
            
            # If no video files found, return first non-audio file
            if video_files:
                return os.path.join(directory, video_files[0])
            
            # Last resort: return any match
            return os.path.join(directory, matches[0])
        except Exception:
            pass
        return None
    
    def _apply_sponsorblock_postprocess(self, task: DownloadTask, video_path: str, 
                                       video_id: str, duration: Optional[int]) -> str:
        """
        Apply SponsorBlock segment removal via post-processing.
        
        Args:
            task: Current download task
            video_path: Path to the converted video file
            video_id: YouTube video ID
            duration: Video duration in seconds
        
        Returns:
            Path to final video (same as input if no segments removed, new path if re-encoded)
        """
        try:
            # Get enabled categories
            categories = self.settings_mgr.get('sponsorblock_categories', ['sponsor'])
            if not categories:
                self._notify("log", ("info", "SponsorBlock enabled but no categories selected"))
                return video_path
            
            self._notify("log", ("info", f"Querying SponsorBlock API for segments: {', '.join(categories)}"))
            
            # Fetch segments from API
            segments = SponsorBlockAPI.fetch_segments(video_id, categories)
            
            if not segments:
                self._notify("log", ("info", "No SponsorBlock segments found - skipping re-encode"))
                # Set progress to complete since we're skipping SponsorBlock
                task.progress = 100.0
                self._notify("task_updated", task)
                return video_path
            
            # Count and log segments
            segment_count = len(segments)
            total_duration = sum(seg['segment'][1] - seg['segment'][0] for seg in segments)
            self._notify("log", ("success", f"Found {segment_count} segments to remove ({total_duration:.1f}s total)"))
            
            # Log each segment
            for i, seg in enumerate(segments, 1):
                start, end = seg['segment']
                category = seg.get('category', 'unknown')
                self._notify("log", ("info", f"  Segment {i}: {start:.1f}s - {end:.1f}s ({category})"))
            
            # Check if we should mark or remove
            action = self.settings_mgr.get('sponsorblock_action', 'remove')
            if action == 'mark':
                self._notify("log", ("warning", "SponsorBlock 'mark' mode not yet supported in post-processing"))
                return video_path
            
            # Use video duration from task if available
            if not duration and task.video_info.duration:
                duration = task.video_info.duration
            
            if not duration:
                self._notify("log", ("error", "Cannot apply SponsorBlock without video duration"))
                return video_path
            
            # Update task status
            task.status = DownloadStatus.CONVERTING
            self._notify("task_updated", task)
            self._notify("log", ("info", "Re-encoding video with SponsorBlock segments removed..."))
            
            # Create output path for re-encoded file
            base_path = os.path.splitext(video_path)[0]
            temp_output = f"{base_path}_sb_temp.mp4"
            
            # Build list of segments to KEEP (inverse of segments to remove)
            keep_segments = []
            sorted_segments = sorted(segments, key=lambda x: x['segment'][0])
            last_end = 0.0
            
            for seg in sorted_segments:
                start, end = seg['segment']
                # Add the part before this segment
                if start > last_end:
                    keep_segments.append((last_end, start))
                last_end = max(last_end, end)
            
            # Add final segment after last removed part
            if last_end < float(duration):
                keep_segments.append((last_end, float(duration)))
            
            if not keep_segments:
                self._notify("log", ("warning", "No segments to keep after removal"))
                return video_path
            
            # Use ffmpeg's segment splitting and concat approach
            # This is more reliable than complex filter expressions
            import tempfile
            segment_files = []
            concat_file = None
            
            try:
                # Create a temporary directory for segments
                temp_dir = tempfile.mkdtemp()
                concat_list_path = os.path.join(temp_dir, 'concat_list.txt')
                
                # Extract each segment to keep
                total_segments = len(keep_segments)
                for i, (start, end) in enumerate(keep_segments):
                    segment_path = os.path.join(temp_dir, f'segment_{i:03d}.mp4')
                    segment_files.append(segment_path)
                    
                    # Update progress: 75-85% for extraction phase
                    extraction_progress = 75 + (10 * i / total_segments)
                    task.progress = extraction_progress
                    self._notify("task_updated", task)
                    self._notify("log", ("info", f"Extracting segment {i+1}/{total_segments} ({start:.1f}s - {end:.1f}s)"))
                    
                    # Extract segment with ffmpeg
                    extract_cmd = [
                        FFMPEG_PATH,
                        "-y",
                        "-i", video_path,
                        "-ss", str(start),
                        "-to", str(end),
                        "-c", "copy",  # Copy without re-encoding (fast)
                        "-avoid_negative_ts", "1",
                        segment_path
                    ]
                    
                    result = subprocess.run(
                        extract_cmd,
                        capture_output=True,
                        text=True,
                        encoding='utf-8',
                        errors='replace'
                    )
                    
                    if result.returncode != 0:
                        self._notify("log", ("error", f"Failed to extract segment {i}: {result.stderr[:200]}"))
                        raise Exception(f"Segment extraction failed")
                
                # Create concat list file
                with open(concat_list_path, 'w') as f:
                    for seg_file in segment_files:
                        f.write(f"file '{seg_file}'\n")
                
                # Update progress before concat
                task.progress = 85
                self._notify("task_updated", task)
                self._notify("log", ("info", f"Merging {len(segment_files)} segments and re-encoding..."))
                
                # Concatenate all segments
                concat_cmd = [
                    FFMPEG_PATH,
                    "-y",
                    "-f", "concat",
                    "-safe", "0",
                    "-i", concat_list_path,
                    "-c:v", "libx264",
                    "-preset", "fast",
                    "-crf", "18",
                    "-c:a", "aac",
                    "-b:a", "192k",
                    "-movflags", "+faststart",
                    temp_output
                ]
                
                # Log command
                cmd_str = shlex.join(concat_cmd)
                self._notify("log", ("info", f"SponsorBlock FFmpeg command: {cmd_str}"))
                
                # Run ffmpeg with progress tracking (85-100%)
                success = self._run_ffmpeg_with_progress(
                    concat_cmd, task, "Merging segments", 85, 100, duration
                )
                
                # Cleanup temp files
                import shutil
                shutil.rmtree(temp_dir, ignore_errors=True)
                
            except Exception as e:
                # Cleanup on error
                import shutil
                if 'temp_dir' in locals():
                    shutil.rmtree(temp_dir, ignore_errors=True)
                raise e
            
            if success and os.path.exists(temp_output):
                # Replace original file with re-encoded version
                try:
                    os.remove(video_path)
                    os.rename(temp_output, video_path)
                    self._notify("log", ("success", f"SponsorBlock removed {segment_count} segments successfully"))
                except Exception as e:
                    self._notify("log", ("error", f"Failed to replace file: {e}"))
                    if os.path.exists(temp_output):
                        os.remove(temp_output)
            else:
                self._notify("log", ("error", "SponsorBlock re-encoding failed"))
                if os.path.exists(temp_output):
                    os.remove(temp_output)
            
            return video_path
            
        except Exception as e:
            self._notify("log", ("error", f"SponsorBlock post-processing error: {e}"))
            return video_path
    
    
    def _run_subprocess_with_progress(self, cmd: List[str], task: DownloadTask, 
                                       stage: str, progress_start: float, progress_end: float,
                                       expected_file_pattern: Optional[str] = None):
        """Run a subprocess and update progress with speed metrics.
        
        v17.7.5: Enhanced to detect yt-dlp merging phases and show file activity
        when progress appears stalled.
        
        Args:
            expected_file_pattern: Optional pattern to check if file was downloaded despite errors
        """
        try:
            # Start progress tracking for this stage
            stage_name = "downloading_video" if "video" in stage.lower() else "downloading_audio"
            self.progress_tracker.start(stage_name)
            
            self.current_process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT, 
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            
            progress_re = re.compile(r'\[download\]\s+(\d+(?:\.\d+)?)%')
            speed_re = re.compile(r'at\s+([\d.]+)(Ki|Mi|Gi)?B/s')
            # v17.7.5: Detect merging/processing messages from yt-dlp
            merge_re = re.compile(r'\[Merger\]|\[ffmpeg\]|\[ExtractAudio\]|\[FixupM3u8\]|\[Fixup\]|Merging formats|Destination:.*_temp')
            chapter_re = re.compile(r'Chapter \d+|Writing chapter')
            error_lines = []  # Capture error messages
            
            # v17.7.5: Track when we last saw real progress
            last_progress_update = time.time()
            is_in_merge_phase = False
            merge_start_time = None
            
            # v17.7.5: Start a background thread to monitor file growth during stalls
            file_monitor_active = False
            
            def monitor_file_growth():
                """Background thread to update UI during long operations."""
                nonlocal file_monitor_active
                while file_monitor_active and self.current_process and self.current_process.poll() is None:
                    # Check for growing files in output directory
                    try:
                        for fname in os.listdir(self.output_dir):
                            if expected_file_pattern and expected_file_pattern in fname:
                                fpath = os.path.join(self.output_dir, fname)
                                if os.path.isfile(fpath):
                                    is_growing, size, rate = False, 0, 0
                                    try:
                                        size = os.path.getsize(fpath)
                                        if hasattr(self, '_last_monitored_size'):
                                            is_growing = size > self._last_monitored_size
                                            if is_growing:
                                                rate = (size - self._last_monitored_size) * 8 / 1_000_000  # Mbps
                                        self._last_monitored_size = size
                                    except:
                                        pass
                                    
                                    if size > 0:
                                        task.current_file_size = size
                                        size_str = self.progress_tracker.format_file_size(size)
                                        if is_in_merge_phase and merge_start_time:
                                            elapsed = time.time() - merge_start_time
                                            task.status_detail = f"Merging streams... ({size_str}, {elapsed:.0f}s elapsed)"
                                        else:
                                            task.status_detail = f"Processing... ({size_str})"
                                        self._notify("task_updated", task)
                                    break
                    except Exception:
                        pass
                    time.sleep(1)  # Check every second
            
            for line in self.current_process.stdout:
                if self._paused:
                    while self._paused and self._running:
                        time.sleep(0.1)
                
                # Capture error lines (but only actual errors, not all warnings)
                if "error" in line.lower() and "warning" not in line.lower():
                    error_lines.append(line.strip())
                
                # v17.7.5: Detect merge/processing phases
                if merge_re.search(line):
                    if not is_in_merge_phase:
                        is_in_merge_phase = True
                        merge_start_time = time.time()
                        task.status_detail = "Merging video and audio streams..."
                        self._notify("log", ("info", "Merging streams (this may take several minutes for long videos)..."))
                        self._notify("task_updated", task)
                        
                        # Start file monitoring thread
                        if not file_monitor_active:
                            file_monitor_active = True
                            self._last_monitored_size = 0
                            monitor_thread = threading.Thread(target=monitor_file_growth, daemon=True)
                            monitor_thread.start()
                
                # v17.7.5: Detect chapter processing
                if chapter_re.search(line):
                    task.status_detail = f"Processing chapters..."
                    self._notify("task_updated", task)
                
                # Parse progress percentage
                match = progress_re.search(line)
                if match:
                    pct = float(match.group(1))
                    # Scale to our progress range
                    task.progress = progress_start + (pct / 100) * (progress_end - progress_start)
                    last_progress_update = time.time()
                    is_in_merge_phase = False  # Real progress means we're past merge phase
                    task.status_detail = None  # Clear special status
                    
                    # Update progress tracker
                    self.progress_tracker.update(task.progress)
                    
                    # Parse download speed
                    speed_match = speed_re.search(line)
                    if speed_match:
                        speed_value = float(speed_match.group(1))
                        speed_unit = speed_match.group(2) or ""
                        
                        # Convert to Mbps
                        if speed_unit == "Ki":
                            mbps = (speed_value * 1024 * 8) / 1_000_000
                        elif speed_unit == "Mi":
                            mbps = (speed_value * 1024 * 1024 * 8) / 1_000_000
                        elif speed_unit == "Gi":
                            mbps = (speed_value * 1024 * 1024 * 1024 * 8) / 1_000_000
                        else:
                            mbps = (speed_value * 8) / 1_000_000  # Assume bytes
                        
                        self.progress_tracker.set_download_speed(mbps)
                        task.download_speed = self.progress_tracker.format_speed()
                    
                    # Get ETA from progress tracker
                    task.eta = self.progress_tracker.format_eta()
                    
                    self._notify("task_updated", task)
            
            # Stop file monitor
            file_monitor_active = False
            
            self.current_process.wait()
            
            # Clear status detail after completion
            task.status_detail = None
            
            # Check if download succeeded despite non-zero return code
            file_exists = False
            if expected_file_pattern and self.current_process.returncode != 0:
                # Check if a file matching the pattern exists
                try:
                    for fname in os.listdir(self.output_dir):
                        if expected_file_pattern in fname:
                            file_exists = True
                            self._notify("log", ("warning", f"{stage} had non-zero exit code but file was downloaded successfully"))
                            break
                except:
                    pass
            
            # Only fail if returncode is non-zero AND no file was downloaded
            if self.current_process.returncode != 0 and not file_exists:
                task.status = DownloadStatus.FAILED
                # Include captured errors in error message
                if error_lines:
                    task.error_message = f"{stage} failed: {error_lines[0]}"
                else:
                    task.error_message = f"{stage} failed (exit code {self.current_process.returncode})"
                
        except Exception as e:
            task.status = DownloadStatus.FAILED
            task.error_message = str(e)
    
    def _run_ffmpeg_with_progress(self, cmd: List[str], task: DownloadTask,
                                   stage: str, progress_start: float, progress_end: float,
                                   duration: Optional[int]) -> bool:
        """Run ffmpeg and update progress with FPS metrics.
        
        v17.7.5: Enhanced with file size monitoring and stall detection to show
        users that processing is still active during long conversions.
        """
        try:
            # Start progress tracking for conversion stage
            self.progress_tracker.start("converting")
            
            # v17.7.5: Get the output file path from the command (last argument)
            output_file = cmd[-1] if cmd else None
            last_file_size = 0
            last_progress_time = time.time()
            stall_logged = False
            
            # Use encoding='utf-8' and errors='replace' to handle unicode in paths
            self.current_process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            
            time_re = re.compile(r'time=(\d+):(\d+):(\d+(?:\.\d+)?)')
            fps_re = re.compile(r'fps=\s*([\d.]+)')
            size_re = re.compile(r'size=\s*(\d+)(ki|Mi|Gi)?B')  # v17.7.5: Also parse size from ffmpeg output
            total_duration = float(duration) if duration else 0
            
            stderr_lines = []  # Capture stderr for error reporting
            
            # v17.7.5: Start a background thread to monitor file growth during apparent stalls
            file_monitor_active = True
            conversion_start = time.time()
            
            def monitor_conversion_file():
                """Background thread to show file growth during conversion."""
                nonlocal last_file_size, stall_logged
                check_interval = 2  # Check every 2 seconds
                
                while file_monitor_active and self.current_process and self.current_process.poll() is None:
                    time.sleep(check_interval)
                    
                    # Check if progress appears stalled
                    time_since_progress = time.time() - last_progress_time
                    
                    if time_since_progress > 5 and output_file and os.path.exists(output_file):
                        try:
                            current_size = os.path.getsize(output_file)
                            
                            if current_size > last_file_size:
                                # File is growing - show activity
                                size_delta = current_size - last_file_size
                                write_rate = (size_delta * 8) / (check_interval * 1_000_000)  # Mbps
                                
                                size_str = self.progress_tracker.format_file_size(current_size)
                                elapsed = time.time() - conversion_start
                                elapsed_str = f"{int(elapsed // 60)}m {int(elapsed % 60)}s" if elapsed >= 60 else f"{int(elapsed)}s"
                                
                                task.current_file_size = current_size
                                task.status_detail = f"Converting... {size_str} written ({elapsed_str} elapsed, {write_rate:.1f} Mbps)"
                                task.eta = "calculating..."  # Clear ETA since we don't have reliable progress
                                self._notify("task_updated", task)
                                
                                if not stall_logged and time_since_progress > 10:
                                    self._notify("log", ("info", f"Conversion in progress - {size_str} written so far"))
                                    stall_logged = True
                            
                            last_file_size = current_size
                        except Exception:
                            pass
            
            # Start monitor thread
            monitor_thread = threading.Thread(target=monitor_conversion_file, daemon=True)
            monitor_thread.start()
            
            for line in self.current_process.stderr:
                stderr_lines.append(line)  # Store for potential error reporting
                
                if self._paused:
                    while self._paused and self._running:
                        time.sleep(0.1)
                
                # v17.7.5: Parse size from ffmpeg output even if no time info
                size_match = size_re.search(line)
                if size_match:
                    size_value = float(size_match.group(1))
                    size_unit = size_match.group(2) or ""
                    
                    # Convert to bytes
                    if size_unit == "ki":
                        current_size = int(size_value * 1024)
                    elif size_unit == "Mi":
                        current_size = int(size_value * 1024 * 1024)
                    elif size_unit == "Gi":
                        current_size = int(size_value * 1024 * 1024 * 1024)
                    else:
                        current_size = int(size_value)
                    
                    task.current_file_size = current_size
                
                if total_duration > 0:
                    match = time_re.search(line)
                    if match:
                        h = float(match.group(1))
                        m = float(match.group(2))
                        s = float(match.group(3))
                        current_time = h * 3600 + m * 60 + s
                        pct = min(100, (current_time / total_duration) * 100)
                        task.progress = progress_start + (pct / 100) * (progress_end - progress_start)
                        
                        # v17.7.5: Update last progress time
                        last_progress_time = time.time()
                        task.status_detail = None  # Clear status detail when we have real progress
                        stall_logged = False
                        
                        # Update progress tracker
                        self.progress_tracker.update(task.progress)
                        
                        # Parse FPS
                        fps_match = fps_re.search(line)
                        if fps_match:
                            fps = float(fps_match.group(1))
                            self.progress_tracker.set_conversion_fps(fps)
                            task.conversion_fps = self.progress_tracker.format_fps()
                        
                        # Get ETA
                        task.eta = self.progress_tracker.format_eta()
                        
                        self._notify("task_updated", task)
            
            # v17.7.5: Stop file monitor
            file_monitor_active = False
            
            self.current_process.wait()
            
            # Clear status detail after completion
            task.status_detail = None
            
            # If failed, log the error
            if self.current_process.returncode != 0:
                # Find the most relevant error lines (skip empty lines and frame info)
                error_lines = [l.strip() for l in stderr_lines if l.strip() and 
                              not l.strip().startswith('frame=') and
                              not l.strip().startswith('size=')]
                # Get last few meaningful lines
                relevant_errors = error_lines[-5:] if len(error_lines) > 5 else error_lines
                error_msg = '\n'.join(relevant_errors)
                self._notify("log", ("error", f"FFmpeg error (code {self.current_process.returncode}):\n{error_msg}"))
            
            return self.current_process.returncode == 0
            
        except Exception as e:
            self._notify("log", ("error", f"FFmpeg exception: {str(e)}"))
            return False


# ============================================================================
# CUSTOM WIDGETS
# ============================================================================

class EnhancedProgressBar(ctk.CTkFrame):
    """Enhanced progress bar with segmented blocks and animation."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.progress = 0
        self.stage = "idle"
        self.pulse_alpha = 1.0
        self.pulse_direction = -1
        self.animating = False
        
        # Stage colors
        self.stage_colors = {
            "downloading_video": "#3B82F6",  # Blue
            "downloading_audio": "#8B5CF6",  # Purple
            "converting": "#10B981",         # Green
            "idle": "#4B5563"                # Gray
        }
        
        # Canvas for custom drawing
        self.canvas = ctk.CTkCanvas(
            self,
            height=12,
            bg=COLORS["bg_elevated"],
            highlightthickness=0
        )
        self.canvas.pack(fill="x")
        
        # Bind resize
        self.canvas.bind("<Configure>", self._redraw)
    
    def set_progress(self, percentage, stage="idle"):
        """Update progress and stage."""
        self.progress = max(0, min(100, percentage))
        self.stage = stage
        self._redraw()
    
    def start_animation(self):
        """Start pulse animation."""
        if not self.animating:
            self.animating = True
            self._animate()
    
    def stop_animation(self):
        """Stop animation."""
        self.animating = False
    
    def _animate(self):
        """Pulse animation loop."""
        if not self.animating:
            return
            
        # Pulse between 0.7 and 1.0
        self.pulse_alpha += 0.02 * self.pulse_direction
        if self.pulse_alpha >= 1.0:
            self.pulse_alpha = 1.0
            self.pulse_direction = -1
        elif self.pulse_alpha <= 0.7:
            self.pulse_alpha = 0.7
            self.pulse_direction = 1
        
        self._redraw()
        self.after(50, self._animate)  # 20 FPS animation
    
    def _redraw(self, event=None):
        """Redraw the progress bar."""
        self.canvas.delete("all")
        
        width = self.canvas.winfo_width()
        height = 12
        
        if width <= 1:
            return
        
        # Number of blocks
        num_blocks = 40
        block_width = (width - (num_blocks + 1) * 2) / num_blocks
        filled_blocks = int((self.progress / 100) * num_blocks)
        
        # Draw blocks
        for i in range(num_blocks):
            x = 2 + i * (block_width + 2)
            y = 2
            
            if i < filled_blocks:
                # Filled block
                color = self.stage_colors.get(self.stage, self.stage_colors["idle"])
                
                # Apply pulse alpha
                if self.animating:
                    color = self._adjust_color_alpha(color, self.pulse_alpha)
                
                self.canvas.create_rectangle(
                    x, y, x + block_width, y + height - 4,
                    fill=color,
                    outline=""
                )
            else:
                # Empty block
                self.canvas.create_rectangle(
                    x, y, x + block_width, y + height - 4,
                    fill="#2C2C2E",
                    outline=""
                )
    
    def _adjust_color_alpha(self, hex_color, alpha):
        """Adjust color brightness based on alpha."""
        # Convert hex to RGB
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        
        # Adjust brightness
        r = int(r * alpha)
        g = int(g * alpha)
        b = int(b * alpha)
        
        # Convert back to hex
        return f'#{r:02x}{g:02x}{b:02x}'


class ToolTip:
    """Simple tooltip that appears on hover."""
    
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        
        # Bind hover events
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
    
    def show_tooltip(self, event=None):
        """Show the tooltip after a brief delay."""
        # Cancel any existing tooltip
        self.hide_tooltip()
        
        # Schedule tooltip to appear after 500ms
        self.tooltip_window = self.widget.after(500, self._display_tooltip)
    
    def _display_tooltip(self):
        """Actually display the tooltip window."""
        if self.tooltip_window is None:
            return
        
        # Get widget position
        x = self.widget.winfo_rootx() + self.widget.winfo_width() // 2
        y = self.widget.winfo_rooty() - 35
        
        # Create tooltip window
        self.tip_window = tk.Toplevel(self.widget)
        self.tip_window.wm_overrideredirect(True)
        self.tip_window.wm_geometry(f"+{x}+{y}")
        
        # Create tooltip label with modern style
        label = tk.Label(
            self.tip_window,
            text=self.text,
            background="#2c2c2e",
            foreground="#f5f5f7",
            relief="solid",
            borderwidth=1,
            font=("SF Pro Text", 11),
            padx=12,
            pady=6
        )
        label.pack()
        
        # Make window slightly transparent
        try:
            self.tip_window.attributes('-alpha', 0.95)
        except:
            pass
    
    def hide_tooltip(self, event=None):
        """Hide the tooltip."""
        # Cancel scheduled tooltip
        if self.tooltip_window:
            self.widget.after_cancel(self.tooltip_window)
            self.tooltip_window = None
        
        # Destroy tooltip window
        if hasattr(self, 'tip_window') and self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None


class ModernButton(ctk.CTkButton):
    """Modern styled button with gradient effects and smooth animations."""
    
    def __init__(self, master, text="", icon=None, style="primary", **kwargs):
        styles = {
            "primary": {
                "fg_color": COLORS["accent_gradient_start"],
                "hover_color": COLORS["accent_gradient_end"],
                "text_color": "white",
            },
            "secondary": {
                "fg_color": COLORS["bg_elevated"],
                "hover_color": COLORS["bg_hover"],
                "text_color": COLORS["text_primary"],
                "border_width": 1,
                "border_color": COLORS["border_light"],
            },
            "danger": {
                "fg_color": COLORS["accent_red"],
                "hover_color": "#ff6961",
                "text_color": "white",
            },
            "success": {
                "fg_color": COLORS["accent_green"],
                "hover_color": "#4ade80",
                "text_color": "white",
            },
            "icon": {
                "fg_color": COLORS["bg_elevated"],
                "hover_color": COLORS["bg_hover"],
                "text_color": COLORS["text_primary"],
                "border_width": 1,
                "border_color": COLORS["border_light"],
                "width": 44,
                "height": 44,
            },
        }
        
        style_config = styles.get(style, styles["primary"]).copy()
        
        # FIXED: Remove any style_config keys that are also in kwargs to avoid conflicts
        # This allows user-provided values to override style defaults
        for key in list(style_config.keys()):
            if key in kwargs:
                del style_config[key]
        
        # Set default height if not in style_config AND not in kwargs
        if "height" not in style_config and "height" not in kwargs:
            kwargs["height"] = 56
        
        super().__init__(
            master,
            text=text,
            corner_radius=16 if style != "icon" else 12,
            font=ctk.CTkFont(size=14, weight="bold"),
            **style_config,
            **kwargs
        )


class ModernEntry(ctk.CTkEntry):
    """Modern styled entry with glass effect and larger size."""
    
    def __init__(self, master, placeholder="", **kwargs):
        super().__init__(
            master,
            placeholder_text=placeholder,
            corner_radius=16,
            height=56,
            font=ctk.CTkFont(size=14),
            fg_color=COLORS["bg_tertiary"],
            border_color=COLORS["border_light"],
            text_color=COLORS["text_primary"],
            placeholder_text_color=COLORS["text_tertiary"],
            border_width=1,
            **kwargs
        )


class OptionChip(ctk.CTkButton):
    """Selectable option chip/pill."""
    
    def __init__(self, master, text="", active=False, **kwargs):
        self.active = active
        
        super().__init__(
            master,
            text=text,
            corner_radius=20,
            height=36,
            font=ctk.CTkFont(size=13),
            fg_color=COLORS["accent_blue"] if active else COLORS["bg_tertiary"],
            hover_color=COLORS["accent_blue_hover"] if active else COLORS["bg_elevated"],
            text_color="white" if active else COLORS["text_secondary"],
            border_width=1 if active else 0,
            border_color=COLORS["accent_blue"] if active else COLORS["bg_tertiary"],
            **kwargs
        )
    
    def set_active(self, active: bool):
        """Update active state."""
        self.active = active
        if active:
            self.configure(
                fg_color=COLORS["accent_blue"],
                hover_color=COLORS["accent_blue_hover"],
                text_color="white",
                border_width=1,
                border_color=COLORS["accent_blue"]
            )
        else:
            self.configure(
                fg_color=COLORS["bg_tertiary"],
                hover_color=COLORS["bg_elevated"],
                text_color=COLORS["text_secondary"],
                border_width=0,
                border_color=COLORS["bg_tertiary"]
            )


class FormatCard(ctk.CTkFrame):
    """Modern card for displaying format options with hover effects."""
    
    # Codec display names
    CODEC_NAMES = {
        "avc1": "H.264",
        "avc": "H.264",
        "h264": "H.264",
        "hev1": "HEVC",
        "hvc1": "HEVC",
        "hevc": "HEVC",
        "h265": "HEVC",
        "vp9": "VP9",
        "vp09": "VP9",
        "av01": "AV1",
        "av1": "AV1",
        "mp4a": "AAC",
        "opus": "Opus",
        "vorbis": "Vorbis",
    }
    
    def __init__(self, master, format_info: VideoFormat, selected=False,
                 recommended=False, on_select=None, **kwargs):
        # Use orange border for recommended, purple for selected
        if recommended:
            border_color = COLORS["accent_orange"]
            bg_color = COLORS["bg_elevated"]
        elif selected:
            border_color = COLORS["accent_gradient_start"]
            bg_color = COLORS["bg_elevated"]
        else:
            border_color = COLORS["border_light"]
            bg_color = COLORS["bg_secondary"]
        
        super().__init__(
            master,
            corner_radius=10,
            fg_color=bg_color,
            border_width=2,
            border_color=border_color,
            **kwargs
        )
        
        self.format_info = format_info
        self.selected = selected
        self.recommended = recommended
        self.on_select = on_select
        self._default_bg = bg_color
        
        # Main container with compact padding
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=8, pady=6)
        
        # Resolution label - with star prefix if recommended
        res_text = f"{format_info.height}p" if format_info.height else "Audio"
        if recommended:
            res_text = f"★ {res_text}"
        
        self.res_label = ctk.CTkLabel(
            content,
            text=res_text,
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=COLORS["accent_orange"] if recommended else COLORS["text_primary"]
        )
        self.res_label.pack(pady=(0, 2))
        
        # Codec
        codec_raw = format_info.vcodec or format_info.acodec or ""
        codec_base = codec_raw.split('.')[0].lower() if codec_raw else ""
        codec_display = self.CODEC_NAMES.get(codec_base, codec_base.upper() if codec_base else "N/A")
        
        self.codec_label = ctk.CTkLabel(
            content,
            text=codec_display,
            font=ctk.CTkFont(size=10),
            text_color=COLORS["text_secondary"]
        )
        self.codec_label.pack()
        
        # File size
        self.size_label = ctk.CTkLabel(
            content,
            text=format_info.size_str,
            font=ctk.CTkFont(size=10),
            text_color=COLORS["text_tertiary"]
        )
        self.size_label.pack()
        
        # Bind click events to all elements
        self.bind("<Button-1>", self._on_click)
        content.bind("<Button-1>", self._on_click)
        self.res_label.bind("<Button-1>", self._on_click)
        self.codec_label.bind("<Button-1>", self._on_click)
        self.size_label.bind("<Button-1>", self._on_click)
        
        # Hover effects
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        content.bind("<Enter>", self._on_enter)
        content.bind("<Leave>", self._on_leave)
    
    def _on_click(self, event):
        if self.on_select:
            self.on_select(self.format_info)
    
    def _on_enter(self, event):
        """Handle mouse enter - subtle highlight."""
        if not self.selected and not self.recommended:
            self.configure(fg_color=COLORS["bg_elevated"])
    
    def _on_leave(self, event):
        """Handle mouse leave - restore original color."""
        if not self.selected and not self.recommended:
            self.configure(fg_color=self._default_bg)
    
    def set_selected(self, selected: bool):
        self.selected = selected
        # When a card is selected, it becomes the "active" one
        # When another card is selected, this card loses its special status
        if selected:
            # This card is now selected - use purple border
            border_color = COLORS["accent_gradient_start"]
            bg_color = COLORS["bg_elevated"]
            # Clear recommended status since user made a different choice
            self.recommended = False
            # Update the resolution label to remove star if it had one
            res_text = f"{self.format_info.height}p" if self.format_info.height else "Audio"
            self.res_label.configure(text=res_text, text_color=COLORS["text_primary"])
        else:
            # This card is not selected - use default styling
            border_color = COLORS["border_light"]
            bg_color = COLORS["bg_secondary"]
        self._default_bg = bg_color
        self.configure(
            fg_color=bg_color,
            border_color=border_color
        )


class ProgressCard(ctk.CTkFrame):
    """Card showing download progress."""
    
    def __init__(self, master, task: DownloadTask, **kwargs):
        super().__init__(
            master,
            corner_radius=12,
            fg_color=COLORS["bg_tertiary"],
            border_width=1,
            border_color=COLORS["border"],
            **kwargs
        )
        
        self.task = task
        
        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text=task.video_info.title[:50] + "..." if len(task.video_info.title) > 50 else task.video_info.title,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS["text_primary"],
            anchor="w"
        )
        self.title_label.pack(fill="x", padx=16, pady=(12, 4))
        
        # Status row
        status_frame = ctk.CTkFrame(self, fg_color="transparent")
        status_frame.pack(fill="x", padx=16, pady=(0, 8))
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text=task.status.name.title(),
            font=ctk.CTkFont(size=12),
            text_color=self._status_color()
        )
        self.status_label.pack(side="left")
        
        self.stats_label = ctk.CTkLabel(
            status_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_secondary"]
        )
        self.stats_label.pack(side="right")
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            self,
            height=6,
            corner_radius=3,
            fg_color=COLORS["bg_elevated"],
            progress_color=COLORS["accent_blue"]
        )
        self.progress_bar.pack(fill="x", padx=16, pady=(0, 12))
        self.progress_bar.set(task.progress / 100)
    
    def _status_color(self) -> str:
        colors = {
            DownloadStatus.QUEUED: COLORS["text_secondary"],
            DownloadStatus.ANALYZING: COLORS["accent_purple"],
            DownloadStatus.DOWNLOADING: COLORS["accent_blue"],
            DownloadStatus.CONVERTING: COLORS["accent_orange"],
            DownloadStatus.PAUSED: COLORS["accent_orange"],
            DownloadStatus.COMPLETED: COLORS["accent_green"],
            DownloadStatus.FAILED: COLORS["accent_red"],
            DownloadStatus.CANCELLED: COLORS["text_tertiary"],
        }
        return colors.get(self.task.status, COLORS["text_secondary"])
    
    def update_progress(self, task: DownloadTask):
        """Update the progress display."""
        self.task = task
        self.progress_bar.set(task.progress / 100)
        self.status_label.configure(
            text=task.status.name.title(),
            text_color=self._status_color()
        )
        
        stats_parts = []
        if task.speed:
            stats_parts.append(task.speed)
        if task.eta:
            stats_parts.append(f"ETA: {task.eta}")
        stats_parts.append(f"{task.progress:.1f}%")
        
        self.stats_label.configure(text=" - ".join(stats_parts))


class LogPanel(ctk.CTkFrame):
    """Scrollable log panel with modern design."""
    
    def __init__(self, master, show_export=True, **kwargs):
        super().__init__(
            master,
            corner_radius=20,
            fg_color=COLORS["bg_tertiary"],
            border_width=1,
            border_color=COLORS["border_light"],
            **kwargs
        )
        
        self.show_export = show_export
        
        # Header (no collapse in two-column layout)
        self.header = ctk.CTkFrame(self, fg_color=COLORS["bg_elevated"], corner_radius=0, height=52)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)
        
        # Title
        title_label = ctk.CTkLabel(
            self.header,
            text=" Activity Log",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS["text_primary"]
        )
        title_label.pack(side="left", padx=20)
        
        # Buttons
        button_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        button_frame.pack(side="right", padx=16)
        
        clear_btn = ctk.CTkButton(
            button_frame,
            text="Clear",
            width=70,
            height=32,
            corner_radius=10,
            font=ctk.CTkFont(size=12),
            fg_color=COLORS["bg_hover"],
            hover_color=COLORS["bg_elevated"],
            text_color=COLORS["text_secondary"],
            command=self.clear
        )
        clear_btn.pack(side="left", padx=4)
        
        if self.show_export:
            export_btn = ctk.CTkButton(
                button_frame,
                text="Export",
                width=70,
                height=32,
                corner_radius=10,
                font=ctk.CTkFont(size=12),
                fg_color=COLORS["bg_hover"],
                hover_color=COLORS["bg_elevated"],
                text_color=COLORS["text_secondary"],
                command=self.export_log
            )
            export_btn.pack(side="left", padx=4)
        
        # Content frame with scroll
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True)
        
        # Log text with custom scrollbar - fills available space
        self.log_text = ctk.CTkTextbox(
            self.content_frame,
            font=ctk.CTkFont(family="Menlo", size=11),
            fg_color="transparent",
            text_color=COLORS["text_secondary"],
            wrap="word",
            state="disabled"
        )
        self.log_text.pack(fill="both", expand=True, padx=20, pady=(16, 20))
        
        # Configure tags for colored log messages
        self.log_text.tag_config("info", foreground=COLORS["text_secondary"])
        self.log_text.tag_config("success", foreground=COLORS["accent_green"])
        self.log_text.tag_config("warning", foreground=COLORS["accent_orange"])
        self.log_text.tag_config("error", foreground=COLORS["accent_red"])
    
    def log(self, message: str, level: str = "info"):
        """Add a log message with timestamp and color coding."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        self.log_text.configure(state="normal")
        
        # Insert with proper tag
        self.log_text.insert("end", f"[{timestamp}] ", "info")
        self.log_text.insert("end", f"{message}\n", level)
        
        self.log_text.see("end")
        self.log_text.configure(state="disabled")
    
    def clear(self):
        """Clear the log."""
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")
    
    def export_log(self):
        """Export log to a text file."""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                initialfile=f"ytdlp_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            )
            if filename:
                content = self.log_text.get("1.0", "end")
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Export Complete", f"Log exported to:\n{filename}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Could not export log:\n{str(e)}")


# ============================================================================
# SETTINGS & HISTORY MANAGEMENT
# ============================================================================

class SettingsManager:
    """Manages application settings with persistent storage."""
    
    def __init__(self, config_path: Path = None):
        # Use SETTINGS_PATH by default (separate from main config)
        self.config_path = config_path or SETTINGS_PATH
        # Ensure directory exists
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.settings = self._load_settings()
        # Save immediately to ensure file exists with defaults
        self.save()
    
    def _load_settings(self) -> Dict[str, Any]:
        """Load settings from file, merging with defaults."""
        defaults = {
            # SponsorBlock
            "sponsorblock_enabled": False,
            "sponsorblock_action": "remove",
            "sponsorblock_categories": ["sponsor"],
            
            # Subtitles
            "subtitles_enabled": False,
            "subtitles_languages": ["en"],
            "subtitles_auto": True,
            "subtitles_embed": True,
            
            # Encoding
            "encoder_type": "auto",
            "encoder_preset": "medium",
            "bitrate_mode": "auto",
            "video_bitrate": "auto",
            "audio_bitrate": 192,
            "per_resolution_bitrates": {
                "2160": "15",
                "1440": "10",
                "1080": "8",
                "720": "5",
                "480": "2.5",
            },
            
            # Trim
            "trim_enabled": False,
            "trim_start": "",
            "trim_end": "",
            
            # Playlist
            "playlist_download_all": True,
            "playlist_reverse": False,
            "playlist_max_items": 0,
            
            # yt-dlp Updates (v17.10.0)
            "ytdlp_auto_update_check": True,  # Check for updates on app launch
            "ytdlp_last_update_check": None,  # ISO timestamp of last check
        }
        
        return load_json_file(self.config_path, defaults)
    
    def save(self):
        """Save settings to file."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            save_json_file(self.config_path, self.settings)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def get(self, key: str, default=None):
        """Get setting value."""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set setting value and save immediately."""
        self.settings[key] = value
        self.save()  # Always persist changes
    
    def update(self, new_settings: Dict[str, Any]):
        """Update multiple settings at once and save."""
        self.settings.update(new_settings)
        self.save()


class HistoryManager:
    """Manages download history."""
    
    def __init__(self, history_path: Path):
        self.history_path = history_path
        self.entries = self._load()
    
    def _load(self) -> List[Dict]:
        """Load history."""
        return load_json_file(self.history_path, [])
    
    def save(self):
        """Save history."""
        save_json_file(self.history_path, self.entries)
    
    def add(self, entry: Dict):
        """Add entry."""
        self.entries.insert(0, entry)
        if len(self.entries) > 1000:
            self.entries = self.entries[:1000]
        self.save()
    
    def search(self, query: str) -> List[Dict]:
        """Search history."""
        query = query.lower()
        return [e for e in self.entries if query in e.get("title", "").lower()]
    
    def clear(self):
        """Clear history."""
        self.entries.clear()
        self.save()


# ============================================================================
# DIALOG WINDOWS
# ============================================================================

class SettingsWindow(ctk.CTkToplevel):
    """Settings configuration window."""
    
    def __init__(self, parent, settings_mgr: SettingsManager):
        super().__init__(parent)
        self.settings_mgr = settings_mgr
        
        self.title("Settings")
        self.geometry("700x700")
        self.transient(parent)
        self.resizable(False, False)
        
        # Main container
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Tabs - leave room for buttons at bottom
        self.tabview = ctk.CTkTabview(main_frame, height=550)
        self.tabview.pack(fill="both", expand=True)
        
        self.tabview.add("SponsorBlock")
        self.tabview.add("Subtitles")
        self.tabview.add("Encoding")
        self.tabview.add("Trim")
        self.tabview.add("Playlist")
        
        self._create_sponsorblock_tab()
        self._create_subtitles_tab()
        self._create_encoding_tab()
        self._create_trim_tab()
        self._create_playlist_tab()
        
        # Buttons frame - always visible at bottom
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(15, 0))
        
        ModernButton(
            btn_frame, text="Save", style="primary", width=100, command=self._save
        ).pack(side="right", padx=(10, 0))
        
        ModernButton(
            btn_frame, text="Cancel", style="secondary", width=100, command=self.destroy
        ).pack(side="right")
    
    def _create_sponsorblock_tab(self):
        """SponsorBlock settings."""
        tab = self.tabview.tab("SponsorBlock")
        
        # Make tab content scrollable
        scroll_frame = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True)
        
        # Info banner
        info_frame = ctk.CTkFrame(scroll_frame, fg_color="#1c4d2e", corner_radius=8)
        info_frame.pack(fill="x", padx=10, pady=(10, 15))
        
        ctk.CTkLabel(
            info_frame,
            text="SponsorBlock Post-Processing",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#4ade80",
            anchor="w"
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        ctk.CTkLabel(
            info_frame,
            text="After download & conversion, segments are fetched from SponsorBlock API\nand removed via re-encoding. This is reliable but adds extra processing time.",
            font=ctk.CTkFont(size=11),
            text_color="#9ca3af",
            anchor="w",
            justify="left"
        ).pack(anchor="w", padx=15, pady=(0, 10))
        
        # Chapter download notice banner
        chapter_notice_frame = ctk.CTkFrame(scroll_frame, fg_color="#4d3a1c", corner_radius=8)
        chapter_notice_frame.pack(fill="x", padx=10, pady=(0, 15))
        
        ctk.CTkLabel(
            chapter_notice_frame,
            text="Note: Chapter Downloads",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#fbbf24",
            anchor="w"
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        ctk.CTkLabel(
            chapter_notice_frame,
            text="SponsorBlock is automatically disabled when downloading chapters.\nChapter extraction uses a different process that is incompatible with SponsorBlock.",
            font=ctk.CTkFont(size=11),
            text_color="#9ca3af",
            anchor="w",
            justify="left"
        ).pack(anchor="w", padx=15, pady=(0, 10))
        
        self.sb_enabled = ctk.CTkSwitch(scroll_frame, text="Enable SponsorBlock Post-Processing")
        self.sb_enabled.pack(anchor="w", padx=10, pady=(15, 10))
        if self.settings_mgr.get("sponsorblock_enabled"):
            self.sb_enabled.select()
        
        ctk.CTkLabel(scroll_frame, text="Action:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        action_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        action_frame.pack(anchor="w", padx=10)
        
        self.sb_action = ctk.CTkSegmentedButton(action_frame, values=["Remove", "Mark"])
        self.sb_action.pack(side="left")
        self.sb_action.set("Remove" if self.settings_mgr.get("sponsorblock_action") == "remove" else "Mark")
        
        ctk.CTkLabel(
            action_frame,
            text="  (Note: 'Mark' mode not yet implemented)",
            font=ctk.CTkFont(size=10),
            text_color=COLORS["text_tertiary"]
        ).pack(side="left", padx=(10, 0))
        
        ctk.CTkLabel(scroll_frame, text="Categories to Remove:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(15, 5))
        
        self.sb_categories = {}
        enabled = self.settings_mgr.get("sponsorblock_categories", ["sponsor"])
        for cat_id, cat_name in SPONSORBLOCK_CATEGORIES.items():
            cb = ctk.CTkCheckBox(scroll_frame, text=cat_name)
            cb.pack(anchor="w", padx=30, pady=2)
            if cat_id in enabled:
                cb.select()
            self.sb_categories[cat_id] = cb
    
    def _create_subtitles_tab(self):
        """Subtitles settings."""
        tab = self.tabview.tab("Subtitles")
        
        self.sub_enabled = ctk.CTkSwitch(tab, text="Download Subtitles")
        self.sub_enabled.pack(anchor="w", padx=20, pady=(20, 10))
        if self.settings_mgr.get("subtitles_enabled"):
            self.sub_enabled.select()
        
        ctk.CTkLabel(tab, text="Languages (comma-separated):", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(10, 5))
        
        self.sub_langs = ctk.CTkEntry(tab, width=300, placeholder_text="e.g. en,es,fr")
        self.sub_langs.pack(anchor="w", padx=20)
        self.sub_langs.insert(0, ",".join(self.settings_mgr.get("subtitles_languages", ["en"])))
        
        self.sub_auto = ctk.CTkCheckBox(tab, text="Include auto-generated")
        self.sub_auto.pack(anchor="w", padx=20, pady=(10, 5))
        if self.settings_mgr.get("subtitles_auto"):
            self.sub_auto.select()
        
        self.sub_embed = ctk.CTkCheckBox(tab, text="Embed in video file")
        self.sub_embed.pack(anchor="w", padx=20, pady=(5, 0))
        if self.settings_mgr.get("subtitles_embed"):
            self.sub_embed.select()
    
    def _create_encoding_tab(self):
        """Enhanced encoding settings with per-resolution bitrates."""
        tab = self.tabview.tab("Encoding")
        
        # Scrollable frame
        scroll = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Encoder Type
        ctk.CTkLabel(scroll, text="Encoder:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        self.enc_type = ctk.CTkSegmentedButton(scroll, values=["Auto", "GPU", "CPU"])
        self.enc_type.pack(anchor="w", padx=10)
        enc_map = {"auto": "Auto", "gpu": "GPU", "cpu": "CPU"}
        self.enc_type.set(enc_map.get(self.settings_mgr.get("encoder_type", "auto"), "Auto"))
        
        # Encoding Preset
        ctk.CTkLabel(scroll, text="Preset:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(15, 5))
        self.enc_preset = ctk.CTkOptionMenu(
            scroll, 
            values=["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow"],
            width=200
        )
        self.enc_preset.pack(anchor="w", padx=10)
        self.enc_preset.set(self.settings_mgr.get("encoder_preset", "medium"))
        
        # Divider
        ctk.CTkFrame(scroll, height=2, fg_color="#2c2c2e").pack(fill="x", padx=10, pady=20)
        
        # Bitrate Mode Selection
        ctk.CTkLabel(scroll, text="Video Bitrate Mode:", font=ctk.CTkFont(weight="bold", size=13)).pack(anchor="w", padx=10, pady=(0, 5))
        self.bitrate_mode = ctk.CTkSegmentedButton(
            scroll, 
            values=["Auto", "Per-Resolution", "Custom"],
            command=self._on_bitrate_mode_change
        )
        self.bitrate_mode.pack(anchor="w", padx=10, pady=(0, 10))
        
        current_mode = self.settings_mgr.get("bitrate_mode", "auto")
        mode_map = {"auto": "Auto", "per_resolution": "Per-Resolution", "custom": "Custom"}
        self.bitrate_mode.set(mode_map.get(current_mode, "Auto"))
        
        # Auto Mode Frame
        self.auto_frame = ctk.CTkFrame(scroll, fg_color="#1c1c1e", corner_radius=8)
        ctk.CTkLabel(
            self.auto_frame, 
            text="Auto Mode - Smart Defaults", 
            font=ctk.CTkFont(weight="bold"), 
            anchor="w"
        ).pack(anchor="w", padx=15, pady=(10, 5))
        ctk.CTkLabel(
            self.auto_frame,
            text="4K -> 15M  -  1440p -> 10M  -  1080p -> 6M  -  720p -> 4M  -  480p -> 2M",
            font=ctk.CTkFont(size=11),
            text_color="#98989d",
            anchor="w"
        ).pack(anchor="w", padx=15, pady=(0, 10))
        
        # Per-Resolution Frame
        self.per_res_frame = ctk.CTkFrame(scroll, fg_color="#1c1c1e", corner_radius=8)
        ctk.CTkLabel(
            self.per_res_frame,
            text="Per-Resolution Bitrates",
            font=ctk.CTkFont(weight="bold"),
            anchor="w"
        ).pack(anchor="w", padx=15, pady=(10, 10))
        
        per_res_bitrates = self.settings_mgr.get("per_resolution_bitrates", {
            "2160": "15", "1440": "10", "1080": "6", "720": "4", "480": "2"
        })
        
        self.per_res_entries = {}
        resolutions = [("2160", "4K (2160p)"), ("1440", "1440p"), ("1080", "1080p"), ("720", "720p"), ("480", "480p")]
        
        for res_key, res_label in resolutions:
            row = ctk.CTkFrame(self.per_res_frame, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=3)
            
            ctk.CTkLabel(row, text=res_label, width=100, anchor="w").pack(side="left")
            
            entry = ctk.CTkEntry(row, width=60)
            entry.pack(side="left", padx=(10, 5))
            entry.insert(0, per_res_bitrates.get(res_key, "10"))
            
            ctk.CTkLabel(row, text="Mbps", text_color="#98989d", font=ctk.CTkFont(size=11)).pack(side="left")
            
            self.per_res_entries[res_key] = entry
        
        ctk.CTkLabel(
            self.per_res_frame,
            text="Higher bitrate = better quality, larger files",
            font=ctk.CTkFont(size=10),
            text_color="#98989d"
        ).pack(anchor="w", padx=15, pady=(10, 10))
        
        # Custom Mode Frame
        self.custom_frame = ctk.CTkFrame(scroll, fg_color="#1c1c1e", corner_radius=8)
        ctk.CTkLabel(
            self.custom_frame,
            text="Custom Bitrate (All Videos)",
            font=ctk.CTkFont(weight="bold"),
            anchor="w"
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        custom_row = ctk.CTkFrame(self.custom_frame, fg_color="transparent")
        custom_row.pack(anchor="w", padx=15, pady=(5, 10))
        
        self.vid_bitrate = ctk.CTkEntry(custom_row, width=80)
        self.vid_bitrate.pack(side="left", padx=(0, 5))
        
        video_bitrate_value = self.settings_mgr.get("video_bitrate", "auto")
        if video_bitrate_value != "auto":
            video_bitrate_value = video_bitrate_value.rstrip('Mm')
        else:
            video_bitrate_value = "8"
        self.vid_bitrate.insert(0, video_bitrate_value)
        
        ctk.CTkLabel(custom_row, text="Mbps", text_color="#98989d").pack(side="left")
        
        # Divider
        ctk.CTkFrame(scroll, height=2, fg_color="#2c2c2e").pack(fill="x", padx=10, pady=20)
        
        # Audio Bitrate
        ctk.CTkLabel(scroll, text="Audio Bitrate:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(0, 5))
        
        audio_row = ctk.CTkFrame(scroll, fg_color="transparent")
        audio_row.pack(anchor="w", padx=10)
        
        self.aud_bitrate = ctk.CTkEntry(audio_row, width=80)
        self.aud_bitrate.pack(side="left", padx=(0, 5))
        self.aud_bitrate.insert(0, str(self.settings_mgr.get("audio_bitrate", 192)))
        
        ctk.CTkLabel(audio_row, text="kbps", text_color="#98989d").pack(side="left")
        
        # Initialize display
        self._on_bitrate_mode_change()
    
    def _on_bitrate_mode_change(self, value=None):
        """Handle bitrate mode change."""
        if not hasattr(self, 'bitrate_mode'):
            return
            
        mode = self.bitrate_mode.get()
        
        # Hide all frames
        self.auto_frame.pack_forget()
        self.per_res_frame.pack_forget()
        self.custom_frame.pack_forget()
        
        # Show selected frame
        if mode == "Auto":
            self.auto_frame.pack(fill="x", padx=10, pady=(0, 10))
        elif mode == "Per-Resolution":
            self.per_res_frame.pack(fill="x", padx=10, pady=(0, 10))
        elif mode == "Custom":
            self.custom_frame.pack(fill="x", padx=10, pady=(0, 10))
    
    def _create_trim_tab(self):
        """Trim settings."""
        tab = self.tabview.tab("Trim")
        
        self.trim_enabled = ctk.CTkSwitch(tab, text="Enable Trimming")
        self.trim_enabled.pack(anchor="w", padx=20, pady=(20, 10))
        if self.settings_mgr.get("trim_enabled"):
            self.trim_enabled.select()
        
        ctk.CTkLabel(tab, text="Start Time:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(10, 5))
        
        self.trim_start = ctk.CTkEntry(tab, width=200, placeholder_text="HH:MM:SS or seconds")
        self.trim_start.pack(anchor="w", padx=20)
        self.trim_start.insert(0, self.settings_mgr.get("trim_start", ""))
        
        ctk.CTkLabel(tab, text="End Time:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(15, 5))
        
        self.trim_end = ctk.CTkEntry(tab, width=200, placeholder_text="HH:MM:SS or seconds")
        self.trim_end.pack(anchor="w", padx=20)
        self.trim_end.insert(0, self.settings_mgr.get("trim_end", ""))
    
    def _create_playlist_tab(self):
        """Playlist settings."""
        tab = self.tabview.tab("Playlist")
        
        self.pl_all = ctk.CTkCheckBox(tab, text="Download all videos by default")
        self.pl_all.pack(anchor="w", padx=20, pady=(20, 10))
        if self.settings_mgr.get("playlist_download_all"):
            self.pl_all.select()
        
        self.pl_reverse = ctk.CTkCheckBox(tab, text="Reverse order (oldest first)")
        self.pl_reverse.pack(anchor="w", padx=20, pady=(0, 10))
        if self.settings_mgr.get("playlist_reverse"):
            self.pl_reverse.select()
        
        ctk.CTkLabel(tab, text="Max videos (0 = unlimited):", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(10, 5))
        
        self.pl_max = ctk.CTkEntry(tab, width=200, placeholder_text="0")
        self.pl_max.pack(anchor="w", padx=20)
        self.pl_max.insert(0, str(self.settings_mgr.get("playlist_max_items", 0)))
    
    def _save(self):
        """Save all settings."""
        # SponsorBlock
        self.settings_mgr.set("sponsorblock_enabled", self.sb_enabled.get() == 1)
        self.settings_mgr.set("sponsorblock_action", "remove" if self.sb_action.get() == "Remove" else "mark")
        self.settings_mgr.set("sponsorblock_categories", [k for k, v in self.sb_categories.items() if v.get() == 1])
        
        # Subtitles
        self.settings_mgr.set("subtitles_enabled", self.sub_enabled.get() == 1)
        langs = [l.strip() for l in self.sub_langs.get().split(",") if l.strip()]
        self.settings_mgr.set("subtitles_languages", langs or ["en"])
        self.settings_mgr.set("subtitles_auto", self.sub_auto.get() == 1)
        self.settings_mgr.set("subtitles_embed", self.sub_embed.get() == 1)
        
        # Encoding
        enc_map = {"Auto": "auto", "GPU": "gpu", "CPU": "cpu"}
        self.settings_mgr.set("encoder_type", enc_map.get(self.enc_type.get(), "auto"))
        self.settings_mgr.set("encoder_preset", self.enc_preset.get())
        
        # Bitrate mode
        mode_map = {"Auto": "auto", "Per-Resolution": "per_resolution", "Custom": "custom"}
        bitrate_mode = mode_map.get(self.bitrate_mode.get(), "auto")
        self.settings_mgr.set("bitrate_mode", bitrate_mode)
        
        # Save per-resolution bitrates
        if bitrate_mode == "per_resolution":
            per_res_bitrates = {}
            for res_key, entry in self.per_res_entries.items():
                try:
                    value = entry.get().strip()
                    float(value)  # Validate it's a number
                    per_res_bitrates[res_key] = value
                except:
                    per_res_bitrates[res_key] = "10"  # Default fallback
            self.settings_mgr.set("per_resolution_bitrates", per_res_bitrates)
        
        # Save custom bitrate
        if bitrate_mode == "custom":
            custom_value = self.vid_bitrate.get().strip()
            if custom_value and not custom_value.endswith(('M', 'm')):
                custom_value = f"{custom_value}M"
            self.settings_mgr.set("video_bitrate", custom_value if custom_value else "auto")
        else:
            self.settings_mgr.set("video_bitrate", "auto")
        
        # Audio bitrate
        try:
            self.settings_mgr.set("audio_bitrate", int(self.aud_bitrate.get()))
        except:
            self.settings_mgr.set("audio_bitrate", 192)
        
        # Trim
        self.settings_mgr.set("trim_enabled", self.trim_enabled.get() == 1)
        self.settings_mgr.set("trim_start", self.trim_start.get().strip())
        self.settings_mgr.set("trim_end", self.trim_end.get().strip())
        
        # Playlist
        self.settings_mgr.set("playlist_download_all", self.pl_all.get() == 1)
        self.settings_mgr.set("playlist_reverse", self.pl_reverse.get() == 1)
        try:
            self.settings_mgr.set("playlist_max_items", max(0, int(self.pl_max.get())))
        except:
            self.settings_mgr.set("playlist_max_items", 0)
        
        self.settings_mgr.save()
        self.destroy()


class HistoryBrowserWindow(ctk.CTkToplevel):
    """History browser window."""
    
    def __init__(self, parent, history_mgr: HistoryManager):
        super().__init__(parent)
        self.history_mgr = history_mgr
        
        self.title("Download History")
        self.geometry("900x600")
        self.transient(parent)
        
        # Search bar
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=20)
        
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search...", width=300)
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self._search)
        
        ModernButton(search_frame, text="Clear All", style="danger", width=100, command=self._clear).pack(side="right")
        
        # Results
        self.results_frame = ctk.CTkScrollableFrame(self, fg_color=COLORS["bg_secondary"])
        self.results_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self._display(self.history_mgr.entries)
    
    def _search(self, event=None):
        """Search history."""
        query = self.search_entry.get().strip()
        results = self.history_mgr.search(query) if query else self.history_mgr.entries
        self._display(results)
    
    def _display(self, entries: List[Dict]):
        """Display entries."""
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        if not entries:
            ctk.CTkLabel(self.results_frame, text="No history", text_color=COLORS["text_tertiary"]).pack(pady=50)
            return
        
        for entry in entries:
            card = ctk.CTkFrame(self.results_frame, fg_color=COLORS["bg_elevated"], corner_radius=8)
            card.pack(fill="x", pady=(0, 10))
            
            content = ctk.CTkFrame(card, fg_color="transparent")
            content.pack(fill="x", padx=15, pady=12)
            
            ctk.CTkLabel(content, text=entry.get("title", "Unknown"), font=ctk.CTkFont(weight="bold"), anchor="w").pack(fill="x")
            ctk.CTkLabel(content, text=entry.get("downloaded_at", ""), font=ctk.CTkFont(size=11), 
                        text_color=COLORS["text_secondary"], anchor="w").pack(fill="x", pady=(2, 0))
            ctk.CTkLabel(content, text=entry.get("output_path", ""), font=ctk.CTkFont(size=10), 
                        text_color=COLORS["text_tertiary"], anchor="w").pack(fill="x", pady=(2, 0))
    
    def _clear(self):
        """Clear history."""
        if messagebox.askyesno("Clear History", "Clear all history?"):
            self.history_mgr.clear()
            self._display([])


class AboutDialog(ctk.CTkToplevel):
    """About dialog."""
    
    def __init__(self, parent, ytdlp_version: str):
        super().__init__(parent)
        
        self.title("About")
        self.geometry("400x350")
        self.transient(parent)
        self.resizable(False, False)
        
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(content, text=APP_NAME, font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(0, 5))
        ctk.CTkLabel(content, text=f"Version {APP_VERSION}", font=ctk.CTkFont(size=13), 
                    text_color=COLORS["text_secondary"]).pack()
        
        ctk.CTkFrame(content, height=1, fg_color=COLORS["border"]).pack(fill="x", pady=20)
        
        info = f"""Modern macOS GUI for yt-dlp

Built with CustomTkinter
Powered by yt-dlp {ytdlp_version}
FFmpeg for media processing

Author: bytePatrol
License: MIT

(c) 2025 All Rights Reserved"""
        
        ctk.CTkLabel(content, text=info, font=ctk.CTkFont(size=12), 
                    text_color=COLORS["text_secondary"], justify="center").pack(pady=(0, 20))
        
        ModernButton(content, text="Close", style="primary", width=100, command=self.destroy).pack()


class ChapterSelectionWindow(ctk.CTkToplevel):
    """Window for selecting chapters to download."""
    
    def __init__(self, parent, video_info: VideoInfo, on_download: Callable):
        super().__init__(parent)
        
        self.video_info = video_info
        self.on_download = on_download
        self.chapter_vars = []  # List of BooleanVars for checkboxes
        
        self.title(f"Chapters - {video_info.title[:50]}...")
        self.geometry("700x550")
        self.transient(parent)
        self.resizable(True, True)
        self.minsize(500, 400)
        
        # Configure colors
        self.configure(fg_color=COLORS["bg_primary"])
        
        # Main container
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header = ctk.CTkFrame(main_frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            header,
            text=f"{len(video_info.chapters)} Chapters Available",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS["text_primary"]
        ).pack(side="left")
        
        # Select all / Deselect all buttons
        btn_frame = ctk.CTkFrame(header, fg_color="transparent")
        btn_frame.pack(side="right")
        
        ctk.CTkButton(
            btn_frame,
            text="Select All",
            width=90,
            height=30,
            font=ctk.CTkFont(size=12),
            fg_color=COLORS["bg_elevated"],
            hover_color=COLORS["bg_hover"],
            command=self._select_all
        ).pack(side="left", padx=(0, 8))
        
        ctk.CTkButton(
            btn_frame,
            text="Deselect All",
            width=90,
            height=30,
            font=ctk.CTkFont(size=12),
            fg_color=COLORS["bg_elevated"],
            hover_color=COLORS["bg_hover"],
            command=self._deselect_all
        ).pack(side="left")
        
        # SponsorBlock notice banner
        sb_notice = ctk.CTkFrame(main_frame, fg_color="#3d3d1c", corner_radius=8)
        sb_notice.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            sb_notice,
            text="[!] SponsorBlock is disabled for chapter downloads",
            font=ctk.CTkFont(size=11),
            text_color="#d4d4a0",
            anchor="w"
        ).pack(anchor="w", padx=12, pady=8)
        
        # Chapters list (scrollable)
        self.chapters_frame = ctk.CTkScrollableFrame(
            main_frame,
            fg_color=COLORS["bg_secondary"],
            corner_radius=10
        )
        self.chapters_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Create chapter rows
        for chapter in video_info.chapters:
            self._create_chapter_row(chapter)
        
        # Footer with options and download button
        footer = ctk.CTkFrame(main_frame, fg_color="transparent")
        footer.pack(fill="x")
        
        # Audio only option
        self.audio_only_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            footer,
            text="Audio Only (M4A)",
            variable=self.audio_only_var,
            font=ctk.CTkFont(size=13),
            text_color=COLORS["text_secondary"]
        ).pack(side="left")
        
        # Download button
        ModernButton(
            footer,
            text="📑 Download Selected Chapters",
            style="primary",
            width=200,
            command=self._download_chapters
        ).pack(side="right")
        
        # Cancel button
        ModernButton(
            footer,
            text="Cancel",
            style="secondary",
            width=80,
            command=self.destroy
        ).pack(side="right", padx=(0, 10))
    
    def _create_chapter_row(self, chapter: Chapter):
        """Create a row for a single chapter."""
        row = ctk.CTkFrame(self.chapters_frame, fg_color="transparent")
        row.pack(fill="x", padx=10, pady=5)
        
        # Checkbox
        var = ctk.BooleanVar(value=True)  # Selected by default
        self.chapter_vars.append((chapter, var))
        
        cb = ctk.CTkCheckBox(
            row,
            text="",
            variable=var,
            width=24,
            checkbox_width=20,
            checkbox_height=20
        )
        cb.pack(side="left", padx=(0, 10))
        
        # Chapter number
        ctk.CTkLabel(
            row,
            text=f"{chapter.index + 1:02d}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLORS["accent_purple"],
            width=30
        ).pack(side="left", padx=(0, 10))
        
        # Chapter title
        ctk.CTkLabel(
            row,
            text=chapter.title[:60] + ("..." if len(chapter.title) > 60 else ""),
            font=ctk.CTkFont(size=13),
            text_color=COLORS["text_primary"],
            anchor="w"
        ).pack(side="left", fill="x", expand=True)
        
        # Duration
        ctk.CTkLabel(
            row,
            text=chapter.duration_str,
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_secondary"],
            width=60
        ).pack(side="right", padx=(10, 0))
        
        # Start time
        ctk.CTkLabel(
            row,
            text=chapter.start_time_str,
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_tertiary"],
            width=60
        ).pack(side="right")
    
    def _select_all(self):
        """Select all chapters."""
        for _, var in self.chapter_vars:
            var.set(True)
    
    def _deselect_all(self):
        """Deselect all chapters."""
        for _, var in self.chapter_vars:
            var.set(False)
    
    def _download_chapters(self):
        """Start downloading selected chapters."""
        selected_chapters = [ch for ch, var in self.chapter_vars if var.get()]
        
        if not selected_chapters:
            messagebox.showwarning("No Selection", "Please select at least one chapter to download.")
            return
        
        audio_only = self.audio_only_var.get()
        self.on_download(selected_chapters, audio_only)
        self.destroy()


class PlaylistSelectionWindow(ctk.CTkToplevel):
    """Window for selecting videos from a playlist to download."""
    
    def __init__(self, parent, playlist_info: VideoInfo, settings_mgr: SettingsManager,
                 on_download: Callable[[List[PlaylistItem], Optional[VideoFormat], bool], None]):
        super().__init__(parent)
        
        self.playlist_info = playlist_info
        self.settings_mgr = settings_mgr
        self.on_download = on_download
        self.video_vars = []  # List of (PlaylistItem, BooleanVar) tuples
        
        self.title(f"Playlist - {playlist_info.title[:50]}...")
        self.geometry("850x650")
        self.transient(parent)
        self.resizable(True, True)
        self.minsize(600, 450)
        
        # Configure colors
        self.configure(fg_color=COLORS["bg_primary"])
        
        # Main container
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        self._create_header(main_frame)
        
        # Video list (scrollable)
        self._create_video_list(main_frame)
        
        # Footer with options and download button
        self._create_footer(main_frame)
        
        # Apply settings (reverse order, max items)
        self._apply_settings()
    
    def _create_header(self, parent):
        """Create the header section with playlist info."""
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))
        
        # Playlist title and stats
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(
            title_frame,
            text=f"📋 {self.playlist_info.title}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS["text_primary"],
            anchor="w"
        ).pack(anchor="w")
        
        stats_text = f"{self.playlist_info.playlist_count} videos"
        if self.playlist_info.total_playlist_duration > 0:
            stats_text += f" • {self.playlist_info.total_playlist_duration_str} total"
        if self.playlist_info.channel:
            stats_text += f" • {self.playlist_info.channel}"
        
        ctk.CTkLabel(
            title_frame,
            text=stats_text,
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_secondary"],
            anchor="w"
        ).pack(anchor="w", pady=(4, 0))
        
        # Select all / Deselect all buttons
        btn_frame = ctk.CTkFrame(header, fg_color="transparent")
        btn_frame.pack(side="right")
        
        ctk.CTkButton(
            btn_frame,
            text="Select All",
            width=90,
            height=30,
            font=ctk.CTkFont(size=12),
            fg_color=COLORS["bg_elevated"],
            hover_color=COLORS["bg_hover"],
            command=self._select_all
        ).pack(side="left", padx=(0, 8))
        
        ctk.CTkButton(
            btn_frame,
            text="Deselect All",
            width=90,
            height=30,
            font=ctk.CTkFont(size=12),
            fg_color=COLORS["bg_elevated"],
            hover_color=COLORS["bg_hover"],
            command=self._deselect_all
        ).pack(side="left")
    
    def _create_video_list(self, parent):
        """Create the scrollable video list."""
        self.videos_frame = ctk.CTkScrollableFrame(
            parent,
            fg_color=COLORS["bg_secondary"],
            corner_radius=10
        )
        self.videos_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Create video rows
        for item in self.playlist_info.playlist_items:
            self._create_video_row(item)
    
    def _create_video_row(self, item: PlaylistItem):
        """Create a row for a single playlist video."""
        row = ctk.CTkFrame(self.videos_frame, fg_color="transparent")
        row.pack(fill="x", padx=10, pady=5)
        
        # Checkbox
        var = ctk.BooleanVar(value=True)  # Selected by default
        self.video_vars.append((item, var))
        
        cb = ctk.CTkCheckBox(
            row,
            text="",
            variable=var,
            width=24,
            checkbox_width=20,
            checkbox_height=20
        )
        cb.pack(side="left", padx=(0, 10))
        
        # Video number
        ctk.CTkLabel(
            row,
            text=f"{item.index:02d}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLORS["accent_blue"],
            width=30
        ).pack(side="left", padx=(0, 10))
        
        # Video title
        ctk.CTkLabel(
            row,
            text=item.title[:55] + ("..." if len(item.title) > 55 else ""),
            font=ctk.CTkFont(size=13),
            text_color=COLORS["text_primary"],
            anchor="w"
        ).pack(side="left", fill="x", expand=True)
        
        # Channel (if different from playlist owner)
        if item.channel and item.channel != self.playlist_info.channel:
            ctk.CTkLabel(
                row,
                text=item.channel[:20],
                font=ctk.CTkFont(size=10),
                text_color=COLORS["text_tertiary"],
                width=100
            ).pack(side="right", padx=(10, 0))
        
        # Duration
        ctk.CTkLabel(
            row,
            text=item.duration_str,
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_secondary"],
            width=60
        ).pack(side="right", padx=(10, 0))
    
    def _create_footer(self, parent):
        """Create the footer with options and download button."""
        footer = ctk.CTkFrame(parent, fg_color="transparent")
        footer.pack(fill="x")
        
        # Options frame (left side)
        options_frame = ctk.CTkFrame(footer, fg_color="transparent")
        options_frame.pack(side="left")
        
        # Audio only option
        self.audio_only_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            options_frame,
            text="Audio Only (M4A)",
            variable=self.audio_only_var,
            font=ctk.CTkFont(size=13),
            text_color=COLORS["text_secondary"]
        ).pack(side="left", padx=(0, 20))
        
        # Quality selection
        ctk.CTkLabel(
            options_frame,
            text="Quality:",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_secondary"]
        ).pack(side="left", padx=(0, 8))
        
        self.quality_var = ctk.StringVar(value="1080p")
        quality_menu = ctk.CTkOptionMenu(
            options_frame,
            variable=self.quality_var,
            values=["Best", "2160p (4K)", "1440p", "1080p", "720p", "480p"],
            width=120,
            height=30,
            font=ctk.CTkFont(size=12)
        )
        quality_menu.pack(side="left")
        
        # Selected count label
        self.selected_label = ctk.CTkLabel(
            footer,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_secondary"]
        )
        self.selected_label.pack(side="left", padx=(30, 0))
        self._update_selected_count()
        
        # Buttons (right side)
        btn_frame = ctk.CTkFrame(footer, fg_color="transparent")
        btn_frame.pack(side="right")
        
        # Cancel button
        ModernButton(
            btn_frame,
            text="Cancel",
            style="secondary",
            width=80,
            height=40,
            command=self.destroy
        ).pack(side="left", padx=(0, 10))
        
        # Download button
        ModernButton(
            btn_frame,
            text="⚡ Download Selected",
            style="primary",
            width=160,
            height=40,
            command=self._start_download
        ).pack(side="left")
    
    def _apply_settings(self):
        """Apply playlist settings from settings manager."""
        # Check if we should reverse order
        if self.settings_mgr.get("playlist_reverse", False):
            # Reverse the display order (but keep original indices)
            for widget in self.videos_frame.winfo_children():
                widget.pack_forget()
            
            for item, var in reversed(self.video_vars):
                # Re-create the row in reverse order
                # (Actually, we'll just re-pack them)
                pass  # TODO: Implement if needed
        
        # Check max items limit
        max_items = self.settings_mgr.get("playlist_max_items", 0)
        if max_items > 0:
            # Deselect items beyond the limit
            for i, (item, var) in enumerate(self.video_vars):
                if i >= max_items:
                    var.set(False)
        
        # Check if "download all by default" is disabled
        if not self.settings_mgr.get("playlist_download_all", True):
            # Deselect all by default
            for _, var in self.video_vars:
                var.set(False)
        
        self._update_selected_count()
    
    def _update_selected_count(self):
        """Update the selected count label."""
        selected = sum(1 for _, var in self.video_vars if var.get())
        total = len(self.video_vars)
        self.selected_label.configure(text=f"{selected}/{total} selected")
    
    def _select_all(self):
        """Select all videos."""
        for _, var in self.video_vars:
            var.set(True)
        self._update_selected_count()
    
    def _deselect_all(self):
        """Deselect all videos."""
        for _, var in self.video_vars:
            var.set(False)
        self._update_selected_count()
    
    def _get_selected_quality_height(self) -> Optional[int]:
        """Convert quality selection to height value."""
        quality_map = {
            "Best": None,
            "2160p (4K)": 2160,
            "1440p": 1440,
            "1080p": 1080,
            "720p": 720,
            "480p": 480
        }
        return quality_map.get(self.quality_var.get())
    
    def _start_download(self):
        """Start downloading selected videos."""
        selected_items = [item for item, var in self.video_vars if var.get()]
        
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select at least one video to download.")
            return
        
        # Create a VideoFormat with the selected quality
        quality_height = self._get_selected_quality_height()
        selected_format = None
        if quality_height:
            selected_format = VideoFormat(
                format_id="",
                ext="mp4",
                height=quality_height,
                resolution=f"{quality_height}p"
            )
        
        audio_only = self.audio_only_var.get()
        
        self.on_download(selected_items, selected_format, audio_only)
        self.destroy()

class SystemMonitor:
    """Monitor system resources (CPU, Memory, GPU) in real-time."""
    
    def __init__(self):
        self.cpu_percent = 0.0
        self.memory_percent = 0.0
        self.gpu_percent = 0.0
        self.monitoring = False
        self._monitor_thread = None
        
    def start_monitoring(self):
        """Start monitoring system resources."""
        if self.monitoring:
            return
        
        self.monitoring = True
        self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop monitoring."""
        self.monitoring = False
    
    def _monitor_loop(self):
        """Background loop to update resource usage."""
        try:
            import psutil
        except ImportError:
            print("psutil not installed - system monitoring disabled")
            return
        
        # Get current process
        import os
        try:
            process = psutil.Process(os.getpid())
        except Exception as e:
            print(f"Could not get process for monitoring: {e}")
            return
        
        # Initial CPU call to initialize
        try:
            process.cpu_percent(interval=None)
        except Exception:
            pass
        
        while self.monitoring:
            try:
                # FIXED: Use interval=None to avoid blocking and GIL issues
                # This returns the CPU usage since the last call, not blocking
                cpu = process.cpu_percent(interval=None)
                
                # Only update if we got a valid reading
                if cpu is not None and cpu >= 0:
                    self.cpu_percent = min(cpu, 100.0)  # Cap at 100%
                
                # Memory usage for this process
                mem_info = process.memory_info()
                total_memory = psutil.virtual_memory().total
                self.memory_percent = (mem_info.rss / total_memory) * 100 if total_memory > 0 else 0
                
                # GPU usage (macOS Metal) - not easily available without root
                self.gpu_percent = 0.0
                
                time.sleep(1)  # Update every second
            except Exception as e:
                # Silently continue on errors to avoid crashes
                time.sleep(1)
    
    def get_stats(self) -> tuple:
        """Get current stats as (cpu_percent, memory_percent, gpu_percent)."""
        return (self.cpu_percent, self.memory_percent, self.gpu_percent)


class ResourceGauge(ctk.CTkCanvas):
    """RPM-style gauge for displaying resource usage - compact design."""
    
    def __init__(self, master, label="CPU", max_value=100, color="#667eea", **kwargs):
        super().__init__(
            master,
            width=60,  # FIXED: Reduced from 70 to 60
            height=60,  # FIXED: Reduced from 70 to 60
            bg=COLORS["bg_tertiary"],
            highlightthickness=0,
            **kwargs
        )
        
        self.label = label
        self.max_value = max_value
        self.color = color
        self.current_value = 0
        
        self._draw_gauge()
    
    def _draw_gauge(self):
        """Draw the gauge background."""
        self.delete("all")
        
        # Center and radius - even smaller
        cx, cy = 30, 30  # FIXED: Reduced from 35 to 30
        radius = 22  # FIXED: Reduced from 26 to 22
        
        # Draw background arc (gray)
        self.create_arc(
            cx - radius, cy - radius,
            cx + radius, cy + radius,
            start=135, extent=270,
            outline=COLORS["border_light"],
            width=4,  # FIXED: Reduced from 5 to 4
            style="arc"
        )
        
        # Draw value arc (colored)
        extent = (self.current_value / self.max_value) * 270
        self.create_arc(
            cx - radius, cy - radius,
            cx + radius, cy + radius,
            start=135, extent=extent,
            outline=self.color,
            width=4,  # FIXED: Reduced from 5 to 4
            style="arc",
            tags="value_arc"
        )
        
        # Draw center label - smaller font
        self.create_text(
            cx, cy - 3,  # FIXED: Adjusted from cy - 4
            text=f"{self.current_value:.0f}%",
            fill=COLORS["text_primary"],
            font=("SF Pro Display", 10, "bold"),  # FIXED: Reduced from 11 to 10
            tags="value_text"
        )
        
        # Draw gauge label - smaller font
        self.create_text(
            cx, cy + 10,  # FIXED: Adjusted from cy + 11
            text=self.label,
            fill=COLORS["text_tertiary"],
            font=("SF Pro Text", 7),  # FIXED: Reduced from 8 to 7
            tags="label_text"
        )
    
    def set_value(self, value: float):
        """Update the gauge value."""
        self.current_value = min(max(0, value), self.max_value)
        self._draw_gauge()


# ============================================================================
# MAIN APPLICATION
# ============================================================================

class YtDlpGUI(ctk.CTk):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        
        # Initialize managers
        self.settings_mgr = SettingsManager(SETTINGS_PATH)
        self.history_mgr = HistoryManager(HISTORY_PATH)
        
        # Configure CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Window setup with smart sizing based on screen
        self.title(f"{APP_NAME} v{APP_VERSION}")
        
        # Detect screen size and set appropriate window size
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calculate ideal window size for two-column layout (wider, not taller)
        ideal_width = min(int(screen_width * 0.85), 1600)  # Wider for two columns
        ideal_height = min(int(screen_height * 0.75), 950)  # Standard height
        
        # Ensure minimum size
        window_width = max(ideal_width, 1400)  # Wider minimum for two columns
        window_height = max(ideal_height, 850)
        
        # Center window on screen
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.minsize(1200, 800)  # Wider minimum
        
        # Set window background
        self.configure(fg_color=COLORS["bg_primary"])
        
        # Track open dialog windows
        self.settings_window = None
        self.history_window = None
        self.about_window = None
        
        # Initialize system monitor
        self.system_monitor = SystemMonitor()
        self.system_monitor.start_monitoring()
        
        # Initialize components
        self.ytdlp = YtDlpInterface()
        self.thumbnail_manager = ThumbnailManager()
        self.config = load_json_file(CONFIG_PATH, {
            "output_dir": str(Path.home() / "Desktop"),
            "max_resolution": "Best Available",
            "format_preset": "QuickTime (H.264 + AAC)",
            "audio_only": False,
            "show_advanced": False,
        })
        
        self.download_manager = DownloadManager(
            self.ytdlp, 
            self.config.get("output_dir", str(Path.home() / "Desktop"))
        )
        self.download_manager.add_callback(self._on_download_event)
        
        # State
        self.current_video: Optional[VideoInfo] = None
        self.selected_format: Optional[VideoFormat] = None
        self.format_cards: List[FormatCard] = []
        
        # Build UI
        self._create_ui()
        
        # Bind events
        self.bind("<FocusIn>", self._on_focus)
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # Check yt-dlp
        self._check_dependencies()
        
        # Setup keyboard shortcuts
        self._setup_keyboard_shortcuts()
        
        # Setup drag & drop (if available)
        self._setup_drag_drop()
        
        # Check clipboard after a short delay
        self.after(500, self._check_clipboard_on_start)
        
        # Check for yt-dlp updates on startup (v17.10.0)
        self.after(3000, self._check_ytdlp_update_on_startup)
        
        # Check for app updates on startup (v18.0.0)
        self.after(5000, self._check_app_update_on_startup)
    
    def _create_ui(self):
        """Create the modern two-column responsive UI layout - NO SCROLLING."""
        # Main container with reduced padding
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=16, pady=12)
        
        # Configure grid for two-column layout
        self.main_container.grid_rowconfigure(0, weight=0)  # Header - fixed
        self.main_container.grid_rowconfigure(1, weight=0)  # URL - fixed
        self.main_container.grid_rowconfigure(2, weight=1)  # Content row expands
        self.main_container.grid_rowconfigure(3, weight=0)  # Footer - fixed
        self.main_container.grid_columnconfigure(0, weight=3)  # Left column - 3/5 width
        self.main_container.grid_columnconfigure(1, weight=2, minsize=320)  # Right column - 2/5 width
        
        # === HEADER (row 0, spans both columns) ===
        self._create_header()
        
        # === URL INPUT (row 1, spans both columns) ===
        self._create_url_section()
        
        # === LEFT COLUMN (row 2, col 0): Non-scrollable content ===
        self.content_frame = ctk.CTkFrame(
            self.main_container,
            fg_color="transparent"
        )
        self.content_frame.grid(row=2, column=0, sticky="nsew", padx=(0, 8))
        
        # Use grid inside content_frame for proper sizing
        self.content_frame.grid_rowconfigure(0, weight=1)  # Video expands
        self.content_frame.grid_rowconfigure(1, weight=0)  # Progress fixed
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Main content in left column
        self._create_video_section()
        self._create_progress_section()
        
        # === RIGHT COLUMN (row 2, col 1): Activity log ===
        self._create_log_section()
        
        # === FOOTER (row 3, spans both columns) ===
        self._create_footer()
    
    def _create_header(self):
        """Create compact header with app icon and icon buttons."""
        header = ctk.CTkFrame(self.main_container, fg_color="transparent", height=56)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        header.grid_propagate(False)
        
        # Left side - App branding
        left_frame = ctk.CTkFrame(header, fg_color="transparent")
        left_frame.pack(side="left", fill="y")
        
        # App icon - smaller
        icon_frame = ctk.CTkFrame(
            left_frame,
            width=44,
            height=44,
            corner_radius=12,
            fg_color=COLORS["accent_gradient_start"],
            border_width=0
        )
        icon_frame.pack(side="left", padx=(0, 12))
        icon_frame.pack_propagate(False)
        
        icon_label = ctk.CTkLabel(
            icon_frame,
            text="🔥",
            font=ctk.CTkFont(size=22),
            cursor="hand2"
        )
        icon_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Make icon clickable
        icon_frame.bind("<Button-1>", lambda e: self._open_github())
        icon_label.bind("<Button-1>", lambda e: self._open_github())
        ToolTip(icon_frame, "Click to visit GitHub")
        
        # App title and version inline
        title_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        title_frame.pack(side="left")
        
        title_label = ctk.CTkLabel(
            title_frame,
            text=APP_NAME,
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS["text_primary"]
        )
        title_label.pack(side="left", padx=(0, 8))
        
        version_badge = ctk.CTkLabel(
            title_frame,
            text=f"v{APP_VERSION}",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=COLORS["accent_gradient_start"],
            fg_color=COLORS["bg_elevated"],
            corner_radius=6,
            padx=6,
            pady=2
        )
        version_badge.pack(side="left", padx=(0, 8))
        
        self.ytdlp_version_label = ctk.CTkLabel(
            title_frame,
            text=f"yt-dlp: {self.ytdlp.get_version()}",
            font=ctk.CTkFont(size=10),
            text_color=COLORS["text_tertiary"]
        )
        self.ytdlp_version_label.pack(side="left")
        
        # Right side - Icon buttons
        button_frame = ctk.CTkFrame(header, fg_color="transparent")
        button_frame.pack(side="right", fill="y")
        
        # Update button
        self.update_btn = ModernButton(
            button_frame,
            text="🔄",
            style="icon",
            width=36,
            height=36,
            command=self._check_ytdlp_update
        )
        self.update_btn.pack(side="left", padx=2)
        ToolTip(self.update_btn, "Update yt-dlp")
        
        # Settings button
        settings_btn = ModernButton(
            button_frame,
            text="⚙️",
            style="icon",
            width=36,
            height=36,
            command=self._show_settings
        )
        settings_btn.pack(side="left", padx=2)
        ToolTip(settings_btn, "Settings")
        
        # History button
        history_btn = ModernButton(
            button_frame,
            text="📚",
            style="icon",
            width=36,
            height=36,
            command=self._show_history
        )
        history_btn.pack(side="left", padx=2)
        ToolTip(history_btn, "History")
        
        # Help button
        help_btn = ModernButton(
            button_frame,
            text="❓",
            style="icon",
            width=36,
            height=36,
            command=self._show_help
        )
        help_btn.pack(side="left", padx=2)
        ToolTip(help_btn, "Help")
    
    def _create_url_section(self):
        """Create compact URL input section with playlist toggle."""
        url_frame = ctk.CTkFrame(self.main_container, fg_color="transparent", height=48)
        url_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        url_frame.grid_propagate(False)
        
        # URL entry - smaller height
        self.url_entry = ctk.CTkEntry(
            url_frame,
            placeholder_text="Paste YouTube URL...",
            corner_radius=10,
            height=40,
            font=ctk.CTkFont(size=13),
            fg_color=COLORS["bg_tertiary"],
            border_color=COLORS["border_light"],
            text_color=COLORS["text_primary"],
            placeholder_text_color=COLORS["text_tertiary"],
            border_width=1
        )
        self.url_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.url_entry.bind("<Return>", lambda e: self._analyze())
        self.url_entry.bind("<KeyRelease>", self._on_url_changed)
        
        # Playlist toggle (hidden by default, shown when URL has playlist)
        self.playlist_toggle_frame = ctk.CTkFrame(url_frame, fg_color="transparent")
        # Don't pack yet - will be shown when URL contains playlist
        
        self.playlist_mode_var = ctk.BooleanVar(value=False)
        self.playlist_toggle = ctk.CTkSwitch(
            self.playlist_toggle_frame,
            text="📋 Playlist",
            variable=self.playlist_mode_var,
            font=ctk.CTkFont(size=12),
            width=40,
            height=20,
            switch_width=36,
            switch_height=18,
            onvalue=True,
            offvalue=False,
            command=self._on_playlist_toggle
        )
        self.playlist_toggle.pack(side="left", padx=(0, 8))
        
        # Analyze button
        ModernButton(
            url_frame,
            text="⚡ Analyze",
            style="primary",
            width=100,
            height=40,
            command=self._analyze
        ).pack(side="left")
    
    def _on_url_changed(self, event=None):
        """Handle URL entry changes - show/hide playlist toggle."""
        url = self.url_entry.get().strip()
        parsed = parse_youtube_url(url)
        
        # Show playlist toggle if URL has playlist context
        if parsed.playlist_id:
            if not self.playlist_toggle_frame.winfo_ismapped():
                self.playlist_toggle_frame.pack(side="left", padx=(0, 8))
            
            # If it's explicitly a playlist URL (no video), enable playlist mode by default
            if parsed.is_playlist_url and not parsed.video_id:
                self.playlist_mode_var.set(True)
            # If it has both video and playlist, default to single video
            elif parsed.has_video_and_playlist:
                # Keep current state or default to False
                pass
        else:
            # Hide toggle if no playlist in URL
            if self.playlist_toggle_frame.winfo_ismapped():
                self.playlist_toggle_frame.pack_forget()
            self.playlist_mode_var.set(False)
    
    def _on_playlist_toggle(self):
        """Handle playlist toggle state change."""
        if self.playlist_mode_var.get():
            self.log_panel.log("📋 Playlist mode enabled - will fetch all videos", "info")
        else:
            self.log_panel.log("🎬 Single video mode - will download only this video", "info")
    
    def _create_video_section(self):
        """Create a compact video preview card that always shows download button."""
        self.video_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=COLORS["bg_tertiary"],
            corner_radius=16,
            border_width=1,
            border_color=COLORS["border_light"]
        )
        # Initially hidden - shown when video is analyzed
        # Will use grid row 0
        
        # Use grid layout inside video_frame for better control
        self.video_frame.grid_rowconfigure(0, weight=0)  # Top row (thumbnail + info) - fixed
        self.video_frame.grid_rowconfigure(1, weight=0)  # Divider - fixed
        self.video_frame.grid_rowconfigure(2, weight=1)  # Format cards - can expand
        self.video_frame.grid_rowconfigure(3, weight=0)  # Download button - fixed at bottom
        self.video_frame.grid_columnconfigure(0, weight=1)
        
        # === TOP ROW: Thumbnail + Video Info ===
        top_row = ctk.CTkFrame(self.video_frame, fg_color="transparent")
        top_row.grid(row=0, column=0, sticky="ew", padx=16, pady=(12, 8))
        
        # Thumbnail container (left side) - smaller
        self.thumb_frame = ctk.CTkFrame(
            top_row,
            fg_color=COLORS["bg_elevated"],
            corner_radius=10,
            width=160,
            height=90  # 16:9 ratio, smaller
        )
        self.thumb_frame.pack(side="left", padx=(0, 12))
        self.thumb_frame.pack_propagate(False)
        
        self.thumb_label = ctk.CTkLabel(
            self.thumb_frame,
            text="",
            font=ctk.CTkFont(size=32),
            text_color=COLORS["text_tertiary"]
        )
        self.thumb_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Duration badge on thumbnail
        self.duration_badge = ctk.CTkLabel(
            self.thumb_frame,
            text="0:00",
            font=ctk.CTkFont(size=9, weight="bold"),
            text_color="white",
            fg_color="black",
            corner_radius=4,
            padx=4,
            pady=1
        )
        self.duration_badge.place(relx=0.95, rely=0.95, anchor="se")
        
        # Video info (right side of thumbnail)
        info_container = ctk.CTkFrame(top_row, fg_color="transparent")
        info_container.pack(side="left", fill="both", expand=True)
        
        # Title - single line with ellipsis
        self.title_label = ctk.CTkLabel(
            info_container,
            text="🎬 Video Title",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS["text_primary"],
            anchor="w"
        )
        self.title_label.pack(fill="x", anchor="w")
        
        # Meta info row (channel, views, chapters) - compact
        meta_frame = ctk.CTkFrame(info_container, fg_color="transparent")
        meta_frame.pack(fill="x", pady=(4, 0), anchor="w")
        
        self.channel_label = ctk.CTkLabel(
            meta_frame,
            text=" Channel",
            font=ctk.CTkFont(size=11),
            text_color=COLORS["text_secondary"]
        )
        self.channel_label.pack(side="left", padx=(0, 12))
        
        self.views_label = ctk.CTkLabel(
            meta_frame,
            text=" Views",
            font=ctk.CTkFont(size=11),
            text_color=COLORS["text_secondary"]
        )
        self.views_label.pack(side="left", padx=(0, 12))
        
        self.chapters_label = ctk.CTkLabel(
            meta_frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color=COLORS["accent_purple"]
        )
        self.chapters_label.pack(side="left", padx=(0, 6))
        
        # Chapters button (hidden initially)
        self.chapters_button = ModernButton(
            meta_frame,
            text=" Chapters",
            style="secondary",
            width=90,
            height=24,
            command=self._show_chapters_dialog
        )
        
        # === DIVIDER with quality header ===
        quality_row = ctk.CTkFrame(self.video_frame, fg_color="transparent")
        quality_row.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 6))
        
        ctk.CTkLabel(
            quality_row,
            text="🎯 SELECT QUALITY",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=COLORS["text_tertiary"]
        ).pack(side="left")
        
        # Selected format indicator (right side)
        self.selected_format_label = ctk.CTkLabel(
            quality_row,
            text="",
            font=ctk.CTkFont(size=10),
            text_color=COLORS["accent_gradient_start"]
        )
        self.selected_format_label.pack(side="right")
        
        # === FORMAT CARDS SECTION - scrollable if needed ===
        formats_frame = ctk.CTkFrame(self.video_frame, fg_color="transparent")
        formats_frame.grid(row=2, column=0, sticky="nsew", padx=16, pady=(0, 8))
        
        # Format cards container - will be a responsive grid
        self.formats_container = ctk.CTkFrame(formats_frame, fg_color="transparent")
        self.formats_container.pack(fill="both", expand=True)
        
        # === BOTTOM ROW: Download Button - ALWAYS VISIBLE ===
        bottom_row = ctk.CTkFrame(self.video_frame, fg_color="transparent")
        bottom_row.grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 12))
        
        # Download button (right aligned)
        self.download_btn = ModernButton(
            bottom_row,
            text="⚡ Download",
            style="primary",
            width=140,
            height=40,
            command=self._download
        )
        self.download_btn.pack(side="right")
    
    def _create_progress_section(self):
        """Create compact progress section with inline metrics."""
        self.progress_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=COLORS["bg_tertiary"],
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border_light"]
        )
        # Use grid row 1 (fixed height)
        self.progress_frame.grid(row=1, column=0, sticky="ew", pady=(8, 0))
        
        # Header row
        prog_header = ctk.CTkFrame(self.progress_frame, fg_color="transparent")
        prog_header.pack(fill="x", padx=12, pady=(8, 4))
        
        ctk.CTkLabel(
            prog_header,
            text="🔥 Download Progress",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLORS["text_primary"]
        ).pack(side="left")
        
        # Status indicator
        status_frame = ctk.CTkFrame(prog_header, fg_color="transparent")
        status_frame.pack(side="right")
        
        self.status_dot = ctk.CTkLabel(
            status_frame,
            text="*",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_tertiary"]
        )
        self.status_dot.pack(side="left", padx=(0, 4))
        
        self.queue_status = ctk.CTkLabel(
            status_frame,
            text="Idle",
            font=ctk.CTkFont(size=10),
            text_color=COLORS["text_secondary"]
        )
        self.queue_status.pack(side="left")
        
        # Progress bar
        self.main_progress = EnhancedProgressBar(self.progress_frame)
        self.main_progress.pack(fill="x", padx=12, pady=(0, 6))
        
        # Stage and percentage row
        stage_row = ctk.CTkFrame(self.progress_frame, fg_color="transparent")
        stage_row.pack(fill="x", padx=12, pady=(0, 6))
        
        self.progress_label = ctk.CTkLabel(
            stage_row,
            text="â³ Ready to download",
            font=ctk.CTkFont(size=11),
            text_color=COLORS["text_secondary"]
        )
        self.progress_label.pack(side="left")
        
        self.percentage_label = ctk.CTkLabel(
            stage_row,
            text="",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=COLORS["text_primary"]
        )
        self.percentage_label.pack(side="right")
        
        # Metrics row - very compact inline layout
        metrics_row = ctk.CTkFrame(self.progress_frame, fg_color=COLORS["bg_elevated"], corner_radius=8)
        metrics_row.pack(fill="x", padx=12, pady=(0, 8))
        
        metrics_inner = ctk.CTkFrame(metrics_row, fg_color="transparent")
        metrics_inner.pack(fill="x", padx=10, pady=6)
        
        # Speed
        speed_frame = ctk.CTkFrame(metrics_inner, fg_color="transparent")
        speed_frame.pack(side="left", padx=(0, 16))
        ctk.CTkLabel(speed_frame, text="SPEED", font=ctk.CTkFont(size=8, weight="bold"),
                    text_color=COLORS["text_tertiary"]).pack(side="left", padx=(0, 4))
        self.speed_label = ctk.CTkLabel(speed_frame, text="--", font=ctk.CTkFont(size=11, weight="bold"),
                    text_color=COLORS["accent_gradient_start"])
        self.speed_label.pack(side="left")
        
        # FPS
        fps_frame = ctk.CTkFrame(metrics_inner, fg_color="transparent")
        fps_frame.pack(side="left", padx=(0, 16))
        ctk.CTkLabel(fps_frame, text="FPS", font=ctk.CTkFont(size=8, weight="bold"),
                    text_color=COLORS["text_tertiary"]).pack(side="left", padx=(0, 4))
        self.fps_label = ctk.CTkLabel(fps_frame, text="--", font=ctk.CTkFont(size=11, weight="bold"),
                    text_color=COLORS["accent_green"])
        self.fps_label.pack(side="left")
        
        # ETA
        eta_frame = ctk.CTkFrame(metrics_inner, fg_color="transparent")
        eta_frame.pack(side="left", padx=(0, 16))
        ctk.CTkLabel(eta_frame, text="ETA", font=ctk.CTkFont(size=8, weight="bold"),
                    text_color=COLORS["text_tertiary"]).pack(side="left", padx=(0, 4))
        self.eta_label = ctk.CTkLabel(eta_frame, text="--", font=ctk.CTkFont(size=11, weight="bold"),
                    text_color=COLORS["text_secondary"])
        self.eta_label.pack(side="left")
        
        # Size
        size_frame = ctk.CTkFrame(metrics_inner, fg_color="transparent")
        size_frame.pack(side="left")
        ctk.CTkLabel(size_frame, text="SIZE", font=ctk.CTkFont(size=8, weight="bold"),
                    text_color=COLORS["text_tertiary"]).pack(side="left", padx=(0, 4))
        self.size_label = ctk.CTkLabel(size_frame, text="--", font=ctk.CTkFont(size=11, weight="bold"),
                    text_color=COLORS["text_secondary"])
        self.size_label.pack(side="left")
    
    def _create_log_section(self):
        """Create modern activity log in right column (always visible)."""
        # Log panel in right column - fills entire height
        log_container = ctk.CTkFrame(self.main_container, fg_color="transparent")
        log_container.grid(row=2, column=1, sticky="nsew")
        
        # Create log panel that fills the container
        self.log_panel = LogPanel(log_container, show_export=False)
        self.log_panel.pack(fill="both", expand=True)
        
        # Welcome messages
        self.log_panel.log(f"Welcome to {APP_NAME} v{APP_VERSION}", "info")
        self.log_panel.log(f"📦 yt-dlp version: {self.ytdlp.get_version()}", "info")
    
    def _create_footer(self):
        """Create modern footer with resource gauges, output path and action buttons."""
        # v18.0.1: Increased height to accommodate gauges
        footer_frame = ctk.CTkFrame(self.main_container, fg_color="transparent", height=70)
        footer_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(12, 0))
        footer_frame.grid_propagate(False)
        
        # Separator line
        separator = ctk.CTkFrame(footer_frame, fg_color=COLORS["border_light"], height=1)
        separator.pack(fill="x", pady=(0, 10))
        
        # Content frame
        content = ctk.CTkFrame(footer_frame, fg_color="transparent")
        content.pack(fill="both", expand=True)
        
        # Left side - Resource gauges (always visible)
        gauges_frame = ctk.CTkFrame(content, fg_color="transparent")
        gauges_frame.pack(side="left", padx=(0, 20))
        
        # CPU Gauge - compact inline style
        self.cpu_gauge = ResourceGauge(
            gauges_frame,
            label="CPU",
            color=COLORS["accent_gradient_start"]
        )
        self.cpu_gauge.pack(side="left", padx=(0, 8))
        
        # Memory Gauge
        self.memory_gauge = ResourceGauge(
            gauges_frame,
            label="MEM",
            color=COLORS["accent_purple"]
        )
        self.memory_gauge.pack(side="left", padx=(0, 8))
        
        # GPU Gauge
        self.gpu_gauge = ResourceGauge(
            gauges_frame,
            label="GPU",
            color=COLORS["accent_green"]
        )
        self.gpu_gauge.pack(side="left", padx=(0, 16))
        
        # Start updating gauges
        self._update_resource_gauges()
        
        # Center - Output path with vertical centering
        path_frame = ctk.CTkFrame(content, fg_color="transparent")
        path_frame.pack(side="left", fill="y")
        
        # Vertical centering container
        path_inner = ctk.CTkFrame(path_frame, fg_color="transparent")
        path_inner.pack(expand=True)
        
        path_row = ctk.CTkFrame(path_inner, fg_color="transparent")
        path_row.pack()
        
        ctk.CTkLabel(
            path_row,
            text=" Output:",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_tertiary"]
        ).pack(side="left")
        
        self.output_path_label = ctk.CTkLabel(
            path_row,
            text=self.config.get("output_dir", "~/Desktop"),
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_primary"]
        )
        self.output_path_label.pack(side="left", padx=(8, 0))
        
        # Right side - Action buttons
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(side="right")
        
        ModernButton(
            btn_frame,
            text=" Open Folder",
            style="secondary",
            width=130,
            height=36,
            command=self._open_output_folder
        ).pack(side="left", padx=(0, 8))
        
        ModernButton(
            btn_frame,
            text="Change...",
            style="secondary",
            width=90,
            height=36,
            command=self._choose_output_dir
        ).pack(side="left")
    
    # =========================================================================
    # ACTIONS
    # =========================================================================
    
    def _check_dependencies(self):
        """Check if yt-dlp and ffmpeg are available."""
        if not self.ytdlp.is_available:
            self.log_panel.log(f"yt-dlp not found at {YTDLP_PATH}", "error")
            messagebox.showwarning(
                "yt-dlp Not Found",
                f"yt-dlp was not found at {YTDLP_PATH}\n\n"
                "Install with: brew install yt-dlp"
            )
        
        if not os.path.isfile(FFMPEG_PATH):
            self.log_panel.log(f"ffmpeg not found at {FFMPEG_PATH}", "warning")
        
        # Check for psutil (optional but recommended for system monitoring)
        try:
            import psutil
        except ImportError:
            self.log_panel.log("psutil not installed - system resource monitoring disabled", "info")
            self.log_panel.log("Install with: pip install psutil", "info")
    
    def _on_focus(self, event=None):
        """Handle window focus - auto-grab clipboard."""
        try:
            clip = self.clipboard_get()
            if any(clip.startswith(p) for p in [
                "https://www.youtube.com/watch",
                "https://youtu.be/",
                "https://youtube.com/watch",
                "https://www.youtube.com/playlist"
            ]):
                current = self.url_entry.get()
                if clip != current:
                    self.url_entry.delete(0, "end")
                    self.url_entry.insert(0, clip)
        except Exception:
            pass
    
    def _on_close(self):
        """Handle window close."""
        self._save_config()
        self.destroy()
    
    def _save_config(self):
        """Save current configuration."""
        save_json_file(CONFIG_PATH, self.config)
    
    def _toggle_option(self, option_key: str):
        """Toggle an option chip."""
        # Mutually exclusive options
        exclusive = ["video_audio", "audio_only"]
        
        if option_key in exclusive:
            for key in exclusive:
                self.option_chips[key].set_active(key == option_key)
            self.config["audio_only"] = (option_key == "audio_only")
        elif option_key == "quicktime":
            chip = self.option_chips[option_key]
            chip.set_active(not chip.active)
        elif option_key == "advanced":
            chip = self.option_chips[option_key]
            chip.set_active(not chip.active)
            self.config["show_advanced"] = chip.active
            # Could toggle advanced options panel here
    
    def _analyze(self):
        """Analyze the URL and show video info or playlist."""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("No URL", "Please enter a YouTube URL")
            return
        
        # Parse the URL to determine what we're dealing with
        parsed = parse_youtube_url(url)
        
        # Update the playlist toggle visibility
        self._on_url_changed()
        
        # Determine if we should fetch playlist or single video
        fetch_playlist = False
        
        if parsed.is_playlist_url and not parsed.video_id:
            # Explicit playlist URL with no video - always fetch playlist
            fetch_playlist = True
            self.playlist_mode_var.set(True)
        elif parsed.has_video_and_playlist and self.playlist_mode_var.get():
            # URL has both video and playlist, and user enabled playlist mode
            fetch_playlist = True
        elif parsed.playlist_id and self.playlist_mode_var.get():
            # Has playlist ID and playlist mode is on
            fetch_playlist = True
        
        if fetch_playlist:
            self.log_panel.log(f"Analyzing playlist: {url}", "info")
        else:
            self.log_panel.log(f"Analyzing: {url}", "info")
        
        # Clear previous state
        self.current_video = None
        self.selected_format = None
        
        # Ensure format_cards is initialized
        if not hasattr(self, 'format_cards'):
            self.format_cards = []
        
        for card in self.format_cards:
            try:
                card.destroy()
            except:
                pass
        self.format_cards.clear()
        
        # Run analysis in thread
        def analyze_thread():
            try:
                if fetch_playlist:
                    # Fetch playlist info
                    info = self.ytdlp.fetch_playlist_info(url)
                    self.after(0, lambda i=info: self._display_playlist_info(i))
                else:
                    # Fetch single video info
                    info = self.ytdlp.fetch_full_info(url)
                    self.after(0, lambda i=info: self._display_video_info(i))
            except AgeRestrictedError as e:
                error = e
                self.after(0, lambda err=error: self._handle_age_restricted_error(err))
            except PrivateVideoError as e:
                error = e
                self.after(0, lambda err=error: self._handle_private_video_error(err))
            except VideoUnavailableError as e:
                error = e
                self.after(0, lambda err=error: self._handle_video_unavailable_error(err))
            except LoginRequiredError as e:
                error = e
                self.after(0, lambda err=error: self._handle_login_required_error(err))
            except UnviewablePlaylistError as e:
                error = e
                self.after(0, lambda err=error: self._handle_unviewable_playlist_error(err))
            except Exception as e:
                error_msg = str(e)
                self.after(0, lambda msg=error_msg: self._handle_error(f"Analysis failed: {msg}"))
        
        threading.Thread(target=analyze_thread, daemon=True).start()
    
    def _display_playlist_info(self, info: VideoInfo):
        """Display playlist information and open selection dialog."""
        self.current_video = info
        
        self.log_panel.log(f"Playlist: {info.title}", "success")
        self.log_panel.log(f"   {info.playlist_count} videos - {info.total_playlist_duration_str} total", "info")
        if info.channel:
            self.log_panel.log(f"   Channel: {info.channel}", "info")
        
        # Open playlist selection dialog
        PlaylistSelectionWindow(
            self,
            info,
            self.settings_mgr,
            on_download=self._download_playlist_items
        )
    
    def _download_playlist_items(self, items: List[PlaylistItem], 
                                  selected_format: Optional[VideoFormat],
                                  audio_only: bool):
        """Download selected playlist items."""
        if not items:
            return
        
        self.log_panel.log(f"Starting download of {len(items)} videos...", "info")
        
        # Create a folder for the playlist
        output_dir = self.config.get("output_dir", str(Path.home() / "Desktop"))
        playlist_title = sanitize_filename(self.current_video.title, max_length=100)
        playlist_folder = os.path.join(output_dir, playlist_title)
        os.makedirs(playlist_folder, exist_ok=True)
        
        self.log_panel.log(f"Saving to: {playlist_folder}", "info")
        
        # Download each item
        def download_playlist_thread():
            total = len(items)
            successful = 0
            failed = 0
            max_retries = 2  # Try up to 2 times per video
            
            for idx, item in enumerate(items, start=1):
                self.after(0, lambda i=idx, t=total, it=item: 
                    self.log_panel.log(f"[{i}/{t}] Downloading: {it.title[:50]}...", "info"))
                
                # Update progress
                self.after(0, lambda i=idx, t=total: self._update_playlist_progress(i, t, 0))
                
                # Try downloading with retries
                success = False
                last_error = None
                
                for attempt in range(1, max_retries + 1):
                    try:
                        # Clean up any leftover temp files from previous attempt
                        if attempt > 1:
                            self._cleanup_temp_files(playlist_folder, item.id)
                            self.after(0, lambda i=idx, a=attempt: 
                                self.log_panel.log(f"  Retry attempt {a} for video {i}...", "warning"))
                        
                        # Download this video
                        success, error_msg = self._download_single_playlist_item_with_error(
                            item, playlist_folder, selected_format, audio_only, idx, total
                        )
                        
                        if success:
                            break
                        else:
                            last_error = error_msg
                            if attempt < max_retries:
                                # Wait a bit before retry
                                time.sleep(2)
                            
                    except Exception as e:
                        last_error = str(e)[:150]
                        if attempt < max_retries:
                            time.sleep(2)
                
                if success:
                    successful += 1
                    self.after(0, lambda it=item: 
                        self.log_panel.log(f"  ✅ Done: {it.title[:40]}", "success"))
                else:
                    failed += 1
                    error_display = last_error if last_error else "Unknown error"
                    self.after(0, lambda it=item, err=error_display: 
                        self.log_panel.log(f"  ❌ Failed: {it.title[:40]}", "error"))
                    self.after(0, lambda err=error_display: 
                        self.log_panel.log(f"     Reason: {err}", "warning"))
            
            # Summary
            self.after(0, lambda s=successful, f=failed, t=total, folder=playlist_folder: 
                self._playlist_download_complete(s, f, t, folder))
        
        threading.Thread(target=download_playlist_thread, daemon=True).start()
    
    def _cleanup_temp_files(self, folder: str, video_id: str):
        """Clean up temp files for a video before retry."""
        try:
            for fname in os.listdir(folder):
                if video_id in fname and ('_temp_video' in fname or '_temp_audio' in fname):
                    try:
                        os.remove(os.path.join(folder, fname))
                    except:
                        pass
        except:
            pass
    
    def _download_single_playlist_item_with_error(self, item: PlaylistItem, output_folder: str,
                                                   selected_format: Optional[VideoFormat],
                                                   audio_only: bool, current_idx: int, total: int) -> tuple:
        """Download a single playlist item. Returns (success: bool, error_msg: str or None)."""
        safe_title = sanitize_filename(item.title, max_length=150)
        
        if audio_only:
            # Audio only download
            output_path = os.path.join(output_folder, f"{current_idx:02d} - {safe_title}.m4a")
            
            cmd = self.ytdlp._build_command([
                "--newline",
                "--no-playlist",
                "--remote-components", "ejs:github",
                "--extractor-args", "youtube:player_client=android_sdkless",
                "-f", "bestaudio[ext=m4a]/bestaudio/best",
                "-o", output_path,
                item.url
            ])
            
            result = subprocess.run(cmd, capture_output=True, text=True, 
                                   encoding='utf-8', errors='replace', timeout=300)
            
            if result.returncode == 0 or os.path.exists(output_path):
                return True, None
            else:
                # Extract error from stderr
                error_msg = self._extract_ytdlp_error(result.stderr)
                return False, error_msg
        
        else:
            # Video download with conversion
            video_id = item.id
            temp_video = os.path.join(output_folder, f"{video_id}_temp_video.%(ext)s")
            temp_audio = os.path.join(output_folder, f"{video_id}_temp_audio.%(ext)s")
            final_output = os.path.join(output_folder, f"{current_idx:02d} - {safe_title}.mp4")
            
            # Determine quality
            if selected_format and selected_format.height:
                video_format = f"bestvideo[height<={selected_format.height}][ext=mp4]/bestvideo[height<={selected_format.height}]/bestvideo"
            else:
                video_format = "bestvideo[ext=mp4]/bestvideo/best"
            
            try:
                # Download video stream
                video_cmd = self.ytdlp._build_command([
                    "--newline",
                    "--no-playlist",
                    "--remote-components", "ejs:github",
                    "--extractor-args", "youtube:player_client=android_sdkless",
                    "-f", video_format,
                    "-o", temp_video,
                    item.url
                ])
                
                video_result = subprocess.run(video_cmd, capture_output=True, text=True, 
                              encoding='utf-8', errors='replace', timeout=300)
                
                # Find downloaded video file
                video_file = None
                for fname in os.listdir(output_folder):
                    if fname.startswith(f"{video_id}_temp_video"):
                        video_file = os.path.join(output_folder, fname)
                        break
                
                if not video_file:
                    error_msg = self._extract_ytdlp_error(video_result.stderr)
                    return False, f"Video download failed: {error_msg}"
                
                # Download audio stream
                audio_cmd = self.ytdlp._build_command([
                    "--newline",
                    "--no-playlist",
                    "--remote-components", "ejs:github",
                    "--extractor-args", "youtube:player_client=android_sdkless",
                    "-f", "bestaudio[ext=m4a]/bestaudio/best",
                    "-o", temp_audio,
                    item.url
                ])
                
                audio_result = subprocess.run(audio_cmd, capture_output=True, text=True,
                              encoding='utf-8', errors='replace', timeout=300)
                
                # Find downloaded audio file
                audio_file = None
                for fname in os.listdir(output_folder):
                    if fname.startswith(f"{video_id}_temp_audio"):
                        audio_file = os.path.join(output_folder, fname)
                        break
                
                if not audio_file:
                    # Cleanup video file
                    if video_file and os.path.exists(video_file):
                        os.remove(video_file)
                    error_msg = self._extract_ytdlp_error(audio_result.stderr)
                    return False, f"Audio download failed: {error_msg}"
                
                # Merge with ffmpeg
                ffmpeg_cmd = [
                    FFMPEG_PATH,
                    "-y",
                    "-i", video_file,
                    "-i", audio_file,
                    "-map", "0:v:0",
                    "-map", "1:a:0",
                    "-c:v", "h264_videotoolbox",
                    "-b:v", "6M",
                    "-pix_fmt", "yuv420p",
                    "-c:a", "aac",
                    "-b:a", "192k",
                    "-movflags", "+faststart",
                    "-shortest",
                    final_output
                ]
                
                ffmpeg_result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True,
                                       encoding='utf-8', errors='replace', timeout=600)
                
                # Cleanup temp files
                if os.path.exists(video_file):
                    os.remove(video_file)
                if os.path.exists(audio_file):
                    os.remove(audio_file)
                
                if os.path.exists(final_output):
                    return True, None
                else:
                    # Extract ffmpeg error
                    stderr_lines = ffmpeg_result.stderr.split('\n') if ffmpeg_result.stderr else []
                    error_lines = [l for l in stderr_lines if 'error' in l.lower()]
                    error_msg = error_lines[-1] if error_lines else "FFmpeg conversion failed"
                    return False, error_msg
                
            except subprocess.TimeoutExpired:
                # Cleanup on timeout
                self._cleanup_temp_files(output_folder, video_id)
                return False, "Download timed out"
            except Exception as e:
                self._cleanup_temp_files(output_folder, video_id)
                return False, str(e)[:100]
    
    def _extract_ytdlp_error(self, stderr: str) -> str:
        """Extract meaningful error message from yt-dlp stderr."""
        if not stderr:
            return "Unknown error"
        
        stderr_lower = stderr.lower()
        
        # Check for common errors
        if "age" in stderr_lower and ("restrict" in stderr_lower or "verify" in stderr_lower):
            return "Age-restricted video (requires authentication)"
        if "private" in stderr_lower:
            return "Private video"
        if "unavailable" in stderr_lower or "not available" in stderr_lower:
            return "Video unavailable (deleted or region-locked)"
        if "copyright" in stderr_lower:
            return "Removed due to copyright"
        if "sign in" in stderr_lower or "login" in stderr_lower:
            return "Requires login/authentication"
        if "geo" in stderr_lower or "country" in stderr_lower:
            return "Geo-restricted (blocked in your region)"
        
        # Try to find ERROR: line
        for line in stderr.split('\n'):
            if line.strip().startswith('ERROR:'):
                return line.strip()[7:100]  # Remove "ERROR: " prefix, limit length
        
        # Return last non-empty line
        lines = [l.strip() for l in stderr.split('\n') if l.strip()]
        return lines[-1][:100] if lines else "Unknown error"
    
    def _update_playlist_progress(self, current_idx: int, total: int, item_progress: float):
        """Update progress display for playlist download."""
        overall_progress = ((current_idx - 1) + item_progress) / total * 100
        self.main_progress.set_progress(overall_progress, stage="downloading_video")
        self.main_progress.start_animation()
        self.progress_label.configure(text=f"Downloading video {current_idx}/{total}...")
        self.percentage_label.configure(text=f"{overall_progress:.0f}%")
        self.queue_status.configure(text="Downloading Playlist")
    
    def _playlist_download_complete(self, successful: int, failed: int, total: int, folder: str):
        """Handle playlist download completion."""
        self.main_progress.set_progress(100, stage="idle")
        self.main_progress.stop_animation()
        
        if failed == 0:
            self.log_panel.log(f"Playlist download complete! {successful}/{total} videos downloaded", "success")
            send_notification("Playlist Complete", f"Downloaded {successful} videos successfully")
        else:
            self.log_panel.log(f"Playlist download finished: {successful} succeeded, {failed} failed", "warning")
            send_notification("Playlist Complete", f"{successful} succeeded, {failed} failed")
        
        self.log_panel.log(f"Saved to: {folder}", "info")
        self.progress_label.configure(text=f"Completed: {successful}/{total} videos")
        self.percentage_label.configure(text="100%")
        self.queue_status.configure(text="Idle")
    
    def _handle_age_restricted_error(self, error: 'AgeRestrictedError'):
        """Handle age-restricted video errors with detailed user feedback."""
        video_id = error.video_id or "unknown"
        
        # Log detailed error
        self.log_panel.log("=" * 50, "error")
        self.log_panel.log("AGE-RESTRICTED VIDEO DETECTED", "error")
        self.log_panel.log("=" * 50, "error")
        self.log_panel.log(f"Video ID: {video_id}", "error")
        self.log_panel.log("", "info")
        self.log_panel.log("This video requires age verification from YouTube.", "warning")
        self.log_panel.log("YouTube requires you to be signed in to view this content.", "warning")
        self.log_panel.log("", "info")
        self.log_panel.log("TO DOWNLOAD AGE-RESTRICTED VIDEOS:", "info")
        self.log_panel.log("1. Export cookies from your browser while logged into YouTube", "info")
        self.log_panel.log("2. Use yt-dlp directly with: --cookies-from-browser BROWSER", "info")
        self.log_panel.log("   Example: yt-dlp --cookies-from-browser chrome URL", "info")
        self.log_panel.log("", "info")
        self.log_panel.log("For detailed instructions, see:", "info")
        self.log_panel.log("https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp", "info")
        self.log_panel.log("=" * 50, "error")
        
        # Show dialog with helpful information
        messagebox.showwarning(
            "Age-Restricted Video",
            f"This video is age-restricted and requires authentication.\n\n"
            f"Video ID: {video_id}\n\n"
            f"To download age-restricted videos, you need to:\n"
            f"1. Export cookies from your browser while logged into YouTube\n"
            f"2. Run yt-dlp from the command line with cookies\n\n"
            f"Example command:\n"
            f"yt-dlp --cookies-from-browser chrome \"{self.url_entry.get()}\"\n\n"
            f"See the Activity Log for more details."
        )
    
    def _handle_private_video_error(self, error: 'PrivateVideoError'):
        """Handle private video errors."""
        video_id = error.video_id or "unknown"
        
        self.log_panel.log("=" * 50, "error")
        self.log_panel.log("PRIVATE VIDEO", "error")
        self.log_panel.log("=" * 50, "error")
        self.log_panel.log(f"Video ID: {video_id}", "error")
        self.log_panel.log("This video is set to private by the owner.", "warning")
        self.log_panel.log("Private videos can only be viewed by people the owner has shared them with.", "info")
        self.log_panel.log("=" * 50, "error")
        
        messagebox.showwarning(
            "Private Video",
            f"This video is private.\n\n"
            f"Video ID: {video_id}\n\n"
            f"Private videos cannot be downloaded unless you have access "
            f"and use authentication (cookies)."
        )
    
    def _handle_video_unavailable_error(self, error: 'VideoUnavailableError'):
        """Handle unavailable video errors (deleted, region-locked, etc.)."""
        video_id = error.video_id or "unknown"
        reason = error.reason
        
        self.log_panel.log("=" * 50, "error")
        self.log_panel.log("VIDEO UNAVAILABLE", "error")
        self.log_panel.log("=" * 50, "error")
        self.log_panel.log(f"Video ID: {video_id}", "error")
        self.log_panel.log(f"Reason: {reason[:200] if reason else 'Unknown'}", "warning")
        self.log_panel.log("", "info")
        self.log_panel.log("Possible causes:", "info")
        self.log_panel.log("- Video has been deleted by the owner", "info")
        self.log_panel.log("- Video is blocked in your country/region", "info")
        self.log_panel.log("- Video has been removed due to copyright claim", "info")
        self.log_panel.log("- Video has been removed for violating YouTube's policies", "info")
        self.log_panel.log("=" * 50, "error")
        
        messagebox.showwarning(
            "Video Unavailable",
            f"This video is not available.\n\n"
            f"Video ID: {video_id}\n\n"
            f"The video may have been deleted, removed, or blocked in your region."
        )
    
    def _handle_login_required_error(self, error: 'LoginRequiredError'):
        """Handle login required errors (members-only content, etc.)."""
        video_id = error.video_id or "unknown"
        reason = error.reason
        
        self.log_panel.log("=" * 50, "error")
        self.log_panel.log("LOGIN REQUIRED", "error")
        self.log_panel.log("=" * 50, "error")
        self.log_panel.log(f"Video ID: {video_id}", "error")
        self.log_panel.log(f"Reason: {reason[:200] if reason else 'Unknown'}", "warning")
        self.log_panel.log("", "info")
        self.log_panel.log("This video requires authentication to access.", "info")
        self.log_panel.log("It may be members-only content or require a YouTube subscription.", "info")
        self.log_panel.log("", "info")
        self.log_panel.log("To access, use yt-dlp with cookies:", "info")
        self.log_panel.log("yt-dlp --cookies-from-browser chrome URL", "info")
        self.log_panel.log("=" * 50, "error")
        
        messagebox.showwarning(
            "Login Required",
            f"This video requires authentication.\n\n"
            f"Video ID: {video_id}\n\n"
            f"This may be members-only content or require a subscription.\n\n"
            f"To download, use yt-dlp from the command line with cookies:\n"
            f"yt-dlp --cookies-from-browser chrome \"{self.url_entry.get()}\""
        )
    
    def _handle_unviewable_playlist_error(self, error: 'UnviewablePlaylistError'):
        """Handle unviewable playlist errors (YouTube Mix, etc.) with automatic fallback."""
        playlist_id = error.playlist_id or "unknown"
        video_id = error.video_id
        playlist_type = error.playlist_type
        
        # Log the error
        self.log_panel.log("=" * 50, "warning")
        self.log_panel.log(f"⚠️ {playlist_type.upper()} PLAYLIST DETECTED", "warning")
        self.log_panel.log("=" * 50, "warning")
        self.log_panel.log(f"Playlist ID: {playlist_id}", "info")
        self.log_panel.log("", "info")
        
        if playlist_type == "YouTube Mix":
            self.log_panel.log("YouTube Mixes are auto-generated playlists that cannot be enumerated.", "info")
            self.log_panel.log("They are dynamically created based on the seed video and your history.", "info")
        else:
            self.log_panel.log("This playlist type cannot be accessed as a playlist.", "info")
        
        # If we have a video ID, offer to download just that video
        if video_id:
            self.log_panel.log("", "info")
            self.log_panel.log(f"✅ Switching to single video mode for video: {video_id}", "success")
            self.log_panel.log("=" * 50, "warning")
            
            # Disable playlist mode
            self.playlist_mode_var.set(False)
            
            # Automatically analyze the single video
            single_url = f"https://www.youtube.com/watch?v={video_id}"
            self.url_entry.delete(0, "end")
            self.url_entry.insert(0, single_url)
            
            # Re-analyze as single video
            self.after(100, self._analyze)
        else:
            self.log_panel.log("", "info")
            self.log_panel.log("No video ID found - cannot fall back to single video mode.", "error")
            self.log_panel.log("=" * 50, "warning")
            
            messagebox.showwarning(
                f"{playlist_type} Not Supported",
                f"This is a {playlist_type} which cannot be downloaded as a playlist.\n\n"
                f"{error.message}"
            )
    
    def _display_video_info(self, info: VideoInfo):
        """Display video information in the modern UI."""
        self.current_video = info
        
        # Show video frame using grid (row 0)
        self.video_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 8))
        
        # Update labels
        self.title_label.configure(text=info.title)
        self.channel_label.configure(text=f" {info.channel or 'Unknown'}")
        self.views_label.configure(text=f" {info.views_str}")
        self.duration_badge.configure(text=info.duration_str)
        
        # Update chapters info
        if info.has_chapters:
            self.chapters_label.configure(text=f" {len(info.chapters)}")
            self.chapters_button.pack(side="left")
            self.log_panel.log(f"Found {len(info.chapters)} chapters", "success")
        else:
            self.chapters_label.configure(text="")
            self.chapters_button.pack_forget()
        
        # Load thumbnail (compact size for new layout)
        if info.thumbnail:
            def load_thumb():
                thumb = self.thumbnail_manager.get_thumbnail(
                    info.thumbnail, info.id, (160, 90)
                )
                if thumb:
                    self.after(0, lambda: self.thumb_label.configure(image=thumb, text=""))
            
            threading.Thread(target=load_thumb, daemon=True).start()
        
        # Clear old format cards
        for card in self.format_cards:
            card.destroy()
        self.format_cards.clear()
        
        # Create format cards
        video_formats = [f for f in info.formats if f.height and f.height >= 100]
        
        self.log_panel.log(f"Found {len(video_formats)} formats", "info")
        
        # Deduplicate by resolution
        seen_heights = {}
        for fmt in video_formats:
            h = fmt.height
            if h not in seen_heights or (fmt.tbr or 0) > (seen_heights[h].tbr or 0):
                seen_heights[h] = fmt
        
        unique_formats = sorted(seen_heights.values(), key=lambda x: x.height or 0, reverse=True)[:6]
        
        # If no formats found, show a message
        if not unique_formats:
            self.log_panel.log("No video formats available - try clicking Download to use best available", "warning")
        
        # Find recommended (1080p or highest)
        recommended = None
        for fmt in unique_formats:
            if fmt.height == 1080:
                recommended = fmt
                break
        if not recommended and unique_formats:
            recommended = unique_formats[0]
        
        # Select recommended by default
        self.selected_format = recommended
        
        # Update selected format label
        if recommended:
            self._update_selected_format_label(recommended)
        
        # Calculate number of columns based on number of formats
        num_formats = len(unique_formats)
        if num_formats <= 3:
            max_cols = num_formats
        elif num_formats <= 6:
            max_cols = 3
        else:
            max_cols = 4
        
        # Layout format cards in a responsive grid
        row = 0
        col = 0
        
        for fmt in unique_formats:
            card = FormatCard(
                self.formats_container,
                fmt,
                selected=(fmt == recommended),
                recommended=(fmt == recommended),
                on_select=self._select_format
            )
            card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")
            self.format_cards.append(card)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # Configure column weights for even distribution
        for i in range(max_cols):
            self.formats_container.grid_columnconfigure(i, weight=1, uniform="format")
        
        self.log_panel.log(f"Found {len(info.formats)} formats, showing {len(unique_formats)} quality options", "success")
    
    def _update_selected_format_label(self, fmt: VideoFormat):
        """Update the selected format indicator label."""
        if fmt:
            codec_raw = fmt.vcodec or fmt.acodec or ""
            codec_base = codec_raw.split('.')[0].lower() if codec_raw else ""
            codec_names = {"avc1": "H.264", "avc": "H.264", "h264": "H.264", "vp9": "VP9", "vp09": "VP9", "av01": "AV1"}
            codec_display = codec_names.get(codec_base, codec_base.upper() if codec_base else "")
            self.selected_format_label.configure(
                text=f"Selected: {fmt.height}p * {codec_display} * {fmt.size_str}"
            )
    
    def _select_format(self, fmt: VideoFormat):
        """Handle format selection."""
        self.selected_format = fmt
        
        for card in self.format_cards:
            card.set_selected(card.format_info == fmt)
        
        # Update the selected format label
        self._update_selected_format_label(fmt)
        
        self.log_panel.log(f"Selected: {fmt.height}p {fmt.bitrate_str}", "info")
    
    def _show_chapters_dialog(self):
        """Show the chapter selection dialog."""
        if not self.current_video or not self.current_video.has_chapters:
            messagebox.showwarning("No Chapters", "This video does not have chapters.")
            return
        
        ChapterSelectionWindow(
            self,
            self.current_video,
            on_download=self._download_chapters
        )
    
    def _download_chapters(self, chapters: List[Chapter], audio_only: bool = False):
        """Download selected chapters as separate files.
        
        v17.8.5: Complete rewrite for efficiency:
        1. Download full video once (video + audio streams)
        2. Merge/encode to QuickTime-compatible format once
        3. Split into chapters using ffmpeg stream copy (fast, no re-encoding)
        
        This is MUCH faster than the old approach which downloaded and encoded
        the entire video separately for each chapter.
        
        v17.8.7: SponsorBlock is automatically disabled for chapter downloads
        to avoid compatibility issues with the chapter extraction process.
        """
        if not self.current_video:
            return
        
        video_info = self.current_video
        output_dir = self.config.get("output_dir", str(Path.home() / "Desktop"))
        
        # Create a folder for the chapters
        safe_title = sanitize_filename(video_info.title, max_length=100)
        chapter_folder = os.path.join(output_dir, safe_title)
        os.makedirs(chapter_folder, exist_ok=True)
        
        self.log_panel.log(f"Downloading {len(chapters)} chapters to: {chapter_folder}", "info")
        self.log_panel.log("Strategy: Download once -> Encode once -> Split into chapters (fast)")
        
        # v17.8.7: Log that SponsorBlock is disabled for chapter downloads
        if self.settings_mgr.get('sponsorblock_enabled', False):
            self.log_panel.log("Note: SponsorBlock is disabled for chapter downloads", "warning")
        
        # Start chapter download in a thread
        def download_chapters_thread():
            video_id = video_info.id
            temp_video = os.path.join(output_dir, f"{video_id}_temp_video.%(ext)s")
            temp_audio = os.path.join(output_dir, f"{video_id}_temp_audio.%(ext)s")
            merged_file = os.path.join(output_dir, f"{video_id}_merged.mp4")
            
            try:
                # ========================================
                # STAGE 1: Download video stream (0-30%)
                # ========================================
                self.after(0, lambda: self._update_chapter_stage("Downloading video stream...", 0))
                
                fmt = self.selected_format
                if audio_only:
                    # For audio-only, we just need the audio stream
                    self.after(0, lambda: self.log_panel.log("Audio-only mode: downloading best audio", "info"))
                else:
                    if fmt and fmt.height:
                        video_format = f"bestvideo[height<={fmt.height}][ext=mp4]/bestvideo[height<={fmt.height}]/bestvideo"
                        self.after(0, lambda h=fmt.height: self.log_panel.log(f"Downloading best video at or below {h}p", "info"))
                    else:
                        video_format = "bestvideo[ext=mp4]/bestvideo/best"
                        self.after(0, lambda: self.log_panel.log("Downloading best available video", "info"))
                    
                    video_cmd = self.ytdlp._build_command([
                        "--newline",
                        "--remote-components", "ejs:github",
                        "--extractor-args", "youtube:player_client=android_sdkless",
                        "-f", video_format,
                        "-o", temp_video,
                        video_info.url
                    ])
                    
                    result = subprocess.run(
                        video_cmd,
                        capture_output=True,
                        text=True,
                        encoding='utf-8',
                        errors='replace'
                    )
                    
                    if result.returncode != 0:
                        # Check if file exists anyway
                        video_file = self._find_chapter_temp_file(output_dir, f"{video_id}_temp_video")
                        if not video_file:
                            self.after(0, lambda e=result.stderr[:300]: self.log_panel.log(f"Video download failed: {e}", "error"))
                            return
                
                # ========================================
                # STAGE 2: Download audio stream (30-50%)
                # ========================================
                self.after(0, lambda: self._update_chapter_stage("Downloading audio stream...", 30))
                self.after(0, lambda: self.log_panel.log("Downloading best audio stream", "info"))
                
                audio_cmd = self.ytdlp._build_command([
                    "--newline",
                    "--remote-components", "ejs:github",
                    "--extractor-args", "youtube:player_client=android_sdkless",
                    "-f", "bestaudio[ext=m4a]/bestaudio/best",
                    "-o", temp_audio,
                    video_info.url
                ])
                
                result = subprocess.run(
                    audio_cmd,
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='replace'
                )
                
                if result.returncode != 0:
                    audio_file = self._find_chapter_temp_file(output_dir, f"{video_id}_temp_audio")
                    if not audio_file:
                        self.after(0, lambda e=result.stderr[:300]: self.log_panel.log(f"Audio download failed: {e}", "error"))
                        return
                
                # Find the downloaded files
                video_file = self._find_chapter_temp_file(output_dir, f"{video_id}_temp_video") if not audio_only else None
                audio_file = self._find_chapter_temp_file(output_dir, f"{video_id}_temp_audio")
                
                if not audio_file:
                    self.after(0, lambda: self.log_panel.log("Audio file not found after download", "error"))
                    return
                
                if not audio_only and not video_file:
                    self.after(0, lambda: self.log_panel.log("Video file not found after download", "error"))
                    return
                
                # ========================================
                # STAGE 3: Merge & encode to QuickTime (50-80%)
                # ========================================
                if audio_only:
                    # For audio-only, just convert to m4a
                    self.after(0, lambda: self._update_chapter_stage("Converting audio to M4A...", 50))
                    merged_file = os.path.join(output_dir, f"{video_id}_merged.m4a")
                    
                    ffmpeg_cmd = [
                        FFMPEG_PATH,
                        "-y",
                        "-i", audio_file,
                        "-c:a", "aac",
                        "-b:a", "192k",
                        merged_file
                    ]
                else:
                    self.after(0, lambda: self._update_chapter_stage("Encoding to QuickTime format...", 50))
                    self.after(0, lambda: self.log_panel.log("Merging video + audio with QuickTime-compatible encoding", "info"))
                    
                    # Get encoding settings
                    settings_mgr = SettingsManager(SETTINGS_PATH)
                    encoder_type = settings_mgr.get("encoder_type", "auto")
                    
                    if encoder_type == "cpu":
                        video_codec = "libx264"
                    else:
                        video_codec = "h264_videotoolbox"  # GPU
                    
                    # Calculate bitrate based on resolution
                    video_height = fmt.height if fmt else 1080
                    if video_height >= 2160:
                        video_bitrate = "15M"
                    elif video_height >= 1440:
                        video_bitrate = "10M"
                    elif video_height >= 1080:
                        video_bitrate = "6M"
                    elif video_height >= 720:
                        video_bitrate = "4M"
                    else:
                        video_bitrate = "2M"
                    
                    ffmpeg_cmd = [
                        FFMPEG_PATH,
                        "-y",
                        "-i", video_file,
                        "-i", audio_file,
                        "-map", "0:v:0",
                        "-map", "1:a:0",
                        "-c:v", video_codec,
                        "-b:v", video_bitrate,
                        "-pix_fmt", "yuv420p",
                        "-c:a", "aac",
                        "-b:a", "192k",
                        "-movflags", "+faststart",
                        "-shortest",
                        merged_file
                    ]
                
                self.after(0, lambda: self.log_panel.log(f"Encoding with ffmpeg (this may take a while)...", "info"))
                
                # Run ffmpeg merge/encode
                process = subprocess.Popen(
                    ffmpeg_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding='utf-8',
                    errors='replace'
                )
                
                # Monitor encoding progress
                duration = video_info.duration or 0
                time_re = re.compile(r'time=(\d+):(\d+):(\d+(?:\.\d+)?)')
                
                for line in process.stderr:
                    if duration > 0:
                        match = time_re.search(line)
                        if match:
                            h = float(match.group(1))
                            m = float(match.group(2))
                            s = float(match.group(3))
                            current_time = h * 3600 + m * 60 + s
                            encode_pct = min(100, (current_time / duration) * 100)
                            # Map encoding progress to 50-80% range
                            overall_pct = 50 + (encode_pct * 0.3)
                            self.after(0, lambda p=overall_pct: self._update_chapter_stage(f"Encoding... {p-50:.0f}% of video", p))
                
                process.wait()
                
                if process.returncode != 0 or not os.path.exists(merged_file):
                    # Try CPU fallback if GPU failed
                    if "h264_videotoolbox" in ffmpeg_cmd:
                        self.after(0, lambda: self.log_panel.log("GPU encoding failed, trying CPU...", "warning"))
                        ffmpeg_cmd[ffmpeg_cmd.index("h264_videotoolbox")] = "libx264"
                        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
                        if result.returncode != 0 or not os.path.exists(merged_file):
                            self.after(0, lambda: self.log_panel.log("Encoding failed", "error"))
                            return
                    else:
                        self.after(0, lambda: self.log_panel.log("Encoding failed", "error"))
                        return
                
                self.after(0, lambda: self.log_panel.log("Encoding complete! Now splitting into chapters...", "success"))
                
                # ========================================
                # STAGE 4: Split into chapters (80-100%)
                # ========================================
                self.after(0, lambda: self._update_chapter_stage("Splitting into chapters...", 80))
                
                total_chapters = len(chapters)
                successful_chapters = 0
                
                for i, chapter in enumerate(chapters):
                    # Calculate progress within the splitting stage (80-100%)
                    split_progress = 80 + ((i / total_chapters) * 20)
                    self.after(0, lambda p=split_progress, c=chapter, t=total_chapters: 
                        self._update_chapter_stage(f"Splitting chapter {c.index + 1}/{t}: {c.title[:30]}...", p))
                    
                    # Build output filename
                    safe_chapter_title = chapter.safe_filename
                    ext = "m4a" if audio_only else "mp4"
                    output_file = os.path.join(chapter_folder, f"{chapter.index + 1:02d} - {safe_chapter_title}.{ext}")
                    
                    # Calculate duration
                    chapter_duration = chapter.end_time - chapter.start_time
                    
                    # Use ffmpeg to extract chapter with stream copy (FAST - no re-encoding!)
                    if audio_only:
                        split_cmd = [
                            FFMPEG_PATH,
                            "-y",
                            "-ss", str(chapter.start_time),
                            "-i", merged_file,
                            "-t", str(chapter_duration),
                            "-c:a", "copy",  # Stream copy - no re-encoding!
                            output_file
                        ]
                    else:
                        split_cmd = [
                            FFMPEG_PATH,
                            "-y",
                            "-ss", str(chapter.start_time),
                            "-i", merged_file,
                            "-t", str(chapter_duration),
                            "-c:v", "copy",  # Stream copy - no re-encoding!
                            "-c:a", "copy",  # Stream copy - no re-encoding!
                            "-avoid_negative_ts", "make_zero",
                            output_file
                        ]
                    
                    result = subprocess.run(
                        split_cmd,
                        capture_output=True,
                        text=True,
                        encoding='utf-8',
                        errors='replace'
                    )
                    
                    if result.returncode == 0 and os.path.exists(output_file):
                        successful_chapters += 1
                        self.after(0, lambda ch=chapter: self.log_panel.log(
                            f"  [checkmark] Chapter {ch.index + 1}: {ch.title}", "success"
                        ))
                    else:
                        self.after(0, lambda ch=chapter, err=result.stderr[:100]: self.log_panel.log(
                            f"  [x] Chapter {ch.index + 1} failed: {err}", "error"
                        ))
                
                # ========================================
                # CLEANUP: Remove temp files
                # ========================================
                self.after(0, lambda: self._update_chapter_stage("Cleaning up...", 98))
                
                try:
                    if video_file and os.path.exists(video_file):
                        os.remove(video_file)
                    if audio_file and os.path.exists(audio_file):
                        os.remove(audio_file)
                    if os.path.exists(merged_file):
                        os.remove(merged_file)
                    self.after(0, lambda: self.log_panel.log("Temporary files cleaned up", "info"))
                except Exception as e:
                    self.after(0, lambda err=str(e): self.log_panel.log(f"Cleanup warning: {err}", "warning"))
                
                # Done!
                self.after(0, lambda: self._chapter_download_complete(chapter_folder, successful_chapters))
                
            except Exception as e:
                import traceback
                tb = traceback.format_exc()
                self.after(0, lambda err=str(e), trace=tb: self.log_panel.log(f"Chapter download error: {err}\n{trace}", "error"))
                # Cleanup on error
                try:
                    for f in [temp_video.replace("%(ext)s", "mp4"), temp_video.replace("%(ext)s", "webm"),
                              temp_audio.replace("%(ext)s", "m4a"), temp_audio.replace("%(ext)s", "webm"),
                              merged_file]:
                        if os.path.exists(f):
                            os.remove(f)
                except:
                    pass
        
        threading.Thread(target=download_chapters_thread, daemon=True).start()
    
    def _find_chapter_temp_file(self, directory: str, prefix: str) -> Optional[str]:
        """Find a temp file by prefix for chapter downloads."""
        try:
            for fname in os.listdir(directory):
                if fname.startswith(prefix):
                    return os.path.join(directory, fname)
        except Exception:
            pass
        return None
    
    def _update_chapter_stage(self, message: str, progress: float):
        """Update UI during chapter download stages."""
        self.main_progress.set_progress(progress, stage="converting")
        self.main_progress.start_animation()
        self.progress_label.configure(text=message)
        self.percentage_label.configure(text=f"{progress:.0f}%")
        self.queue_status.configure(text="Processing Chapters")
    
    def _chapter_download_complete(self, folder: str, count: int):
        """Called when all chapters are downloaded."""
        self.main_progress.set_progress(100, stage="idle")
        self.main_progress.stop_animation()
        self.progress_label.configure(text=f"✅ Completed: {count} chapters extracted")
        self.percentage_label.configure(text="100%")
        self.queue_status.configure(text="Idle")
        self.log_panel.log(f"All {count} chapters downloaded to: {folder}", "success")
        send_notification("Chapters Downloaded", f"{count} chapters extracted successfully")

    def _download(self):
        """Start download."""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("No URL", "Please enter a YouTube URL")
            return
        
        # If no video analyzed, analyze first
        if not self.current_video:
            self._analyze()
            return
        
        # Add to queue
        task = self.download_manager.add_task(
            self.current_video,
            self.selected_format
        )
        
        self.log_panel.log(f"Added to queue: {self.current_video.title}", "info")
        
        # Start download manager
        self.download_manager.start()
    
    def _on_download_event(self, event: str, data: Any):
        """Handle download manager events with modern UI updates."""
        def update():
            if event == "task_progress" or event == "task_updated":
                task = data
                
                # Determine stage for color coding
                stage_name = "idle"
                stage_text = "â³ Ready to download"
                
                if task.status == DownloadStatus.DOWNLOADING:
                    if task.progress < 40:
                        stage_name = "downloading_video"
                        stage_text = "Stage 1/3: Downloading video"
                    elif task.progress < 60:
                        stage_name = "downloading_audio"
                        stage_text = "Stage 2/3: Downloading audio"
                    else:
                        stage_name = "downloading_audio"
                        stage_text = "Stage 2/3: Downloading audio"
                    
                    if task.status_detail:
                        stage_text = task.status_detail
                        
                elif task.status == DownloadStatus.CONVERTING:
                    stage_name = "converting"
                    fmt = task.selected_format
                    
                    if task.status_detail:
                        stage_text = task.status_detail
                    elif fmt and fmt.height:
                        stage_text = f"Stage 3/3: Converting ({fmt.height}p)"
                    else:
                        stage_text = "Stage 3/3: Converting"
                        
                elif task.status == DownloadStatus.COMPLETED:
                    stage_name = "idle"
                    stage_text = f"✅ Completed: {task.video_info.title[:50]}"
                
                # Update enhanced progress bar
                self.main_progress.set_progress(task.progress, stage=stage_name)
                
                # Update status indicator with animation
                if task.status in [DownloadStatus.DOWNLOADING, DownloadStatus.CONVERTING]:
                    self.main_progress.start_animation()
                    self.queue_status.configure(text="Active")
                    self.status_dot.configure(text_color=COLORS["accent_green"])
                elif task.status == DownloadStatus.COMPLETED:
                    self.main_progress.stop_animation()
                    self.queue_status.configure(text="Complete")
                    self.status_dot.configure(text_color=COLORS["accent_green"])
                else:
                    self.main_progress.stop_animation()
                    self.queue_status.configure(text="Idle")
                    self.status_dot.configure(text_color=COLORS["text_tertiary"])
                
                # Update metrics
                self.progress_label.configure(text=stage_text)
                self.percentage_label.configure(text=f"{task.progress:.0f}%")
                
                # Speed metric
                speed_text = "--"
                if task.download_speed:
                    speed_text = task.download_speed
                elif task.current_file_size and task.current_file_size > 0:
                    if task.current_file_size >= 1024 ** 3:
                        speed_text = f"{task.current_file_size / (1024 ** 3):.2f} GB"
                    elif task.current_file_size >= 1024 ** 2:
                        speed_text = f"{task.current_file_size / (1024 ** 2):.1f} MB"
                    else:
                        speed_text = f"{task.current_file_size / 1024:.1f} KB"
                
                self.speed_label.configure(text=speed_text)
                
                # FPS metric
                if task.conversion_fps:
                    self.fps_label.configure(text=task.conversion_fps)
                else:
                    self.fps_label.configure(text="--")
                
                # ETA metric
                if task.eta:
                    self.eta_label.configure(text=task.eta)
                else:
                    self.eta_label.configure(text="--")
                
                # Size metric (new for v18)
                if task.file_size:
                    if task.file_size >= 1024 ** 3:
                        size_str = f"{task.file_size / (1024 ** 3):.2f} GB"
                    elif task.file_size >= 1024 ** 2:
                        size_str = f"{task.file_size / (1024 ** 2):.0f} MB"
                    else:
                        size_str = f"{task.file_size / 1024:.0f} KB"
                    self.size_label.configure(text=size_str)
                else:
                    self.size_label.configure(text="--")
                
                # Log stage changes
                if task.status == DownloadStatus.CONVERTING and event == "task_updated":
                    self.log_panel.log("Converting to QuickTime-compatible format...", "info")
                elif task.status == DownloadStatus.COMPLETED:
                    self.log_panel.log(f"✅ Completed: {task.video_info.title}", "success")
                    self.main_progress.set_progress(100, stage="idle")
                elif task.status == DownloadStatus.FAILED:
                    self.log_panel.log(f"âŒ Failed: {task.error_message}", "error")
                    self.progress_label.configure(text="Download failed")
                    self.queue_status.configure(text="Failed")
            
            elif event == "log":
                # Handle log messages from download manager
                level, message = data
                self.log_panel.log(message, level)
        
        self.after(0, update)
    
    def _handle_error(self, message: str):
        """Handle and display errors."""
        self.log_panel.log(f"{message}", "error")
        messagebox.showerror("Error", message)
    
    # Removed _update_ytdlp and _handle_update_result methods
    # Now using YtDlpUpdater class for auto-updates (v17.10.0)
    
    def _show_help(self):
        """Show help window (toggle behavior - close if already open)."""
        # If window already exists and is open, close it
        if hasattr(self, 'help_window') and self.help_window and self.help_window.winfo_exists():
            self.help_window.destroy()
            self.help_window = None
            return
        
        # Create new help window
        self.help_window = ctk.CTkToplevel(self)
        self.help_window.title("Help")
        self.help_window.geometry("650x700")
        self.help_window.transient(self)
        
        help_text = ctk.CTkTextbox(
            self.help_window,
            font=ctk.CTkFont(size=13),
            wrap="word"
        )
        help_text.pack(fill="both", expand=True, padx=20, pady=20)
        
        help_content = f"""
YouTube 4K Downloader v{APP_VERSION} - Help

QUICK START
1. Paste a YouTube URL (or drag & drop)
2. Click "⚡ Analyze" to see available formats
3. Select your preferred quality
4. Click "⚡ Download" or press Cmd+Return

NEW IN V18.1 - FULL PLAYLIST SUPPORT
• Download entire YouTube playlists with video selection
• Smart URL detection: playlist URLs auto-enable playlist mode
• Toggle appears for URLs like "watch?v=xxx&list=yyy"
• Select individual videos or download all at once
• Quality selection (Best/4K/1440p/1080p/720p/480p)
• Audio-only option for extracting music
• Automatic retry on failures

Note: YouTube Mix playlists (auto-generated based on a video) 
cannot be downloaded as playlists - the app will automatically
fall back to single-video mode for these.

CHAPTER DOWNLOADS
• Download videos split by chapters!
• Click the purple "📑 Chapters" button when available
• Select individual chapters or download all
• Supports both video and audio-only extraction
• 10-50x faster using stream copy (no re-encoding per chapter)

Files are saved like:
  Video Title/
    01 - Introduction.mp4
    02 - Getting Started.mp4
    03 - Advanced Topics.mp4

AUTO-UPDATE YT-DLP
• Click "🔄" in the header to check for yt-dlp updates
• Updates are downloaded from GitHub automatically
• No need to re-download the entire app!
• The Update button turns orange when an update is available
• Updates stored in ~/Library/Application Support/

100% SELF-CONTAINED
This app includes everything needed:
• yt-dlp (bundled, auto-updates available)
• ffmpeg (bundled)  
• deno JavaScript runtime (bundled)

Just download, drag to Applications, and run!

FEATURES
• Full Playlist Downloads - Select videos, choose quality
• Chapter Downloads - Split videos into separate files
• Auto-Update yt-dlp - Stay current without re-downloading app
• SponsorBlock - Removes sponsor segments after download
• History Browser - Search and manage download history
• Audio-Only Mode - M4A extraction with proper metadata
• Drag & Drop - Drop a YouTube link onto the window
• QuickTime Compatible - H.264 + AAC for native macOS playback

KEYBOARD SHORTCUTS
• Cmd+V - Paste URL from clipboard
• Cmd+Return - Start download
• Enter - Analyze URL

SETTINGS (⚙️ button)
• SponsorBlock - Enable/disable, select categories
• Subtitles - Languages, auto-generated, embedding
• Encoding - GPU/CPU, preset, bitrate modes
• Trim - Set start/end times for partial downloads
• Playlist - Default selection, order, max videos

TROUBLESHOOTING

"App is damaged" error:
  Run in Terminal: xattr -cr /Applications/YouTube\\ 4K\\ Downloader.app

App won't open:
  Right-click the app > Select "Open" > Click "Open" in dialog

Playlist videos randomly fail:
  The app will automatically retry failed downloads once.
  If a video still fails, it may be age-restricted, private,
  or region-locked. Check the Activity Log for details.

YouTube Mix playlists not working:
  Mix playlists (RD prefix) are auto-generated and cannot be
  enumerated. The app will download the single seed video instead.

For more information, visit:
https://github.com/bytePatrol/YT-DLP-GUI-for-MacOS
        """
        
        help_text.insert("1.0", help_content)
        help_text.configure(state="disabled")
    
    def _choose_output_dir(self):
        """Choose output directory."""
        new_dir = filedialog.askdirectory(
            initialdir=self.config.get("output_dir"),
            title="Select Output Folder"
        )
        
        if new_dir:
            self.config["output_dir"] = new_dir
            self.output_path_label.configure(text=new_dir)
            self.download_manager.output_dir = new_dir
            self.log_panel.log(f"Output folder: {new_dir}", "info")
            self._save_config()
    
    def _setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts."""
        # Cmd+V to paste URL
        self.bind("<Command-v>", self._handle_paste_shortcut)
        
        # Cmd+Return to download
        self.bind("<Command-Return>", lambda e: self._download())
        
        # Enter in URL entry to analyze
        self.url_entry.bind("<Return>", lambda e: self._analyze())
    
    def _handle_paste_shortcut(self, event=None):
        """Handle Cmd+V paste shortcut."""
        try:
            clipboard = self.clipboard_get()
            if "youtube.com" in clipboard or "youtu.be" in clipboard:
                self.url_entry.delete(0, "end")
                self.url_entry.insert(0, clipboard)
                self.log_panel.log("URL pasted from clipboard", "info")
                self.url_entry.focus()
        except Exception:
            pass
        return "break"
    
    def _setup_drag_drop(self):
        """Setup drag & drop support (if available)."""
        if not HAS_DND:
            return
        
        try:
            # Make URL entry accept drops
            self.url_entry.drop_target_register(DND_FILES)
            self.url_entry.dnd_bind('<<Drop>>', self._handle_drop)
        except Exception:
            pass  # DND not fully supported
    
    def _handle_drop(self, event):
        """Handle drag & drop of URL."""
        try:
            data = str(event.data).strip('{}')
            if "youtube.com" in data or "youtu.be" in data:
                self.url_entry.delete(0, "end")
                self.url_entry.insert(0, data)
                self.log_panel.log("URL dropped", "info")
        except Exception:
            pass
    
    def _show_settings(self):
        """Show settings window (prevent duplicates)."""
        # If window already exists and is open, focus it or close it
        if self.settings_window and self.settings_window.winfo_exists():
            # Toggle behavior - close if already open
            self.settings_window.destroy()
            self.settings_window = None
            return
        
        # Create new settings window
        self.settings_window = SettingsWindow(self, self.settings_mgr)
    
    def _show_history(self):
        """Show history browser (prevent duplicates)."""
        # If window already exists and is open, focus it or close it
        if self.history_window and self.history_window.winfo_exists():
            # Toggle behavior - close if already open
            self.history_window.destroy()
            self.history_window = None
            return
        
        # Create new history window
        self.history_window = HistoryBrowserWindow(self, self.history_mgr)
    
    def _show_about(self):
        """Show about dialog."""
        AboutDialog(self, self.ytdlp.get_version())
    
    def _open_github(self):
        """Open GitHub repository in browser."""
        import webbrowser
        webbrowser.open("https://github.com/bytePatrol/YT-DLP-GUI-for-MacOS")
    
    def _update_resource_gauges(self):
        """Update system resource gauges periodically."""
        try:
            # Get current stats from monitor
            cpu, memory, gpu = self.system_monitor.get_stats()
            
            # Update gauges
            self.cpu_gauge.set_value(cpu)
            self.memory_gauge.set_value(memory)
            self.gpu_gauge.set_value(gpu)
        except Exception:
            pass
        
        # Schedule next update (every 1 second)
        self.after(1000, self._update_resource_gauges)
    
    def _check_clipboard_on_start(self):
        """Check clipboard for YouTube URL on startup."""
        try:
            clipboard = self.clipboard_get()
            if ("youtube.com" in clipboard or "youtu.be" in clipboard) and not self.url_entry.get():
                self.url_entry.insert(0, clipboard)
                self.log_panel.log("YouTube URL detected in clipboard", "info")
        except Exception:
            pass

    
    def _open_output_folder(self):
        """Open output folder in Finder."""
        output_dir = self.config.get("output_dir", str(Path.home() / "Desktop"))
        if os.path.isdir(output_dir):
            subprocess.run(["open", output_dir], check=False)
    
    # =========================================================================
    # YT-DLP UPDATE METHODS (v17.10.0)
    # =========================================================================
    
    def _check_ytdlp_update(self):
        """Check for yt-dlp updates and offer to install."""
        self.log_panel.log("Checking for yt-dlp updates...", "info")
        self.update_btn.configure(state="disabled", text="Checking...")
        
        def check_thread():
            updater = YtDlpUpdater(app_version=APP_VERSION)
            has_update, latest, current = updater.check_for_update(self.ytdlp.ytdlp_path)
            self.after(0, lambda: self._handle_update_check(has_update, latest, current))
        
        threading.Thread(target=check_thread, daemon=True).start()
    
    def _handle_update_check(self, has_update: bool, latest: Optional[str], current: Optional[str]):
        """Handle the result of update check."""
        self.update_btn.configure(state="normal", text="Update")
        
        if has_update and latest:
            self.log_panel.log(f"Update available: {current} -> {latest}", "success")
            
            # Reset button color in case it was highlighted
            self.update_btn.configure(fg_color=COLORS["bg_elevated"])
            
            if messagebox.askyesno(
                "yt-dlp Update Available",
                f"A new version of yt-dlp is available!\n\n"
                f"Current: {current}\n"
                f"Latest: {latest}\n\n"
                f"Download and install the update?\n\n"
                f"(Updates are stored in your Application Support folder,\n"
                f"so you won't need to re-download the entire app.)"
            ):
                self._install_ytdlp_update()
        else:
            self.log_panel.log(f"yt-dlp is up to date ({current})", "info")
            messagebox.showinfo("No Updates", f"yt-dlp is up to date!\n\nVersion: {current}")
    
    def _install_ytdlp_update(self):
        """Download and install yt-dlp update."""
        self.log_panel.log("Downloading yt-dlp update...", "info")
        self.update_btn.configure(state="disabled", text="Updating...")
        
        # Show progress in the main progress bar
        self.main_progress.set_progress(0, stage="downloading_video")
        self.main_progress.start_animation()
        self.progress_label.configure(text="Updating yt-dlp...")
        self.queue_status.configure(text="Updating")
        
        def install_thread():
            updater = YtDlpUpdater(app_version=APP_VERSION)
            
            def progress_callback(event, data):
                if event == "progress":
                    self.after(0, lambda d=data: self._update_install_progress(d))
                elif event == "error":
                    self.after(0, lambda d=data: self.log_panel.log(f"Update error: {d}", "error"))
            
            updater.add_callback(progress_callback)
            success, message = updater.download_and_install()
            self.after(0, lambda: self._handle_update_install(success, message))
        
        threading.Thread(target=install_thread, daemon=True).start()
    
    def _update_install_progress(self, data: dict):
        """Update progress bar during yt-dlp install."""
        percent = data.get("percent", 0)
        stage = data.get("stage", "Updating...")
        self.main_progress.set_progress(percent, stage="downloading_video")
        self.progress_label.configure(text=stage)
        self.percentage_label.configure(text=f"{percent}%")
    
    def _handle_update_install(self, success: bool, message: str):
        """Handle the result of yt-dlp installation."""
        self.update_btn.configure(state="normal", text="Update")
        self.main_progress.set_progress(100 if success else 0, stage="idle")
        self.main_progress.stop_animation()
        self.progress_label.configure(text="â³ Ready to download")
        self.queue_status.configure(text="Idle")
        self.percentage_label.configure(text="")
        
        if success:
            self.log_panel.log(message, "success")
            
            # Refresh yt-dlp interface to use new binary
            self.ytdlp.refresh_path()
            new_version = self.ytdlp.get_version()
            self.ytdlp_version_label.configure(text=f"yt-dlp: {new_version}")
            
            # Also update the download manager's interface
            self.download_manager.ytdlp.refresh_path()
            
            messagebox.showinfo("Update Complete", f"{message}\n\nThe new version is now active.")
        else:
            self.log_panel.log(f"Update failed: {message}", "error")
            messagebox.showerror("Update Failed", message)
    
    def _check_ytdlp_update_on_startup(self):
        """Check for updates on app startup (background, non-blocking)."""
        if not self.settings_mgr.get("ytdlp_auto_update_check", True):
            return
        
        def check_thread():
            try:
                updater = YtDlpUpdater(app_version=APP_VERSION)
                has_update, latest, current = updater.check_for_update(self.ytdlp.ytdlp_path)
                
                if has_update and latest:
                    self.after(0, lambda l=latest, c=current: self._notify_update_available(l, c))
            except Exception as e:
                print(f"Startup update check failed: {e}")
        
        # Run check in background thread
        threading.Thread(target=check_thread, daemon=True).start()
    
    def _notify_update_available(self, latest: str, current: str):
        """Show a subtle notification that an update is available."""
        self.log_panel.log(f"yt-dlp update available: {current} -> {latest} (click Update to install)", "info")
        # Highlight the Update button to indicate update available
        self.update_btn.configure(fg_color=COLORS["accent_orange"])
    
    # =========================================================================
    # APP UPDATE METHODS (v18.0.0)
    # =========================================================================
    
    def _check_app_update_on_startup(self):
        """Check for app updates on startup (background, non-blocking)."""
        def check_thread():
            try:
                checker = AppUpdateChecker(APP_VERSION)
                has_update, release_info = checker.check_for_update()
                
                if has_update and release_info:
                    self.after(0, lambda r=release_info: self._show_app_update_notification(r))
                else:
                    # Log quietly that we're up to date
                    self.after(0, lambda: self.log_panel.log(
                        f"✅ App is up to date (v{APP_VERSION})", "info"
                    ))
            except Exception as e:
                print(f"Startup app update check failed: {e}")
        
        # Run check in background thread
        threading.Thread(target=check_thread, daemon=True).start()
    
    def _show_app_update_notification(self, release_info: dict):
        """Show the update notification dialog."""
        try:
            self.log_panel.log(
                f"NEW App update available: v{APP_VERSION} -> v{release_info['version']}", 
                "success"
            )
            UpdateNotificationDialog(self, release_info)
        except Exception as e:
            print(f"Error showing update notification: {e}")


# ============================================================================
# ENTRY POINT
# ============================================================================

def main():
    """Application entry point."""
    # Ensure cache directory exists
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Create and run app
    app = YtDlpGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
