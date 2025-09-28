# mPyGUI

The (very WIP) ffmpeg GUI (Python Edition). Based on [MPEGUI](https://github.com/plxl/mpegui).

In its current state it does not do anything.

Some dependencies may not work on all platforms; such as `tkdnd` not working on NixOS.

## Running

If you want to run from the latest without building, you can install the necessary dependencies and setup the project as a module.

1. Create and enter a virtual environment at the root of the project
```
python -m venv .venv
source .venv/Scripts/activate
```

2. If you want to make edits you can install the module in editable mode
```
pip install -e .
```
OR if you don't plan to make edits then just:
```
pip install .
```

3. Run the app
```
python -m mpygui
```

## Build

The project is setup to use `pyinstaller` for Windows and Linux, and `py2app` for macOS. All binaries are located in `./dist`

1. Create and enter a virtual environment at the root of the project
```
python -m venv .venv
source .venv/Scripts/activate
```

2. Install all dependencies for building
```
pip install ".[build]"
```

### Windows / Linux

3. Run `pyinstaller` to build
```
pyinstaller --onefile --windowed --add-data "src/common/ctk_extensions/themes/resources/*.json:common/ctk_extensions/themes/resources" --name mPyGUI src/mpygui/launch.py
```

### macOS

3. Run `setup.py` to build with py2app
```
python setup.py py2app
```
