from tkinter import *
from tkinter.ttk import *
from logic_UI import UI_browse_path, UI_get_data, UI_get_video_info

#Create the main window
window = Tk()
window.title("Extractor V2")
window.geometry("900x600")
#------------------------------------
#widgets
Label(window, text="Video Link:").pack(pady=(20, 5))
link_entry = Entry(window, width=80)
link_entry.pack(pady=(0, 20))

Label(window, text="Enter save path:").pack(pady=(0, 5))
path_entry = Entry(window, width=60)
path_entry.pack(pady=(0, 10))
#adding browse button 
browse_button = Button(window, text="Browse", command=lambda: UI_browse_path(path_entry))
browse_button.pack(pady=(0, 20))

#download button
download_button = Button(window, text="Download Video",command=lambda: UI_get_data(link_entry, path_entry))
download_button.pack(pady=(10, 20))

#Fetch video quaility info 
Label(window, text="Available qualities:").pack(pady=(0, 5))
quality_listbox = Listbox(window, height=8, width=30)
quality_listbox.pack(pady=(0, 10))

Select_video = Button(window, text="Get Video Info", command=lambda: UI_get_video_info(link_entry, quality_listbox))
Select_video.pack(pady=(10, 20))

window.mainloop()