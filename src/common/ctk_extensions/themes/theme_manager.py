import customtkinter as ctk
from importlib import resources
import os

def init_theme():
    theme_path = resources.files("common.ctk_extensions.themes.resources").joinpath("lavender.json")
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme(os.fspath(theme_path))
