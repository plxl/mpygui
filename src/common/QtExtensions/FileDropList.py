from PySide6.QtWidgets import QListWidget, QAbstractItemView
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent, QWheelEvent


class FileDropList(QListWidget):
    files_dropped = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # --------------------------------------------------------------------------------------------------
        # nice modern smooth scrolling
        # --------------------------------------------------------------------------------------------------
        self._anim = QPropertyAnimation(self.verticalScrollBar(), b"value", self)
        self._anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self._anim.setDuration(150)

    def wheelEvent(self, event: QWheelEvent):
        # trackpad / high-res
        if not event.pixelDelta().isNull():
            delta = event.pixelDelta().y()
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta)
            event.accept()

        # mouse wheel
        elif not event.angleDelta().isNull():
            sb = self.verticalScrollBar()
            cur_value = sb.value()
            end_value = cur_value

            if self._anim.state() == QPropertyAnimation.State.Running:
                self._anim.stop()
                if self._anim.endValue():
                    # allows additive scrolling (goes faster if you move the mousewheel faster)
                    end_value = self._anim.endValue()

            delta = event.angleDelta().y()
            step = -delta * 0.3
            end_value += step

            # lock the value between min and maximum so it animates
            # smoothly to top/bottom even when scrolling past
            if end_value > cur_value:
                end_value = min(end_value, sb.maximum())
            else:
                end_value = max(end_value, sb.minimum())

            self._anim.setStartValue(cur_value)
            self._anim.setEndValue(end_value)
            self._anim.start()

            event.accept()

        else:
            super().wheelEvent(event)

    # --------------------------------------------------------------------------------------------------
    # drag and drop events
    # --------------------------------------------------------------------------------------------------
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            files = []
            for url in event.mimeData().urls():
                local_path = url.toLocalFile()
                if local_path:
                    files.append(local_path)

            if files:
                self.files_dropped.emit(files)
            event.acceptProposedAction()
        else:
            event.ignore()
