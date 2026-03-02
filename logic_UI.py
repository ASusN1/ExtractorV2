import threading
import tkinter as tk
from tkinter import filedialog
from download_logic import get_video_info, get_video_qualities, get_download_option
from animation_player import display_animation
import time

# Store animation reset timers per window
_animation_reset_timers = {}
# Track active downloads to prevent progress updates after completion
_active_downloads = set()

def UI_get_data(link_entry, path_entry, progress_bar, window, quality_listbox=None, download_option_var=None, animation_label=None, status_label=None):
    """Extract values from Entry widgets and start download with progress tracking"""
    link = link_entry.get().strip()
    save_path = path_entry.get().strip()
    
    # Cancel any pending reset timer
    _cancel_reset_timer(window)
    
    # Validate inputs
    if not link or not save_path:
        print("Both fields are required.")
        UI_update_status_label(status_label, "Both fields are required.")
        # Show error animation for validation failure
        if animation_label is not None:
            display_animation(animation_label, 'error')
        # Schedule reset to static after 10 seconds
        _schedule_reset_animation(window, animation_label, 10000)
        return

    # Reset progress bar
    UI_progress_bar_update(progress_bar, 0)
    UI_set_progress_color(progress_bar, 'blue')
    UI_update_status_label(status_label, "Starting download...")

#WHen user select the resolution --> pass that to the download function to download the specific quality
    selected_quality = None
    user_selected_get_video_info = False
    if quality_listbox is not None:
        selection = quality_listbox.curselection()
        if selection:
            selected_quality = quality_listbox.get(selection[0])
            user_selected_get_video_info = True  # User selected from quality list
    
    # Get the download option (audio/video/both)
    download_option = "both"
    if download_option_var is not None:
        download_option = download_option_var.get()
    
    # Start download in background thread
    thread = threading.Thread(
        target=_download_thread,
        args=(link, save_path, progress_bar, window, selected_quality, download_option, user_selected_get_video_info, animation_label, status_label),
        daemon=True
    )
    thread.start()
#----------------------------------------
def UI_browse_path(path_entry): #keep
    # Open a directory chooser and insert the selected path into the Entry widget.
    # Do not create a new root; assume the main application already has one.
    selected = filedialog.askdirectory()
    if not selected:
        return
    path_entry.delete(0, tk.END)
    path_entry.insert(0, selected)

#----------------------------------------
def UI_get_video_info(link_entry, quality_listbox=None): 
    #video info without downloading and return the available qualities to display in the listbox
    # Extract link from the Entry widget and fetch info.
    link = link_entry.get().strip()
    if not link:
        print("Link is required.")
        return
    try:
        qualities = get_video_qualities(link)
        if quality_listbox is not None:
            quality_listbox.delete(0, tk.END)
            if qualities:
                for quality in qualities:
                    quality_listbox.insert(tk.END, quality)
            else:
                quality_listbox.insert(tk.END, "No available video formats found.")
        print(f"Found {len(qualities)} quality options")
    except Exception as e:
        print(f"Error: {e}")

#---------------------------------------------
def UI_progress_bar_update(progress_bar, percentage):
    #Update progress bar value
    if progress_bar is None:
        return
    
    # Clamp percentage between 0 and 100
    percentage = max(0, min(100, percentage))
    progress_bar['value'] = percentage

#---------------------------------------------
def UI_set_progress_color(progress_bar, color):
    #Set progress bar color based on status
    if progress_bar is None:
        return
    
    color_styles = {
        'blue': 'Blue.Horizontal.TProgressbar',
        'green': 'Green.Horizontal.TProgressbar',
        'red': 'Red.Horizontal.TProgressbar'
    }
    
    style = color_styles.get(color, 'Blue.Horizontal.TProgressbar')
    progress_bar.configure(style=style)

#---------------------------------------------
def UI_update_status_label(status_label, text):
    # Update status text under download controls
    if status_label is None:
        return
    status_label.config(text=text)

def _clean_progress_text(text):
    # Remove ANSI color codes from yt-dlp output strings
    if not text:
        return ""
    cleaned = str(text)
    while '\x1b[' in cleaned:
        start = cleaned.find('\x1b[')
        end = cleaned.find('m', start)
        if end == -1:
            cleaned = cleaned[:start]
            break
        cleaned = cleaned[:start] + cleaned[end + 1:]
    return cleaned.strip()

#---------------------------------------------
def _schedule_reset_animation(window, animation_label, delay_ms=10000):
    """Schedule animation reset to static after specified delay"""
    def reset_to_static():
        if animation_label is not None:
            display_animation(animation_label, 'static')
        # Clear the timer
        if window in _animation_reset_timers:
            del _animation_reset_timers[window]
    
    # Schedule the reset
    timer_id = window.after(delay_ms, reset_to_static)
    _animation_reset_timers[window] = timer_id

def _cancel_reset_timer(window):
    """Cancel any pending animation reset timer"""
    if window in _animation_reset_timers:
        window.after_cancel(_animation_reset_timers[window])
        del _animation_reset_timers[window]

#---------------------------------------------
def _progress_hook(d, progress_bar, window, animation_label=None, status_label=None):
    #Process yt-dlp progress data and update UI
    # Ignore progress if download already finished
    if id(window) not in _active_downloads:
        return
    
    if d['status'] == 'downloading':
        downloaded = d.get('downloaded_bytes', 0)
        total = d.get('total_bytes') or d.get('total_bytes_estimate', 1)
        percentage = (downloaded / total * 100) if total > 0 else 0
        UI_set_progress_color(progress_bar, 'blue')
        UI_progress_bar_update(progress_bar, percentage)
        percent_text = _clean_progress_text(d.get('_percent_str', ''))
        total_text = _clean_progress_text(d.get('_total_bytes_str', ''))
        speed_text = _clean_progress_text(d.get('_speed_str', ''))
        eta_text = _clean_progress_text(d.get('_eta_str', ''))

        status_text = f"{percent_text} of {total_text} at {speed_text}".strip()
        if eta_text:
            status_text = f"{status_text} Eastimate time {eta_text}."
        UI_update_status_label(status_label, status_text)
        # Show downloading animation
        if animation_label is not None:
            display_animation(animation_label, 'downloading')
        window.update_idletasks()
    elif d['status'] == 'finished':
        UI_set_progress_color(progress_bar, 'green')
        UI_progress_bar_update(progress_bar, 100)
        UI_update_status_label(status_label, "Download finished. Processing file...")
        # Show success animation
        if animation_label is not None:
            display_animation(animation_label, 'success')
        window.update_idletasks()

#---------------------------------------------
def _download_thread(link, save_path, progress_bar, window, selected_quality, download_option, user_selected_get_video_info, animation_label=None, status_label=None):
    #Run download in background thread with progress tracking
    window_id = id(window)
    _active_downloads.add(window_id)
    
    def progress_callback(d):
        _progress_hook(d, progress_bar, window, animation_label, status_label)
    
    try:
        if animation_label is not None:
            display_animation(animation_label, 'downloading')
        
        get_video_info(link, save_path, progress_callback, selected_quality, download_option, user_selected_get_video_info)
        _active_downloads.discard(window_id)
        
        UI_set_progress_color(progress_bar, 'green')
        UI_update_status_label(status_label, "Download completed successfully.")
        if animation_label is not None:
            display_animation(animation_label, 'success')
        _schedule_reset_animation(window, animation_label, 10000)
        print("Download completed successfully.")
    except Exception as e:
        _active_downloads.discard(window_id)
        print(f"Error: {e}")
        UI_set_progress_color(progress_bar, 'red')
        UI_progress_bar_update(progress_bar, 0)
        UI_update_status_label(status_label, f"Error: {e}")
        if animation_label is not None:
            display_animation(animation_label, 'failed')
        _schedule_reset_animation(window, animation_label, 10000)
#---------------------------------------------
def open_settings_window(parent_window):
    """Open settings popup window"""
    settings_window = tk.Toplevel(parent_window)
    settings_window.title("Settings")
    settings_window.geometry("400x300")
    settings_window.configure(bg="#bcb9b8")
    
    title_label = tk.Label(settings_window, text="Settings", font=("Arial", 14, "bold"))
    title_label.pack(pady=10)
    
    content_frame = tk.Frame(settings_window)
    content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    content_label = tk.Label(content_frame, text="Select an option", wraplength=350, justify=tk.LEFT)
    content_label.pack(fill=tk.BOTH, expand=True)
    
    def show_info():
        content_label.config(text="Info:\nThis is the GIMME VIDEO application.\nVersion 1.0\n\nA tool to download videos easily.")
    
    def show_tutorial():
        content_label.config(text="Tutorial:\n1. Enter video link\n2. Choose save path\n3. Select download option\n4. Click Get Video Info\n5. Click Download Video")
    
    def contribute():
        content_label.config(text="You can contribute to this project:\nFeature coming soon")
    
    button_frame = tk.Frame(settings_window)
    button_frame.pack(pady=10)
    
    tk.Button(button_frame, text="Info", command=show_info, width=15).pack(pady=5)
    tk.Button(button_frame, text="Tutorial", command=show_tutorial, width=15).pack(pady=5)
    tk.Button(button_frame, text="Project contribute", command=contribute, width=15).pack(pady=5)
