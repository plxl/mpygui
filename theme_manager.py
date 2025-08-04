import threading
import darkdetect
import customtkinter as ctk

def init_theme():
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("themes/lavender.json")
    
    t = threading.Thread(target=darkdetect.listener, args=(_on_theme_change,))
    t.daemon = True
    t.start()

    
def _on_theme_change(mode: str):
    ctk.set_appearance_mode(mode)