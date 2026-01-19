#!/usr/bin/env python3
"""
YouTube 4K Downloader v17 - Modern macOS Video Downloader

A complete rebuild with:
- Modern dark mode UI using CustomTkinter
- Fully responsive layout
- Video thumbnails and previews
- Download queue with pause/resume
- Playlist support
- SponsorBlock integration (POST-PROCESSING)
- Subtitle downloads
- PERSISTENT SETTINGS (v17 fix)
- Self-contained app with bundled ffmpeg AND deno
- And much more...

v17.7.0 Changes:
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
- Fixed crash with emoji/unicode in video titles (ÃƒÂ°Ã…Â¸Ã¢â‚¬Â¡Ã‚ÂµÃƒÂ°Ã…Â¸Ã¢â‚¬Â¡Ã‚Â±ÃƒÂ°Ã…Â¸Ã‹Å“Ã¢â‚¬Â¦ etc.)
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
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any, Callable
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
APP_VERSION = "17.7.4"

# Configuration paths - using proper config directory
CONFIG_DIR = Path.home() / ".config" / "yt-dlp-gui"
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

CONFIG_PATH = CONFIG_DIR / "config.json"
SETTINGS_PATH = CONFIG_DIR / "settings.json"  # Separate file for settings
HISTORY_PATH = CONFIG_DIR / "history.json"
CACHE_DIR = Path.home() / ".cache" / "yt_dlp_gui"

def find_executable(name: str) -> str:
    """Find executable, checking bundled resources first for self-contained app."""
    import shutil
    
    # Check if we're running from a .app bundle - prefer bundled executables
    if getattr(sys, 'frozen', False):
        bundle_dir = os.path.dirname(os.path.dirname(sys.executable))
        resources_dir = os.path.join(bundle_dir, 'Resources')
        bundled_path = os.path.join(resources_dir, name)
        if os.path.isfile(bundled_path):
            print(f"DEBUG find_executable: Found bundled {name} at {bundled_path}")
            return bundled_path
    
    # Special handling for yt-dlp: prefer Python module method
    if name == "yt-dlp":
        # Try to import yt-dlp as a Python module first (most reliable)
        try:
            import yt_dlp
            print(f"DEBUG find_executable: yt_dlp module found, using python-module method")
            return "python-module"
        except ImportError as e:
            print(f"DEBUG find_executable: yt_dlp module NOT found ({e}), falling back to paths")
            pass
        
        # Check Homebrew paths
        homebrew_paths = [
            "/opt/homebrew/bin/yt-dlp",
            "/usr/local/bin/yt-dlp",
        ]
        for p in homebrew_paths:
            if os.path.isfile(p):
                print(f"DEBUG find_executable: Found yt-dlp at {p}")
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

# Color Palette - iOS Dark Mode Inspired
COLORS = {
    "bg_primary": "#0d0d0f",
    "bg_secondary": "#161618",
    "bg_tertiary": "#1c1c1e",
    "bg_elevated": "#2c2c2e",
    "bg_hover": "#3a3a3c",
    
    "text_primary": "#f5f5f7",
    "text_secondary": "#98989d",
    "text_tertiary": "#636366",
    
    "accent_blue": "#0a84ff",
    "accent_blue_hover": "#409cff",
    "accent_green": "#30d158",
    "accent_orange": "#ff9f0a",
    "accent_red": "#ff453a",
    "accent_purple": "#bf5af2",
    
    "border": "#2c2c2e",
    "border_focus": "#0a84ff",
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


# ============================================================================
# DATA CLASSES
# ============================================================================

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
    is_playlist: bool = False
    playlist_count: Optional[int] = None
    
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
            print(f"DEBUG: Running command: {' '.join(cmd)}")  # Debug output
            result = subprocess.run(
                cmd,
                capture_output=True, text=True, check=False
            )
            print(f"DEBUG: Return code: {result.returncode}")  # Debug output
            print(f"DEBUG: stdout: {result.stdout[:100]}")  # Debug output
            print(f"DEBUG: stderr: {result.stderr[:100]}")  # Debug output
            if result.returncode == 0:
                self._version = result.stdout.strip().split('\n')[0]
                return self._version
        except Exception as e:
            print(f"DEBUG: Exception: {e}")  # Debug output
        return "Not found"
    
    def fetch_video_info(self, url: str) -> VideoInfo:
        """Fetch video metadata using yt-dlp -J."""
        try:
            result = subprocess.run(
                self._build_command(["-J", "--flat-playlist", url]),
                capture_output=True, text=True, check=False
            )
            
            if result.returncode != 0:
                raise RuntimeError(f"yt-dlp error: {result.stderr.strip()}")
            
            data = json.loads(result.stdout)
            return self._parse_video_info(data, url)
            
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse yt-dlp output: {e}")
    
    def fetch_full_info(self, url: str) -> VideoInfo:
        """Fetch full video info including all formats using --list-formats."""
        try:
            # First get basic metadata with -J (this works for basic info)
            result_info = subprocess.run(
                self._build_command(["-J", "--flat-playlist", url]),
                capture_output=True, text=True, check=False, timeout=30
            )
            
            if result_info.returncode != 0:
                raise RuntimeError(f"yt-dlp error: {result_info.stderr.strip()}")
            
            data = json.loads(result_info.stdout)
            info = self._parse_video_info(data, url, include_formats=False)
            
            # Now get formats using --list-formats (this shows ALL formats)
            result_formats = subprocess.run(
                self._build_command([
                    "--list-formats",
                    "--remote-components", "ejs:github",
                    url
                ]),
                capture_output=True, text=True, check=False, timeout=30
            )
            
            if result_formats.returncode == 0:
                # Parse the format table output
                info.formats = self._parse_format_table(result_formats.stdout)
            
            return info
            
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse yt-dlp output: {e}")
        except subprocess.TimeoutExpired:
            raise RuntimeError("yt-dlp took too long to respond")
    
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
            if not line or line.startswith('[') or line.startswith('â”€'):
                continue
            
            # Skip audio-only lines (we want video formats)
            if 'audio only' in line.lower() and 'video' not in line.lower():
                continue
            
            # Split by â”‚ separator to get sections
            sections = line.split('â”‚')
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
        
    def start(self, stage="downloading"):
        """Start tracking a new stage."""
        self.start_time = time.time()
        self.history = []
        self.current_stage = stage
        self.download_speed = None
        self.conversion_fps = None
        
    def update(self, percentage):
        """Update progress percentage."""
        if self.start_time is None:
            self.start()
            
        current_time = time.time()
        self.history.append((current_time, percentage))
        
        # Keep only last window_size seconds
        cutoff_time = current_time - self.window_size
        self.history = [(t, p) for t, p in self.history if t >= cutoff_time]
    
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
                "-f", video_format,
                "-o", temp_video,
                video_info.url
            ]
            
            # NOTE: SponsorBlock is now applied via post-processing (after download)
            # See _apply_sponsorblock_postprocess() method
            
            video_cmd = self.ytdlp._build_command(video_cmd_args)
            self._run_subprocess_with_progress(video_cmd, task, "Downloading video", 0, 40, video_id)
            
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
                "-f", "bestaudio[ext=m4a]/bestaudio/best",
                "-o", temp_audio,
                video_info.url
            ])
            
            self._run_subprocess_with_progress(audio_cmd, task, "Downloading audio", 40, 60, video_id)
            
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
            success = self._run_ffmpeg_with_progress(ffmpeg_cmd, task, "Converting", 60, progress_end, video_info.duration)
            
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
                    from pathlib import Path as PathLib
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
                    hist_mgr = HistoryManager(PathLib.home() / ".yt_dlp_gui_v16_history.json")
                    hist_mgr.add(history_entry)
                except Exception:
                    pass  # Don't fail download if history fails
                
                send_notification("Download Complete", f"{video_info.title}")
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
            error_lines = []  # Capture error messages
            
            for line in self.current_process.stdout:
                if self._paused:
                    while self._paused and self._running:
                        time.sleep(0.1)
                
                # Capture error lines (but only actual errors, not all warnings)
                if "error" in line.lower() and "warning" not in line.lower():
                    error_lines.append(line.strip())
                
                # Parse progress percentage
                match = progress_re.search(line)
                if match:
                    pct = float(match.group(1))
                    # Scale to our progress range
                    task.progress = progress_start + (pct / 100) * (progress_end - progress_start)
                    
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
            
            self.current_process.wait()
            
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
        """Run ffmpeg and update progress with FPS metrics."""
        try:
            # Start progress tracking for conversion stage
            self.progress_tracker.start("converting")
            
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
            total_duration = float(duration) if duration else 0
            
            stderr_lines = []  # Capture stderr for error reporting
            
            for line in self.current_process.stderr:
                stderr_lines.append(line)  # Store for potential error reporting
                
                if self._paused:
                    while self._paused and self._running:
                        time.sleep(0.1)
                
                if total_duration > 0:
                    match = time_re.search(line)
                    if match:
                        h = float(match.group(1))
                        m = float(match.group(2))
                        s = float(match.group(3))
                        current_time = h * 3600 + m * 60 + s
                        pct = min(100, (current_time / total_duration) * 100)
                        task.progress = progress_start + (pct / 100) * (progress_end - progress_start)
                        
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
            
            self.current_process.wait()
            
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


class ModernButton(ctk.CTkButton):
    """Modern styled button with hover effects."""
    
    def __init__(self, master, text="", icon=None, style="primary", **kwargs):
        styles = {
            "primary": {
                "fg_color": COLORS["accent_blue"],
                "hover_color": COLORS["accent_blue_hover"],
                "text_color": "white",
            },
            "secondary": {
                "fg_color": COLORS["bg_elevated"],
                "hover_color": COLORS["bg_hover"],
                "text_color": COLORS["text_primary"],
                "border_width": 1,
                "border_color": COLORS["border"],
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
        }
        
        style_config = styles.get(style, styles["primary"])
        
        super().__init__(
            master,
            text=text,
            corner_radius=10,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            **style_config,
            **kwargs
        )


class ModernEntry(ctk.CTkEntry):
    """Modern styled entry with focus effects."""
    
    def __init__(self, master, placeholder="", **kwargs):
        super().__init__(
            master,
            placeholder_text=placeholder,
            corner_radius=10,
            height=44,
            font=ctk.CTkFont(size=14),
            fg_color=COLORS["bg_tertiary"],
            border_color=COLORS["border"],
            text_color=COLORS["text_primary"],
            placeholder_text_color=COLORS["text_tertiary"],
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
    """Card for displaying a format option."""
    
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
        super().__init__(
            master,
            corner_radius=12,
            fg_color=COLORS["bg_elevated"] if selected else COLORS["bg_tertiary"],
            border_width=2,
            border_color=COLORS["accent_blue"] if selected else COLORS["border"],
            **kwargs
        )
        
        self.format_info = format_info
        self.selected = selected
        self.on_select = on_select
        
        # Resolution label
        res_text = f"{format_info.height}p" if format_info.height else "Audio"
        self.res_label = ctk.CTkLabel(
            self,
            text=res_text,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLORS["text_primary"]
        )
        self.res_label.pack(pady=(12, 4))
        
        # Codec info - get friendly name
        codec_raw = format_info.vcodec or format_info.acodec or ""
        codec_base = codec_raw.split('.')[0].lower() if codec_raw else ""
        codec_display = self.CODEC_NAMES.get(codec_base, codec_base.upper() if codec_base else "N/A")
        
        # Details
        details = f"{codec_display} - {format_info.size_str}\n{format_info.bitrate_str}"
        self.details_label = ctk.CTkLabel(
            self,
            text=details,
            font=ctk.CTkFont(size=11),
            text_color=COLORS["text_secondary"],
            justify="center"
        )
        self.details_label.pack(pady=(0, 12))
        
        # Recommended badge
        if recommended:
            self.badge = ctk.CTkLabel(
                self,
                text="Recommended",
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=COLORS["accent_orange"],
                fg_color=COLORS["bg_primary"],
                corner_radius=8,
                padx=8,
                pady=2
            )
            self.badge.place(relx=0.5, y=-8, anchor="n")
        
        # Bind click
        self.bind("<Button-1>", self._on_click)
        self.res_label.bind("<Button-1>", self._on_click)
        self.details_label.bind("<Button-1>", self._on_click)
    
    def _on_click(self, event):
        if self.on_select:
            self.on_select(self.format_info)
    
    def set_selected(self, selected: bool):
        self.selected = selected
        self.configure(
            fg_color=COLORS["bg_elevated"] if selected else COLORS["bg_tertiary"],
            border_color=COLORS["accent_blue"] if selected else COLORS["border"]
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
    """Scrollable log panel."""
    
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            corner_radius=12,
            fg_color=COLORS["bg_primary"],
            border_width=1,
            border_color=COLORS["border"],
            **kwargs
        )
        
        # Header
        header = ctk.CTkFrame(self, fg_color=COLORS["bg_tertiary"], corner_radius=0)
        header.pack(fill="x")
        
        ctk.CTkLabel(
            header,
            text="Activity Log",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=COLORS["text_secondary"]
        ).pack(side="left", padx=16, pady=10)
        
        # Clear button
        ctk.CTkButton(
            header,
            text="Clear",
            width=60,
            height=28,
            corner_radius=6,
            font=ctk.CTkFont(size=12),
            fg_color=COLORS["bg_elevated"],
            hover_color=COLORS["bg_hover"],
            text_color=COLORS["text_secondary"],
            command=self.clear
        ).pack(side="right", padx=10, pady=6)
        
        # Log text
        self.log_text = ctk.CTkTextbox(
            self,
            font=ctk.CTkFont(family="Menlo", size=12),
            fg_color="transparent",
            text_color=COLORS["text_secondary"],
            wrap="word",
            state="disabled"
        )
        self.log_text.pack(fill="both", expand=True, padx=8, pady=8)
    
    def log(self, message: str, level: str = "info"):
        """Add a log message."""
        colors = {
            "info": COLORS["text_secondary"],
            "success": COLORS["accent_green"],
            "warning": COLORS["accent_orange"],
            "error": COLORS["accent_red"],
        }
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"[{timestamp}] {message}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")
    
    def clear(self):
        """Clear the log."""
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")


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

Ãƒâ€š(c) 2025 All Rights Reserved"""
        
        ctk.CTkLabel(content, text=info, font=ctk.CTkFont(size=12), 
                    text_color=COLORS["text_secondary"], justify="center").pack(pady=(0, 20))
        
        ModernButton(content, text="Close", style="primary", width=100, command=self.destroy).pack()




# ============================================================================
# MAIN APPLICATION
# ============================================================================

class YtDlpGUI(ctk.CTk):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        
        # Initialize managers - using separate paths for config vs settings
        self.settings_mgr = SettingsManager(SETTINGS_PATH)  # Advanced settings (SponsorBlock, encoding, etc.)
        self.history_mgr = HistoryManager(HISTORY_PATH)
        
        # Configure CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Window setup
        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.geometry("1050x800")
        self.minsize(900, 700)
        
        # Set window background
        self.configure(fg_color=COLORS["bg_primary"])
        
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
    
    def _create_ui(self):
        """Create the main UI layout."""
        # Main container with padding
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        self._create_header()
        
        # URL input section
        self._create_url_section()
        
        # Quick options
        self._create_quick_options()
        
        # Video preview section (hidden until video is loaded)
        self._create_video_section()
        
        # Progress section
        self._create_progress_section()
        
        # Log panel
        self._create_log_section()
        
        # Footer
        self._create_footer()
    
    def _create_header(self):
        """Create the header with title and version."""
        header = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header.pack(fill="x", pady=(0, 16))
        
        # Title
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left")
        
        ctk.CTkLabel(
            title_frame,
            text=APP_NAME,
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COLORS["text_primary"]
        ).pack(side="left")
        
        # Version badge
        ctk.CTkLabel(
            title_frame,
            text=f"v{APP_VERSION}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLORS["accent_blue"],
            fg_color=COLORS["bg_elevated"],
            corner_radius=12,
            padx=10,
            pady=4
        ).pack(side="left", padx=(12, 0))
        
        # yt-dlp version
        self.ytdlp_version_label = ctk.CTkLabel(
            header,
            text=f"yt-dlp: {self.ytdlp.get_version()}",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_tertiary"]
        )
        self.ytdlp_version_label.pack(side="left", padx=(20, 0))
        
        # Header buttons
        btn_frame = ctk.CTkFrame(header, fg_color="transparent")
        btn_frame.pack(side="right")
        
        # Removed "Update yt-dlp" button - app has bundled yt-dlp that can't self-update
        
        ModernButton(
            btn_frame,
            text="Settings",
            style="secondary",
            width=90,
            command=self._show_settings
        ).pack(side="left", padx=(0, 8))
        
        ModernButton(
            btn_frame,
            text="History",
            style="secondary",
            width=90,
            command=self._show_history
        ).pack(side="left", padx=(0, 8))
        
        ModernButton(
            btn_frame,
            text="About",
            style="secondary",
            width=80,
            command=self._show_about
        ).pack(side="left", padx=(0, 8))
        
        ModernButton(
            btn_frame,
            text="Help",
            style="secondary",
            width=80,
            command=self._show_help
        ).pack(side="left")
    
    def _create_url_section(self):
        """Create URL input section."""
        url_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        url_frame.pack(fill="x", pady=(0, 12))
        
        # URL entry
        self.url_entry = ModernEntry(
            url_frame,
            placeholder="Paste YouTube URL here (Cmd+V) or drag & drop...",
        )
        self.url_entry.pack(side="left", fill="x", expand=True, padx=(0, 12))
        self.url_entry.bind("<Return>", lambda e: self._analyze())
        
        # Buttons
        ModernButton(
            url_frame,
            text="Download",
            style="primary",
            width=130,
            command=self._download
        ).pack(side="left", padx=(0, 8))
        
        ModernButton(
            url_frame,
            text="Analyze",
            style="secondary",
            width=100,
            command=self._analyze
        ).pack(side="left")
    
    def _create_quick_options(self):
        """Create quick option chips."""
        options_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        options_frame.pack(fill="x", pady=(0, 20))
        
        self.option_chips = {}
        
        options = [
            ("video_audio", "Video + Audio", True),
            ("audio_only", "Audio Only", False),
            ("quicktime", "QuickTime", False),
        ]
        
        for key, text, active in options:
            chip = OptionChip(
                options_frame,
                text=text,
                active=active,
                command=lambda k=key: self._toggle_option(k)
            )
            chip.pack(side="left", padx=(0, 8))
            self.option_chips[key] = chip
    
    def _create_video_section(self):
        """Create video preview section."""
        self.video_frame = ctk.CTkFrame(
            self.main_container,
            fg_color=COLORS["bg_tertiary"],
            corner_radius=16,
            border_width=1,
            border_color=COLORS["border"]
        )
        # Initially hidden - will be shown when video is analyzed
        
        # Preview content
        self.preview_frame = ctk.CTkFrame(self.video_frame, fg_color="transparent")
        self.preview_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left side - thumbnail
        self.thumb_frame = ctk.CTkFrame(
            self.preview_frame,
            fg_color=COLORS["bg_elevated"],
            corner_radius=12,
            width=280,
            height=158
        )
        self.thumb_frame.pack(side="left", padx=(0, 20))
        self.thumb_frame.pack_propagate(False)
        
        self.thumb_label = ctk.CTkLabel(
            self.thumb_frame,
            text="",
            font=ctk.CTkFont(size=48),
            text_color=COLORS["text_tertiary"]
        )
        self.thumb_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Duration badge
        self.duration_badge = ctk.CTkLabel(
            self.thumb_frame,
            text="0:00",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="white",
            fg_color="#1a1a1a",
            corner_radius=4,
            padx=6,
            pady=2
        )
        self.duration_badge.place(relx=0.95, rely=0.95, anchor="se")
        
        # Right side - info
        info_frame = ctk.CTkFrame(self.preview_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)
        
        self.title_label = ctk.CTkLabel(
            info_frame,
            text="Video Title",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS["text_primary"],
            anchor="w",
            wraplength=500
        )
        self.title_label.pack(fill="x", pady=(0, 8))
        
        # Meta info
        meta_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        meta_frame.pack(fill="x", pady=(0, 16))
        
        self.channel_label = ctk.CTkLabel(
            meta_frame,
            text="Channel",
            font=ctk.CTkFont(size=13),
            text_color=COLORS["text_secondary"]
        )
        self.channel_label.pack(side="left", padx=(0, 16))
        
        self.views_label = ctk.CTkLabel(
            meta_frame,
            text="Views",
            font=ctk.CTkFont(size=13),
            text_color=COLORS["text_secondary"]
        )
        self.views_label.pack(side="left", padx=(0, 16))
        
        # Format selection label
        ctk.CTkLabel(
            info_frame,
            text="SELECT QUALITY",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=COLORS["text_tertiary"]
        ).pack(anchor="w", pady=(0, 8))
        
        # Format cards container (scrollable)
        self.formats_scroll = ctk.CTkScrollableFrame(
            info_frame,
            fg_color="transparent",
            height=100,
            orientation="horizontal"
        )
        self.formats_scroll.pack(fill="x")
    
    def _create_progress_section(self):
        """Create enhanced progress/queue section with metrics."""
        self.progress_frame = ctk.CTkFrame(
            self.main_container,
            fg_color=COLORS["bg_tertiary"],
            corner_radius=16,
            border_width=1,
            border_color=COLORS["border"]
        )
        self.progress_frame.pack(fill="x", pady=(0, 16))
        
        # Header
        prog_header = ctk.CTkFrame(self.progress_frame, fg_color="transparent")
        prog_header.pack(fill="x", padx=20, pady=(16, 8))
        
        ctk.CTkLabel(
            prog_header,
            text="Downloads",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLORS["text_primary"]
        ).pack(side="left")
        
        self.queue_status = ctk.CTkLabel(
            prog_header,
            text="Idle",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_tertiary"]
        )
        self.queue_status.pack(side="right")
        
        # Enhanced progress bar
        self.main_progress = EnhancedProgressBar(self.progress_frame)
        self.main_progress.pack(fill="x", padx=20, pady=(0, 12))
        
        # Metrics row - Stage and Progress Percentage
        metrics_row1 = ctk.CTkFrame(self.progress_frame, fg_color="transparent")
        metrics_row1.pack(fill="x", padx=20, pady=(0, 6))
        
        self.progress_label = ctk.CTkLabel(
            metrics_row1,
            text="Ready to download",
            font=ctk.CTkFont(size=13),
            text_color=COLORS["text_secondary"]
        )
        self.progress_label.pack(side="left")
        
        self.percentage_label = ctk.CTkLabel(
            metrics_row1,
            text="",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=COLORS["text_primary"]
        )
        self.percentage_label.pack(side="right")
        
        # Metrics row 2 - Speed, FPS, ETA
        metrics_row2 = ctk.CTkFrame(self.progress_frame, fg_color="transparent")
        metrics_row2.pack(fill="x", padx=20, pady=(0, 16))
        
        self.speed_label = ctk.CTkLabel(
            metrics_row2,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["accent_blue"]
        )
        self.speed_label.pack(side="left", padx=(0, 12))
        
        self.fps_label = ctk.CTkLabel(
            metrics_row2,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["accent_green"]
        )
        self.fps_label.pack(side="left", padx=(0, 12))
        
        self.eta_label = ctk.CTkLabel(
            metrics_row2,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_secondary"]
        )
        self.eta_label.pack(side="right")
    
    def _create_log_section(self):
        """Create log panel."""
        self.log_panel = LogPanel(self.main_container, height=150)
        self.log_panel.pack(fill="both", expand=True, pady=(0, 16))
        
        # Welcome message
        self.log_panel.log(f"Welcome to {APP_NAME} v{APP_VERSION}", "info")
        self.log_panel.log(f"yt-dlp version: {self.ytdlp.get_version()}", "info")
    
    def _create_footer(self):
        """Create footer with output path and buttons."""
        footer = ctk.CTkFrame(self.main_container, fg_color="transparent")
        footer.pack(fill="x")
        
        # Output path
        path_frame = ctk.CTkFrame(footer, fg_color="transparent")
        path_frame.pack(side="left")
        
        ctk.CTkLabel(
            path_frame,
            text="Output:",
            font=ctk.CTkFont(size=13),
            text_color=COLORS["text_tertiary"]
        ).pack(side="left")
        
        self.output_path_label = ctk.CTkLabel(
            path_frame,
            text=self.config.get("output_dir", "~/Desktop"),
            font=ctk.CTkFont(size=13),
            text_color=COLORS["text_primary"]
        )
        self.output_path_label.pack(side="left", padx=(8, 0))
        
        # Footer buttons
        btn_frame = ctk.CTkFrame(footer, fg_color="transparent")
        btn_frame.pack(side="right")
        
        ModernButton(
            btn_frame,
            text="Open Folder",
            style="secondary",
            width=120,
            command=self._open_output_folder
        ).pack(side="left", padx=(0, 8))
        
        ModernButton(
            btn_frame,
            text="Change...",
            style="secondary",
            width=90,
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
        """Analyze the URL and show video info."""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("No URL", "Please enter a YouTube URL")
            return
        
        self.log_panel.log(f"Analyzing: {url}", "info")
        
        # BUGFIX v16.1: Clear previous state to fix empty format box
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
                info = self.ytdlp.fetch_full_info(url)
                self.after(0, lambda: self._display_video_info(info))
            except Exception as e:
                self.after(0, lambda: self._handle_error(f"Analysis failed: {e}"))
        
        threading.Thread(target=analyze_thread, daemon=True).start()
    
    def _display_video_info(self, info: VideoInfo):
        """Display video information in the UI."""
        self.current_video = info
        
        # Show video frame
        self.video_frame.pack(fill="x", pady=(0, 16), before=self.progress_frame)
        
        # Update labels
        self.title_label.configure(text=info.title)
        self.channel_label.configure(text=f"{info.channel or 'Unknown'}")
        self.views_label.configure(text=f"{info.views_str} views")
        self.duration_badge.configure(text=info.duration_str)
        
        # Load thumbnail
        if info.thumbnail:
            def load_thumb():
                thumb = self.thumbnail_manager.get_thumbnail(
                    info.thumbnail, info.id, (280, 158)
                )
                if thumb:
                    self.after(0, lambda: self.thumb_label.configure(image=thumb, text=""))
            
            threading.Thread(target=load_thumb, daemon=True).start()
        
        # Clear old format cards
        for card in self.format_cards:
            card.destroy()
        self.format_cards.clear()
        
        # Create format cards
        # Filter formats - include video-only and combined formats with height
        video_formats = [f for f in info.formats if f.height and f.height >= 100]
        
        # Log what we found for debugging
        self.log_panel.log(f"Video formats found: {len(video_formats)} with heights: {[f.height for f in video_formats[:10]]}", "info")
        
        # Deduplicate by resolution (keep best bitrate per resolution)
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
        
        for fmt in unique_formats:
            card = FormatCard(
                self.formats_scroll,
                fmt,
                selected=(fmt == recommended),
                recommended=(fmt == recommended),
                on_select=self._select_format,
                width=130
            )
            card.pack(side="left", padx=(0, 10))
            self.format_cards.append(card)
        
        self.log_panel.log(f"Found {len(info.formats)} formats, showing {len(unique_formats)} quality options", "success")
    
    def _select_format(self, fmt: VideoFormat):
        """Handle format selection."""
        self.selected_format = fmt
        
        for card in self.format_cards:
            card.set_selected(card.format_info == fmt)
        
        self.log_panel.log(f"Selected: {fmt.height}p {fmt.bitrate_str}", "info")
    
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
        """Handle download manager events with enhanced metrics."""
        def update():
            if event == "task_progress" or event == "task_updated":
                task = data
                
                # Determine stage for color coding
                stage_name = "idle"
                stage_text = "Ready to download"
                
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
                elif task.status == DownloadStatus.CONVERTING:
                    stage_name = "converting"
                    fmt = task.selected_format
                    if fmt and fmt.height:
                        stage_text = f"Stage 3/3: Converting ({fmt.height}p)"
                    else:
                        stage_text = "Stage 3/3: Converting"
                elif task.status == DownloadStatus.COMPLETED:
                    stage_name = "idle"
                    stage_text = f"Completed: {task.video_info.title}"
                
                # Update enhanced progress bar
                self.main_progress.set_progress(task.progress, stage=stage_name)
                
                # Start/stop animation
                if task.status in [DownloadStatus.DOWNLOADING, DownloadStatus.CONVERTING]:
                    self.main_progress.start_animation()
                    self.queue_status.configure(text="Active")
                else:
                    self.main_progress.stop_animation()
                    self.queue_status.configure(text="Idle")
                
                # Update metrics labels
                self.progress_label.configure(text=stage_text)
                self.percentage_label.configure(text=f"{task.progress:.0f}%")
                
                # Update speed/fps/eta
                if task.download_speed:
                    self.speed_label.configure(text=task.download_speed)
                else:
                    self.speed_label.configure(text="")
                
                if task.conversion_fps:
                    self.fps_label.configure(text=task.conversion_fps)
                else:
                    self.fps_label.configure(text="")
                
                if task.eta:
                    self.eta_label.configure(text=f"ETA: {task.eta}")
                else:
                    self.eta_label.configure(text="")
                
                # Log stage changes
                if task.status == DownloadStatus.CONVERTING and event == "task_updated":
                    self.log_panel.log("Converting to QuickTime-compatible format...", "info")
                elif task.status == DownloadStatus.COMPLETED:
                    self.log_panel.log(f"Completed: {task.video_info.title}", "success")
                    self.main_progress.set_progress(100, stage="idle")
                elif task.status == DownloadStatus.FAILED:
                    self.log_panel.log(f"Failed: {task.error_message}", "error")
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
    # The bundled app cannot self-update yt-dlp
    
    def _show_help(self):
        """Show help window."""
        help_window = ctk.CTkToplevel(self)
        help_window.title("Help")
        help_window.geometry("600x500")
        help_window.transient(self)
        
        help_text = ctk.CTkTextbox(
            help_window,
            font=ctk.CTkFont(size=13),
            wrap="word"
        )
        help_text.pack(fill="both", expand=True, padx=20, pady=20)
        
        help_content = """
YouTube 4K Downloader v17 - Help

QUICK START
1. Paste a YouTube URL (or drag & drop)
2. Click "Analyze" to see available formats
3. Select your preferred quality
4. Click "Download" or press Cmd+Return

NEW IN V17.7
- FIXED: SponsorBlock now works via post-processing!
- After download, segments are fetched from SponsorBlock API
- Video is re-encoded with sponsor segments removed
- More reliable than trying to integrate during download

NEW IN V17
- FIXED: Settings now persist between sessions!
- Settings stored in ~/.config/yt-dlp-gui/
- SponsorBlock, Encoding, Subtitles settings are saved

FEATURES
- Settings window (Ã¢Å’Ëœ,) - Configure SponsorBlock, subtitles, encoding
- SponsorBlock post-processing - Removes sponsor segments after download
- History browser - Search and manage download history
- Playlist support - Download entire playlists with selection
- Enhanced audio-only mode - M4A/MP3 with proper metadata
- Drag & drop URLs - Just drop a YouTube link onto the window

KEYBOARD SHORTCUTS
- Ã¢Å’ËœV - Paste URL from clipboard
- Cmd+Return - Start download
- Enter - Analyze URL

OPTIONS & FEATURES
- Video + Audio: Download complete video
- Audio Only: Extract audio as M4A/MP3  
- QuickTime Compatible: Apple-optimized encoding
- SponsorBlock: Remove sponsor segments via post-processing
- Subtitles: Download and embed multiple languages
- Trim: Cut start/end of videos
- Automatic clipboard detection
- Thumbnail previews
- Progress tracking with ETA
- macOS notifications
- Download history

REQUIREMENTS
- yt-dlp: brew install yt-dlp
- ffmpeg: brew install ffmpeg

For more information, visit:
https://github.com/yt-dlp/yt-dlp
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
        """Show settings window."""
        SettingsWindow(self, self.settings_mgr)
    
    def _show_history(self):
        """Show history browser."""
        HistoryBrowserWindow(self, self.history_mgr)
    
    def _show_about(self):
        """Show about dialog."""
        AboutDialog(self, self.ytdlp.get_version())
    
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
