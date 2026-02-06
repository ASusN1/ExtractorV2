from tkinter import *
from tkinter.ttk import *
from download_logic import get_video_info


window = Tk()
window.title("Extractor V2")

#User enter link from youyube 
Label(window, text="YouTube Video Link:").pack(pady=(20, 5))
link_entry = Entry(window, width=80)
link_entry.pack(pady=(0, 20))
#Get path from usser : either type or browse
Label(window, text="Enter save path:").pack(pady=(0, 5))
path_entry = Entry(window, width=80)
path_entry.pack(pady=(0, 10))
#download button
button = Button(window, text="Download Video", )

#overal shape 0

window.geometry("900x600")
window.mainloop()