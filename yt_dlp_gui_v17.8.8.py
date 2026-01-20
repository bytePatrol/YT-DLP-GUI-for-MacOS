#!/usr/bin/env python3
"""
YouTube 4K Downloader v17 - Modern macOS Video Downloader

A professional-grade macOS application for downloading YouTube videos with a modern,
dark-mode UI built using CustomTkinter. This application is designed to be fully
self-contained, bundling all dependencies (ffmpeg, deno, yt-dlp) for a seamless
user experience.

Features:
    - Modern dark mode UI with iOS-inspired design
    - Support for 4K, 1440p, 1080p, 720p, and other resolutions
    - Video thumbnails and metadata preview
    - Download queue with progress tracking
    - Playlist support with chapter extraction
    - SponsorBlock integration (post-processing removal of sponsor segments)
    - Subtitle downloading and embedding
    - QuickTime-compatible H.264 + AAC output format
    - Persistent settings stored in ~/.config/yt-dlp-gui/
    - Self-contained app bundle with bundled ffmpeg and deno

Architecture:
    The application follows a layered architecture:

    1. UI Layer (CustomTkinter widgets):
       - YtDlpGUI: Main application window
       - SettingsWindow, HistoryBrowserWindow, AboutDialog: Modal dialogs
       - Custom widgets: EnhancedProgressBar, ModernButton, FormatCard, etc.

    2. Business Logic Layer:
       - DownloadManager: Manages download queue and threading
       - YtDlpInterface: Wrapper for yt-dlp commands
       - SponsorBlockAPI: Client for SponsorBlock segment data

    3. Data Layer:
       - SettingsManager: Persistent settings storage
       - HistoryManager: Download history tracking
       - Dataclasses: VideoFormat, VideoInfo, DownloadTask, Chapter

Usage:
    Run directly:
        python3 yt_dlp_gui_v17.8.8.py

    Or build as macOS app:
        ./build_app.sh

Dependencies:
    Required:
        - customtkinter >= 5.0
        - pillow >= 9.0
        - requests >= 2.28
        - yt-dlp >= 2023.0

    Optional:
        - tkinterdnd2 (for drag & drop support)

For version history, see CHANGELOG.md

Author: bytePatrol
License: MIT
Version: 17.8.8
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
APP_VERSION = "17.8.8"

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
            return bundled_path

    # Special handling for yt-dlp: prefer Python module method
    if name == "yt-dlp":
        # Try to import yt-dlp as a Python module first (most reliable)
        try:
            import yt_dlp
            return "python-module"
        except ImportError:
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
    """Represents a single video/audio format available for download.

    This class holds metadata about a specific format option returned by yt-dlp,
    including resolution, codec information, and file size estimates.

    Attributes:
        format_id: Unique identifier for this format (e.g., '137', '140').
        ext: File extension (e.g., 'mp4', 'webm', 'm4a').
        resolution: Resolution string (e.g., '1920x1080').
        height: Video height in pixels (e.g., 1080, 720).
        width: Video width in pixels (e.g., 1920, 1280).
        fps: Frames per second (e.g., 30, 60).
        vcodec: Video codec (e.g., 'avc1', 'vp9', 'av1').
        acodec: Audio codec (e.g., 'mp4a', 'opus').
        filesize: Exact file size in bytes (if known).
        filesize_approx: Approximate file size in bytes.
        tbr: Total bitrate in kbps.
        vbr: Video bitrate in kbps.
        abr: Audio bitrate in kbps.
        is_video_only: True if format contains only video (no audio).
        is_audio_only: True if format contains only audio (no video).
        is_quicktime_compatible: True if format is compatible with QuickTime/Apple.
    """
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
    tbr: Optional[float] = None
    vbr: Optional[float] = None
    abr: Optional[float] = None
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
    """Represents a chapter/segment within a video.

    YouTube videos can have chapters defined by the uploader, which appear
    in the video timeline. This class stores metadata for a single chapter,
    enabling chapter-based downloading.

    Attributes:
        index: Zero-based index of the chapter in the video.
        title: Human-readable title of the chapter.
        start_time: Start time of the chapter in seconds from video start.
        end_time: End time of the chapter in seconds from video start.
    """
    index: int
    title: str
    start_time: float
    end_time: float
    
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
class VideoInfo:
    """Represents complete metadata for a YouTube video or playlist.

    This class aggregates all information about a video retrieved from yt-dlp,
    including basic metadata, available formats, and chapter information.

    Attributes:
        id: YouTube video ID (e.g., 'dQw4w9WgXcQ').
        title: Video title.
        url: Full URL to the video.
        thumbnail: URL to the video thumbnail image.
        duration: Video duration in seconds.
        channel: Name of the channel that uploaded the video.
        view_count: Number of views.
        upload_date: Upload date in YYYYMMDD format.
        description: Video description text.
        formats: List of available download formats.
        chapters: List of chapters (if video has chapters).
        is_playlist: True if this represents a playlist, not a single video.
        playlist_count: Number of videos in playlist (if is_playlist is True).
    """
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
    chapters: List[Chapter] = field(default_factory=list)
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
    
    @property
    def has_chapters(self) -> bool:
        """Check if video has chapters."""
        return len(self.chapters) > 0


@dataclass
class DownloadTask:
    """Represents a download task in the queue.

    This class tracks the state of a single download operation, including
    progress metrics, status, and output information. Tasks are managed
    by DownloadManager and updated throughout the download lifecycle.

    Attributes:
        id: Unique identifier for this task (typically the video ID).
        video_info: Metadata about the video being downloaded.
        selected_format: The format chosen for download.
        output_path: Path to the final output file (set after completion).
        status: Current status of the download (QUEUED, DOWNLOADING, etc.).
        progress: Download progress as a percentage (0.0 to 100.0).
        speed: Legacy speed field (deprecated, use download_speed).
        eta: Estimated time remaining as a formatted string.
        download_speed: Current download speed (e.g., '5.2 MB/s').
        conversion_fps: FFmpeg encoding speed in frames per second.
        file_size: Final file size in bytes after completion.
        status_detail: Detailed status message for UI display.
        current_file_size: Current size of file being written (for progress).
        error_message: Error description if status is FAILED.
        started_at: Timestamp when download started.
        completed_at: Timestamp when download completed.
    """
    id: str
    video_info: VideoInfo
    selected_format: Optional[VideoFormat] = None
    output_path: Optional[str] = None
    status: DownloadStatus = DownloadStatus.QUEUED
    progress: float = 0.0
    speed: Optional[str] = None
    eta: Optional[str] = None
    download_speed: Optional[str] = None
    conversion_fps: Optional[str] = None
    file_size: Optional[int] = None
    status_detail: Optional[str] = None
    current_file_size: Optional[int] = None
    error_message: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


# ============================================================================
# SPONSORBLOCK API
# ============================================================================

class SponsorBlockAPI:
    """Interface for the SponsorBlock crowdsourced sponsorship database.

    SponsorBlock is a community-driven API that provides timestamps for
    sponsor segments, intros, outros, and other skippable content in
    YouTube videos. This class provides methods to query the API and
    convert segments to FFmpeg filter expressions for removal.

    The API uses a privacy-preserving hash prefix mechanism to avoid
    sending full video IDs.

    Attributes:
        API_BASE: Base URL for the SponsorBlock API.

    See Also:
        https://sponsor.ajay.app/ - SponsorBlock project website
        https://wiki.sponsor.ajay.app/w/API_Docs - API documentation
    """

    API_BASE = "https://sponsor.ajay.app/api"
    
    @staticmethod
    def get_video_hash_prefix(video_id: str) -> str:
        """Generate SHA256 hash prefix for privacy-preserving API queries.

        The SponsorBlock API accepts hash prefixes instead of full video IDs
        to protect user privacy. The server returns data for all videos
        matching the prefix, and the client filters for the exact match.

        Args:
            video_id: YouTube video ID (e.g., 'dQw4w9WgXcQ').

        Returns:
            First 4 characters of the SHA256 hash of the video ID.
        """
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
    """Create a filesystem-safe filename from arbitrary text.

    Sanitizes input by removing or replacing characters that are problematic
    for filesystems, shells, or encoding. This includes emoji, special shell
    characters, and non-ASCII characters that may cause issues on macOS.

    Args:
        name: The original filename or title to sanitize.
        max_length: Maximum length of the resulting filename. Defaults to 200.

    Returns:
        A safe filename containing only ASCII letters, numbers, spaces, and
        basic punctuation. Returns "video" if the result would be empty.

    Example:
        >>> sanitize_filename('My Video 🎬 (2024)')
        'My Video _ _2024_'
    """
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
    """Format a duration in seconds as a human-readable time string.

    Converts a floating-point seconds value to HH:MM:SS or MM:SS format,
    depending on whether the duration exceeds one hour.

    Args:
        seconds: Duration in seconds. Negative values are treated as 0.

    Returns:
        Formatted time string in HH:MM:SS format if >= 1 hour,
        otherwise MM:SS format.

    Example:
        >>> format_time(3661.5)
        '01:01:01'
        >>> format_time(125)
        '02:05'
    """
    seconds = int(max(0, seconds))
    h, remainder = divmod(seconds, 3600)
    m, s = divmod(remainder, 60)
    if h:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def send_notification(title: str, message: str):
    """Send macOS notification safely.

    Escapes special characters to prevent shell injection attacks
    from malicious video titles.
    """
    try:
        # Escape backslashes and quotes to prevent AppleScript injection
        safe_title = title.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")
        safe_message = message.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")
        # Truncate to reasonable length
        safe_title = safe_title[:100]
        safe_message = safe_message[:200]
        script = f'display notification "{safe_message}" with title "{safe_title}"'
        subprocess.run(["osascript", "-e", script], check=False, capture_output=True, timeout=5)
    except (subprocess.TimeoutExpired, OSError):
        pass


def load_json_file(path: Path, default: Any = None) -> Any:
    """Load JSON data from a file with fallback to default values.

    Reads and parses a JSON file. If the file doesn't exist or cannot be
    parsed, returns the default value. When both the default and loaded
    data are dictionaries, merges them (loaded values override defaults).

    Args:
        path: Path to the JSON file to load.
        default: Default value to return if file doesn't exist or is invalid.
            If a dict, will be merged with loaded data.

    Returns:
        The loaded JSON data, merged with defaults if both are dicts,
        or the default value if loading fails.

    Note:
        Prints a warning message to stdout if loading fails.
    """
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


def save_json_file(path: Path, data: Any) -> None:
    """Save data to a JSON file with automatic directory creation.

    Serializes data to JSON format and writes it to the specified file.
    Creates parent directories if they don't exist. Uses 2-space
    indentation for readability.

    Args:
        path: Destination path for the JSON file.
        data: Data to serialize. Must be JSON-serializable. Objects with
            __str__ methods are converted using str() as a fallback.

    Note:
        Prints an error message to stdout if saving fails.
    """
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
    """High-level interface for interacting with yt-dlp.

    Provides methods to fetch video metadata, list available formats, and
    build download commands. Supports multiple execution modes:
    - Direct executable invocation
    - Python module execution (via `python -m yt_dlp`)
    - Homebrew-installed yt-dlp with system Python

    The class automatically detects the best execution method based on
    the yt-dlp installation location.

    Attributes:
        ytdlp_path: Path to yt-dlp executable or "python-module" for module mode.

    Example:
        >>> ytdlp = YtDlpInterface()
        >>> if ytdlp.is_available:
        ...     info = ytdlp.fetch_video_info('https://youtube.com/watch?v=...')
        ...     print(info.title)
    """

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
        """Find a system Python interpreter for running Homebrew scripts.

        When yt-dlp is installed via Homebrew, it may require execution
        through a specific Python interpreter rather than direct invocation.

        Returns:
            Path to the first available Python 3 interpreter, or None if
            no suitable interpreter is found.
        """
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
        """Build the command list to execute yt-dlp with given arguments.

        Constructs the appropriate command based on the execution mode
        (direct, module, or system Python). Automatically includes
        JavaScript runtime arguments if Deno is bundled with the app.

        Args:
            args: Command-line arguments to pass to yt-dlp.

        Returns:
            Complete command list suitable for subprocess execution.
        """
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
        """Check if yt-dlp is available for use.

        Returns:
            True if yt-dlp can be executed (either as module or file exists).
        """
        if self._use_python_module:
            try:
                import yt_dlp
                return True
            except ImportError:
                return False
        return os.path.isfile(self.ytdlp_path)
    
    def get_version(self) -> str:
        """Get the yt-dlp version string.

        Caches the version after first retrieval for efficiency.

        Returns:
            Version string (e.g., '2024.01.01') or "Not found" if
            yt-dlp cannot be executed.
        """
        if self._version:
            return self._version
        try:
            cmd = self._build_command(["--version"])
            result = subprocess.run(
                cmd,
                capture_output=True, text=True, check=False, timeout=10,
                encoding='utf-8', errors='replace'
            )
            if result.returncode == 0:
                self._version = result.stdout.strip().split('\n')[0]
                return self._version
        except (subprocess.TimeoutExpired, OSError, ValueError):
            pass
        return "Not found"

    def fetch_video_info(self, url: str) -> VideoInfo:
        """Fetch basic video metadata from a URL.

        Uses yt-dlp's JSON output mode (-J) with flat playlist mode to
        quickly retrieve video information without downloading.

        Args:
            url: YouTube URL (video, playlist, or channel).

        Returns:
            VideoInfo object containing video metadata.

        Raises:
            RuntimeError: If yt-dlp fails or returns invalid JSON.
        """
        try:
            result = subprocess.run(
                self._build_command(["-J", "--flat-playlist", url]),
                capture_output=True, text=True, check=False, timeout=30,
                encoding='utf-8', errors='replace'
            )
            
            if result.returncode != 0:
                raise RuntimeError(f"yt-dlp error: {result.stderr.strip()}")
            
            data = json.loads(result.stdout)
            return self._parse_video_info(data, url)
            
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse yt-dlp output: {e}")
    
    def fetch_full_info(self, url: str) -> VideoInfo:
        """Fetch complete video metadata including all available formats.

        Performs two yt-dlp calls: one for basic metadata and another
        for the complete format list. This provides more detailed format
        information than fetch_video_info().

        Args:
            url: YouTube URL (video, playlist, or channel).

        Returns:
            VideoInfo object with complete metadata and format list.

        Raises:
            RuntimeError: If yt-dlp fails, times out, or returns invalid data.
        """
        try:
            # First get basic metadata with -J (this works for basic info)
            result_info = subprocess.run(
                self._build_command(["-J", "--flat-playlist", url]),
                capture_output=True, text=True, check=False, timeout=30,
                encoding='utf-8', errors='replace'
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
                capture_output=True, text=True, check=False, timeout=30,
                encoding='utf-8', errors='replace'
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
                        except ValueError:
                            pass
                        break
                    # Match patterns like "1.8M" or "4M"
                    elif re.match(r'^[\d.]+M$', part):
                        try:
                            tbr = int(float(part[:-1]) * 1000)
                        except ValueError:
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
                        except ValueError:
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
                        except ValueError:
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
                        except ValueError:
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
                    except ValueError:
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
    """Manages the download queue and executes download operations.

    Provides a thread-safe queue system for downloading videos using yt-dlp.
    Supports pausing, resuming, and cancelling downloads, with progress
    tracking and callback notifications for UI updates.

    Features:
    - Thread-safe task queue with add/remove operations
    - Progress tracking with ETA calculation
    - SponsorBlock integration for removing sponsored segments
    - Callback system for real-time status updates
    - Support for concurrent format downloads and remuxing

    Attributes:
        ytdlp: YtDlpInterface instance for executing downloads.
        output_dir: Default directory for downloaded files.
        queue: List of pending and active DownloadTask objects.
        current_task: Currently executing download task, if any.

    Example:
        >>> manager = DownloadManager(ytdlp_interface, '/path/to/downloads')
        >>> manager.add_callback(lambda event, data: print(f'{event}: {data}'))
        >>> task = manager.add_task(video_info, selected_format)
        >>> manager.start()
    """

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
    
    def add_callback(self, callback: Callable[[str, Any], None]) -> None:
        """Register a callback for download status updates.

        Callbacks are invoked with (event, data) parameters when download
        state changes. Events include: 'task_added', 'task_removed',
        'task_updated', 'queue_complete'.

        Args:
            callback: Function accepting (event: str, data: Any) parameters.
        """
        self._callbacks.append(callback)
    
    def _notify(self, event: str, data: Any = None) -> None:
        """Notify all registered callbacks of an event.

        Catches and logs exceptions from callbacks to prevent one
        failing callback from affecting others.

        Args:
            event: Event name (e.g., 'task_added', 'task_updated').
            data: Event-specific data, typically a DownloadTask or task ID.
        """
        for cb in self._callbacks:
            try:
                cb(event, data)
            except Exception as e:
                print(f"Callback error: {e}")
    
    def add_task(self, video_info: VideoInfo, selected_format: Optional[VideoFormat] = None) -> DownloadTask:
        """Add a new download task to the queue.

        Creates a DownloadTask from video metadata and queues it for
        processing. Notifies callbacks with 'task_added' event.

        Args:
            video_info: Video metadata from YtDlpInterface.
            selected_format: Specific format to download, or None for default.

        Returns:
            The created DownloadTask object.
        """
        task = DownloadTask(
            id=f"{video_info.id}_{int(time.time())}",
            video_info=video_info,
            selected_format=selected_format,
        )
        
        with self._lock:
            self.queue.append(task)
        
        self._notify("task_added", task)
        return task
    
    def remove_task(self, task_id: str) -> None:
        """Remove a task from the queue by ID.

        Thread-safe removal of a queued task. Does not affect tasks
        that are currently downloading.

        Args:
            task_id: Unique identifier of the task to remove.
        """
        with self._lock:
            self.queue = [t for t in self.queue if t.id != task_id]
        self._notify("task_removed", task_id)
    
    def start(self) -> None:
        """Start processing the download queue.

        Spawns a daemon thread to process queued tasks. If already
        running, this method returns immediately without effect.
        """
        if self._running:
            return
        
        self._running = True
        self._paused = False
        threading.Thread(target=self._process_queue, daemon=True).start()
    
    def pause(self) -> None:
        """Pause queue processing.

        Sets the paused flag and updates the current task status.
        The download process continues but new tasks are not started.
        """
        self._paused = True
        if self.current_task:
            self.current_task.status = DownloadStatus.PAUSED
            self._notify("task_updated", self.current_task)
    
    def resume(self) -> None:
        """Resume queue processing after a pause.

        Clears the paused flag and updates the current task status
        back to DOWNLOADING.
        """
        self._paused = False
        if self.current_task:
            self.current_task.status = DownloadStatus.DOWNLOADING
            self._notify("task_updated", self.current_task)
    
    def cancel_current(self) -> None:
        """Cancel the currently active download.

        Terminates the yt-dlp subprocess and marks the task as cancelled.
        The queue continues processing the next task.
        """
        if self.current_process:
            self.current_process.terminate()
        if self.current_task:
            self.current_task.status = DownloadStatus.CANCELLED
            self._notify("task_updated", self.current_task)
    
    def _process_queue(self) -> None:
        """Main queue processing loop (runs in background thread).

        Continuously checks for queued tasks and processes them one at
        a time. Handles pausing, cancellation, and status updates.
        """
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
                "--extractor-args", "youtube:player_client=android_sdkless",
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
            except (ValueError, AttributeError):
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
                        except OSError:
                            pass

                if files_removed:
                    self._notify("log", ("info", f"Cleaned up temp files: {', '.join(files_removed)}"))
            except OSError as e:
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
                except OSError:
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
                                    except OSError:
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
                except OSError:
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
    """Animated progress bar with segmented block visualization.

    Displays download progress as a series of blocks that fill in as the
    download progresses. Supports different colors for different stages
    (downloading video, audio, converting) and includes a pulsing
    animation effect for active downloads.

    Attributes:
        progress: Current progress percentage (0-100).
        stage: Current download stage ('downloading_video', 'downloading_audio',
            'converting', or 'idle').
        animating: Whether the pulse animation is currently active.
    """

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
    """Styled button with predefined appearance themes.

    Extends CTkButton with predefined styles (primary, secondary, danger,
    success) that automatically apply appropriate colors, borders, and
    hover effects consistent with the application's design system.

    Args:
        master: Parent widget.
        text: Button label text.
        icon: Optional icon character to prepend to text.
        style: Button style - 'primary', 'secondary', 'danger', or 'success'.
        **kwargs: Additional arguments passed to CTkButton.
    """

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
    """Styled text entry field with consistent appearance.

    Extends CTkEntry with predefined styling matching the application's
    dark theme, including rounded corners, appropriate colors, and
    placeholder text styling.

    Args:
        master: Parent widget.
        placeholder: Placeholder text shown when entry is empty.
        **kwargs: Additional arguments passed to CTkEntry.
    """

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
    """Toggleable chip/pill button for option selection.

    A compact button styled as a pill/chip that can be toggled between
    active and inactive states. Used for filter options, format selection,
    and other binary choices.

    Args:
        master: Parent widget.
        text: Chip label text.
        active: Initial selection state.
        **kwargs: Additional arguments passed to CTkButton.

    Attributes:
        active: Current selection state (True if selected).
    """

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
    """Card widget displaying a video/audio format option.

    Shows format information (resolution, codec, file size, bitrate) in
    a clickable card format. Used in the format selection UI to allow
    users to choose their preferred download format.

    Args:
        master: Parent widget.
        format_info: VideoFormat object containing format metadata.
        selected: Whether this card is currently selected.
        recommended: Whether to show a 'Recommended' badge.
        on_select: Callback function when card is clicked.
        **kwargs: Additional arguments passed to CTkFrame.

    Attributes:
        format_info: The VideoFormat this card represents.
        selected: Current selection state.
    """

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
    """Card widget displaying download task progress.

    Shows a download task's current state including title, status,
    progress bar, and statistics (speed, ETA). Automatically updates
    colors based on the task status.

    Args:
        master: Parent widget.
        task: DownloadTask to display.
        **kwargs: Additional arguments passed to CTkFrame.

    Attributes:
        task: The DownloadTask being displayed.
    """

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
    """Scrollable activity log panel with timestamped messages.

    Displays application activity messages with timestamps and color-coded
    severity levels. Includes a header with title and clear button.

    Args:
        master: Parent widget.
        **kwargs: Additional arguments passed to CTkFrame.

    Methods:
        log(message, level): Add a timestamped message with severity level.
        clear(): Clear all log messages.
    """

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
    """Manages application settings with persistent JSON storage.

    Handles loading, saving, and accessing application settings. Settings
    are stored in a JSON file and merged with defaults on load to ensure
    new settings are available after updates.

    Settings categories include:
    - SponsorBlock: segment removal preferences
    - Subtitles: language and embedding options
    - Encoding: video/audio bitrate and encoder settings
    - Trim: video trimming start/end times
    - Playlist: download order and limits

    Args:
        config_path: Path to settings JSON file. Defaults to SETTINGS_PATH.

    Attributes:
        settings: Dictionary of current settings.
        config_path: Path to the settings file.
    """

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
    """Manages persistent download history.

    Tracks completed downloads with metadata (title, URL, date, file path)
    and provides search functionality. History is limited to 1000 entries
    with oldest entries automatically pruned.

    Args:
        history_path: Path to history JSON file.

    Attributes:
        entries: List of history entry dictionaries.
        history_path: Path to the history file.
    """

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
    """Modal window for configuring application settings.

    Provides a tabbed interface for configuring:
    - SponsorBlock: segment removal categories and behavior
    - Subtitles: language preferences and embedding options
    - Encoding: video/audio quality and encoder settings
    - Trim: video start/end time clipping
    - Playlist: download order and item limits

    Args:
        parent: Parent window.
        settings_mgr: SettingsManager instance to read/write settings.
    """

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
                except (ValueError, AttributeError):
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
        except (ValueError, TypeError):
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
        except (ValueError, TypeError):
            self.settings_mgr.set("playlist_max_items", 0)
        
        self.settings_mgr.save()
        self.destroy()


class HistoryBrowserWindow(ctk.CTkToplevel):
    """Window for browsing and searching download history.

    Displays a searchable list of previously downloaded videos with
    title, date, and file path. Allows clearing the entire history.

    Args:
        parent: Parent window.
        history_mgr: HistoryManager instance for history data.
    """

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
    """Application information dialog.

    Displays version information, credits, and links to the project
    repository and donation page.

    Args:
        parent: Parent window.
        ytdlp_version: Version string of the installed yt-dlp.
    """

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
    """Window for selecting specific video chapters to download.

    Displays a list of available chapters with checkboxes for selection.
    Users can select individual chapters or use select/deselect all.
    Selected chapters are downloaded as separate files.

    Args:
        parent: Parent window.
        video_info: VideoInfo containing chapter metadata.
        on_download: Callback function receiving list of selected chapters.

    Note:
        SponsorBlock is automatically disabled for chapter downloads
        to avoid timing conflicts.
    """

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
            text=" SponsorBlock is disabled for chapter downloads",
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
            text="Download Selected Chapters",
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


# ============================================================================
# MAIN APPLICATION
# ============================================================================

class YtDlpGUI(ctk.CTk):
    """Main application window for 4K YouTube Downloader.

    The primary GUI class that orchestrates all application functionality
    including URL input, format selection, download management, and
    settings configuration.

    Features:
    - URL paste/drag-drop with automatic video info fetching
    - Format selection with quality presets and manual format cards
    - Progress tracking with ETA and speed display
    - Clipboard monitoring for YouTube URLs
    - Keyboard shortcuts for common actions
    - Persistent settings and download history

    Attributes:
        settings_mgr: SettingsManager for application preferences.
        history_mgr: HistoryManager for download history.
        ytdlp: YtDlpInterface for yt-dlp operations.
        download_manager: DownloadManager for queue management.
        current_video: Currently loaded VideoInfo, if any.
        selected_format: Currently selected VideoFormat for download.

    Example:
        >>> app = YtDlpGUI()
        >>> app.mainloop()
    """

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
        
        # Footer MUST be created first when using side="bottom" 
        # This ensures it stays at the bottom regardless of other elements
        self._create_footer()
        
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
        self.info_frame = ctk.CTkFrame(self.preview_frame, fg_color="transparent")
        self.info_frame.pack(side="left", fill="both", expand=True)
        
        self.title_label = ctk.CTkLabel(
            self.info_frame,
            text="Video Title",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS["text_primary"],
            anchor="w",
            wraplength=500
        )
        self.title_label.pack(fill="x", pady=(0, 8))
        
        # Meta info
        meta_frame = ctk.CTkFrame(self.info_frame, fg_color="transparent")
        meta_frame.pack(fill="x", pady=(0, 10))
        
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
        
        # Chapters label (hidden by default, shown when chapters detected)
        self.chapters_label = ctk.CTkLabel(
            meta_frame,
            text="",
            font=ctk.CTkFont(size=13),
            text_color=COLORS["accent_purple"]
        )
        self.chapters_label.pack(side="left", padx=(0, 16))
        
        # Chapters button (hidden by default)
        self.chapters_button = ModernButton(
            meta_frame,
            text="Download Chapters",
            style="secondary",
            width=160,
            command=self._show_chapters_dialog
        )
        # Will be packed when chapters are detected
        
        # Format selection label
        ctk.CTkLabel(
            self.info_frame,
            text="SELECT QUALITY",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=COLORS["text_tertiary"]
        ).pack(anchor="w", pady=(0, 8))
        
        # Format cards container (scrollable)
        self.formats_scroll = ctk.CTkScrollableFrame(
            self.info_frame,
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
        self.log_panel = LogPanel(self.main_container, height=120)
        self.log_panel.pack(fill="x", pady=(0, 8))  # Changed from fill="both", expand=True
        
        # Welcome message
        self.log_panel.log(f"Welcome to {APP_NAME} v{APP_VERSION}", "info")
        self.log_panel.log(f"yt-dlp version: {self.ytdlp.get_version()}", "info")
    
    def _create_footer(self):
        """Create footer with output path and buttons."""
        self.footer = ctk.CTkFrame(self.main_container, fg_color="transparent", height=40)
        self.footer.pack(fill="x", side="bottom", pady=(0, 5))  # Pack at bottom to ensure visibility
        self.footer.pack_propagate(False)  # Prevent footer from shrinking
        
        # Output path
        path_frame = ctk.CTkFrame(self.footer, fg_color="transparent")
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
        btn_frame = ctk.CTkFrame(self.footer, fg_color="transparent")
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
            except (tk.TclError, RuntimeError):
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
        
        # Update chapters info
        if info.has_chapters:
            self.chapters_label.configure(text=f"{len(info.chapters)} chapters")
            self.chapters_button.pack(side="left")
            self.log_panel.log(f"Found {len(info.chapters)} chapters in video", "success")
        else:
            self.chapters_label.configure(text="")
            self.chapters_button.pack_forget()
        
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
        self.log_panel.log("Strategy: Download once â†’ Encode once â†’ Split into chapters (fast)", "info")
        
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
                except OSError:
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
        self.progress_label.configure(text=f"Completed: {count} chapters extracted")
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
                    
                    # v17.7.5: Show detailed status if available (e.g., "Merging streams...")
                    if task.status_detail:
                        stage_text = task.status_detail
                        
                elif task.status == DownloadStatus.CONVERTING:
                    stage_name = "converting"
                    fmt = task.selected_format
                    
                    # v17.7.5: Prefer status_detail if available (shows file size during stalls)
                    if task.status_detail:
                        stage_text = task.status_detail
                    elif fmt and fmt.height:
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
                
                # v17.7.5: Show file size if available during stalls
                speed_text = ""
                if task.download_speed:
                    speed_text = task.download_speed
                elif task.current_file_size and task.current_file_size > 0:
                    # Show current file size when no speed available
                    if task.current_file_size >= 1024 ** 3:
                        speed_text = f"{task.current_file_size / (1024 ** 3):.2f} GB"
                    elif task.current_file_size >= 1024 ** 2:
                        speed_text = f"{task.current_file_size / (1024 ** 2):.1f} MB"
                    else:
                        speed_text = f"{task.current_file_size / 1024:.1f} KB"
                
                self.speed_label.configure(text=speed_text)
                
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
YouTube 4K Downloader v17.8 - Help

QUICK START
1. Paste a YouTube URL (or drag & drop)
2. Click "Analyze" to see available formats
3. Select your preferred quality
4. Click "Download" or press Cmd+Return

NEW IN V17.8 - CHAPTER DOWNLOADS
- Download videos split by chapters!
- Select individual chapters or download all
- Supports both video and audio-only extraction
- Files named with chapter number and title
- 10-50x faster using stream copy (no re-encoding per chapter)

100% SELF-CONTAINED
This app includes everything needed - no manual installation required:
- yt-dlp (bundled)
- ffmpeg (bundled)  
- deno JavaScript runtime (bundled)

Just download, drag to Applications, and run!

FEATURES
- Chapter Downloads - Split videos into separate files per chapter
- Settings window - Configure SponsorBlock, subtitles, encoding
- SponsorBlock - Removes sponsor segments after download
- History browser - Search and manage download history
- Playlist support - Download entire playlists
- Audio-only mode - M4A/MP3 with proper metadata
- Drag & drop URLs - Drop a YouTube link onto the window
- QuickTime Compatible - H.264 + AAC for native macOS playback

KEYBOARD SHORTCUTS
- Cmd+V - Paste URL from clipboard
- Cmd+Return - Start download
- Enter - Analyze URL

CHAPTER DOWNLOADS
When a video has chapters:
1. Click "Analyze" to load video info
2. A purple "Download Chapters" button appears
3. Select which chapters to download
4. Choose "Audio Only" for audio extraction
5. Each chapter becomes a separate file!

Files are saved like:
  Video Title/
    01 - Introduction.mp4
    02 - Getting Started.mp4
    03 - Advanced Topics.mp4

OPTIONS
- Video + Audio: Download complete video
- Audio Only: Extract audio as M4A/MP3
- QuickTime Compatible: Apple-optimized encoding
- SponsorBlock: Remove sponsor segments
- Subtitles: Download and embed multiple languages
- Trim: Cut start/end of videos

TROUBLESHOOTING
"App is damaged" error:
  Run in Terminal: xattr -cr /Applications/YouTube\\ 4K\\ Downloader.app

App won't open:
  Right-click the app > Select "Open" > Click "Open" in dialog

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
