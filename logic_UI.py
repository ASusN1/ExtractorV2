import tkinter as tk
from tkinter import filedialog
from download_logic import get_video_info, get_video_qualities


def UI_get_data(link_entry, path_entry): #keep
#Extract values from the given Entry widgets and call downloader
    link = link_entry.get().strip()
    save_path = path_entry.get().strip()
    if not link or not save_path:
        print("Both fields are required.")
        return
    try:
        get_video_info(link, save_path)
        print("Download completed successfully.")
    except Exception as e:
        print(f"Error: {e}")
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
def UI_get_video_info(link_entry, quality_listbox=None): #not sure what to do with quality listbox yet, maybe add a new function to get 
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
