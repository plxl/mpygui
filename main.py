import customtkinter as ctk
from app.theme_manager import init_theme
from app.logger import log
from tkinterdnd2 import DND_FILES, TkinterDnD
from utils import parse_tkdnd_files
from pathlib import Path

PD = 10 # global padding
CR = 20 # global corner radius

class App(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self):
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)  

        self.title("mPyGUI: The ffmpeg GUI (Python Edition)")
        self.set_center()
        self.create_layout()

    def set_center(self):
        self.width, self.height = 1100, 600
        x = (self.winfo_screenwidth() - self.width) // 2
        y = (self.winfo_screenheight() - self.height) // 2
        self.geometry(f"{self.width}x{self.height}+{x}+{y}")

    def create_layout(self):
        self.grid_columnconfigure(0, weight=0) # list files
        self.grid_columnconfigure(1, weight=1) # controls
        self.grid_rowconfigure(0, weight=1) # list and controls
        self.grid_rowconfigure(1, weight=0) # command + output
        
        self.create_sidebar()

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, corner_radius=CR)
        self.sidebar.grid(row=0, rowspan=1, column=0, padx=PD, pady=PD, sticky="ns")
        
        self.sidebar.drop_target_register(DND_FILES)
        self.sidebar.dnd_bind("<<Drop>>", self.sidebar_on_drop)
        self.files = []
        self.file_buttons = []

    def sidebar_on_drop(self, event):
        files = [f[0] or f[1] for f in parse_tkdnd_files(event.data)]
        
        for i, file in enumerate(files):
            row_index = len(self.files) + i
            filename = Path(file).name
            button = ctk.CTkButton(self.sidebar, text=filename, anchor="w", corner_radius=10)
            button.grid(row=row_index, column=0, padx=PD, pady=(PD, 0), sticky="new")
            self.file_buttons.append(button)
        
        # append only after adding buttons for correct row indicies
        self.files.extend(files)
        


def main():
    init_theme()

    log.info("Starting app")
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
