# setup.py
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
