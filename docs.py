import sys
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QFileDialog
from PySide6.QtWidgets import (QTableWidget, QHBoxLayout, QVBoxLayout,
                               QStackedLayout, QTextEdit)
from PySide6.QtCore import Qt

welcome_path = "documentation/welcome"
load_path = "documentation/load"
spreadsheet_path = "documentation/spreadsheet"
analyse_path = "documentation/analyse"

class DocumentationTextArea(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.layout = QStackedLayout()

        self.welcome_text = QTextEdit()
        self.load_text = QTextEdit()
        self.spreadsheet_text = QTextEdit()
        self.analyse_text = QTextEdit()

        self.welcome_text.setReadOnly(True)
        self.load_text.setReadOnly(True)
        self.spreadsheet_text.setReadOnly(True)
        self.analyse_text.setReadOnly(True)

        self.welcome_text.append(open(welcome_path).read())
        self.load_text.append(open(load_path).read())
        self.spreadsheet_text.append(open(spreadsheet_path).read())
        self.analyse_text.append(open(analyse_path).read())

        self.layout.addWidget(self.welcome_text)
        self.layout.addWidget(self.load_text)
        self.layout.addWidget(self.spreadsheet_text)
        self.layout.addWidget(self.analyse_text)

        self.setLayout(self.layout)


class DocumentationButtonArrea(QWidget):
    def __init__(self, parent, text_area):
        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)

        self.welcome_button = QPushButton("Welcome")
        self.load_button = QPushButton("Loading Data")
        self.spreadsheet_button = QPushButton("Spreadsheet View")
        self.analyse_button = QPushButton("Analysing Data")

        self.welcome_button.clicked.connect(parent.welcome)
        self.load_button.clicked.connect(parent.load)
        self.spreadsheet_button.clicked.connect(parent.spreadsheet)
        self.analyse_button.clicked.connect(parent.analyse)

        self.layout.addWidget(self.welcome_button)
        self.layout.addWidget(self.load_button)
        self.layout.addWidget(self.spreadsheet_button)
        self.layout.addWidget(self.analyse_button)

        self.setLayout(self.layout)


class DocumentationWindow(ToolBarWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QHBoxLayout()
        self.text_area = DocumentationTextArea(self)
        self.button_area = DocumentationButtonArrea(self, self.text_area)

        self.layout.addWidget(self.button_area)
        self.layout.addWidget(self.text_area)
        self.setLayout(self.layout)

    def welcome(self):
        self.text_area.layout.setCurrentIndex(0)

    def load(self):
        self.text_area.layout.setCurrentIndex(1)

    def spreadsheet(self):
        self.text_area.layout.setCurrentIndex(2)

    def analyse(self):
        self.text_area.layout.setCurrentIndex(3)
