# mPyGUI

The (very WIP) ffmpeg GUI (Python Edition). Based on [MPEGUI](https://github.com/plxl/mpegui).

In its current state it does not do anything.

## Requirements

Currently developing with:
- Python >= 3.13
- PySide6
- qt-material
- darkdetect

For building:
- pyinstaller (Windows/Linux)
- py2app (macOS)

## Running

If you want to run from the latest without building, you can install the necessary dependencies and setup the project as a module.

1. Create and enter a virtual environment at the root of the project.

2. Install module and dependencies. Optionally, use `-e` to install the module in editable mode so you can make modifications:
    ```sh
    pip install [-e] .
    ```

3. Run the app
    ```sh
    python -m mpygui
    ```

## Building

The project is setup to use `pyinstaller` for Windows and Linux, and `py2app` for macOS. All binaries are located in `./dist`.

Note that without any optimisations, py2app produces ~1.3GB `.app` bundles due to PySide6.

1. Create and enter a virtual environment at the root of the project.

2. Install all dependencies for building
    ```sh
    pip install ".[build]"
    ```

### Windows / Linux

3. Run `pyinstaller` to build
    ```sh
    pyinstaller --onefile --windowed -n mPyGUI src/mpygui/launch.py
    ```

### macOS

3. Run `setup.py` to build with py2app
    ```sh
    python setup.py py2app
    ```
