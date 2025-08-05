import customtkinter as ctk
from app.theme_manager import init_theme
from app.logger import log

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("mPyGUI: The ffmpeg GUI (Python Edition)")

        # center window on screen
        self.width, self.height = 1100, 600
        x = (self.winfo_screenwidth() - self.width) // 2
        y = (self.winfo_screenheight() - self.height) // 2
        self.geometry(f"{self.width}x{self.height}+{x}+{y}")

def main():
    init_theme()

    log.info("Starting app")
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
