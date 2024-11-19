from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt


class FileDropWidget(QLabel):
    def __init__(self, callback):
        super().__init__()
        self.setText("\n\n Drop files here \n\n")
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa
            }
        """)
        self.setAcceptDrops(True)
        self.callback = callback

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        self.callback(files)
