# YouTube 4K Downloader for macOS

A modern, fully self-contained YouTube video downloader with a beautiful dark mode interface. No dependencies required, No Ads, No Telemetry, No "Calling Home", No Donation Requests or Nags - just download and run! Our downloader is one of the only working MacOS applications that can download true 4K content directly from YouTube and convert it into MacOS compatible format so that no 3rd party video players are required to watch, plus our script can automatically remove sponsor segments within a video so you're truly getting an ad free experience. Full source code is published for your review.

## Screenshots

### Main Interface
<img src="assets/screenshot.png" width="700" alt="YouTube 4K Downloader Main">

### Chapter Downloads
<img src="assets/chapters.png" width="700" alt="Chapter Downloads">

### Settings
<img src="assets/screenshot-settings.png" width="500" alt="Settings Window">

### Download Progress
<img src="assets/screenshot-download.png" width="700" alt="Download Progress">

## Features

- 🔄 **Auto-Update yt-dlp** - Keep yt-dlp current without re-downloading the app
- 📺 **4K/1080p/720p Downloads** - Select your preferred quality
- 🍪 **Burner Account Cookies** - Protect your personal YouTube account with browser profile support
- 📁 **Chapter Downloads** - Split videos into separate files per chapter
- 🎨 **Modern Dark Mode UI** - Professional redesign with responsive layout
- ✂️ **Per-Video Trimming** - Set start/end times directly on the main screen
- 📦 **100% Self-Contained** - No Homebrew, no Python, no dependencies
- ⚡ **Fast Downloads** - Separate video+audio download with smart merging
- 🎵 **Audio Only Mode** - Extract audio as M4A or MP3
- 📋 **Playlist Support** - Download entire playlists with video selection
- 🛡️ **SponsorBlock Integration** - Automatically remove sponsor segments
- 💬 **Subtitles** - Download and embed subtitles in multiple languages
- 🎬 **QuickTime Compatible** - H.264 + AAC encoding for native macOS playback
- 📊 **Progress Tracking** - Real-time speed, ETA, and progress display
- 🔔 **Notifications** - macOS notifications when downloads complete
- 📜 **Download History** - Browse and search past downloads

## Burner Account Cookie Management

### Protect Your YouTube Account!

YouTube may ban or restrict accounts used for downloading videos. The Burner Account Cookie Management system helps you:

- **Create dedicated browser profiles** for downloading
- **Select specific browser profiles** instead of just browsers
- **Visual warnings** when using "Default" profiles (likely personal accounts)
- **Cookie health monitoring** with status indicators
- **Step-by-step Burner Account Setup Guide** with instructions for Chrome, Firefox, and Edge

### How It Works

1. Go to **Settings > Cookies** tab
2. Enable browser cookies
3. Click **"Burner Account Guide"** to see step-by-step instructions
4. Create a new browser profile (e.g., "YT Downloader")
5. Sign into YouTube with a burner account in that profile
6. Select the profile in the app and test your cookies

### Why Use a Burner Account?

Using your personal YouTube account for downloading can result in:
- Account restrictions or suspension
- Loss of YouTube Premium benefits
- IP address blocking

A burner account protects your main account while still giving you authenticated access for reliable downloads.

### Supported Browsers

| Browser | Profile Support |
|---------|----------------|
| Google Chrome | ✅ Full support |
| Mozilla Firefox | ✅ Full support |
| Microsoft Edge | ✅ Full support |
| Safari | ⚠️ Limited (no multi-profile) |

## Playlist Support

Download entire YouTube playlists with smart video selection!

- **Smart URL Detection** - Automatically detects playlist vs single video URLs
- **Video Selection Dialog** - See all videos with titles, durations, and channels
- **Batch Quality Selection** - Choose quality for all videos at once
- **Audio-Only Mode** - Extract audio from entire playlists
- **Automatic Retry** - Failed videos are retried automatically

### Organized Downloads
```
Playlist Title/
├── 01 - First Video.mp4
├── 02 - Second Video.mp4
├── 03 - Third Video.mp4
└── ...
```

## Chapter Downloads

Download YouTube videos split by their chapters! Perfect for podcasts, music compilations, tutorials, and long videos.

1. Analyze a YouTube video that has chapters
2. Click the purple **"Chapters"** button
3. Select which chapters to download
4. Choose **Audio Only** if you just want the audio
5. Each chapter becomes a separate file!

### Output Structure
```
Video Title/
├── 01 - Introduction.mp4
├── 02 - Getting Started.mp4
├── 03 - Advanced Topics.mp4
└── ...
```

## Auto-Update yt-dlp

YouTube frequently changes their API, which requires yt-dlp updates. Update yt-dlp directly from within the app - no re-download needed!

- **One-click updates** - Stable or nightly builds
- **Automatic check on launch** - Button turns orange when update available
- **Nightly builds** - Get the latest YouTube fixes immediately
- **No admin required** - Updates stored in `~/Library/Application Support/`

## Installation

### Option 1: Download the App (Recommended)

1. Go to the [Releases](https://github.com/bytePatrol/YT-DLP-GUI-for-MacOS/releases) page
2. Download `YouTube.4K.Downloader.app.zip`
3. Unzip and drag to your **Applications** folder

### First Launch

macOS blocks apps from unidentified developers:

1. **Double-click** the app (it will be blocked)
2. Open **System Settings** → **Privacy & Security**
3. Click **"Open Anyway"** next to the blocked app message
4. Future launches work normally

**Alternative:** Run `xattr -cr /Applications/YouTube\ 4K\ Downloader.app` in Terminal

### Option 2: Run from Source

```bash
git clone https://github.com/bytePatrol/YT-DLP-GUI-for-MacOS.git
cd YT-DLP-GUI-for-MacOS
pip install customtkinter pillow requests yt-dlp psutil
python yt_dlp_gui_v19_0_0.py
```

## Usage

1. **Paste a YouTube URL** - Copy a link and paste it (or drag & drop)
2. **Click Analyze** - View available formats and quality options
3. **Select Quality** - Choose from 4K, 1080p, 720p, etc.
4. **Optional: Enable Trim** - Check "Trim video" and set start/end times
5. **Click Download** - Watch the progress with real-time stats

### Trimming Videos

Trim videos directly from the main screen - no need to dig through settings!

1. After analyzing a video, check **"Trim video"**
2. Enter **Start** and **End** times (formats: `1:30`, `0:45`, `1:30:00`)
3. Click **Download** - only the specified portion will be downloaded

Trim settings reset automatically when you analyze a new video.

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Cmd+V` | Paste URL from clipboard |
| `Cmd+Return` | Start download |
| `Return` | Analyze URL |

## Settings

Access settings via the **Settings** button in the header:

| Tab | Options |
|-----|---------|
| **Cookies** | Browser profile selection, burner account setup, cookie testing |
| **SponsorBlock** | Enable/disable, select categories to remove |
| **Subtitles** | Languages, auto-generated, embedding |
| **Encoding** | GPU/CPU, preset, bitrate modes |
| **Playlist** | Default selection, order, max videos |
| **Advanced** | Troubleshooting tips, debug info |

**Note:** Trim controls are now on the main screen (next to quality selection) for convenient per-video trimming.

## System Requirements

- macOS 10.13 (High Sierra) or later
- Apple Silicon (M1/M2/M3/M4) or Intel Mac
- ~200MB disk space

## Troubleshooting

### "403 Forbidden" or download failures

1. **Enable browser cookies** in Settings > Cookies
2. **Use a burner account** (follow the built-in guide!)
3. **Update yt-dlp** to nightly build via the **Update** button
4. **Close your browser** completely before downloading

### "Analysis timed out" error

1. **Wait a few minutes** - YouTube may be rate limiting your IP
2. **Update yt-dlp** to the latest nightly build
3. **Check your internet connection**
4. Try a different network or VPN if issues persist

### "Age-restricted video" error

Enable cookies from a browser where you're signed into YouTube. Use a burner account to protect your personal account.

### "App is damaged" error

```bash
xattr -cr /Applications/YouTube\ 4K\ Downloader.app
```

### Cookie errors

- Close the browser completely (Cmd+Q) before downloading
- Make sure you're signed into YouTube in the selected profile
- Firefox usually works best for cookie extraction

## Building from Source

```bash
git clone https://github.com/bytePatrol/YT-DLP-GUI-for-MacOS.git
cd YT-DLP-GUI-for-MacOS
./build_app.sh
```

## Tech Stack

- **Python 3** + **CustomTkinter** - Modern UI
- **yt-dlp** - Video downloading (bundled, auto-updatable)
- **ffmpeg** - Video processing (bundled)
- **deno** - JavaScript runtime (bundled)
- **py2app** - macOS app bundling

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The amazing video download library
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern UI framework
- [SponsorBlock](https://sponsor.ajay.app/) - Community-driven sponsor segment database

## Author

**bytePatrol**

---

⭐ If you find this useful, please star the repository!
