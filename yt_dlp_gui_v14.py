#!/usr/bin/env python3
"""
yt-dlp GUI v14

New in v14 vs v13:
- Improved initial window sizing:
  * After building the UI, we ask Tk for the required width/height,
    then set the window geometry and a minimum size so that all widgets
    are visible without manual resizing.

All other features from v13 remain:
- yt-dlp version display + update button
- Help panel
- Clipboard auto-grab
- Audio-only mode
- Simple vs Advanced mode
- GPU/CPU encoding, bitrate presets, max resolution cap
- Per-resolution favorite bitrate overrides (non-forcing suggestions)
- Per-download Bitrate Override (Mbps)
- QuickTime-compatible direct downloads and AV1+convert pipeline
- macOS notifications
"""

import subprocess
import json
import os
import re
import shlex
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText

# Paths to binaries installed via Homebrew
YTDLP_PATH = "/opt/homebrew/bin/yt-dlp"
FFMPEG_PATH = "/opt/homebrew/bin/ffmpeg"

# Keep same config path as v13 so your settings carry over
CONFIG_PATH = os.path.expanduser("~/.yt_dlp_gui_v13_config.json")


# ---------- Utility functions (non-GUI) ----------

def seconds_to_hhmmss(seconds):
    """Convert seconds to HH:MM:SS for ETA display."""
    seconds = int(round(max(0, seconds)))
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


def run_yt_dlp_json(url):
    """Run yt-dlp with -J to get JSON metadata for a single video."""
    try:
        result = subprocess.run(
            [YTDLP_PATH, "-J", url],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        raise RuntimeError(f"yt-dlp not found at {YTDLP_PATH}")

    if result.returncode != 0:
        raise RuntimeError(
            f"yt-dlp error (code {result.returncode}):\n{result.stderr.strip()}"
        )

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse yt-dlp JSON: {e}")


def sanitize_filename(name, max_length=200):
    """Make a filesystem-safe filename from a title."""
    invalid = '<>:"/\\|?*'
    cleaned = []
    for c in name:
        if c in invalid or ord(c) < 32:
            cleaned.append("_")
        else:
            cleaned.append(c)
    safe = "".join(cleaned).strip().rstrip(".")

    if not safe:
        safe = "video"

    if len(safe) > max_length:
        safe = safe[:max_length].rstrip(".")

    return safe


def human_size(num_bytes):
    """Convert bytes to human-readable (MB or GiB)."""
    if not num_bytes or num_bytes <= 0:
        return "size unknown"
    kb = num_bytes / 1024.0
    mb = kb / 1024.0
    gb = mb / 1024.0
    if gb >= 1:
        return f"{gb:.2f} GiB"
    else:
        return f"{mb:.0f} MB"


def pretty_size_short(num_bytes):
    """
    Short, rounded size for list views:
    e.g. 144MB, 705MB, 1.3GB, 2.6GB
    """
    if not num_bytes or num_bytes <= 0:
        return "unknown"
    mb = num_bytes / (1024.0 * 1024.0)
    if mb >= 1024:
        gb = mb / 1024.0
        if gb >= 10:
            return f"{gb:.0f}GB"
        else:
            return f"{gb:.1f}GB"
    else:
        if mb >= 100:
            return f"{mb:.0f}MB"
        else:
            return f"{mb:.1f}MB"


def pretty_bitrate_mbps_from_fmt(fmt):
    """
    Return a short Mbps string from fmt['tbr'] / fmt['vbr'],
    e.g. '0.7 Mbps', '13.3 Mbps'.
    """
    tbr = fmt.get("tbr") or fmt.get("vbr")
    if not tbr:
        return "unknown"
    try:
        kbps = float(tbr)
    except (TypeError, ValueError):
        return "unknown"
    if kbps <= 0:
        return "unknown"
    mbps = kbps / 1000.0
    return f"{mbps:.1f} Mbps"


def source_bitrate_kbps_from_fmt(fmt, fallback_mbps=8.0):
    """
    Get a sensible target bitrate (in kbps) from a yt-dlp format dict.
    Prefer fmt['tbr'] or fmt['vbr'] if present.
    Clamp to a reasonable range (300–20000 kbps).
    Fallback to preset Mbps if missing or invalid.
    """
    kbps = fmt.get("tbr") or fmt.get("vbr")
    if kbps:
        try:
            kbps = int(round(float(kbps)))
        except (TypeError, ValueError):
            kbps = None

    if kbps is None:
        kbps = int(fallback_mbps * 1000)

    kbps = max(300, min(kbps, 20000))
    return kbps


def send_macos_notification(title, message):
    """Use AppleScript to send a native macOS notification."""
    script = f'display notification "{message}" with title "{title}"'
    try:
        subprocess.run(["osascript", "-e", script], check=False)
    except Exception:
        # Non-fatal if notifications fail
        pass


# ---------- Tooltip helper ----------

class ToolTip:
    """Simple tooltip implementation for Tk widgets."""

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = ttk.Label(
            tw,
            text=self.text,
            relief="solid",
            borderwidth=1,
            padding=(5, 3),
            justify="left",
            wraplength=300,
        )
        label.pack()

    def hide_tip(self, event=None):
        tw = self.tipwindow
        self.tipwindow = None
        if tw is not None:
            tw.destroy()


def create_tooltip(widget, text):
    ToolTip(widget, text)


# ---------- Format helpers ----------

def quicktime_compatible_formats(formats, min_height=480, prefer_h264=True):
    """
    Return progressive formats likely QuickTime-compatible:
     - video + audio
     - ext in mp4/m4v/mov
     - vcodec H.264 (avc/h264) or HEVC (hev1/hvc1)

    Adds f["_low_res"] flag if below min_height.
    Sorted by resolution & bitrate (highest first).
    """
    qt = []
    for f in formats or []:
        vcodec = (f.get("vcodec") or "").lower()
        acodec = (f.get("acodec") or "").lower()
        ext = (f.get("ext") or "").lower()
        h = f.get("height") or 0

        if vcodec in ("", "none") or acodec in ("", "none"):
            continue
        if ext not in ("mp4", "m4v", "mov"):
            continue

        if prefer_h264:
            if "avc" not in vcodec and "h264" not in vcodec:
                continue
        else:
            if not any(t in vcodec for t in ("avc", "h264", "hev1", "hvc1", "hevc")):
                continue

        f["_low_res"] = h < min_height
        qt.append(f)

    def sort_key(f):
        h = f.get("height") or 0
        tbr = f.get("tbr") or f.get("vbr") or 0
        try:
            tbr_val = float(tbr)
        except (TypeError, ValueError):
            tbr_val = 0.0
        return (h, tbr_val)

    qt.sort(key=sort_key, reverse=True)
    return qt


def av01_mp4_video_only_formats(formats):
    """
    Return mp4 video-only AV1 formats (for manual selection).
    Sorted by resolution & bitrate, highest first.
    """
    others = []
    for f in formats or []:
        vcodec = (f.get("vcodec") or "").lower()
        acodec = (f.get("acodec") or "").lower()
        ext = (f.get("ext") or "").lower()

        if "av01" not in vcodec:
            continue
        if acodec not in ("", "none"):
            continue
        if ext != "mp4":
            continue

        others.append(f)

    def sort_key(f):
        h = f.get("height") or 0
        tbr = f.get("tbr") or f.get("vbr") or 0
        try:
            tbr_val = float(tbr)
        except (TypeError, ValueError):
            tbr_val = 0.0
        return (h, tbr_val)

    others.sort(key=sort_key, reverse=True)
    return others


# ---------- Main GUI class ----------

class YTDLPGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("yt-dlp GUI v14")

        self.config_data = self.load_config()
        self.output_dir = self.config_data.get("output_dir",
                                               os.path.expanduser("~/Desktop"))
        self.last_duration = None  # seconds
        self.ytdlp_version_var = tk.StringVar(value="yt-dlp: checking…")

        # Per-resolution preferred overrides (string Mbps values)
        self.res_override_vars = {}

        # Build UI
        self.create_widgets()
        self.bind_events()
        self.refresh_yt_dlp_version()

        # NEW: ask Tk how big the UI wants to be, then set geometry & minimum size
        self.update_idletasks()
        req_w = self.winfo_reqwidth()
        req_h = self.winfo_reqheight()
        min_w = max(950, req_w)
        min_h = max(600, req_h)
        self.geometry(f"{min_w}x{min_h}")
        # Allow height to shrink a bit, but keep width so buttons are visible
        self.minsize(min_w, 500)

    # ----- Config -----

    def load_config(self):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def save_config(self):
        cfg = {
            "output_dir": self.output_dir,
            "encode_mode": self.encode_mode_var.get(),
            "bitrate": self.bitrate_var.get(),
            "keep_raw": self.keep_raw_var.get(),
            "max_resolution": self.max_res_var.get(),
            "audio_only": self.audio_only_var.get(),
            "simple_mode": self.simple_mode_var.get(),
        }
        # Add per-resolution overrides
        profiles = {}
        for key, var in self.res_override_vars.items():
            val = var.get().strip()
            if val:
                profiles[key] = val
        cfg["res_overrides"] = profiles

        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(cfg, f, indent=2)
        except Exception as e:
            self.log(f"Warning: could not save config: {e}")

        self.config_data = cfg

    # ----- Events -----

    def bind_events(self):
        self.bind("<FocusIn>", self._on_focus_in)

    def _on_focus_in(self, event=None):
        try:
            clip = self.clipboard_get()
        except tk.TclError:
            return
        if clip.startswith("https://www.youtube.com/watch?v=") or clip.startswith("https://youtu.be/"):
            self.url_var.set(clip)

    # ----- UI construction -----

    def create_widgets(self):
        # Header bar
        header = ttk.Frame(self)
        header.pack(fill="x", padx=10, pady=(8, 4))

        title_label = ttk.Label(header, text="yt-dlp GUI v14", font=("TkDefaultFont", 11, "bold"))
        title_label.pack(side="left")

        ver_label = ttk.Label(header, textvariable=self.ytdlp_version_var)
        ver_label.pack(side="left", padx=10)

        self.help_btn = ttk.Button(header, text="Help", command=self.show_help_panel)
        self.help_btn.pack(side="right")
        create_tooltip(self.help_btn, "Open detailed help and explanations for all options.")

        self.update_btn = ttk.Button(header, text="Check for yt-dlp update", command=self.check_for_yt_dlp_update)
        self.update_btn.pack(side="right", padx=(0, 6))
        create_tooltip(self.update_btn,
                       "Run 'yt-dlp -U' to check for and apply updates.\n"
                       "Note: if yt-dlp is managed by Homebrew, you may prefer 'brew upgrade yt-dlp'.")

        # URL + mode controls
        top_frame = ttk.Frame(self)
        top_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(top_frame, text="YouTube URL:").pack(side="left")
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(top_frame, textvariable=self.url_var, width=50)
        self.url_entry.pack(side="left", fill="x", expand=True, padx=5)

        self.audio_only_var = tk.BooleanVar(value=self.config_data.get("audio_only", False))
        self.audio_only_cb = ttk.Checkbutton(
            top_frame,
            text="Audio only (m4a)",
            variable=self.audio_only_var,
        )
        self.audio_only_cb.pack(side="left", padx=5)
        create_tooltip(self.audio_only_cb,
                       "If enabled, download bestaudio and save as .m4a.\n"
                       "Video formats and ffmpeg re-encoding are skipped.")

        self.simple_mode_var = tk.BooleanVar(value=self.config_data.get("simple_mode", True))
        self.simple_cb = ttk.Checkbutton(
            top_frame,
            text="Simple mode",
            variable=self.simple_mode_var,
            command=self._update_mode,
        )
        self.simple_cb.pack(side="left", padx=5)
        create_tooltip(self.simple_cb,
                       "Simple mode hides advanced encoding options.\n"
                       "QuickTime-compatible formats below 480p are also hidden.")

        btn_frame = ttk.Frame(top_frame)
        btn_frame.pack(side="left", padx=5)

        self.analyze_btn = ttk.Button(btn_frame, text="Analyze Only", command=self.analyze_only)
        self.analyze_btn.pack(side="left", padx=(0, 5))
        create_tooltip(self.analyze_btn,
                       "Fetch metadata & available formats with yt-dlp, but do not download.\n"
                       "Useful for inspecting quality/size before committing.")

        self.download_btn = ttk.Button(btn_frame, text="Download / Convert", command=self.download_best_and_convert)
        self.download_btn.pack(side="left")
        create_tooltip(self.download_btn,
                       "Main workflow: analyze formats, let you choose, then download & convert\n"
                       "to a QuickTime-friendly MP4 (or audio-only m4a).")

        # Advanced options frame
        self.advanced_frame = ttk.LabelFrame(self, text="Advanced Options")
        self.advanced_frame.pack(fill="x", padx=10, pady=(0, 10))

        encoder_frame = ttk.Frame(self.advanced_frame)
        encoder_frame.pack(side="left", padx=5, pady=5)
        ttk.Label(encoder_frame, text="Video encoder:").pack(anchor="w")
        self.encode_mode_var = tk.StringVar(value=self.config_data.get("encode_mode", "gpu"))
        self.gpu_rb = ttk.Radiobutton(encoder_frame, text="GPU (h264_videotoolbox)",
                                      variable=self.encode_mode_var, value="gpu")
        self.gpu_rb.pack(anchor="w")
        self.cpu_rb = ttk.Radiobutton(encoder_frame, text="CPU (libx264)",
                                      variable=self.encode_mode_var, value="cpu")
        self.cpu_rb.pack(anchor="w")
        create_tooltip(self.gpu_rb,
                       "Use macOS VideoToolbox hardware acceleration (GPU) to encode H.264.")
        create_tooltip(self.cpu_rb,
                       "Use libx264 software encoder (CPU). Slower but very compatible.")

        bitrate_frame = ttk.Frame(self.advanced_frame)
        bitrate_frame.pack(side="left", padx=20, pady=5)

        ttk.Label(bitrate_frame, text="Bitrate preset:").pack(anchor="w")
        self.bitrate_var = tk.StringVar(value=self.config_data.get("bitrate", "8M"))
        self.bitrate_combo = ttk.Combobox(
            bitrate_frame,
            textvariable=self.bitrate_var,
            values=["4M", "8M", "16M"],
            state="readonly",
            width=6,
        )
        self.bitrate_combo.pack(anchor="w")
        create_tooltip(self.bitrate_combo,
                       "Fallback maximum video bitrate.\n"
                       "Also used as a cap if source bitrate is unknown.")

        ttk.Label(bitrate_frame, text="Max resolution cap:").pack(anchor="w", pady=(6, 0))
        self.max_res_var = tk.StringVar(value=self.config_data.get("max_resolution", "No limit"))
        self.max_res_combo = ttk.Combobox(
            bitrate_frame,
            textvariable=self.max_res_var,
            values=["No limit", "720p", "1080p", "1440p", "2160p"],
            state="readonly",
            width=10,
        )
        self.max_res_combo.pack(anchor="w")
        create_tooltip(self.max_res_combo,
                       "For the fallback bestvideo path, limit resolution to this height.\n"
                       "Example: 1080p will avoid downloading 4K sources.")

        self.keep_raw_var = tk.BooleanVar(value=self.config_data.get("keep_raw", False))
        self.keep_raw_cb = ttk.Checkbutton(
            self.advanced_frame,
            text="Keep raw bestvideo / bestaudio files",
            variable=self.keep_raw_var,
        )
        self.keep_raw_cb.pack(anchor="w", padx=5, pady=(0, 5))
        create_tooltip(self.keep_raw_cb,
                       "If checked, keep the intermediate video-only & audio-only files\n"
                       "that yt-dlp downloads before ffmpeg combines them.")

        folder_frame = ttk.Frame(self.advanced_frame)
        folder_frame.pack(fill="x", padx=5, pady=5)
        ttk.Label(folder_frame, text="Output folder:").pack(side="left")
        self.output_dir_var = tk.StringVar(value=self.output_dir)
        self.output_entry = ttk.Entry(folder_frame, textvariable=self.output_dir_var, width=40)
        self.output_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.browse_btn = ttk.Button(folder_frame, text="Browse…", command=self.choose_output_dir)
        self.browse_btn.pack(side="left")
        create_tooltip(self.output_entry,
                       "Folder where finished files are written.")
        create_tooltip(self.browse_btn,
                       "Choose the folder where output files will be saved.")

        # Per-resolution preferred overrides
        res_cfg = self.config_data.get("res_overrides", {})
        res_frame = ttk.LabelFrame(
            self.advanced_frame,
            text="Preferred bitrate overrides per resolution (Mbps, optional)",
        )
        res_frame.pack(fill="x", padx=5, pady=(0, 5))

        create_tooltip(
            res_frame,
            "Optional per-resolution favorites, in Mbps.\n"
            "If set, these are used as suggestions to auto-fill the Bitrate Override field\n"
            "when selecting a format of that resolution. They NEVER force a setting.\n"
            "You can clear or change the override per download."
        )

        self.res_override_vars = {}
        res_order = [("2160p", "2160"), ("1440p", "1440"),
                     ("1080p", "1080"), ("720p", "720"), ("480p", "480")]

        for label_text, key in res_order:
            sub = ttk.Frame(res_frame)
            sub.pack(side="left", padx=5, pady=2)
            ttk.Label(sub, text=label_text).pack(anchor="w")
            var = tk.StringVar(value=str(res_cfg.get(key, "")))
            entry = ttk.Entry(sub, textvariable=var, width=6)
            entry.pack(anchor="w")
            create_tooltip(
                entry,
                f"Favorite bitrate (in Mbps) to use as a suggestion\n"
                f"when selecting {label_text} formats.\n"
                f"Leave blank to have no suggestion for {label_text}."
            )
            self.res_override_vars[key] = var

        # Progress bar + label
        progress_frame = ttk.Frame(self)
        progress_frame.pack(fill="x", padx=10, pady=(0, 10))
        self.progress_var = tk.DoubleVar(value=0.0)
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100.0)
        self.progress_bar.pack(fill="x", side="left", expand=True)
        self.progress_label_var = tk.StringVar(value="Idle")
        ttk.Label(progress_frame, textvariable=self.progress_label_var,
                  width=35, anchor="w").pack(side="left", padx=(8, 0))

        # Log area
        log_frame = ttk.LabelFrame(self, text="Status / Log")
        log_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.log_text = ScrolledText(log_frame, state="disabled", height=15)
        self.log_text.pack(fill="both", expand=True)

        # Bottom summary + open output button
        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(fill="x", padx=10, pady=(0, 10))
        self.summary_label = ttk.Label(bottom_frame, text="", anchor="w")
        self.summary_label.pack(side="left", fill="x", expand=True)
        self.open_output_btn = ttk.Button(bottom_frame, text="Open Output Folder",
                                          command=self.open_output_folder, state="disabled")
        self.open_output_btn.pack(side="right")
        create_tooltip(self.open_output_btn,
                       "Reveal the current output folder in Finder.")

        self._update_mode()

    # ----- Mode & header helpers -----

    def _update_mode(self):
        if self.simple_mode_var.get():
            self.advanced_frame.forget()
        else:
            self.advanced_frame.pack(fill="x", padx=10, pady=(0, 10))
        self.save_config()

    def refresh_yt_dlp_version(self):
        try:
            result = subprocess.run(
                [YTDLP_PATH, "--version"],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0 and result.stdout.strip():
                ver_line = result.stdout.strip().splitlines()[0].strip()
                self.ytdlp_version_var.set(f"yt-dlp: {ver_line}")
            else:
                self.ytdlp_version_var.set("yt-dlp: unknown")
        except FileNotFoundError:
            self.ytdlp_version_var.set("yt-dlp not found")

    def check_for_yt_dlp_update(self):
        """Run 'yt-dlp -U' to check for and apply updates, then refresh version."""
        if not os.path.isfile(YTDLP_PATH):
            messagebox.showerror("yt-dlp not found",
                                 f"yt-dlp was not found at {YTDLP_PATH}")
            return

        if not messagebox.askyesno(
            "Update yt-dlp",
            "This will run 'yt-dlp -U' to check for and install updates.\n\n"
            "If yt-dlp is managed by Homebrew, you may prefer:\n"
            "  brew upgrade yt-dlp\n\n"
            "Continue with in-app update?"
        ):
            return

        self.update_btn["state"] = "disabled"
        self.log("Running yt-dlp -U (check for updates)…")

        try:
            proc = subprocess.run(
                [YTDLP_PATH, "-U"],
                capture_output=True,
                text=True,
                check=False,
            )
            if proc.stdout:
                self.log(proc.stdout.strip())
            if proc.stderr:
                self.log(proc.stderr.strip())

            if proc.returncode == 0:
                messagebox.showinfo(
                    "yt-dlp update",
                    "yt-dlp -U finished.\n\nIf an update was available, it should now "
                    "be installed."
                )
                send_macos_notification("yt-dlp GUI", "yt-dlp update check finished.")
            else:
                messagebox.showwarning(
                    "yt-dlp update",
                    f"'yt-dlp -U' exited with code {proc.returncode}.\n"
                    "See the log for details."
                )
        except Exception as e:
            messagebox.showerror("yt-dlp update error", str(e))
            self.log(f"Update error: {e}")
        finally:
            self.update_btn["state"] = "normal"
            self.refresh_yt_dlp_version()

    def show_help_panel(self):
        """Open a scrollable help window explaining all options."""
        win = tk.Toplevel(self)
        win.title("Help - yt-dlp GUI v14")
        win.geometry("720x540")
        win.transient(self)

        txt = ScrolledText(win, wrap="word")
        txt.pack(fill="both", expand=True)

        help_text = """
yt-dlp GUI v14 – Help

MAIN WORKFLOW
-------------
1. Paste or auto-grab a YouTube URL into the URL field.
2. Optionally enable "Audio only (m4a)" if you want just the audio.
3. Leave "Simple mode" on for a clean UI, or turn it off for advanced controls.
4. Click "Download / Convert".
   - The app analyzes the video with yt-dlp.
   - If QuickTime-compatible formats exist, you can pick one (no conversion).
   - Otherwise, pick an AV1 video-only format and the app will:
     * download the chosen video-only stream + best audio-only
     * use ffmpeg to combine and convert to QuickTime-friendly H.264 + AAC.

ANALYZE ONLY
------------
"Analyze Only" runs yt-dlp in metadata mode and shows you:
- QuickTime-compatible formats (video + audio, usually mp4, H.264).
- AV1 mp4 video-only formats (for download + convert).
No files are downloaded in this mode; it is just for inspection.

AUDIO ONLY (m4a)
----------------
If "Audio only (m4a)" is enabled:
- The app downloads the best audio stream with yt-dlp.
- If ffmpeg is installed, it converts to AAC in an .m4a container.
- This is useful for podcasts or music videos where you don't need video.

SIMPLE vs ADVANCED MODE
-----------------------
Simple mode:
- Hides advanced encoding options.
- Hides very low resolution QuickTime formats (< 480p) so selection is cleaner.

Advanced mode:
- Shows:
  * Video encoder: GPU vs CPU
  * Bitrate preset
  * Max resolution cap
  * "Keep raw bestvideo/bestaudio files"
  * Output folder selector
  * Per-resolution preferred bitrate overrides

ENCODER OPTIONS
---------------
GPU (h264_videotoolbox):
- Uses macOS VideoToolbox hardware acceleration.
- Usually faster for H.264 encoding on Apple Silicon / modern Macs.

CPU (libx264):
- Software encoder; typically slower but very compatible.
- Might be useful if GPU encoding behaves oddly for specific sources.

BITRATE PRESET
--------------
- Acts as a rough maximum target bitrate when the source bitrate is unknown.
- When the source format has a defined bitrate (tbr/vbr), the app will:
  * Use the source bitrate (kbps) for ffmpeg encoding, unless overridden.

MAX RESOLUTION CAP
------------------
- Applies in the fallback "bestvideo" pipeline.
- Example: 1080p will avoid downloading 4K sources, which saves bandwidth.

KEEP RAW FILES
--------------
- If enabled, the intermediate video-only and audio-only files downloaded by
  yt-dlp will be left on disk after ffmpeg finishes.
- If disabled (default), these temp files are removed to save space.

BITRATE OVERRIDE (Mbps) – PER DOWNLOAD
--------------------------------------
- At the bottom of the "Select Format" window, there is a field:
    Bitrate Override (Mbps, optional)

- If you enter a value (e.g. 10), that bitrate will be used for ffmpeg
  re-encoding instead of the source bitrate.
- This is useful when:
  * The source 4K AV1 stream has a very low bitrate (e.g., 3.8 Mbps) and you
    want to re-encode with a higher H.264 bitrate (e.g., 15 Mbps).
- If left blank, the app uses the source bitrate reported by yt-dlp.

PER-RESOLUTION FAVORITE OVERRIDES
---------------------------------
- In Advanced Options you can set favorite bitrates (in Mbps) for resolutions:
    2160p, 1440p, 1080p, 720p, 480p.

- These are NOT forced. Instead:
  * When you select a format in the format selection dialog, if the
    Bitrate Override field is currently empty and there is a configured
    favorite for that resolution, the app auto-fills the override field
    with that value.
  * You can clear or change this per download.

- Example:
  * You set:
      2160p = 15
      1080p = 5
  * When you select a 2160p format, if the override box is empty, it will
    auto-fill with "15".
  * If you prefer to match source bitrate for a particular video, simply
    clear the override box before confirming.

YT-DLP VERSION & UPDATES
------------------------
- The header shows the current yt-dlp version as reported by:
    yt-dlp --version
- "Check for yt-dlp update" runs:
    yt-dlp -U
  and then refreshes the displayed version.
- If yt-dlp is Homebrew-managed, you may prefer:
    brew upgrade yt-dlp

MACOS NOTIFICATIONS
-------------------
- When a download/conversion finishes, the app sends a macOS notification.
- When yt-dlp update check finishes, you also get a notification.

OPEN OUTPUT FOLDER
------------------
- The "Open Output Folder" button reveals the current output directory
  in Finder for quick access to finished files.
"""
        txt.insert("1.0", help_text)
        txt.configure(state="disabled")

    # ----- General helpers -----

    def choose_output_dir(self):
        new_dir = filedialog.askdirectory(initialdir=self.output_dir, title="Select output folder")
        if new_dir:
            self.output_dir = new_dir
            self.output_dir_var.set(new_dir)
            self.log(f"Output folder set to: {new_dir}")
            self.save_config()

    def log(self, text):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", text + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")
        self.update_idletasks()

    def set_progress(self, percent, label_text=None):
        try:
            self.progress_var.set(max(0.0, min(100.0, float(percent))))
        except (TypeError, ValueError):
            pass
        if label_text is not None:
            self.progress_label_var.set(label_text)
        self.update_idletasks()

    def open_output_folder(self):
        if os.path.isdir(self.output_dir):
            subprocess.run(["open", self.output_dir], check=False)

    # ----- Format analysis only -----

    def analyze_only(self):
        """Run yt-dlp -J and show formats dialog but do NOT download."""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Missing URL", "Please paste a YouTube URL.")
            return

        self.log(f"Analyzing URL (no download): {url}")
        try:
            info = run_yt_dlp_json(url)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.log(f"Error: {e}")
            return

        formats = info.get("formats") or []
        qt_formats = quicktime_compatible_formats(formats)
        other_formats = av01_mp4_video_only_formats(formats)

        if self.simple_mode_var.get():
            qt_formats = [f for f in qt_formats if not f.get("_low_res", False)]

        self.prompt_format_choice(qt_formats, other_formats, analyze_only=True)

    # ----- Format choice dialog (with bitrate override + per-res suggestions) -----

    def prompt_format_choice(self, qt_formats, other_formats, analyze_only=False):
        """
        Show a modal dialog listing:
          - QuickTime-compatible formats
          - AV1 mp4 video-only formats
        Also includes a "Bitrate Override (Mbps)" entry.

        Uses per-resolution favorites as suggestions:
        - If you click a format and the override box is empty:
          * If there's a favorite for that resolution, it's auto-filled.

        For normal use, returns (mode, fmt, override_str) where:
            mode = "quicktime" or "other" or None
            fmt  = format dict or None
            override_str = string from the override entry (may be "")

        For analyze_only mode:
            No value is returned; instead a brief info dialog is shown.
        """
        dialog = tk.Toplevel(self)
        dialog.title("Select Format to Download")
        dialog.transient(self)
        dialog.grab_set()

        ttk.Label(
            dialog,
            text=(
                "Select a QuickTime-compatible format (no conversion), "
                "or an AV1 mp4 video-only format (download + convert).\n"
                "Optionally specify a Bitrate Override (Mbps) for ffmpeg.\n"
                "Per-resolution favorites will auto-fill when the box is empty."
            ),
            justify="left",
        ).pack(padx=10, pady=10)

        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # QuickTime list
        qt_frame = ttk.LabelFrame(main_frame, text="QuickTime-compatible (no conversion)")
        qt_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        qt_list = tk.Listbox(qt_frame, height=10, width=40)
        qt_scroll = ttk.Scrollbar(qt_frame, orient="vertical", command=qt_list.yview)
        qt_list.config(yscrollcommand=qt_scroll.set)
        qt_list.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=(5, 5))
        qt_scroll.pack(side="right", fill="y", padx=(0, 5), pady=(5, 5))

        for f in qt_formats:
            h = f.get("height") or 0
            res = f"{h}P" if h else "Unknown"
            filesize = f.get("filesize") or f.get("filesize_approx")
            size_str = pretty_size_short(filesize)
            br_str = pretty_bitrate_mbps_from_fmt(f)
            label = f"{res} - {size_str} - {br_str}"
            qt_list.insert("end", label)

        if qt_formats:
            qt_list.select_set(0)

        # AV1 mp4 video-only list
        other_frame = ttk.LabelFrame(main_frame, text="Other formats (AV1 mp4 video-only → convert)")
        other_frame.pack(side="left", fill="both", expand=True, padx=(5, 0))

        other_list = tk.Listbox(other_frame, height=10, width=40)
        other_scroll = ttk.Scrollbar(other_frame, orient="vertical", command=other_list.yview)
        other_list.config(yscrollcommand=other_scroll.set)
        other_list.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=(5, 5))
        other_scroll.pack(side="right", fill="y", padx=(0, 5), pady=(5, 5))

        for f in other_formats:
            h = f.get("height") or 0
            res = f"{h}P" if h else "Unknown"
            filesize = f.get("filesize") or f.get("filesize_approx")
            size_str = pretty_size_short(filesize)
            br_str = pretty_bitrate_mbps_from_fmt(f)
            label = f"{res} - {size_str} - {br_str}"
            other_list.insert("end", label)

        if other_formats:
            other_list.select_set(0)

        # Bitrate override entry
        override_frame = ttk.Frame(dialog)
        override_frame.pack(fill="x", padx=10, pady=(0, 5))
        ttk.Label(override_frame, text="Bitrate Override (Mbps, optional):").pack(side="left")
        override_var = tk.StringVar(value="")
        override_entry = ttk.Entry(override_frame, textvariable=override_var, width=10)
        override_entry.pack(side="left", padx=(5, 0))
        create_tooltip(
            override_entry,
            "Optional: force ffmpeg to use this video bitrate (in Mbps) instead of\n"
            "the source bitrate. Leave blank to match the source.\n"
            "Per-resolution favorites will auto-fill this when selecting a format,\n"
            "but you can always clear or change it."
        )

        result = {"mode": None, "fmt": None, "override": ""}

        def apply_profile_for_fmt(fmt):
            """If override box is empty and we have a profile for this height, fill it."""
            if override_var.get().strip():
                return  # user already typed something; don't override

            h = fmt.get("height") or 0
            if not h:
                return

            for key in self.res_override_vars:
                try:
                    res_h = int(key)
                except ValueError:
                    continue
                if res_h == h:
                    val = self.res_override_vars[key].get().strip()
                    if val:
                        override_var.set(val)
                    break

        def on_qt_select(event=None):
            sel = qt_list.curselection()
            if not sel or not qt_formats:
                return
            fmt = qt_formats[sel[0]]
            apply_profile_for_fmt(fmt)

        def on_other_select(event=None):
            sel = other_list.curselection()
            if not sel or not other_formats:
                return
            fmt = other_formats[sel[0]]
            apply_profile_for_fmt(fmt)

        qt_list.bind("<<ListboxSelect>>", on_qt_select)
        other_list.bind("<<ListboxSelect>>", on_other_select)

        if qt_formats and qt_list.curselection():
            apply_profile_for_fmt(qt_formats[qt_list.curselection()[0]])
        elif other_formats and other_list.curselection():
            apply_profile_for_fmt(other_formats[other_list.curselection()[0]])

        def choose_qt():
            if not qt_formats:
                messagebox.showwarning("No QuickTime formats", "No QuickTime-compatible formats available.")
                return
            sel = qt_list.curselection()
            if not sel:
                messagebox.showwarning("No selection", "Please select a QuickTime format.")
                return
            idx = sel[0]
            result["mode"] = "quicktime"
            result["fmt"] = qt_formats[idx]
            result["override"] = override_var.get().strip()
            dialog.destroy()

        def choose_other():
            if not other_formats:
                messagebox.showwarning("No other formats", "No AV1 mp4 video-only formats available.")
                return
            sel = other_list.curselection()
            if not sel:
                messagebox.showwarning("No selection", "Please select an 'Other' format.")
                return
            idx = sel[0]
            result["mode"] = "other"
            result["fmt"] = other_formats[idx]
            result["override"] = override_var.get().strip()
            dialog.destroy()

        def cancel():
            result["mode"] = None
            result["fmt"] = None
            result["override"] = ""
            dialog.destroy()

        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=(0, 10))
        ttk.Button(btn_frame, text="QuickTime (no conversion)", command=choose_qt).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="AV1 mp4 + convert", command=choose_other).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=cancel).pack(side="left", padx=5)

        dialog.protocol("WM_DELETE_WINDOW", cancel)
        self.wait_window(dialog)

        if analyze_only:
            if result["mode"] and result["fmt"]:
                f = result["fmt"]
                h = f.get("height") or 0
                res = f"{h}P" if h else "Unknown"
                filesize = f.get("filesize") or f.get("filesize_approx")
                size_str = human_size(filesize)
                br_str = pretty_bitrate_mbps_from_fmt(f)
                messagebox.showinfo(
                    "Format info",
                    f"Selected format: {res}\n"
                    f"Estimated size: {size_str}\n"
                    f"Bitrate: {br_str}\n"
                    f"Bitrate override (if any): {result['override'] or 'none'}",
                )
            return None

        return result["mode"], result["fmt"], result["override"]

    # ----- Main download / convert workflow -----

    def download_best_and_convert(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Missing URL", "Please paste a YouTube URL.")
            return

        if not os.path.isfile(FFMPEG_PATH) and not self.audio_only_var.get():
            messagebox.showerror("ffmpeg not found",
                                 f"ffmpeg was not found at {FFMPEG_PATH}")
            self.log(f"ffmpeg not found at {FFMPEG_PATH}")
            return

        if not self._ensure_output_dir():
            return

        self.download_btn["state"] = "disabled"
        self.analyze_btn["state"] = "disabled"
        self.open_output_btn["state"] = "disabled"
        self.set_progress(0, "Starting…")
        self.log(f"Processing URL: {url}")

        try:
            info = run_yt_dlp_json(url)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.log(f"Error: {e}")
            self._reset_buttons()
            return

        video_id = info.get("id") or "video"
        title = info.get("title") or "video"
        safe_title = sanitize_filename(title)
        duration = info.get("duration")
        self.last_duration = duration

        self.log(f"Video ID: {video_id}")
        self.log(f"Video title: {title}")
        if duration:
            self.log(f"Duration: {seconds_to_hhmmss(duration)}")

        # Audio-only path
        if self.audio_only_var.get():
            output_path = self._audio_only_pipeline(url, info, safe_title, duration)
            if output_path:
                self._job_finished({"mode": "audio", "output": output_path})
            else:
                self._reset_buttons()
            return

        formats = info.get("formats") or []
        qt_formats = quicktime_compatible_formats(formats)
        other_formats = av01_mp4_video_only_formats(formats)

        if self.simple_mode_var.get():
            qt_formats = [f for f in qt_formats if not f.get("_low_res", False)]

        chosen_mode = None
        chosen_fmt = None
        override_mbps = None

        if qt_formats or other_formats:
            res = self.prompt_format_choice(qt_formats, other_formats, analyze_only=False)
            if res:
                chosen_mode, chosen_fmt, override_str = res
                if override_str:
                    try:
                        val = float(override_str)
                        if val > 0:
                            override_mbps = val
                    except ValueError:
                        messagebox.showwarning(
                            "Bitrate override ignored",
                            "Bitrate override must be a number (Mbps). "
                            "Using source bitrate instead."
                        )
                        override_mbps = None
        else:
            self.log("No QuickTime-compatible or AV1 mp4 video-only formats found; using fallback pipeline.")

        if (qt_formats or other_formats) and chosen_mode is None:
            self.log("User canceled format selection.")
            self.set_progress(0, "Canceled")
            self._reset_buttons()
            return

        if chosen_mode == "quicktime" and chosen_fmt:
            self.log("User chose QuickTime direct download (no conversion).")
            output_path = self._download_quicktime(url, safe_title, chosen_fmt)
            if output_path:
                self._job_finished({"mode": "quicktime", "output": output_path})
            else:
                self._reset_buttons()
            return

        if chosen_mode == "other" and chosen_fmt:
            self.log("User chose AV1 video-only + convert pipeline.")
            output_path = self._pipeline_selected_video_fmt(
                url, chosen_fmt, video_id, safe_title, duration, override_mbps=override_mbps
            )
            if output_path:
                self._job_finished({"mode": "convert", "output": output_path})
            else:
                self._reset_buttons()
            return

        self.log("Using fallback bestvideo/bestaudio pipeline.")
        output_path = self._full_pipeline_best_av(
            url, info, video_id, safe_title, duration, override_mbps=override_mbps
        )
        if output_path:
            self._job_finished({"mode": "fallback", "output": output_path})
        else:
            self._reset_buttons()

    def _job_finished(self, summary):
        out = summary.get("output")
        if out:
            self.summary_label.config(text=f"Finished: {os.path.basename(out)}")
            self.open_output_btn["state"] = "normal"
            send_macos_notification("yt-dlp GUI", f"Download complete:\n{os.path.basename(out)}")
        else:
            self.summary_label.config(text="Finished (no output)")
        self.set_progress(100, "Done")
        self._reset_buttons()
        self.save_config()

    def _reset_buttons(self):
        self.download_btn["state"] = "normal"
        self.analyze_btn["state"] = "normal"

    # ----- File helpers -----

    def _ensure_output_dir(self):
        if not os.path.isdir(self.output_dir):
            try:
                os.makedirs(self.output_dir, exist_ok=True)
                self.log(f"Created output folder: {self.output_dir}")
            except OSError as e:
                messagebox.showerror("Output folder error", str(e))
                self.log(f"Error creating output folder: {e}")
                return False
        return True

    def _cleanup_temp(self, prefix):
        if not os.path.isdir(self.output_dir):
            return
        for fname in os.listdir(self.output_dir):
            if fname.startswith(prefix):
                try:
                    os.remove(os.path.join(self.output_dir, fname))
                    self.log(f"Removed old temp file: {fname}")
                except OSError as e:
                    self.log(f"Could not remove temp file {fname}: {e}")

    def _find_downloaded(self, prefix):
        if not os.path.isdir(self.output_dir):
            return None
        for fname in os.listdir(self.output_dir):
            if fname.startswith(prefix):
                return os.path.join(self.output_dir, fname)
        return None

    # ----- Process runners -----

    def _run_ytdlp_with_progress(self, cmd, stage_label):
        self.log("Running yt-dlp command:")
        self.log(" ".join(cmd))
        self.set_progress(0, f"{stage_label} (0%)")

        re_full = re.compile(r"\[download\]\s+(\d+(?:\.\d+)?)%.*?ETA\s+([0-9:]+)")
        re_pct_only = re.compile(r"\[download\]\s+(\d+(?:\.\d+)?)%")

        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
        except FileNotFoundError as e:
            self.log(f"Error launching yt-dlp: {e}")
            return 1

        for line in proc.stdout:
            s = line.rstrip()
            self.log(s)

            m_full = re_full.search(s)
            m = m_full or re_pct_only.search(s)
            if m:
                try:
                    pct = float(m.group(1))
                except ValueError:
                    pct = None
                eta_text = None
                if m_full and len(m_full.groups()) >= 2:
                    eta_text = m_full.group(2)
                if pct is not None:
                    label = f"{stage_label} ({pct:.1f}%)"
                    if eta_text:
                        label += f" - ETA {eta_text}"
                    self.set_progress(pct, label)

        proc.wait()
        if proc.returncode == 0:
            self.set_progress(100, f"{stage_label} (100%)")
        return proc.returncode

    def _run_ffmpeg_with_progress(self, cmd, stage_label, duration):
        self.log("Running ffmpeg command:")
        self.log(" ".join(shlex.quote(c) for c in cmd))
        self.set_progress(0, f"{stage_label} (0%)")

        time_re = re.compile(r"time=(\d+):(\d+):(\d+(?:\.\d+)?)")
        speed_re = re.compile(r"speed=\s*([\d\.]+)x")

        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
        except FileNotFoundError as e:
            self.log(f"Error launching ffmpeg: {e}")
            return 1

        total_dur = float(duration) if duration else 0.0
        last_speed = 1.0
        smooth_eta = None

        for line in proc.stdout:
            s = line.rstrip()
            self.log(s)

            if total_dur > 0:
                m_time = time_re.search(s)
                if m_time:
                    try:
                        h = float(m_time.group(1))
                        m_ = float(m_time.group(2))
                        s_ = float(m_time.group(3))
                        t_sec = h * 3600 + m_ * 60 + s_
                    except ValueError:
                        t_sec = None

                    if t_sec is not None:
                        pct = min(100.0, (t_sec / total_dur) * 100.0)

                        m_speed = speed_re.search(s)
                        if m_speed:
                            try:
                                last_speed = max(0.1, float(m_speed.group(1)))
                            except ValueError:
                                pass

                        remaining = max(0.0, (total_dur - t_sec) / last_speed)

                        if smooth_eta is None:
                            smooth_eta = remaining
                        else:
                            alpha = 0.3
                            smooth_eta = alpha * remaining + (1 - alpha) * smooth_eta

                        eta_str = seconds_to_hhmmss(smooth_eta)
                        self.set_progress(pct, f"{stage_label} ({pct:.1f}%) - ETA {eta_str}")

        proc.wait()
        if proc.returncode == 0:
            self.set_progress(100, f"{stage_label} (100%)")
        return proc.returncode

    # ----- QuickTime direct path -----

    def _download_quicktime(self, url, safe_title, fmt):
        fmt_id = fmt.get("format_id")
        ext = fmt.get("ext") or "mp4"
        output_template = os.path.join(self.output_dir, f"{safe_title}.%(ext)s")

        self.log(f"QuickTime format id: {fmt_id}, ext: {ext}")
        ytdlp_cmd = [YTDLP_PATH, "--newline", "-f", fmt_id, "-o", output_template, url]

        rc = self._run_ytdlp_with_progress(ytdlp_cmd, "Downloading QuickTime format")
        if rc != 0:
            messagebox.showerror("Download failed", f"yt-dlp exited with code {rc}.")
            self.log(f"QuickTime download failed (code {rc})")
            return None

        return os.path.join(self.output_dir, f"{safe_title}.{ext}")

    # ----- AV1 + convert path (selected format) -----

    def _pipeline_selected_video_fmt(self, url, fmt, video_id, safe_title, duration,
                                     override_mbps=None):
        video_prefix = f"{video_id}.video."
        audio_prefix = f"{video_id}.audio."

        self._cleanup_temp(video_prefix)
        self._cleanup_temp(audio_prefix)

        fmt_id = fmt.get("format_id")
        video_template = os.path.join(self.output_dir, "%(id)s.video.%(ext)s")

        self.log(f"Downloading video-only format: {fmt_id}")
        ytdlp_video_cmd = [YTDLP_PATH, "--newline", "-f", fmt_id, "-o", video_template, url]
        rc = self._run_ytdlp_with_progress(ytdlp_video_cmd, "Downloading video-only")
        if rc != 0:
            messagebox.showerror("Download failed", f"yt-dlp video-only failed (code {rc})")
            self.log(f"Video-only download failed (code {rc})")
            return None

        video_path = self._find_downloaded(video_prefix)
        if not video_path:
            messagebox.showerror("Error", "Video-only file not found after download.")
            self.log("Video-only file missing after download.")
            return None
        self.log(f"Video file: {video_path}")

        audio_template = os.path.join(self.output_dir, "%(id)s.audio.%(ext)s")
        ytdlp_audio_cmd = [YTDLP_PATH, "--newline", "-f", "bestaudio", "-o", audio_template, url]
        rc = self._run_ytdlp_with_progress(ytdlp_audio_cmd, "Downloading best audio")
        if rc != 0:
            messagebox.showerror("Download failed", f"yt-dlp audio-only failed (code {rc})")
            self.log(f"Audio-only download failed (code {rc})")
            return None

        audio_path = self._find_downloaded(audio_prefix)
        if not audio_path:
            messagebox.showerror("Error", "Audio-only file not found after download.")
            self.log("Audio-only file missing.")
            return None
        self.log(f"Audio file: {audio_path}")

        output_path = os.path.join(self.output_dir, f"{safe_title}.mp4")
        counter = 1
        base, ext = os.path.splitext(output_path)
        while os.path.exists(output_path):
            output_path = f"{base} ({counter}){ext}"
            counter += 1

        preset = self.bitrate_var.get()
        if preset.endswith("M"):
            try:
                preset_mbps = float(preset[:-1])
            except ValueError:
                preset_mbps = 8.0
        else:
            preset_mbps = 8.0

        if override_mbps is not None:
            target_kbps = max(300, min(int(override_mbps * 1000), 50000))
            self.log(f"Bitrate override active: using {override_mbps:.2f} Mbps "
                     f"({target_kbps} kbps) for encoding.")
        else:
            target_kbps = source_bitrate_kbps_from_fmt(fmt, fallback_mbps=preset_mbps)
            self.log(f"Using source-based bitrate ≈ {target_kbps} kbps.")

        bitrate_str = f"{target_kbps}k"
        bufsize_str = f"{target_kbps * 2}k"

        encode_mode = self.encode_mode_var.get()
        use_gpu = (encode_mode == "gpu")

        if use_gpu:
            vcodec_args = [
                "-c:v", "h264_videotoolbox",
                "-b:v", bitrate_str,
                "-maxrate", bitrate_str,
                "-bufsize", bufsize_str,
                "-pix_fmt", "yuv420p",
            ]
        else:
            vcodec_args = [
                "-c:v", "libx264",
                "-preset", "medium",
                "-b:v", bitrate_str,
                "-maxrate", bitrate_str,
                "-bufsize", bufsize_str,
                "-pix_fmt", "yuv420p",
            ]

        ffmpeg_cmd = [
            FFMPEG_PATH,
            "-y",
            "-i", video_path,
            "-i", audio_path,
            "-map", "0:v:0",
            "-map", "1:a:0",
            *vcodec_args,
            "-c:a", "aac",
            "-b:a", "192k",
            "-movflags", "+faststart",
            "-shortest",
            output_path,
        ]

        rc = self._run_ffmpeg_with_progress(ffmpeg_cmd, "ffmpeg encode & mux", duration or 0)
        if rc != 0:
            messagebox.showerror("ffmpeg failed", f"ffmpeg exited with code {rc}")
            self.log(f"ffmpeg failed (code {rc})")
            return None

        self.log("ffmpeg conversion complete.")

        if not self.keep_raw_var.get():
            try:
                os.remove(video_path)
                self.log(f"Removed temp video: {video_path}")
            except Exception:
                pass
            try:
                os.remove(audio_path)
                self.log(f"Removed temp audio: {audio_path}")
            except Exception:
                pass

        return output_path

    # ----- Fallback bestvideo path -----

    def _full_pipeline_best_av(self, url, info, video_id, safe_title, duration,
                               override_mbps=None):
        formats = info.get("formats") or []

        res_map = {"720p": 720, "1080p": 1080, "1440p": 1440, "2160p": 2160}
        max_res_choice = self.max_res_var.get()
        max_height = res_map.get(max_res_choice)

        candidates = []
        for f in formats:
            vcodec = (f.get("vcodec") or "").lower()
            acodec = (f.get("acodec") or "").lower()
            h = f.get("height") or 0
            if vcodec in ("", "none"):
                continue
            if acodec not in ("", "none"):
                continue
            if max_height and h and h > max_height:
                continue
            candidates.append(f)

        if not candidates and max_height:
            candidates = [
                f for f in formats
                if (f.get("vcodec") or "").lower() not in ("", "none")
                and (f.get("acodec") or "").lower() in ("", "none")
            ]

        if not candidates:
            messagebox.showerror("Error", "No suitable video-only format found.")
            self.log("No candidates for bestvideo.")
            return None

        def sort_key(f):
            h = f.get("height") or 0
            tbr = f.get("tbr") or f.get("vbr") or 0
            try:
                tbr_val = float(tbr)
            except (TypeError, ValueError):
                tbr_val = 0.0
            return (h, tbr_val)

        candidates.sort(key=sort_key, reverse=True)
        best_fmt = candidates[0]
        self.log(f"Fallback bestvideo chosen: height={best_fmt.get('height')} "
                 f"tbr={best_fmt.get('tbr') or best_fmt.get('vbr')}")

        return self._pipeline_selected_video_fmt(
            url, best_fmt, video_id, safe_title, duration, override_mbps=override_mbps
        )

    # ----- Audio-only pipeline -----

    def _audio_only_pipeline(self, url, info, safe_title, duration):
        audio_prefix = f"{info.get('id')}.audio."
        self._cleanup_temp(audio_prefix)

        audio_template = os.path.join(self.output_dir, "%(id)s.audio.%(ext)s")
        ytdlp_audio_cmd = [YTDLP_PATH, "--newline", "-f", "bestaudio", "-o", audio_template, url]
        rc = self._run_ytdlp_with_progress(ytdlp_audio_cmd, "Downloading best audio")
        if rc != 0:
            messagebox.showerror("Download failed", f"yt-dlp audio-only failed (code {rc})")
            self.log(f"Audio-only download failed (code {rc})")
            return None

        audio_path = self._find_downloaded(audio_prefix)
        if not audio_path:
            messagebox.showerror("Error", "Audio-only file not found after download.")
            self.log("Audio-only file missing.")
            return None
        self.log(f"Audio file: {audio_path}")

        if not os.path.isfile(FFMPEG_PATH):
            self.log("ffmpeg not found; returning raw audio file without conversion.")
            return audio_path

        output_path = os.path.join(self.output_dir, f"{safe_title}.m4a")
        counter = 1
        base, ext = os.path.splitext(output_path)
        while os.path.exists(output_path):
            output_path = f"{base} ({counter}){ext}"
            counter += 1

        ffmpeg_cmd = [
            FFMPEG_PATH,
            "-y",
            "-i", audio_path,
            "-vn",
            "-c:a", "aac",
            "-b:a", "192k",
            "-movflags", "+faststart",
            output_path,
        ]

        rc = self._run_ffmpeg_with_progress(ffmpeg_cmd, "Converting audio to m4a", duration or 0)
        if rc != 0:
            messagebox.showerror("ffmpeg failed", f"ffmpeg exited with code {rc}")
            self.log(f"ffmpeg failed (audio-only) (code {rc})")
            return None

        self.log("Audio conversion complete (m4a).")

        if not self.keep_raw_var.get():
            try:
                os.remove(audio_path)
                self.log(f"Removed temp audio: {audio_path}")
            except Exception:
                pass

        return output_path


# ---------- Entry point ----------

def main():
    app = YTDLPGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
