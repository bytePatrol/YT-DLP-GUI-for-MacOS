# Changelog

All notable changes to YouTube 4K Downloader will be documented in this file.

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
- Improved parsing of yt-dlp's format table output to handle `â”‚` separator characters
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

No Homebrew or manual installation required.
