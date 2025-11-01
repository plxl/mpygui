from common.logger import log
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSplitter,
    QFrame,
    QStyleFactory,
    QLabel,
    QPushButton,
)
from PySide6.QtCore import Qt, QEvent
from qt_material import QtStyleTools, apply_stylesheet
import darkdetect

from common.QtExtensions import FileDropList


class MainWindow(QMainWindow, QtStyleTools):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("mPyGUI: The ffmpeg GUI (Python Edition)")
        self.create_layout()
        self.apply_initial_theme()

        self.files = []

    def create_layout(self):
        log.info("Creating layout")

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.central_layout = QVBoxLayout(self.central)

        self.create_top()
        self.create_bottom()
        self.central_layout.addWidget(self.vsplitter)

    def create_top(self):
        self.hsplitter = QSplitter(Qt.Orientation.Horizontal)
        self.create_sidebar()
        self.create_content()
        self.hsplitter.addWidget(self.sidebar)
        self.hsplitter.addWidget(self.content_frame)
        # configure splitter fixed sides and sizes
        self.hsplitter.setStretchFactor(0, 0)
        self.hsplitter.setStretchFactor(1, 1)  # content resizes with window
        self.hsplitter.setSizes([140, 9999])
        self.hsplitter.setCollapsible(0, True)
        self.hsplitter.setCollapsible(1, False)
        self.hsplitter.setMinimumHeight(80)

    def create_sidebar(self):
        self.sidebar = QFrame()
        self.list_files = FileDropList(self.sidebar)
        self.list_files.files_dropped.connect(self.sidebar_on_drop)
        self.list_files.selectionModel().selectionChanged.connect(self.sidebar_on_select)
        self.list_files.setStyleSheet("background: transparent; border: none;")
        self.sidebar_layout = QHBoxLayout(self.sidebar)
        self.sidebar_layout.addWidget(self.list_files)
        self.sidebar.setMinimumWidth(80)

    def sidebar_on_drop(self, files):
        log.info(f"[Sidebar] {len(files)} files dropped")
        for file in files:
            filename = Path(file).name
            self.list_files.addItem(filename)

        self.files.extend(files)

    def sidebar_on_select(self, *_):
        selected = self.get_selected_files()
        log.info(f"[Sidebar] Files Selected: {len(selected)}")

        if len(selected) > 0:
            self.content.setVisible(True)

        else:
            self.content.setVisible(False)

    def get_selected_files(self) -> list[str]:
        return [self.files[i.row()] for i in self.list_files.selectedIndexes()]

    def create_content(self):
        self.content_frame = QFrame()
        self.content_frame.setMinimumWidth(80)
        self.content = QFrame()
        self.content.setStyleSheet("background: red")
        self.content.setVisible(False)
        self.lbl_filename = QLabel(f"Nothing selected")
        self.content_layout = QVBoxLayout(self.content_frame)
        self.content_layout.addWidget(self.lbl_filename)
        self.content_layout.addWidget(self.content)

    def create_bottom(self):
        self.vsplitter = QSplitter(Qt.Orientation.Vertical)
        self.create_cmdout()
        self.vsplitter.addWidget(self.hsplitter)
        self.vsplitter.addWidget(self.cmdout)
        # configure splitter fixed sides and sizes
        self.vsplitter.setStretchFactor(0, 1)
        self.vsplitter.setStretchFactor(1, 0)
        self.vsplitter.setSizes([9999, 120])
        self.vsplitter.setCollapsible(0, False)
        self.vsplitter.setCollapsible(1, True)

    def create_cmdout(self):
        self.cmdout = QFrame()
        self.cmdout.setMinimumHeight(80)

    def apply_initial_theme(self, style=QStyleFactory.create("Fusion")):
        theme = darkdetect.theme().lower()
        if theme == "dark":
            apply_stylesheet(self, theme="dark_purple.xml", style=style)
        else:
            apply_stylesheet(self, theme="light_purple.xml", style=style, invert_secondary=True)

    def changeEvent(self, ev):
        if ev.type() == QEvent.ThemeChange:
            self.apply_initial_theme()
        super().changeEvent(ev)


class mPyGUI:
    def __init__(self):
        self.app = QApplication([])
        self.window = MainWindow()
        self.set_center()

    def set_center(self):
        w, h = 600, 600
        screen = self.app.screens()[0].size()
        x = (screen.width() - w) // 2
        y = (screen.height() - h) // 2
        self.window.setGeometry(x, y, w, h)
        log.info(f"Set window geometry to center: {[x, y, w, h]}")

    def run(self):
        self.window.show()
        self.app.exec()
