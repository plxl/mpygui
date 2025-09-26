import customtkinter as ctk
import tkinter as tk
from app.theme_manager import init_theme
from app.logger import log
from tkinterdnd2 import DND_FILES, TkinterDnD
from app.utils import parse_tkdnd_files
from pathlib import Path
from app.splitter import Splitter
from app.ctk_custom_listbox import CTkCustomListbox

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
        self.width, self.height = 600, 600
        x = (self.winfo_screenwidth() - self.width) // 2
        y = (self.winfo_screenheight() - self.height) // 2
        self.geometry(f"{self.width}x{self.height}+{x}+{y}")

    def create_layout(self):
        self.grid_columnconfigure(0, weight=0) # list files
        self.grid_columnconfigure(1, weight=0) # splitter
        self.grid_columnconfigure(2, weight=1) # controls
        self.grid_rowconfigure(0, weight=1) # list and controls
        self.grid_rowconfigure(1, weight=0) # splitter
        self.grid_rowconfigure(1, weight=0) # command + output

        self.create_sidebar()
        self.create_output()

    def create_sidebar(self):
        self.sidebar = CTkCustomListbox(
            self,
            width=120,
            corner_radius=CR,
            border_width=0,
            fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"],
            multiple_selection=True,
            command=self.sidebar_on_select
        )
        self.sidebar.grid(row=0, column=0, padx=(PD, PD/2), pady=(PD, PD/2), sticky="nesw")
        self.sidebar.grid_columnconfigure(0, weight=1)
        
        # add splitter for resizing
        self.sidebar_splitter = Splitter(self, self.sidebar)
        self.sidebar_splitter.grid(row=0, column=1, sticky="ns")
        
        # parent frame is required when using either ScrollableFrame or CTkListbox
        self.sidebar._parent_frame.drop_target_register(DND_FILES)
        self.sidebar._parent_frame.dnd_bind("<<Drop>>", self.sidebar_on_drop)
        self.files = []

    def sidebar_on_drop(self, event):
        files = [f[0] or f[1] for f in parse_tkdnd_files(event.data)]
        
        for file in files:
            filename = Path(file).name
            self.sidebar.insert("END", filename)
        
        # append only after adding buttons for correct row indicies
        self.files.extend(files)
        
    def sidebar_on_select(self, value):
        indicies = self.sidebar.curselection()
        print(indicies)
        
    def create_output(self):
        self.output = ctk.CTkFrame(self, height=140, corner_radius=CR)
        self.output.grid(row=3, columnspan=3, padx=(PD, PD/2), pady=(PD/2, PD), sticky="nsew")
        
        # add splitter for resizing
        self.output_splitter = Splitter(self, self.output, orientation=tk.HORIZONTAL)
        self.output_splitter.grid(row=1, columnspan=3, sticky="ew")
        


def main():
    init_theme()

    log.info("Starting app")
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
