import customtkinter as ctk
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
THEMES_DIR = BASE_DIR / "resources"

def init_theme(themes_dir = THEMES_DIR):
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme(themes_dir / "lavender.json")
