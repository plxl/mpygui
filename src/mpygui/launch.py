from common.ctk_extensions.themes import theme_manager
from common.logger import log
from mpygui.app.gui import App

def main():
    log.info("Initialising themes")
    theme_manager.init_theme()
    
    log.info("Starting app")
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
