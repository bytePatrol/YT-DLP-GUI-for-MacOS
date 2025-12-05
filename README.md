# yt-dlp GUI for macOS

A macOS desktop GUI for [yt-dlp](https://github.com/yt-dlp/yt-dlp) and [ffmpeg](https://ffmpeg.org/), written in Python + Tkinter.

I made this GUI because most "downloaders" can only download macOS & iOS compatible YouTube videos in 360P resolution. If you wanted 720P, 1080P or 4K these downloaders would still "work" but your video would not play on macOS & iOS without the use of a 3rd party tool such as Infuse Player.

To resolve this limitation we must use YT-DLP to download the raw high resolution video & audio file directly from YouTube then use ffmpeg to combine & convert to a compatible format (H.264 + AAC MP4) so that it will play natively on macOS or iOS products.

I simply made a GUI to make this entire process easier. The code is well documented for easy modification & tweaking and it ensures its uses the constantly latest updated YT-DLP.

This app makes it easy to:

- Paste a YouTube URL
- Inspect available formats with friendly, rounded labels
- Download **QuickTime-compatible** formats directly (no conversion)
- Download **AV1 mp4 video-only** formats and convert them to H.264 MP4
- Control bitrate, GPU vs CPU encoding, resolution caps and more

Everything is wrapped in a simple desktop GUI with saved preferences and macOS notifications.

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the App](#running-the-app)
  - [Optional: macOS Clickable Launcher](#optional-macos-clickable-launcher)
- [Usage](#usage)
  - [Basic Workflow](#basic-workflow)
  - [Clipboard Auto-Grab](#clipboard-auto-grab)
  - [Header Bar: Version, Updates, Help](#header-bar-version-updates-help)
  - [Simple vs Advanced Mode](#simple-vs-advanced-mode)
  - [Audio-Only Mode](#audio-only-mode)
  - [Format Selection Dialog](#format-selection-dialog)
  - [Bitrate Override & Favorites](#bitrate-override--favorites)
  - [Advanced Options](#advanced-options)
  - [Progress, ETA & Logs](#progress-eta--logs)
  - [Saved Settings](#saved-settings)
  - [macOS Notifications](#macos-notifications)
- [Common Scenarios](#common-scenarios)
- [Troubleshooting](#troubleshooting)
- [Disclaimer](#disclaimer)
- [License](#license)

---

## Features

### High-level

- ✅ macOS desktop GUI (Python + Tkinter)
- ✅ No manual command-line flags needed
- ✅ Smart format inspection via `yt-dlp -J`
- ✅ Auto-sizing window so controls are visible on launch

### Video & audio

- **QuickTime-compatible formats:**
  - Progressive mp4 / m4v / mov (video + audio in one file)
  - H.264 (and optionally HEVC) for easy playback
- **AV1 mp4 video-only formats:**
  - Choose the exact resolution and file size you want
  - Automatically download `bestaudio` and combine via ffmpeg
  - Convert to H.264 + AAC MP4 for maximum compatibility
- **Audio-only mode (m4a):**
  - Download bestaudio and convert to AAC `.m4a` (if ffmpeg is available)

### Encoding & quality control

- **Encoder selection:**
  - GPU: `h264_videotoolbox` (macOS VideoToolbox)
  - CPU: `libx264`
- **Bitrate control:**
  - Global presets: `4M`, `8M`, `16M`
  - Smart source bitrate detection:
    - Use `tbr` / `vbr` from the chosen format when available
    - Fall back to preset if not
  - **Bitrate Override** (per download):
    - Type a value in Mbps (e.g. `10`) for custom H.264 bitrate
- **Per-resolution favorite overrides:**
  - Optional favorites per resolution (2160p / 1440p / 1080p / 720p / 480p)
  - Used as *suggested* overrides when you select a format
  - Never forced; you can edit or clear them per download

### Workflow & UX

- **Simple mode:**
  - Hides advanced encoding controls
  - Hides very low-res QuickTime formats (< 480p) in the picker
- **Advanced mode:**
  - Shows encoder selector, presets, caps, favorites, keep-raw toggle and output folder
- **Analyze Only:**
  - Inspect formats without downloading anything
- **Clipboard auto-grab:**
  - URL field auto-fills from the clipboard when the window gains focus
- **Built-in help panel:**
  - Explains all options inside the app

### Feedback & persistence

- Progress bar with:
  - Stage name (download / encode / mux)
  - Percentage
  - Smoothed ETA
- Full log panel showing `yt-dlp` and `ffmpeg` output
- Summary row + “Open Output Folder” button
- Settings persisted to `~/.yt_dlp_gui_v13_config.json`
- macOS notifications on completion and after update checks

---

## Requirements

- macOS (Apple Silicon or Intel)
- Python **3.12** (or compatible) with `tkinter` available
- [Homebrew](https://brew.sh/) (recommended)
- `yt-dlp` installed (default path in script: `/opt/homebrew/bin/yt-dlp`)
- `ffmpeg` installed (default path in script: `/opt/homebrew/bin/ffmpeg`)

If `yt-dlp` or `ffmpeg` are installed elsewhere, update the constants at the top of the script:

```python
YTDLP_PATH = "/opt/homebrew/bin/yt-dlp"
FFMPEG_PATH = "/opt/homebrew/bin/ffmpeg"
```

## Installation

1. **Install Homebrew** (if you don’t have it):

        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

2. **Install Python + Tk:**

        brew install python@3.12 python-tk@3.12

3. **Install yt-dlp and ffmpeg:**

        brew install yt-dlp ffmpeg

4. **Download the script:**

   Save `yt_dlp_gui_v14.py` somewhere convenient, for example:

    /Users/yourname/Documents/yt_dlp_gui_v14.py

5. **(Optional) Make the script executable:**

    chmod +x ~/Documents/yt_dlp_gui_v14.py


## Running the App

From Terminal:

    cd ~/Documents
    /opt/homebrew/opt/python@3.12/bin/python3.12 yt_dlp_gui_v14.py

Adjust the path if your Python or script location differs (you can also just use `python3` if that’s Python 3.12 with Tk).


### Optional: macOS Clickable Launcher

To create a double-clickable `.app`:

1. Open **Script Editor** (Spotlight → “Script Editor”).
2. Create a new script with:

        do shell script "/opt/homebrew/opt/python@3.12/bin/python3.12 /Users/yourname/Documents/yt_dlp_gui_v14.py >/dev/null 2>&1 &"

3. Save as:
   - **File Format:** Application  
   - **Name:** `yt-dlp GUI Launcher.app`  
   - **Location:** Desktop (or wherever you like)

4. Double-click the new app to launch the GUI.  
   On first run, macOS may ask for confirmation under **System Settings → Privacy & Security**.


## Usage

### Basic Workflow

1. Launch the app.
2. Paste a YouTube URL into the **YouTube URL** field.
   - Or copy a YouTube link and let **clipboard auto-grab** fill it in.
3. Choose:
   - **Audio only (m4a)** if you only need audio, or  
   - Leave it unchecked for full video.
4. Choose **Simple mode** or disable it for advanced controls.
5. Click **Download / Convert**.
6. When the **Format Selection** dialog appears:
   - Choose a QuickTime format (left list) for direct download (no conversion), or
   - Choose an AV1 mp4 video-only format (right list) for download + ffmpeg conversion.
7. Watch the progress bar and log.
8. When finished, check the summary and click **Open Output Folder**.


### Clipboard Auto-Grab

- When the window gains focus, the app checks your clipboard.
- If it looks like a YouTube URL (`https://www.youtube.com/watch?v=...` or `https://youtu.be/...`), it auto-fills the **YouTube URL** field.
- You can still paste or edit the URL manually.


### Header Bar: Version, Updates, Help

- **yt-dlp version label**
  - Runs `yt-dlp --version` at startup and shows `yt-dlp: <version>` in the header.
- **Check for yt-dlp update** button
  - Runs `yt-dlp -U`.
  - Logs output in the Status / Log panel.
  - Shows a dialog and a macOS notification when finished.
- **Help** button
  - Opens a scrollable in-app help panel explaining all features.


### Simple vs Advanced Mode

- **Simple mode ON (default)**
  - Hides advanced encoding options.
  - Hides very low-resolution QuickTime formats (< 480p) in the picker.
- **Simple mode OFF**
  - Shows:
    - GPU / CPU encoder selection
    - Bitrate preset (4M / 8M / 16M)
    - Max resolution cap
    - “Keep raw bestvideo / bestaudio” checkbox
    - Output folder selector
    - Per-resolution favorite bitrate overrides


### Audio-Only Mode

Checkbox: **Audio only (m4a)**

- When enabled:
  - `yt-dlp` downloads `bestaudio` to a temp file.
  - If `ffmpeg` is available, it converts to AAC `.m4a` (192 kbps, `+faststart`).
  - If `ffmpeg` is not available, you keep the raw bestaudio file.
- No video formats or video encoding are used.
- Ideal for music, podcasts, interviews, etc.


### Format Selection Dialog

The dialog appears when:

- You click **Analyze Only**, or  
- You click **Download / Convert** and compatible formats are found.

It has two lists:


#### QuickTime-Compatible (no conversion)

- Progressive formats with:
  - Container: mp4 / m4v / mov  
  - Video + audio in one file  
  - H.264 (and optionally HEVC)
- Displayed as:

    1080P - 705MB - 3.6 Mbps  
    720P  - 379MB - 1.9 Mbps  
    ...

Selecting one and clicking **QuickTime (no conversion)**:

- Uses `yt-dlp` only.
- No ffmpeg step; output is already QuickTime-friendly.


#### Other Formats (AV1 mp4 video-only → convert)

- AV1 video-only formats where:
  - Container: mp4  
  - `vcodec` includes `av01`  
  - `acodec` is empty or `none` (video-only)
- Displayed similarly:

  2160P - 2.6GB - 13.3 Mbps  
  1440P - 1.3GB - 6.6 Mbps  
  ...

Selecting one and clicking **AV1 mp4 + convert**:

1. Downloads the selected AV1 video-only stream.
2. Downloads `bestaudio` separately.
3. Uses ffmpeg to:
   - Combine video + audio
   - Re-encode video to H.264
   - Encode audio to AAC
   - Output an MP4 that plays in QuickTime.


#### Dialog Buttons

- **QuickTime (no conversion)** → Use left list only, yt-dlp only.  
- **AV1 mp4 + convert** → Use right list, yt-dlp + ffmpeg pipeline.  
- **Cancel** → Close the dialog  
  - Cancels the job if you were in Download / Convert.  
  - Just closes inspection if you used Analyze Only.


### Bitrate Override & Favorites

#### Per Download Bitrate Override

Under the format lists is:

> Bitrate Override (Mbps, optional)

- If left blank:
  - Uses the format’s source bitrate (`tbr` / `vbr`).
  - If not available, falls back to the Bitrate preset.
- If you enter a value:
  - Interpreted as Mbps (e.g. `10` → ~10,000 kbps).
  - Used as the ffmpeg target video bitrate for that job.

Example:

- An AV1 4K format shows: `2160P - 387MB - 3.8 Mbps` (very compressed).
- Set override to `12`–`18` Mbps to re-encode H.264 at a higher bitrate and reduce visible artifacts.


#### Per-Resolution Favorite Overrides

In Advanced Options you can set favorites for:

- 2160p  
- 1440p  
- 1080p  
- 720p  
- 480p  

Behavior:

- When you select a format in the dialog:
  - If the Bitrate Override box is **empty** and a favorite exists for that resolution:
    - The app auto-fills the override with that favorite.
- If you’ve already typed something, the app does **not** overwrite it.
- Clearing the override field tells the app to use the source bitrate instead.


## Advanced Options

Visible when **Simple mode** is OFF.

1. **Video encoder**
   - **GPU (h264_videotoolbox)**:
     - macOS hardware acceleration.
     - Usually much faster for H.264 encodes.
   - **CPU (libx264)**:
     - Software encoder, slower but very robust.

2. **Bitrate preset (4M / 8M / 16M)**
   - Used when the source format does not provide a bitrate.
   - If a source bitrate exists, it is used instead (unless overridden).

3. **Max resolution cap**
   - Options: `No limit`, `720p`, `1080p`, `1440p`, `2160p`.
   - Used only in the fallback `bestvideo/bestaudio` path.
   - Limits the maximum height of the auto-selected bestvideo format.

4. **Keep raw bestvideo / bestaudio files**
   - If checked:
     - Keeps intermediate `.video.*` and `.audio.*` files.
   - If unchecked (default):
     - Deletes them after output is created.

5. **Output folder**
   - Defaults to `~/Desktop`.
   - You can:
     - Edit the path manually.
     - Use the **Browse…** button.
   - The app attempts to create the folder if it doesn’t exist.


### Progress, ETA & Logs

**Progress bar + label**

- Shows:
  - Current stage (“Downloading best audio”, “ffmpeg encode & mux”, etc.)
  - Percentage completion
  - ETA (especially during ffmpeg convert)

For `yt-dlp`:

- Parses `[download]` lines for `%` and `ETA`.

For `ffmpeg`:

- Uses the `time=` field (current encoded timestamp).
- Uses the total duration from yt-dlp metadata.
- Tracks `speed=` (e.g. `1.8x`) to estimate remaining time.
- Smooths ETA to avoid big jumps frame to frame.

**Status / Log panel**

- Scrollable text area with:
  - `yt-dlp` stdout / stderr
  - `ffmpeg` stdout / stderr
  - Internal messages (format choices, errors, etc.)
- You can select and copy text from the log for debugging.

**Summary + Open Output Folder**

- After successful completion:
  - Summary label: `Finished: <filename>`
  - “Open Output Folder” button:
    - Opens the output directory in Finder.


## Saved Settings

Configuration is saved in:

    ~/.yt_dlp_gui_v13_config.json

Persisted settings include:

- Output folder
- Encoder choice (GPU/CPU)
- Bitrate preset (4M / 8M / 16M)
- Keep raw flag
- Max resolution cap
- Audio-only checkbox state
- Simple mode checkbox state
- Per-resolution bitrate favorites (2160 / 1440 / 1080 / 720 / 480)

Settings are loaded on startup so your preferences carry over between sessions.


## macOS Notifications

The app uses `osascript` to trigger native macOS notifications:

- After a download / conversion completes:
  - Title: `yt-dlp GUI`
  - Body: `Download complete: <filename>`
- After a `yt-dlp -U` update check:
  - Notification that the update process finished.

If notifications fail (e.g. `osascript` not available), the error is logged but the app continues to run.


## Common Scenarios

### Scenario 1 – “Just give me a good MP4”

1. Leave **Simple mode ON**.
2. Paste a YouTube URL.
3. Make sure **Audio only (m4a)** is **unchecked**.
4. Click **Download / Convert**.
5. In the **Format Selection** dialog:
   - If a decent 720p/1080p QuickTime format is visible in the **left** list:
     - Select it → click **QuickTime (no conversion)**.
   - Otherwise:
     - Select a high-resolution AV1 format in the **right** list → click **AV1 mp4 + convert**.
6. Wait for the job to complete, then click **Open Output Folder** to see the final MP4.

### Scenario 2 – High-quality 4K AV1 → H.264

1. Turn **Simple mode OFF**.
2. In the per-resolution favorites (Advanced Options), set for example:
   - `2160p` → `15` (for 15 Mbps).
3. Paste a 4K YouTube URL.
4. Click **Download / Convert**.
5. In the **Format Selection** dialog:
   - Choose a `2160P` AV1 entry from the **right** list.
   - Verify the **Bitrate Override (Mbps)** box auto-filled to your favorite (e.g. `15`) and adjust if needed.
6. Click **AV1 mp4 + convert**.
7. The app downloads the AV1 video + bestaudio, re-encodes to H.264 at ~15 Mbps, and outputs a QuickTime-compatible MP4.

### Scenario 3 – Audio-only (m4a) for podcasts or music

1. Check **Audio only (m4a)**.
2. Paste a YouTube URL.
3. Click **Download / Convert**.
4. The app:
   - Downloads `bestaudio` with `yt-dlp`,
   - Converts it to AAC `.m4a` (if `ffmpeg` is available),
   - Shows the resulting file in the summary area.
5. Click **Open Output Folder** to reveal the `.m4a` file in Finder.

### Scenario 4 – Inspect formats without downloading

1. Paste a YouTube URL.
2. Click **Analyze Only**.
3. In the **Format Selection** dialog:
   - Review QuickTime-compatible formats in the **left** list.
   - Review AV1 mp4 video-only formats in the **right** list.
4. Optionally click a format to see how its resolution, file size and bitrate compare.
5. Click **Cancel** to close the dialog when you’re done inspecting (no files are downloaded).



## Troubleshooting

### `yt-dlp` not found / version label is empty

- Run:

        which yt-dlp

- Update `YTDLP_PATH` at the top of the script to match the location.


### `ffmpeg` not found

- Install via Homebrew:

        brew install ffmpeg

- Or update `FFMPEG_PATH` to match your installation path.


### Output file is unexpectedly huge

- Check the **Bitrate Override** field:
  - Very large numbers (e.g. 40 Mbps) will produce huge files.
- Try:
  - Clearing the override to use the source bitrate, or
  - Lowering the override value.


### GPU encoding issues

- In Advanced Options:
  - Switch from **GPU (h264_videotoolbox)** to **CPU (libx264)**.
- Try the job again; it will be slower but often more reliable.

### Window doesn’t fit controls

- v14 auto-sizes the window and enforces a minimum width so everything is visible.
- You can still resize manually if needed.



## Disclaimer


- This project is a GUI wrapper around yt-dlp and ffmpeg.
-   Respect YouTube’s Terms of Service.
-   Only download content when you have the legal rights to do so.
-   The author(s) are not responsible for misuse of this tool.
