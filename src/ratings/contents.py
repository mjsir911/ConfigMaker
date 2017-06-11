#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import
from builtins import range
from builtins import super
from builtins import str
from builtins import round
from future import standard_library
standard_library.install_aliases()
import PySide as Py

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

class MainWidget(Py.QtGui.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = Py.QtGui.QVBoxLayout()




        # Actual content inside window
        self.resultsInput = Py.QtGui.QLineEdit()
        labelgroup = Py.QtGui.QHBoxLayout()
        desclabel = Py.QtGui.QLabel("Description")
        self.resultsInput.setPlaceholderText("Description")

        # Fix focus probs
        self.resultsInput.selectAll()
        self.resultsInput.setFocus()
        self.resultsInput.clearFocus()

        #self.resultsInput.setPlaceholderText(Py.QtGui.QApplication.translate("mainWindow", "Username", None, Py.QtGui.QApplication.UnicodeUTF8)) # Why translate when you could not?
        # Sub layouts inside of layouts!
        buttonlayout = Py.QtGui.QHBoxLayout()
        buttonlayout.setSpacing(-0.1)
        self.ratingsButton = Py.QtGui.QPushButton("Ratings")
        self.ratingsButton = Py.QtGui.QToolButton()
        self.ratingsButton.setText("Ratings")
        # Hi
        self.ratingsWidget = RatingsWidget(self)
        # Make buttons do stuff
        self.ratingsButton.clicked.connect(self.ratingsWidget.show)

        labelgroup.addWidget(desclabel)
        labelgroup.addWidget(self.resultsInput)
        self.layout.addLayout(labelgroup)
        buttonlayout.addWidget(self.ratingsButton)
        # Add Widgets to layout
        self.layout.addLayout(buttonlayout)
        self.setLayout(self.layout)

class RatingsWidget(Py.QtGui.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.alltheratings = []
        self.layout = Py.QtGui.QVBoxLayout()
        self.rName = Py.QtGui.QComboBox()
        self.rName.setEditable(True)
        self.rName.hide()
        #Set editable
        # Allow duplicates
        # Insert policy
        self.rName.currentIndexChanged.connect(self.change)
        self.layout.addWidget(self.rName)
        self.setLayout(self.layout)
        self.hide()
    def show(self):
        super().show()
        self.parent.layout.addWidget(self)
        self.parent.ratingsButton.setEnabled(False)

    def add(self):
        rating = SingularRating()
        for oldrating in self.alltheratings:
            try:
                self.layout.removeWidget(oldrating)
                oldrating.hide()
            except:
                pass
                #print(e) # if there are no ratings, cant remove one more
        self.alltheratings.append(rating)
        self.layout.addWidget(rating)
        self.rName.addItem("Question {} Label".format(self.rName.currentIndex() + 2))
        self.rName.setCurrentIndex(self.rName.count() - 1)
        self.show()

        # Show the combo box when its shown
        self.rName.show()
    def change(self):
        for oldrating in self.alltheratings:
            try:
                self.layout.removeWidget(oldrating)
                oldrating.hide()
            except Exception as e:
                print(e)
        #print(Py.QtGui.QComboBox.InsertAfterCurrent)
        self.rName.setInsertPolicy(Py.QtGui.QComboBox.InsertPolicy(Py.QtGui.QComboBox.InsertAfterCurrent))
        if self.rName.count() > len(self.alltheratings):
            print(self.rName.currentIndex() - 1)
            self.rName.removeItem(self.rName.currentIndex() - 1)
        currentrating = self.alltheratings[self.rName.currentIndex()]
        self.layout.addWidget(currentrating)
        self.rName.setInsertPolicy(
                self.rName.InsertPolicy(
                        self.rName.InsertAfterCurrent))
        currentrating.show()

class SingularRating(Py.QtGui.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = Py.QtGui.QVBoxLayout()
        #self.nameInput = Py.QtGui.QLineEdit()
        #self.nameInput.setPlaceholderText("Name")
        self.question = Py.QtGui.QLineEdit()
        self.question.setPlaceholderText("Question")
        #self.questionNum = Py.QtGui.QSpinBox()
        #self.questionNum.setRange(1, 5)
        self.options = OptionalOptions(layout, parent=self)
        self.rType = Py.QtGui.QComboBox()
        self.rType.addItem("Radio Buttons")
        self.rType.addItem("Check Boxes")
        self.rType.addItem("Free Response")
        self.rType.currentIndexChanged.connect(self.options.check)
        #layout.addWidget(self.nameInput)
        #layout.addWidget(self.questionNum)
        layout.addWidget(self.question)
        layout.addWidget(self.rType)
        self.setLayout(layout)
        self.options.check()

class OptionalOptions(Py.QtGui.QWidget):
    maxoptions = 5
    def __init__(self, playout, parent=None):
        super().__init__(parent)
        self.responses = []
        self.playout = playout
        self.parent = parent
        layout = Py.QtGui.QVBoxLayout()
        self.questionNum = Py.QtGui.QSpinBox()
        self.questionNum.setRange(2, self.maxoptions)
        self.questionNum.valueChanged.connect(self.responseCheck)
        layout.addWidget(self.questionNum)
        self.setLayout(layout)
        for x in range(0, self.maxoptions):
            response = Responses(x)
            self.responses.append(response)
            layout.addWidget(response)
        self.responseCheck()
        self.hide()
    def responseCheck(self):
        for x in self.responses:
            x.check(self.questionNum.value())
    def check(self):
        text = self.parent.rType.currentText()
        if text == "Radio Buttons":
            self.show()
            self.questionNum.setRange(2, self.maxoptions)
        elif text == "Check Boxes":
            self.show()
            self.questionNum.setRange(1, self.maxoptions)
        elif text == "Free Response":
            self.hide()
        else:
            print(text)
    def show(self):
        super().show()
        self.playout.addWidget(self)
    def hide(self):
        super().hide()
        self.playout.removeWidget(self)

class Responses(Py.QtGui.QWidget):
    def __init__(self, num, parent=None):
        super().__init__(parent)
        self.layout = Py.QtGui.QVBoxLayout()
        self.num = num
        #self.hr = Py.QtGui.QSpacerItem(20, 40, Py.QtGui.QSizePolicy.Minimum, Py.QtGui.QSizePolicy.Expanding)
        self.selection = Py.QtGui.QLineEdit()
        self.selection.setPlaceholderText("Text")
        self.questionNum = Py.QtGui.QSpinBox()
        self.recode = Py.QtGui.QSpinBox()
        #self.recode.setPlaceholderText("Number")
        self.questionNum.setRange(0, -1)

        self.hbox = Py.QtGui.QHBoxLayout()
        self.hbox.addWidget(self.recode)
        self.hbox.addWidget(self.selection)
        self.layout.addLayout(self.hbox)
        #self.layout.addItem(self.hr)
        self.setLayout(self.layout)
    def check(self, maxnum):
        if self.num > maxnum - 1:
            self.hide()
        else:
            self.show()