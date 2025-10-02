# this is for building on macOS with py2app only

# for Windows/Linux, use:
# pyinstaller --onefile --windowed -n mPyGUI src/mpygui/launch.py

# on macOS:
# python setup.py py2app

from setuptools import setup

APP = ["src/mpygui/launch.py"]
OPTIONS = {
    "packages": ["mpygui", "common"],
}

setup(
    app=APP,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
