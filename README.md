# YouTube 4K Downloader for macOS

A modern, fully self-contained YouTube video downloader with a beautiful dark mode interface. No dependencies required - just download and run!

## Screenshots

### Main Interface
<img src="assets/screenshot.png" width="700" alt="YouTube 4K Downloader Main">

### Settings
<img src="assets/screenshot-settings.png" width="500" alt="Settings Window">

### Download Progress
<img src="assets/screenshot-download.png" width="700" alt="Download Progress">

## Features

- **ðŸŽ¬ 4K/1080p/720p Downloads** - Select your preferred quality
- **ðŸŽ¨ Modern Dark Mode UI** - Beautiful iOS-inspired interface
- **ðŸ“¦ 100% Self-Contained** - No Homebrew, no Python, no dependencies
- **âš¡ Fast Downloads** - Separate video+audio download with smart merging
- **ðŸŽµ Audio Only Mode** - Extract audio as M4A or MP3
- **ðŸ“‹ Playlist Support** - Download entire playlists
- **âœ‚ï¸ SponsorBlock Integration** - Automatically remove sponsor segments
- **ðŸ“ Subtitles** - Download and embed subtitles
- **ðŸŽ QuickTime Compatible** - H.264 + AAC encoding for native macOS playback
- **ðŸ“Š Progress Tracking** - Real-time speed, ETA, and progress display
- **ðŸ”” Notifications** - macOS notifications when downloads complete
- **ðŸ“œ Download History** - Browse and search past downloads

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
python yt_dlp_gui_v17.7.3.py
```

## Usage

1. **Paste a YouTube URL** - Copy a YouTube link and it will auto-detect, or paste manually
2. **Click Analyze** - View available formats and quality options
3. **Select Quality** - Choose from 4K, 1080p, 720p, etc.
4. **Click Download** - Watch the progress with real-time stats

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
- Apple Silicon (M1/M2/M3) or Intel Mac
- ~200MB disk space

## Tech Stack

- **Python 3** - Core application
- **CustomTkinter** - Modern UI framework
- **yt-dlp** - Video downloading engine
- **ffmpeg** - Video processing and encoding
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

⭐ If you find this useful, please star the repository!
