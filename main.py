import customtkinter as ctk
from app.theme_manager import init_theme
from app.logger import log

PD = 10 # global padding
CR = 20 # global corner radius

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

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

def main():
    init_theme()

    log.info("Starting app")
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
