# Changelog

All notable changes to YouTube 4K Downloader will be documented in this file.

## [18.1.3] - 2026-01-28

### 🔄 Unified Retry System
- **All downloads now use a unified retry system** with 6 total attempts (5 retries + 1 initial)
- **Progressive delays between retries**: 5s, 10s, 15s, 20s, 25s - gives YouTube time to lift rate limits
- **Silent retries for first 2 attempts** - only logs if problem persists after 3rd failure
- Shows "Waiting Xs for YouTube..." during retry delays so app doesn't appear frozen
- Applies to: main downloads, chapter downloads, playlist downloads (video and audio)

### 🎬 True 4K Downloads
- **FIXED: 4K downloads were actually downloading 1080p and upscaling to fake 4K!**
- Now correctly prioritizes RESOLUTION over codec for 4K+ content
- YouTube only offers H.264 up to 1080p; 4K requires VP9/AV1 codecs
- For 1080p and below, still prefers H.264 for hardware decoding benefits
- Resolution is verified after download to ensure you get true 4K quality

### 🔧 403 Forbidden Error Fixes
- Removed forced `player_client` settings that YouTube was actively blocking
- Lets yt-dlp use its default player client selection (much more reliable)
- Better detection of incomplete downloads (.part files no longer falsely reported as success)
- Validates file size to ensure downloads are actually complete

### 📊 Better Progress Feedback
- Chapter encoding now shows **FPS, Speed, and ETA** during conversion
- Progress bar updates during retry waits so app doesn't appear frozen
- Cleaner Activity Log - removed alarming ERROR messages during normal retries
- Filtered confusing yt-dlp warnings (ffmpeg installation, DASH m4a, etc.)

### 🍎 macOS Improvements  
- Fixed "Install ffmpeg" warning by passing `--ffmpeg-location` to yt-dlp
- Uses ffmpeg instead of ffprobe for resolution detection (ffprobe not bundled)
- Clear explanation of CPU usage during 4K encoding:
  - VP9 **decoding** uses CPU (unavoidable on macOS - no hardware VP9 decoder)
  - H.264 **encoding** uses Apple Media Engine (VideoToolbox)
- VideoToolbox hardware encoder confirmation in logs

### 📁 File Handling Improvements
- Better temp file detection with multiple search strategies
- Handles yt-dlp naming variations (format IDs in filenames like `video.f313.webm`)
- Longer waits for file system sync to prevent race conditions
- Validates file size (>10KB) to ensure downloads are complete

## [18.1.2] - 2026-01-26

### Added
- **Automatic Retry for Playlist Downloads** - Failed videos are automatically retried once before marking as failed
- **Detailed Error Reporting for Playlists** - Activity log now shows specific reasons for failed downloads:
  - Age-restricted videos
  - Private videos
  - Region-locked content
  - Copyright-removed videos
  - Videos requiring authentication
- **Temp File Cleanup Before Retry** - Leftover temp files are cleaned up before each retry attempt

### Fixed
- **Help Button Encoding** - Fixed broken â" emoji in the Help button
- **Help Window Toggle** - Clicking Help twice now closes the window instead of opening duplicates
- **Updated Help Content** - Help now reflects v18.1 features including playlist support, YouTube Mix handling, and troubleshooting tips

### Changed
- Playlist download loop now uses new `_download_single_playlist_item_with_error()` that returns error details
- Added `_extract_ytdlp_error()` helper to parse meaningful error messages from yt-dlp stderr
- Added `_cleanup_temp_files()` helper to remove partial downloads before retry
- Help window made taller (700px) to accommodate more content

## [18.1.1] - 2026-01-26

### Added
- **YouTube Mix/Radio Playlist Detection** - App now properly detects auto-generated playlists that cannot be enumerated
  - Playlists starting with `RD` prefix (YouTube Mix/Radio) are detected early
  - Clear error message explaining why Mix playlists can't be downloaded as playlists
  - Automatic fallback to single-video mode when a Mix URL contains a video ID
- **New Exception Class** - `UnviewablePlaylistError` for handling special playlist types

### Fixed
- **"This playlist type is unviewable" error** - No longer shows cryptic yt-dlp error message
- URLs like `watch?v=xxx&list=RDxxx` now automatically switch to single-video mode
- Improved error handling for other unviewable/private playlists

### Changed
- Playlist mode toggle automatically disabled when falling back from Mix playlists
- Activity log shows detailed explanation of why Mix playlists aren't supported
- URL entry is updated to clean single-video URL when falling back

## [18.1.0] - 2026-01-26

### Added
- **Full Playlist Download Support** - Download entire YouTube playlists with video selection
  - Smart URL detection: Explicit playlist URLs auto-enable playlist mode
  - Toggle switch appears for URLs with both video and playlist context (e.g., `watch?v=xxx&list=yyy`)
  - Playlist selection dialog shows all videos with checkboxes, durations, and channels
  - Select All / Deselect All buttons for quick selection
  - Quality dropdown (Best/4K/1440p/1080p/720p/480p) for batch downloads
  - Audio-only mode for extracting audio from all selected videos
  - Downloads saved to organized folder: `PlaylistTitle/01 - VideoTitle.mp4`
  - Progress tracking shows current video and overall playlist progress
- **New Data Structures**
  - `ParsedYouTubeURL` - Smart URL parsing to extract video ID, playlist ID, and URL type
  - `PlaylistItem` - Represents individual videos in a playlist with metadata
  - `PlaylistSelectionWindow` - Modern dialog for selecting playlist videos to download
- **Playlist Settings Integration** - Existing settings now functional:
  - "Download all videos by default" - Pre-selects all videos in playlist dialog
  - "Reverse order (oldest first)" - Reverses video order in selection
  - "Max videos" - Limits number of videos shown/downloaded

### Changed
- URL input now shows playlist toggle when URL contains playlist context
- Analysis detects explicit playlist URLs vs video-in-playlist URLs
- `clean_youtube_url()` uses new `ParsedYouTubeURL` for smarter URL handling

### Technical Details
- `fetch_playlist_info()` uses `--flat-playlist` for fast metadata fetch (60s timeout)
- Batch download processes videos sequentially with per-video error handling
- Failed videos don't stop the batch - summary shows success/failure counts
- Timeout protection: 300s for downloads, 600s for ffmpeg merge operations

## [18.0.9] - 2026-01-26

### Fixed
- **Fixed timeout when analyzing URLs with playlist parameters** - URLs like `watch?v=xxx&list=yyy&index=5` no longer cause "yt-dlp took too long to respond" errors
- Playlist/index parameters are now stripped from URLs when analyzing single videos
- Added `--no-playlist` flag to yt-dlp commands to prevent playlist metadata fetching
- Added `clean_youtube_url()` helper function to sanitize URLs before processing

### Changed
- Replaced `--flat-playlist` with `--no-playlist` for faster single-video analysis
- URLs with playlist parameters now work the same as clean video URLs

## [18.0.8] - 2026-01-24

### Added
- **Age-restricted video detection** - App now properly detects and reports age-restricted videos with helpful instructions
- **Private video detection** - Clear error message when attempting to download private videos
- **Video unavailable detection** - Handles deleted, region-blocked, and copyright-claimed videos
- **Login required detection** - Identifies members-only and subscription content
- Custom exception classes for specific YouTube error types with user-friendly messages
- Detailed Activity Log output with step-by-step instructions for workarounds

### Fixed
- **Restored all emoji icons** - UI emojis now display correctly
- **Fixed lambda closure bug** - Exception handlers in threaded analysis now properly capture error objects
- **Removed duplicate exception classes** - Cleaned up duplicate YtDlpError class definitions that were causing issues
- App no longer appears frozen when analyzing problematic videos - proper error feedback is shown

### Changed
- All UI elements now use proper UTF-8 encoding
- Activity Log messages include status emojis for better visual feedback
- Error dialogs provide specific instructions based on the type of error encountered

## [18.0.7] - 2026-01-24

### Added
- **Age-restricted video detection** - App now properly detects and reports age-restricted videos instead of appearing frozen
- Custom exception classes for specific YouTube errors:
  - `AgeRestrictedError` - For videos requiring age verification
  - `PrivateVideoError` - For private videos
  - `VideoUnavailableError` - For deleted, removed, or region-blocked videos
  - `LoginRequiredError` - For members-only or subscription content
- Detailed error messages in the Activity Log explaining why a video cannot be downloaded
- User-friendly dialog boxes with specific instructions for each error type
- Instructions for using `--cookies-from-browser` workaround for age-restricted content

### Changed
- `fetch_full_info()` now parses yt-dlp errors to identify specific failure reasons
- `_analyze()` method now handles each error type with appropriate user feedback
- Error logging now includes visual separators and step-by-step instructions

### Fixed
- App no longer appears frozen when analyzing age-restricted videos
- Users now receive clear feedback about why certain videos cannot be downloaded

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

---

## Installation

Download the latest `.app` from the [Releases](https://github.com/bytePatrol/YT-DLP-GUI-for-MacOS/releases) page and drag it to your Applications folder.

## Requirements

The app is fully self-contained with bundled dependencies:
- yt-dlp (bundled)
- ffmpeg (bundled)
- deno (bundled)

**No Homebrew or manual installation required.**
