from common.logger import log
from mpygui.app.gui import mPyGUI


def main():
    log.info("Starting app")
    mpygui = mPyGUI()
    mpygui.run()


if __name__ == "__main__":
    main()
