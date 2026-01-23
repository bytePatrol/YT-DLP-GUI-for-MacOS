# Changelog

All notable changes to YouTube 4K Downloader will be documented in this file.

## [18.0.6] - 2026-01-23

### Fixed
- **Update Available dialog now shows buttons** - "Download Update" and "Remind Me Later" buttons were being cut off at the bottom of the dialog
- Removed duplicate `UpdateNotificationDialog` class that was causing issues
- Fixed changelog frame height to ensure buttons are always visible
- Cleaned up corrupted emoji characters in button text

### Changed
- Updated README with correct first-launch instructions for macOS Gatekeeper
- Installation instructions now explain the System Settings → Privacy & Security → "Open Anyway" workflow
- Added `psutil` to the list of required dependencies in README

## [17.10.0] - 2026-01-21

### Added
- **Auto-update yt-dlp from GitHub releases!** No more re-downloading the entire app when yt-dlp updates
- Update button in header with visual indicator (turns orange when update available)
- Background check for updates on app launch (configurable in settings)
- YtDlpUpdater class for managing yt-dlp binary downloads and installation
- User-installed yt-dlp stored in `~/Library/Application Support/YouTube 4K Downloader/`
- Version caching for faster startup

### Changed
- `find_executable()` now checks user-installed yt-dlp location first
- YtDlpInterface now has `refresh_path()` method to pick up updates
- Updated help text with auto-update instructions
- Settings now include `ytdlp_auto_update_check` option

### Technical Details
- Downloads standalone `yt-dlp_macos` binary (universal for ARM64 and Intel)
- Verifies downloaded binary before replacing existing one
- Removes macOS quarantine attribute automatically
- Progress shown in main progress bar during download
- All operations are non-blocking with proper threading

## [17.9.0] - 2026-01-20

### Security
- **Fixed shell injection vulnerability** in macOS notifications - malicious video titles could no longer execute arbitrary AppleScript commands
- Added input sanitization (escaping `\`, `"`, `'`) in `send_notification()` function
- Added input truncation (100/200 char limits) to prevent buffer overflow attacks
- Added subprocess timeouts to prevent hanging:
  - `get_version()`: 10 second timeout
  - `fetch_video_info()`: 30 second timeout
  - `fetch_full_info()`: 30 second timeout
  - `send_notification()`: 5 second timeout

### Changed
- **Complete documentation overhaul** - Added comprehensive Google-style docstrings to all 25+ classes and functions
- Replaced 200+ lines of version history in file header with professional module documentation
- Added architecture overview documenting UI Layer, Business Logic Layer, and Data Layer
- Version history now references CHANGELOG.md instead of inline comments

### Fixed
- **Eliminated all bare `except:` clauses** - Now uses specific exception types:
  - `except ValueError:` for parsing errors
  - `except (ValueError, AttributeError):` for settings validation
  - `except (ValueError, TypeError):` for numeric conversions
  - `except (tk.TclError, RuntimeError):` for widget destruction
  - `except (subprocess.TimeoutExpired, OSError, ValueError):` for subprocess calls
  - `except OSError:` for file operations
- Removed all debug print statements for cleaner production output
- Improved type hints with explicit return types (`-> None`, `-> str`, etc.)
- Consistent code formatting and whitespace cleanup

### Documentation
- `VideoFormat`: Full attribute descriptions for all 16 fields
- `Chapter`: Chapter metadata and duration properties explained
- `VideoInfo`: Complete video metadata documentation
- `DownloadTask`: All 18 attributes documented with types and descriptions
- `SponsorBlockAPI`: API usage and privacy-preserving hash mechanism
- `YtDlpInterface`: Multiple execution modes documented with examples
- `DownloadManager`: Thread-safety and callback system explained
- All UI widgets: `EnhancedProgressBar`, `ModernButton`, `FormatCard`, etc.
- All dialog windows: `SettingsWindow`, `HistoryBrowserWindow`, `ChapterSelectionWindow`

## [17.8.8] - 2026-01-19

### Fixed
- **History now saves correctly** - Downloads were being saved to wrong file path (`~/.yt_dlp_gui_v16_history.json` instead of `~/.config/yt-dlp-gui/history.json`)

### Changed
- Updated Help menu with accurate, current information
- Removed outdated references to manual yt-dlp/ffmpeg installation (app is 100% self-contained)
- Fixed broken emoji/unicode characters throughout the codebase
- Updated documentation to highlight chapter download features

## [17.8.7] - 2026-01-19

### Changed
- SponsorBlock is now automatically disabled for chapter downloads
- Added notice in SponsorBlock settings explaining chapter download limitation
- Added notice in chapter selection window about SponsorBlock being disabled
- This prevents potential issues with chapter extraction and SponsorBlock conflicts

## [17.8.6] - 2026-01-19

### Fixed
- **Footer no longer disappears after clicking Analyze**
- Footer (Output path, Open Folder, Change buttons) now stays visible permanently
- Fixed layout issue where dynamically showing video_frame pushed footer off screen
- Log panel no longer expands infinitely, allowing footer to remain visible
- Can now download multiple videos without restarting the app

## [17.8.5] - 2026-01-19

### Changed
- **MAJOR PERFORMANCE FIX: Chapter downloads are now 10-50x faster!**
- New strategy: Download once Ã¢â€ â€™ Encode once Ã¢â€ â€™ Split into chapters
- Old method downloaded and encoded the ENTIRE video for EACH chapter (extremely slow)
- New method uses ffmpeg stream copy to split chapters (instant, no re-encoding)

### Fixed
- Fixed bug where only 3 chapters were output despite selecting more
- Added proper progress tracking through all stages (download/encode/split)
- Temp files are now properly cleaned up after chapter extraction

## [17.8.4] - 2026-01-19

### Fixed
- **Chapter downloads now work with bundled ffmpeg**
- Added `--ffmpeg-location` to chapter extraction commands
- yt-dlp's `--download-sections` requires ffmpeg for partial video extraction
- Error "ffmpeg is not installed" no longer occurs when downloading chapters

## [17.8.3] - 2026-01-19

### Fixed
- **CRITICAL: All downloads now work with YouTube's SABR streaming restrictions**
- Added `--extractor-args youtube:player_client=android_sdkless` to ALL yt-dlp commands
- Added `--remote-components ejs:github` for JavaScript challenge solving
- Fixed chapter downloads failing with "Some web client https formats have been skipped"
- Fixed main video/audio downloads that were also affected by SABR restrictions
- `android_sdkless` client bypasses YouTube's SABR-only enforcement

## [17.8.2] - 2026-01-19

### Fixed
- **App no longer appears frozen during long merge/conversion operations** - Videos with many chapters would cause the app to appear unresponsive for 9+ minutes
- **Analyze button now works** - Fixed UTF-8 encoding issue in `fetch_video_info()` and `fetch_full_info()`
- **Footer stays visible** - Output path and buttons no longer disappear after clicking Analyze
- Progress bar and status now show activity even when ffmpeg/yt-dlp don't output progress percentages

### Added
- **Chapter Downloads Restored** - Download videos split by chapters!
  - Automatically detects YouTube chapters from video metadata
  - Shows chapter count in video info (e.g., "Ã°Å¸â€œÅ¡ 37 chapters")
  - Purple "Download Chapters" button appears when chapters are available
  - Chapter selection dialog with Select All/Deselect All options
  - Support for both video and audio-only chapter extraction
  - Chapter files named with number prefix and chapter title (e.g., "01 - Introduction.mp4")
  - Progress tracking shows current chapter being extracted
  - All chapter files saved to a folder named after the video
- **Real-time file size monitoring** - When progress parsing fails, shows current output file size
- **Detailed status messages** - Status bar shows "Processing chapters...", "Merging streams...", etc.
- **Background file growth detection** - Monitor thread tracks output file growth during stalls

### Changed
- Enhanced `_run_subprocess_with_progress` to detect yt-dlp's `[Merger]` and `[ffmpeg]` phases
- Enhanced `_run_ffmpeg_with_progress` with file monitoring when time-based progress unavailable
- DownloadTask now includes `status_detail` and `current_file_size` fields
- Removed debug print statements from `get_version()`

## [17.7.4] - 2026-01-19

### Fixed
- **Tcl/Tk bundling** - App now bundles Tcl/Tk frameworks to fix "py2app launch issues" error
- Users no longer need to run `brew install tcl-tk` to launch the app
- Build script auto-detects and bundles Tcl/Tk from Python installation
- **Settings window** - Save/Cancel buttons now visible; window is taller and scrollable

### Changed
- **Ad-hoc code signing** - App is now signed to prevent "app is damaged" errors
- Improved dependency bundling for more reliable launches on all Macs
- Build script now uses ASCII-safe output (no more garbled Unicode characters)
- Better verification of bundled components during build

### Added
- Build script now checks for and bundles Tcl.framework and Tk.framework
- Verification step confirms all required frameworks are present

## [17.7.3] - 2026-01-18

### Fixed
- **File size display** - Format cards now correctly show file sizes (e.g., "668 MB") instead of "Unknown"
- Improved parsing of yt-dlp's format table output to handle separator characters
- Better regex matching for file sizes (MiB, GiB, KiB), bitrates, and resolutions
- FPS values now correctly parsed from format table

### Changed
- App renamed from "yt-dlp GUI" to "YouTube 4K Downloader"
- Bundle identifier changed to `com.bytepatrol.youtube4kdownloader`

## [17.7.2] - 2026-01-18

### Changed
- Rebranded app from "yt-dlp GUI" to "YouTube 4K Downloader"
- Updated window title, help text, and all UI references

## [17.7.1] - 2026-01-17

### Fixed
- Minor bug fixes and stability improvements

## [17.7.0] - 2026-01-17

### Added
- **SponsorBlock post-processing** - Now works reliably by querying SponsorBlock API after download
- Segments are fetched and removed via ffmpeg re-encoding
- Detailed segment information shown in activity log

### Fixed
- SponsorBlock now actually removes sponsor segments (previous versions had integration issues)

## [17.6.0] - 2026-01-16

### Changed
- Reverted to proven separate download strategy (fast, reliable)
- Using bundled ffmpeg for QuickTime-compatible encoding (H.264 + AAC)
- SponsorBlock kept disabled during download phase due to YouTube API restrictions

## [17.4.0] - 2026-01-15

### Changed
- Reverted to separate video+audio download strategy (known to work reliably)
- Disabled SponsorBlock in download commands (not compatible with current YouTube API)
- SponsorBlock UI remains but feature was non-functional until v17.7.0

## [17.0.0] - 2026-01-10

### Added
- Modern dark mode UI using CustomTkinter
- Fully responsive layout
- Video thumbnails and previews
- Download queue with pause/resume
- Playlist support
- Subtitle downloads
- Persistent settings (stored in `~/.config/yt-dlp-gui/`)
- Self-contained app with bundled ffmpeg and deno
- Per-resolution bitrate settings
- Enhanced progress tracking with ETA
- macOS notifications on completion
- Download history browser
- Drag & drop URL support

### Fixed
- Settings persistence - SponsorBlock, Encoding, etc. now save properly
- Separated settings.json from config.json to prevent overwrites

---

## Installation

Download the latest `.app` from the [Releases](https://github.com/bytePatrol/YT-DLP-GUI-for-MacOS/releases) page and drag it to your Applications folder.

## Requirements

The app is fully self-contained with bundled dependencies:
- yt-dlp (bundled)
- ffmpeg (bundled)
- deno (bundled)

**No Homebrew or manual installation required.**
