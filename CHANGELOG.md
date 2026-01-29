# Changelog

All notable changes to YouTube 4K Downloader will be documented in this file.

## [18.5.0] - 2026-01-29

### 🍪 Burner Account Cookie Management

Comprehensive cookie management system to protect your personal YouTube account!

**Browser Profile Detection**
- Automatically detects browser profiles for Chrome, Firefox, Edge, and Safari
- Shows profile names and identifies which are likely personal accounts
- Select specific profiles instead of just selecting a browser

**New Cookies Tab in Settings**
- Dedicated "Cookies" tab (first tab for easy access)
- Browser and profile dropdowns with auto-detection
- Visual warnings for "Default" profiles (likely personal accounts)
- Cookie status display with last test time
- "Test Cookies" button to verify authentication
- "Open Browser Profile" button for quick sign-in

**Burner Account Setup Guide**
- In-app step-by-step guide for creating burner accounts
- Separate instructions for Chrome/Edge, Firefox, and Safari
- Tips for using temporary email services
- Warnings about protecting your personal account

**Technical Improvements**
- Profile-specific cookie extraction using yt-dlp's `BROWSER:PROFILE` syntax
- Firefox profile directory detection (handles random prefixes like `ef91sfop.yt-burner`)
- Faster format fallback - switches to alternative format after first failure instead of third
- Improved cookie test that recognizes "signature solving" warnings as success

### Fixed
- Update dialog buttons now display correctly (was using undefined color)
- App icon displays properly (was showing ¥ symbol)
- Various emoji encoding issues throughout the UI

---

## [18.1.x] - January 2026

### 18.1.4 - YouTube 403 Fix
- Fixed YouTube blocking `android_sdkless` client causing 403 errors
- Added yt-dlp nightly build support for latest YouTube fixes
- Improved retry logic with longer delays (10s, 20s, 30s, 45s, 60s)
- Better error messages with actionable solutions

### 18.1.3 - Unified Retry System
- All downloads use unified retry system with 6 attempts
- Progressive delays between retries
- True 4K downloads (fixed issue where 4K was actually upscaled 1080p)
- Better progress feedback during encoding

### 18.1.2 - Playlist Reliability
- Automatic retry for failed playlist videos
- Detailed error reporting (age-restricted, private, region-locked)
- Temp file cleanup before retries

### 18.1.1 - Mix Playlist Handling
- Detects YouTube Mix playlists (auto-generated "Radio" playlists)
- Automatic fallback to single video mode for Mix playlists

### 18.1.0 - Full Playlist Support
- Download entire YouTube playlists with video selection
- Smart URL detection for playlist vs single video
- Playlist selection dialog with Select All/Deselect All
- Quality selection for all videos at once
- Audio-only playlist mode
- Organized output with numbered filenames

---

## [18.0.x] - January 2026

### 18.0.8 - Smart Error Detection
- Intelligently detects why videos can't be downloaded
- Clear instructions for age-restricted, private, and region-locked content

### 18.0.7 - Chapter Downloads
- Download videos split by their chapters
- Chapter selection dialog
- Audio-only chapter extraction

### 18.0.6 - Auto-Update yt-dlp
- Update yt-dlp directly from within the app
- One-click stable or nightly updates
- No admin required

### 18.0.0 - Complete Redesign
- Modern dark mode interface with iOS-inspired design
- Glass morphism design with beautiful translucent effects
- Collapsible activity log
- History browser for past downloads
- SponsorBlock integration
- Subtitle support
- GPU/CPU encoding options

---

For full version history, see the [GitHub releases](https://github.com/bytePatrol/YT-DLP-GUI-for-MacOS/releases).
