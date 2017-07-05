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
standard_library.install_aliases()
import PySide.QtCore
import PySide.QtGui
import PySide as Py
import sys
import os
import json

from shared import *

__appname__     = ''
__author__      = 'Marco Sirabella'
__copyright__   = ''
__credits__     = ['Marco Sirabella',
                   'Kevin Cole']  # Authors and bug reporters
__license__     = 'GPL'
__version__     = '1.0'
__maintainers__ = 'Marco Sirabella'
__email__       = 'msirabel@gmail.com'
__status__      = 'Prototype'  # 'Prototype', 'Development' or 'Production'
__module__      = ''


responses = {'radio': 0, 'check': 1, 'free': 2}

responses = {'Radio Buttons': 'radio',
             'Check Boxes': 'check',
             'Free Response': 'free'
             }


class SubWindow(PySide.QtGui.QDialog):
        maxoptions = 5

        def __init__(self, parent=None):
                self.data = {'type': 'rating'}
                super().__init__(parent)
                self.layout = Py.QtGui.QVBoxLayout()
                self.name = description_and_label('Column Heading',
                                                  Py.QtGui.QLineEdit())
                self.layout.addLayout(self.name)
                self.question = description_and_label('Question',
                                                      Py.QtGui.QLineEdit())
                self.layout.addLayout(self.question)

                #self.questionNum = Py.QtGui.QSpinBox()
                #self.questionNum.setRange(1, 5)

                self.rType = Py.QtGui.QComboBox()

                for button_type in responses.keys():
                        self.rType.addItem(button_type)

                self.rType.currentIndexChanged.connect(self.check)
                self.layout.addWidget(self.rType)

                self.responses = []
                self.parent = parent
                self.questionNum = Py.QtGui.QSpinBox()
                self.questionNum.setRange(2, self.maxoptions)
                self.questionNum.valueChanged.connect(self.responseCheck)
                self.layout.addWidget(self.questionNum)
                for x in range(0, self.maxoptions):
                        response = self.Response(x)
                        self.responses.append(response)
                        self.layout.addWidget(response)

                buttonlayout = PySide.QtGui.QHBoxLayout()
                buttonlayout.addWidget(okbutt(self.write))
                buttonlayout.addWidget(okbutt(func=lambda: self.close(),
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
                if text == 'Radio Buttons':
                        self.questionNum.setRange(2, self.maxoptions)
                elif text == 'Check Boxes':
                        self.questionNum.setRange(1, self.maxoptions)
                elif text == 'Free Response':
                        self.questionNum.setRange(0, 0)
                else:
                        print('error: {}'.format(text))

        class Response(Py.QtGui.QWidget):

                def __init__(self, num, parent=None):
                        super().__init__(parent)
                        self.parent = parent
                        self.layout = Py.QtGui.QVBoxLayout()
                        self.num = num
                        #self.hr = Py.QtGui.QSpacerItem(20, 40,
                        #                               Py.QtGui.QSizePolicy.Minimum,
                        #                               Py.QtGui.QSizePolicy.Expanding)
                        self.selection = Py.QtGui.QLineEdit()
                        self.selection.setPlaceholderText('Text')
                        self.questionNum = Py.QtGui.QSpinBox()
                        self.recode = Py.QtGui.QSpinBox()
                        #self.recode.setPlaceholderText('Number')
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
                self.data['name'] = self.name.inputobj.text()
                self.data['subtype'] = responses[self.rType.currentText()]
                self.data['question'] = self.question.inputobj.text()
                self.data['options'] = [(x.selection.text(),
                                         x.recode.value())
                                        for x in self.responses
                                        if not x.isHidden()]
                self.hide()
                if self not in self.parent.things:
                        self.parent.things.append(self)
                self.parent.update_dropdown()

        def write_file(self, prefix, pathdir):
                with open('{}/rating/{}.json'.format(pathdir,
                                                     self.data['name']), 'w') as outfile:
                        pretty_print = {'sort_keys': True,
                                        'indent': 4,
                                        'separators': (',', ': ')}
                        outfile.write(json.dumps(self.data, **pretty_print))
                        # Multiple ratings with same name


class MyWindow(BaseWindow):
    name = 'rating'
    namevar = 'name'
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
