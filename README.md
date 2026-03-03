# Video Downloader

A simple GUI application for downloading videos from YouTube and other platforms.

## Features
- Easy-to-use graphical interface
- Quality selection
- Audio-only, video-only, or both options
- Live download progress with speed and ETA
- Animated status indicators

## Requirements
- Python 3.7+
- yt-dlp
- Pillow

## Installation

```bash
pip install yt-dlp Pillow
```

## Usage

```bash
python Main.py
```

1. Paste video URL
2. Choose save location
3. Click "Get Video Info" to see quality options (optional)
4. Select download type (audio/video/both)
5. Click "Download Video"

## Files to Commit to GitHub

✅ **DO COMMIT:**
- `Main.py`
- `logic_UI.py`
- `download_logic.py`
- `animation_player.py`
- All `computer_*.png` and `computer_*.gif` files
- `.gitignore`
- `README.md`

❌ **DO NOT COMMIT:**
- `build/` folder (contains build artifacts with personal paths)
- `dist/` folder (contains .exe, large file)
- `__pycache__/` folder (Python cache)
- `*.spec` files (PyInstaller spec)
- `goals.txt` (personal notes)
- `test.py` (personal test file)

The `.gitignore` file automatically excludes these for you.

## Legal
Use this tool responsibly and respect copyright laws.
