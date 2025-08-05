import threading
import darkdetect
import customtkinter as ctk
from .logger import log
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
THEMES_DIR = BASE_DIR / "themes"

def init_theme():
    log.info("Initialising ctk theme")
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme(THEMES_DIR / "lavender.json")
    
    log.info("Creating darkdetect listener")
    t = threading.Thread(target=darkdetect.listener, args=(_on_theme_change,))
    t.daemon = True
    t.start()

    
def _on_theme_change(mode: str):
    log.info(f"_on_theme_change: Detected mode '{mode}'")
    ctk.set_appearance_mode(mode)