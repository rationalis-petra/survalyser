from PySide6.QtWidgets import QWidget, QVBoxLayout, QToolBar
from PySide6.QtGui import QAction
from icons import sv_icons


class ToolBarWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.layout = QVBoxLayout()

        self.toolbar = QToolBar()
        self.action_home = QAction(sv_icons.home, "Home", self.toolbar)
        self.action_home.triggered.connect(parent.go_home)

        self.toolbar.addAction(self.action_home)

        self.child = QWidget()

        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.child)

        super().setLayout(self.layout)

    def setLayout(self, layout):
        self.child.setLayout(layout)

    def getBar(self):
        return self.toolbar
