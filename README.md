# YouTube 4K Downloader for macOS

A modern, fully self-contained YouTube video downloader with a beautiful dark mode interface. No dependencies required - just download and run!

## Screenshots

### Main Interface
<img src="assets/screenshot.png" width="700" alt="YouTube 4K Downloader Main">

### Chapter Downloads (NEW in v17.8)
<img src="assets/chapters.png" width="700" alt="Chapter Downloads">

### Chapter Selection Dialog
<img src="assets/screenshot-chapters.png" width="700" alt="Chapter Selection Dialog">

### Settings
<img src="assets/screenshot-settings.png" width="500" alt="Settings Window">

### Download Progress
<img src="assets/screenshot-download.png" width="700" alt="Download Progress">

## Features

- **🎬 4K/1080p/720p Downloads** - Select your preferred quality
- **📚 Chapter Downloads** - Split videos into separate files per chapter
- **🎨 Modern Dark Mode UI** - Beautiful iOS-inspired interface
- **📦 100% Self-Contained** - No Homebrew, no Python, no dependencies
- **⚡ Fast Downloads** - Separate video+audio download with smart merging
- **🎵 Audio Only Mode** - Extract audio as M4A or MP3
- **📋 Playlist Support** - Download entire playlists
- **✂️ SponsorBlock Integration** - Automatically remove sponsor segments
- **📝 Subtitles** - Download and embed subtitles
- **🎬 QuickTime Compatible** - H.264 + AAC encoding for native macOS playback
- **📊 Progress Tracking** - Real-time speed, ETA, and progress display
- **🔔 Notifications** - macOS notifications when downloads complete
- **📜 Download History** - Browse and search past downloads

## NEW: Chapter Downloads (v17.8)

Download YouTube videos split by their chapters! Perfect for:
- **Podcasts** - Download each topic as a separate file
- **Music compilations** - Extract individual songs
- **Tutorials** - Get specific sections you need
- **Long videos** - Download only the chapters you want

### How to use:
1. Analyze a YouTube video that has chapters
2. A purple **"Download Chapters"** button will appear
3. Select which chapters to download (or download all)
4. Choose **Audio Only** if you just want the audio
5. Click Download - each chapter becomes a separate file!

### Output Structure:
```
Video Title/
├── 01 - Introduction.mp4
├── 02 - Getting Started.mp4
├── 03 - Advanced Topics.mp4
└── ...
```

### Performance:
Chapter downloads are **10-50x faster** than previous methods! The app downloads and encodes the video once, then uses stream copy to split into chapters (no re-encoding per chapter).

## Installation

### Option 1: Download the App (Recommended)

1. Go to the [Releases](https://github.com/bytePatrol/YT-DLP-GUI-for-MacOS/releases) page
2. Download `YouTube.4K.Downloader.app.zip`
3. Unzip and drag to your Applications folder
4. **Important:** Right-click the app and select **"Open"** (required for first launch)

### ⚠️ "App is Damaged" or "Can't Be Opened" Error?

This is a macOS Gatekeeper issue, not actual damage. Fix it by running this in Terminal:

```bash
xattr -cr /Applications/YouTube\ 4K\ Downloader.app
```

Then open the app normally. This only needs to be done once.

### Option 2: Run from Source

```bash
# Clone the repository
git clone https://github.com/bytePatrol/YT-DLP-GUI-for-MacOS.git
cd YT-DLP-GUI-for-MacOS

# Install dependencies
pip install customtkinter pillow requests yt-dlp

# Run the app
python yt_dlp_gui_v17_8_8.py
```

## Usage

1. **Paste a YouTube URL** - Copy a YouTube link and it will auto-detect, or paste manually
2. **Click Analyze** - View available formats and quality options
3. **Select Quality** - Choose from 4K, 1080p, 720p, etc.
4. **Click Download** - Watch the progress with real-time stats
5. **For Chapters** - Click the purple "Download Chapters" button if available

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `⌘V` | Paste URL from clipboard |
| `⌘Return` | Start download |
| `Return` | Analyze URL |

## Settings

Access settings via the **Settings** button to configure:

- **SponsorBlock** - Enable/disable, select categories to remove
- **Subtitles** - Languages, auto-generated, embedding
- **Encoding** - GPU/CPU, preset, bitrate modes
- **Trim** - Set start/end times
- **Playlist** - Download options for playlists

## System Requirements

- macOS 10.13 (High Sierra) or later
- Apple Silicon (M1/M2/M3/M4) or Intel Mac
- ~200MB disk space

## Tech Stack

- **Python 3** - Core application
- **CustomTkinter** - Modern UI framework
- **yt-dlp** - Video downloading engine (bundled)
- **ffmpeg** - Video processing and encoding (bundled)
- **deno** - JavaScript runtime for yt-dlp (bundled)
- **py2app** - macOS app bundling

## Building from Source

```bash
# Clone and enter directory
git clone https://github.com/bytePatrol/YT-DLP-GUI-for-MacOS.git
cd YT-DLP-GUI-for-MacOS

# Build using the build script (recommended)
./build_app.sh

# Or manually:
pip install py2app customtkinter pillow requests yt-dlp
python setup.py py2app
```

## Troubleshooting

### "App is damaged and can't be opened"
This is a Gatekeeper issue. Run in Terminal:
```bash
xattr -cr /Applications/YouTube\ 4K\ Downloader.app
```

### "App can't be opened because it is from an unidentified developer"
Right-click the app → Select "Open" → Click "Open" in the dialog.

### App launches but immediately crashes
Run this in Terminal to see the error:
```bash
/Applications/YouTube\ 4K\ Downloader.app/Contents/MacOS/YouTube\ 4K\ Downloader
```

### Downloads fail or no formats shown
- Make sure you have an internet connection
- Try updating yt-dlp: The bundled version may be outdated for some videos
- Some videos may be region-locked or private

### Chapter downloads not showing
- Not all YouTube videos have chapters defined
- Chapters must be set by the video creator
- Try a video known to have chapters (like podcasts or music compilations)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The amazing video download library
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern UI framework
- [SponsorBlock](https://sponsor.ajay.app/) - Community-driven sponsor segment database

## Author

**bytePatrol**

---

⭐ If you find this useful, please star the repository!
