from tkinter import *
from tkinter.ttk import *

# Dark mode colors
DARK_BG = "#262626"  # Black background
DARK_BTN = "#FF7F11"  # Orange button color
DARK_TEXT = "#FFFDD0"  # Cream/off-white text color

# Light mode colors (default tkinter colors)
LIGHT_BG = "#f0f0f0"  # Default light gray
LIGHT_BTN = "#d9d9d9"  # Default button gray
LIGHT_TEXT = "#000000"  # Black text


def apply_dark_mode(window, widgets_dict):
    """Apply dark mode theme to the main window and all widgets"""
    # Set window background
    window.configure(bg=DARK_BG)
    
    # Apply to all Labels
    for label in widgets_dict.get('labels', []):
        label.configure(background=DARK_BG, foreground=DARK_TEXT)
    
    # Apply to all Entry widgets
    for entry in widgets_dict.get('entries', []):
        entry.configure(background="#333333", foreground=DARK_TEXT, insertbackground=DARK_TEXT)
    
    # Apply to all Buttons (ttk)
    style = Style()
    style.configure("Dark.TButton", background=DARK_BTN, foreground=DARK_TEXT)
    for button in widgets_dict.get('buttons', []):
        button.configure(style="Dark.TButton")
    
    # Apply to Listbox
    for listbox in widgets_dict.get('listboxes', []):
        listbox.configure(background="#333333", foreground=DARK_TEXT, selectbackground=DARK_BTN)
    
    # Apply to Radiobuttons
    for radio in widgets_dict.get('radiobuttons', []):
        radio.configure(background=DARK_BG, foreground=DARK_TEXT)
    
    # Update progress bar styles for dark mode
    style.configure("Blue.Horizontal.TProgressbar", troughcolor='#333333', background=DARK_BTN, thickness=20)
    style.configure("Green.Horizontal.TProgressbar", troughcolor='#333333', background='#00FF00', thickness=20)
    style.configure("Red.Horizontal.TProgressbar", troughcolor='#333333', background='#FF0000', thickness=20)


def apply_light_mode(window, widgets_dict):
    """Apply light mode theme to the main window and all widgets"""
    # Set window background
    window.configure(bg=LIGHT_BG)
    
    # Apply to all Labels
    for label in widgets_dict.get('labels', []):
        label.configure(background=LIGHT_BG, foreground=LIGHT_TEXT)
    
    # Apply to all Entry widgets
    for entry in widgets_dict.get('entries', []):
        entry.configure(background="white", foreground=LIGHT_TEXT, insertbackground=LIGHT_TEXT)
    
    # Apply to all Buttons (ttk)
    style = Style()
    style.configure("Light.TButton", background=LIGHT_BTN, foreground=LIGHT_TEXT)
    for button in widgets_dict.get('buttons', []):
        button.configure(style="Light.TButton")
    
    # Apply to Listbox
    for listbox in widgets_dict.get('listboxes', []):
        listbox.configure(background="white", foreground=LIGHT_TEXT, selectbackground="#0078d7")
    
    # Apply to Radiobuttons
    for radio in widgets_dict.get('radiobuttons', []):
        radio.configure(background=LIGHT_BG, foreground=LIGHT_TEXT)
    
    # Update progress bar styles for light mode
    style.configure("Blue.Horizontal.TProgressbar", troughcolor='white', background='blue', thickness=20)
    style.configure("Green.Horizontal.TProgressbar", troughcolor='white', background='green', thickness=20)
    style.configure("Red.Horizontal.TProgressbar", troughcolor='white', background='red', thickness=20)


def open_theme_selector(window, widgets_dict):
    """Open a popup window for theme selection"""
    popup = Toplevel(window)
    popup.title("Select Theme")
    popup.geometry("300x150")
    popup.configure(bg=DARK_BG)
    popup.resizable(False, False)
    
    # Center the popup
    popup.transient(window)
    popup.grab_set()
    
    # Title label
    title_label = Label(popup, text="Choose Your Theme", background=DARK_BG, foreground=DARK_TEXT)
    title_label.pack(pady=20)
    
    # Button frame
    button_frame = Frame(popup)
    button_frame.configure(style="Dark.TFrame")
    button_frame.pack(pady=10)
    
    # Dark mode button
    def select_dark():
        apply_dark_mode(window, widgets_dict)
        popup.destroy()
    
    dark_btn = Button(button_frame, text="Dark Mode", command=select_dark, width=15)
    dark_btn.configure(style="Dark.TButton")
    dark_btn.pack(side=LEFT, padx=10)
    
    # Light mode button
    def select_light():
        apply_light_mode(window, widgets_dict)
        popup.destroy()
    
    light_btn = Button(button_frame, text="Light Mode", command=select_light, width=15)
    light_btn.configure(style="Dark.TButton")
    light_btn.pack(side=LEFT, padx=10)
