#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import super
from builtins import open
from builtins import zip
from future import standard_library
import PySide.QtCore
import PySide.QtGui
import PySide as Py
import sys
import os
import json


from shared import *

standard_library.install_aliases()

__appname__     = ""
__author__      = "Marco Sirabella"
__copyright__   = ""
__credits__     = ["Marco Sirabella",
                   "Kevin Cole"]  # Authors and bug reporters
__license__     = "GPL"
__version__     = "1.0"
__maintainers__ = "Marco Sirabella"
__email__       = "msirabel@gmail.com"
__status__      = "Prototype"  # "Prototype", "Development" or "Production"
__module__      = ""

responses = {'Single choice': 'single',
             'Multiple choice': 'multi',
             'Fill in': 'fill'
             }


class SubWindow(PySide.QtGui.QDialog):
    maxoptions = 5
    def __init__(self, parent=None):
        self.data = {'type': 'rating'}
        super().__init__(parent)
        self.layout = Py.QtGui.QVBoxLayout()
        sublayout = PySide.QtGui.QFormLayout()
        self.layout.addLayout(sublayout)
        self.name = PySide.QtGui.QLineEdit()
        sublayout.addRow('Response id:', self.name)
        self.question = PySide.QtGui.QLineEdit()
        sublayout.addRow('Question:', self.question)

        #self.questionNum = Py.QtGui.QSpinBox()
        #self.questionNum.setRange(1, 5)

        self.rType = Py.QtGui.QComboBox()
        sublayout.addRow('Response type:', self.rType)

        for button_type in responses.keys():
            self.rType.addItem(button_type)

        self.rType.currentIndexChanged.connect(self.check)

        self.responses = []
        self.parent = parent
        self.questionNum = Py.QtGui.QSpinBox()
        self.questionNum.setRange(2, self.maxoptions)
        self.questionNum.valueChanged.connect(self.responseCheck)
        sublayout.addRow('Number of choices:', self.questionNum)
        for x in range(0, self.maxoptions):
            response = self.Response(x)
            self.responses.append(response)
            self.layout.addWidget(response)

        buttonlayout = PySide.QtGui.QHBoxLayout()
        buttonlayout.addWidget(okbutt(self.write))
        buttonlayout.addWidget(okbutt(
                                      func=lambda: self.close(),
                                      buttonText='Cancel',
        ))
        self.layout.addLayout(buttonlayout)
        self.responseCheck()
        self.setLayout(self.layout)
        self.check()

    def responseCheck(self):
        for x in self.responses:
            x.check(self.questionNum.value())

    def check(self):
        text = self.rType.currentText()
        if text == "Single choice":
            self.questionNum.setRange(2, self.maxoptions)
        elif text == "Multiple choice":
            self.questionNum.setRange(1, self.maxoptions)
        elif text == "Fill in":
            self.questionNum.setRange(0, 0)
        else:
            print('error: {}'.format(text))

    class Response(Py.QtGui.QWidget):
        def __init__(self, num, parent=None):
            super().__init__(parent)
            self.parent = parent
            self.layout = Py.QtGui.QVBoxLayout()
            self.num = num
            #self.hr = Py.QtGui.QSpacerItem(20, 40, Py.QtGui.QSizePolicy.Minimum, Py.QtGui.QSizePolicy.Expanding)
            self.selection = Py.QtGui.QLineEdit()
            self.selection.setPlaceholderText("Text")
            self.questionNum = Py.QtGui.QSpinBox()
            self.recode = Py.QtGui.QSpinBox()
            self.recode.setValue(num + 1)
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

    def write(self):
        self.data['name'] = self.name.text()
        self.data['subtype'] = responses[self.rType.currentText()]
        self.data['question'] = self.question.text()
        self.data['options'] = [(x.recode.value(), x.selection.text())
                                for x in self.responses if not x.isHidden()]
        self.hide()
        if self not in self.parent.things:
            self.parent.things.append(self)
        self.parent.update_dropdown()

    def write_file(self, fp):
        logger.info('writing sub-file %s', fp.name)
        pretty_print = {'sort_keys': True,
                        'indent': 4,
                        'separators': (',', ': ')
                        }
        fp.write(json.dumps(self.data, **pretty_print))


class MyWindow(BaseWindow):
    name = 'rating'
    namevar = 'name'
    subthing = 'question'
    subwind = SubWindow


app = PySide.QtGui.QApplication(sys.argv)
main_window = MyWindow()
main_window.show()
font = app.font()
font.setPointSize(24)
app.setFont(font)
app.exec_()

#if __name__ == '__main__':
#       main()
