# Changelog

All notable changes to YouTube 4K Downloader will be documented in this file.

## [18.0.2] - 2026-01-22

### 🎉 MAJOR RELEASE: Complete UI/UX Redesign

This is a major update featuring a complete visual overhaul with modern 2026 design standards.

### Added
- **App Update Checker** - Automatically checks for new app versions on GitHub
  - Shows notification dialog when updates are available
  - Displays changelog and release notes
  - One-click link to download page
- **Two-Column Layout** - Video/progress on left, activity log on right
- **Real-time System Resource Gauges** - CPU, Memory, and GPU usage displays in footer
- **Glass Morphism Design** - Modern semi-transparent backgrounds with blur effects
- **Purple-Blue Gradient Accents** - Beautiful gradient color scheme throughout

### Fixed
- **NO-SCROLL LAYOUT** - Everything now fits without scrolling at any window size
- **"Best" badge no longer overlaps resolution text** - Now displays inline as "⭐1080p"
- **Progress bar and metrics always fully visible** - No more cut-off sections
- **Resource gauges always visible in footer** - CPU/Memory/GPU monitors no longer hidden

### Changed
- Complete visual overhaul with contemporary design standards
- Removed ScrollableFrame - using pure grid layout for better performance
- Much more compact design throughout:
  - Header reduced from 72px to 56px
  - URL input reduced from 64px to 48px
  - Thumbnail reduced from 180x101 to 160x90
  - Format cards: smaller padding, single-line details
  - Progress section: tighter spacing
  - All fonts slightly smaller for better density
- Video section now uses grid row 0 (expands), progress uses row 1 (fixed)
- Wider minimum window size (1200x800) optimized for two-column layout

### Design Highlights
- 🎨 Glass morphism effects with semi-transparent backgrounds
- 💫 Purple-blue gradient color scheme (#667eea → #764ba2)
- 📐 Responsive flexbox layout with no cut-off sections
- 🎯 Collapsible activity log panel (max 200px, scrollable)
- 📱 Modern card-based interface with generous spacing
- ✨ Smooth hover effects and transitions
- 🔘 Larger touch targets (56-60px buttons)
- 💎 Softer corners (16-20px border radius)

## [18.0.1] - 2026-01-22

### Fixed
- **Resource gauges (CPU/Memory/GPU) now in footer** - Always visible without scrolling
- **Gauges no longer cut off** even on smaller screens
- **Download metrics (Speed/FPS/ETA/Size) always visible** in compact inline row

### Changed
- More compact video card with smaller thumbnail and tighter spacing
- More compact format cards (quality selection buttons)
- More compact progress section with inline metrics bar
- Footer shows system resources alongside output path
- Overall ~30% reduction in vertical space usage

## [18.0.0] - 2026-01-22

### Added
- **Complete Visual Overhaul** - 2026 modern design standards
- **Glass Morphism Effects** - Semi-transparent backgrounds with blur
- **Purple-Blue Gradient Color Scheme** - Modern accent colors
- **Collapsible Activity Log** - Saves space, max 200px height
- **Responsive Layout** - Fixed header/footer, scrollable content
- **Real-time System Monitoring** - CPU, Memory, GPU gauges (requires psutil)
- **Larger Modern Buttons** - 56-60px height for better touch targets
- **Icon-First Header Design** - Circular icon buttons
- **Enhanced Progress Section** - Cleaner metrics display
- **Improved Quality Cards** - Better visual hierarchy
- **Smooth Hover Effects** - Transitions throughout

### Changed
- Better spacing and padding (20-24px standard)
- Softer border radius (16-20px vs 8-10px)
- All v17.10 features maintained (auto-update, chapters, SponsorBlock, etc.)

### Technical
- New `SystemMonitor` class for real-time resource tracking
- New `ResourceGauge` widget for RPM-style displays
- Requires `psutil` package for system monitoring (optional but recommended)

---

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
