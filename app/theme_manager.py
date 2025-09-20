import customtkinter as ctk
from .logger import log
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
THEMES_DIR = BASE_DIR / "themes"

def init_theme():
    log.info("Initialising ctk theme")
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme(THEMES_DIR / "lavender.json")
