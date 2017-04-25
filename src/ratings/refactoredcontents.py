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
    if button is not None:
        button = PySide.QtGui.QPushButton(ok)
    else:
        if button.text() is not "":
            button.setText(ok)
    button.clicked.connect(func)
    layout.addWidget(button)
    return button

savedcontents = {}

mainWidget = wandl(PySide.QtGui.QWidget(), PySide.QtGui.QVBoxLayout())
description = PySide.QtGui.QLineEdit()
mainWidget.layout.addLayout(layout('Description', description))
description_ok = PySide.QtGui.QPushButton()

def lockDescription():
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

z = contents.RatingsWidget()
mainWidget.layout.addWidget(z)
mainWidget.ratingsWidget = z
