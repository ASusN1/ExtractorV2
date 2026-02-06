from tkinter import *
from tkinter.ttk import *
from download_logic import get_video_info
from logic_UI import UI_get_data

#Create the main window
window = Tk()
window.title("Extractor V2")
window.geometry("900x600")
#------------------------------------

#widgets
#User enter link from youyube 
Label(window, text="Video Link:").pack(pady=(20, 5))
link_entry = Entry(window, width=80)
link_entry.pack(pady=(0, 20))
#Get path from usser : either type or browse
Label(window, text="Enter save path:").pack(pady=(0, 5))
path_entry = Entry(window, width=80)
path_entry.pack(pady=(0, 10))
#download button
#button = Button(window, text="Download Video", )

window.mainloop()