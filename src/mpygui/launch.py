if __name__ == "__main__":
    print("Launch app with 'python -m mpygui' from root")
    exit()

from src.common.ctk_extensions.themes import theme_manager
from src.common.logger import log
from .app.gui import App

def main():
    log.info("Initialising themes")
    theme_manager.init_theme()
    
    log.info("Starting app")
    app = App()
    app.mainloop()
