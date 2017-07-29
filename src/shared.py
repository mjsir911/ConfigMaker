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

        with open('style.css', 'r') as fp:
            self.setStyleSheet(fp.read())
        #self.setStyleSheet('* { font-size: 32px; }')

        self.show()


class MainWidget(PySide.QtGui.QGroupBox):
    """ Put main content here """
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setLayout(PySide.QtGui.QHBoxLayout())

        leftlayout = PySide.QtGui.QVBoxLayout()
        rightlayout = PySide.QtGui.QVBoxLayout()
        self.layout().addLayout(leftlayout, 1)
        self.layout().addLayout(rightlayout, 1)

        description_layout = PySide.QtGui.QFormLayout()
        leftlayout.addLayout(description_layout)
        leftlayout.addSpacing(20)

        description_layout.addRow("Ratings &description: ",
                                  PySide.QtGui.QLineEdit())

        self.add_button = PySide.QtGui.QPushButton('Add Question', parent=self)
        self.add_button.setMinimumHeight(50)
        leftlayout.addWidget(self.add_button)
        self.things = PySide.QtGui.QListWidget()
        leftlayout.addWidget(self.things)
        savelayout = PySide.QtGui.QHBoxLayout()
        leftlayout.addLayout(savelayout)

        self.save_button = PySide.QtGui.QPushButton('Save', parent=self)
        savelayout.addStretch(2)
        savelayout.addWidget(self.save_button, stretch=2)
        savelayout.addStretch(2)
        self.save_button.setMinimumHeight(50)
        self.save_button.setAutoDefault(True)
        self.save_button.setDefault(True)


if __name__ == '__main__':
    from sys import argv, exit
    app = PySide.QtGui.QApplication(argv)
    dumbthing = MainWindow()
    exit(app.exec_())
