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
import PySide
import contents

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


def layout(text, inputobj):
    layout = PySide.QtGui.QHBoxLayout()
    label  = PySide.QtGui.QLabel(text)
    layout.addWidget(label)
    layout.addWidget(inputobj)
    try:
        inputobj.setPlaceholderText(text)
    except:
        pass
    return layout

def wandl(widget, layout):
    widget.layout = layout
    widget.setLayout(widget.layout)
    return widget

def okbutt(layout, func, button=None):
    ok = 'OK'
    if button is None:
        button = PySide.QtGui.QPushButton(ok)
    else:
        if button.text() is not "":
            button.setText(ok)
    button.clicked.connect(func)
    layout.addWidget(button)
    return button

savedcontents = {
        'ratings': []
        }

mainWidget = wandl(PySide.QtGui.QWidget(), PySide.QtGui.QVBoxLayout())
description = PySide.QtGui.QLineEdit()
mainWidget.layout.addLayout(layout('Description', description))
description_ok = PySide.QtGui.QPushButton()
description_ok.setText('OK')

def lockDescription():
    """ Take a description and on ok hide """
    text = description.text()
    if text:
        description.setEnabled(False)
        savedcontents['description'] = description.text()
        mainWidget.layout.removeWidget(description_ok)
        description_ok.hide()
    else:
        PySide.QtGui.QMessageBox.critical(mainWidget, 'Empty Description',
        'Description box cannot be empty')

okbutt(mainWidget.layout, lockDescription, description_ok)

rW = ratingsWidget  = wandl(PySide.QtGui.QWidget(), PySide.QtGui.QVBoxLayout())
rW.rName = PySide.QtGui.QComboBox()
rW.rName.setEditable(True)
rW.layout.addWidget(rW.rName)

alltheratings = []

class SingularRating(PySide.QtGui.QWidget):
    def __init__(self):
        self.parent = ratingsWidget
        self.num = self.parent.rName.count()
        self.parent.rName.addItem("Question {} Label".format(self.num))
        self.parent.rName.setCurrentIndex(self.num)
        alltheratings.append(self)
        print(self.num)
        super().__init__(self.parent)
        layout = PySide.QtGui.QVBoxLayout()
        #self.nameInput = PySide.QtGui.QLineEdit()
        #self.nameInput.setPlaceholderText("Name")
        self.question = PySide.QtGui.QLineEdit()
        self.question.setPlaceholderText("Question")
        #self.questionNum = PySide.QtGui.QSpinBox()
        #self.questionNum.setRange(1, 5)
        self.options = OptionalOptions(layout, parent=self)
        self.rType = PySide.QtGui.QComboBox()
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
        self.show()
        #self.parent.layout.addWidget(self)

    def show(self):
        super().show()
        #for old in alltheratings:
            #try:
                #old.hide()
            #except:
                #pass
        #self.parent.rName.setCurrentIndex(self.num)
        self.parent.layout.addWidget(self)

    def hide(self):
        self.parent.rName.setCurrentIndex(-1)
        self.parent.layout.removeWidget(self)
        super().hide()

    def ok(self):
        oner = {}
        savedcontents['ratings'].append(oner)
        oner['name'] = self.parent.rName.itemText(self.num)
        oner['question'] = self.question.text()
        if self.rType.currentText() == "Free Response":
            subtype = "free"
        elif self.rType.currentText() == "Check Boxes":
            subtype = "check"
        elif self.rType.currentText() == "Radio Buttons":
            subtype = "radio"
        else:
            print(self.rType.currentText())

        oner['subtype'] = subtype
        oner['options'] = []

        if subtype is not "free":
            print('not free')
            for option in self.options.responses:
                print('for opt in responses')
                if not option.isHidden():
                    print('if not hid')
                    option = [option.selection.text(),
                            option.recode.value()]
                    oner['options'].append(option)
                    print(option)
        else:
            oner['options'] = None

        self.hide()

ratingsWidget.add = SingularRating


ratings_ok = PySide.QtGui.QPushButton()
ratings_ok.setText('OK')

def okRating():
    current = alltheratings[ratingsWidget.rName.currentIndex()]
    current.ok()

okbutt(ratingsWidget.layout, okRating, ratings_ok)

def onComboChange():
    i = ratingsWidget.rName.currentIndex()
    print(i)
    if i >= 0:
        selected = alltheratings[ratingsWidget.rName.currentIndex()]
        selected.show()
        rW.layout.addWidget(selected)

ratingsWidget.rName.currentIndexChanged.connect(onComboChange)

class OptionalOptions(PySide.QtGui.QWidget):
    maxoptions = 5
    def __init__(self, playout, parent=None):
        super().__init__(parent)
        self.responses = []
        self.playout = playout
        self.parent = parent
        layout = PySide.QtGui.QVBoxLayout()
        self.questionNum = PySide.QtGui.QSpinBox()
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

class Responses(PySide.QtGui.QWidget):
    def __init__(self, num, parent=None):
        super().__init__(parent)
        self.layout = PySide.QtGui.QVBoxLayout()
        self.num = num
        #self.hr = PySide.QtGui.QSpacerItem(20, 40, PySide.QtGui.QSizePolicy.Minimum, PySide.QtGui.QSizePolicy.Expanding)
        self.selection = PySide.QtGui.QLineEdit()
        self.selection.setPlaceholderText("Text")
        self.questionNum = PySide.QtGui.QSpinBox()
        self.recode = PySide.QtGui.QSpinBox()
        #self.recode.setPlaceholderText("Number")
        self.questionNum.setRange(0, -1)

        self.hbox = PySide.QtGui.QHBoxLayout()
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

#z = contents.RatingsWidget(mainWidget)
mainWidget.layout.addWidget(ratingsWidget)
mainWidget.ratingsWidget = ratingsWidget
