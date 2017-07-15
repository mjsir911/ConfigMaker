#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import PySide.QtGui
import PySide.QtCore

from builtins import super

__appname__     = ""
__author__      = "Marco Sirabella"
__copyright__   = ""
__credits__     = ["Marco Sirabella"]  # Authors and bug reporters
__license__     = "GPL"
__version__     = "1.0"
__maintainers__ = "Marco Sirabella"
__email__       = "msirabel@gmail.com"
__status__      = "Prototype"  # "Prototype", "Development" or "Production"
__module__      = ""


class MainWindow(PySide.QtGui.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initGUI()

    def initGUI(self):
        self.setWindowTitle("ScribblerSeq")
        self.showMaximized()

        self.setCentralWidget(MainWidget(parent=self))

        font = PySide.QtGui.QFont()
        font.setFamily(font.defaultFamily())
        font.setPointSize(28)
        self.setFont(font)

        left_layout = PySide.QtGui.QVBoxLayout()
        self.centralWidget().layout().addLayout(left_layout, stretch=2)

        description_layout = PySide.QtGui.QFormLayout(parent=self)
        description_layout.addRow("Ratings description: ",
                                  PySide.QtGui.QLineEdit())
        left_layout.addLayout(description_layout)

        self.show()


class MainWidget(PySide.QtGui.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=None)
        self.setLayout(PySide.QtGui.QHBoxLayout())


if __name__ == '__main__':
    from sys import argv, exit
    app = PySide.QtGui.QApplication(argv)
    dumbthing = MainWindow()
    exit(app.exec_())
