import sys
import re
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from file_drop_widget import FileDropWidget
from utils import apply_offset_to_file


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ASS Subtitle Time Offset Adjuster')
        self.setGeometry(100, 100, 400, 200)
        self.layout = QVBoxLayout()

        self.offset_input = QLineEdit(self)
        self.offset_input.setPlaceholderText('Enter time offset in seconds...')
        self.layout.addWidget(self.offset_input)
        self.drop_area = FileDropWidget(self.process_files)
        self.layout.addWidget(self.drop_area)
        self.setLayout(self.layout)

    def process_files(self, files):
        offset = float(self.offset_input.text())

        for file_path in files:
            result = apply_offset_to_file(file_path, offset)
            if result:
                QMessageBox.information(None, "Success", "Offset applied successfully!")
            break


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
