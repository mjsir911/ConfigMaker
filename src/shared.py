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

        self.show()


class MainWidget(PySide.QtGui.QGroupBox):
    """ Put main content here """
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setLayout(PySide.QtGui.QHBoxLayout())

        description_layout = PySide.QtGui.QFormLayout()
        self.layout().addLayout(description_layout)

        description_layout.addRow("Ratings &description: ",
                                  PySide.QtGui.QLineEdit())


if __name__ == '__main__':
    from sys import argv, exit
    app = PySide.QtGui.QApplication(argv)
    dumbthing = MainWindow()
    exit(app.exec_())
