To run the app as-is, you’ll need:

    macOS (Apple Silicon or Intel).
    Python 3.12 (or compatible) with tkinter available.
    yt-dlp installed at /opt/homebrew/bin/yt-dlp.
    ffmpeg installed at /opt/homebrew/bin/ffmpeg.

If your binaries live elsewhere, edit the top of the script: YTDLP_PATH and FFMPEG_PATH.


========== TYPICAL ONE TIME SETUP ==========

Typical one-time setup:
# Install Homebrew (if needed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Python + Tk
brew install python@3.12 python-tk@3.12

# yt-dlp and ffmpeg
brew install yt-dlp ffmpeg

Place yt_dlp_gui_v14.py somewhere convenient, e.g. ~/Documents, then run:
cd ~/Documents
/opt/homebrew/opt/python@3.12/bin/python3.12 yt_dlp_gui_v14.py
