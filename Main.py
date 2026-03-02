from tkinter import *
from tkinter.ttk import *
import os
from logic_UI import UI_browse_path, UI_get_data, UI_get_video_info, open_settings_window
from animation_player import display_animation


# Create the main window
window = Tk()
window.title("GIMME VIDEO")
window.configure(bg="#bcb9b8")
# Widgets
Label(window, text="Video Link:").grid(row = 0, column = 0)
link_entry = Entry(window, width=60)
link_entry.grid(row=0, column=1)

Label(window, text="Enter save path:").grid(row=1, column=0, pady=(0, 5))
path_entry = Entry(window, width=60)
path_entry.grid(row=1, column=1, pady=(0, 10))
# Add browse button
browse_button = Button(window, text="BROWSE", command=lambda: UI_browse_path(path_entry))
browse_button.grid(row=1, column=2, pady=(0, 10))

# Get video info button
Select_video = Button(window, text="Get Video Info", command=lambda: UI_get_video_info(link_entry, quality_listbox))
Select_video.grid(row=0, column=2)

# Add radio buttons for audio/video/both options
download_option = StringVar(value="video")
Label(window, text="Download Options:").grid(row=2, column=0, pady=(10, 5), sticky='w')
audio_check = Radiobutton(window, text="Audio Only", variable=download_option, value="audio")
audio_check.grid(row=3, column=0, pady=(0, 5), sticky='w')
video_check = Radiobutton(window, text="Video Only", variable=download_option, value="video")
video_check.grid(row=4, column=0, pady=(0, 5), sticky='w')
both_check = Radiobutton(window, text="Both", variable=download_option, value="both")
both_check.grid(row=5, column=0, pady=(0, 10), sticky='w')

# Fetch video quality info
Label(window, text="Available qualities:").grid(row=2, column=1, pady=(10, 5), sticky='w', columnspan=2)
quality_listbox = Listbox(window, height=8, width=40)
quality_listbox.grid(row=3, column=1, rowspan=3, pady=(0, 10), columnspan=2, sticky='w')
quality_listbox.configure(bg="#8d8986", fg="#000000")

# Download button
download_button = Button(window, text="Download Video", width=20, command=lambda: UI_get_data(link_entry, path_entry, progress_bar, window, quality_listbox, download_option, animation_label, status_label))
download_button.grid(row=6, column=1, pady=(10, 0), sticky='w')

# Status label (between download button and progress bar)
status_label = Label(window, text="", width=60, anchor="center")
status_label.grid(row=7, column=0, pady=(0, 8), columnspan=3)

# Animation label (right side)
animation_label = Label(window, background="#bcb9b8")
animation_label.grid(row=3, column=2, rowspan=3, padx=(8, 0), sticky='nw')
display_animation(animation_label, "static")  # Display static state on startup

# Progress bar
# Style progress bar
style = Style()
style.theme_use('default')
style.configure("TLabel", background="#bcb9b8", foreground="#000000")
style.configure("TRadiobutton", background="#bcb9b8", foreground="#000000")
style.map("TRadiobutton", background=[("active", "#bcb9b8")], foreground=[("active", "#000000")])
style.configure("TButton", background="#8d8986", foreground="#000000")
style.map("TButton", background=[("active", "#8d8986")], foreground=[("active", "#000000")])
style.configure("TEntry", fieldbackground="#8d8986", foreground="#000000")
style.configure("Blue.Horizontal.TProgressbar", troughcolor='white', background='blue', thickness=20)
style.configure("Green.Horizontal.TProgressbar", troughcolor='white', background='green', thickness=20)
style.configure("Red.Horizontal.TProgressbar", troughcolor='white', background='red', thickness=20)

progress_bar = Progressbar(window, orient=HORIZONTAL, length=400, mode='determinate', style="Blue.Horizontal.TProgressbar")
progress_bar.grid(row=8, column=0, pady=(0, 20), columnspan=3)

# Settings button
settings_button = Button(window, text="Settings", width=10, command=lambda: open_settings_window(window))
settings_button.grid(row=6, column=2, pady=10)

# Icon
icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "computer_static.png")
icon = PhotoImage(file=icon_path)
window.iconphoto(True, icon)
window.geometry("600x400")
window.mainloop()