import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt


class SurvalyserMain(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.menu_layout = QtWidgets.QVBoxLayout()
        self.menu_layout.setAlignment(Qt.AlignCenter)

        self.title_label = QLabel("Survalyser")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.menu_layout.addWidget(self.title_label)

        self.resume_btn = QPushButton("Resume")
        self.save_btn = QPushButton("Saves")
        self.load_btn = QPushButton("Load Data")

        self.resume_btn.clicked.connect(self.on_resume)
        self.save_btn.clicked.connect(self.on_save)
        self.load_btn.clicked.connect(self.on_load)

        self.menu_layout.addWidget(self.resume_btn)
        self.menu_layout.addWidget(self.save_btn)
        self.menu_layout.addWidget(self.load_btn)

        self.setLayout(self.menu_layout)
        self.resize(500, 500)
        self.move(100, 100)

        self.setWindowTitle("Survalyser")

        self.show()

    def on_load(self):
        filed = QtWidgets.QFileDialog()
        #filed.setAcceptMode(QtWidgtes.QFileDialog.AcceptOpen)
        filed.show()

    def on_resume(self):
        pass

    def on_save(self):
        pass


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = SurvalyserMain()
    win.show()
    app.exec()


main()
