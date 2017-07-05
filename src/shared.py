#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import PySide
import PySide.QtCore
import PySide.QtGui

import os

from builtins import super

import json

import logging

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

logger = logging.getLogger()
logging.basicConfig()
logger.setLevel(logging.DEBUG)

defaultdir = os.path.expanduser('~/.config/sound-advice/')


def description_and_label(text, inputobj):
    layout = PySide.QtGui.QHBoxLayout()
    layout.setAlignment(PySide.QtCore.Qt.AlignCenter)
    label  = PySide.QtGui.QLabel(text)
    label.setText(label.text() + ': ')
    #label.text += ': '
    print(label.text())
    layout.addWidget(label)
    layout.name = label
    layout.addWidget(inputobj)
    layout.inputobj = inputobj
    try:
        inputobj.setPlaceholderText(text)
    except:
        pass
    return layout

def wandl(widget, layout):
    widget.layout = layout
    widget.setLayout(widget.layout)
    return widget

def okbutt(func, button=None, buttonText='OK'):
    print(buttonText)
    if button is None:
        button = PySide.QtGui.QPushButton(buttonText)
    else:
        if button.text() is not "":
            button.setText(buttonText)
    button.clicked.connect(func)
    return button

import abc
import six


#class MyWindow(PySide.QtGui.QMainWindow):
#@six.add_metaclass(abc.ABCMeta)
class BaseWindow(PySide.QtGui.QMainWindow):
    namevar = ''
    name = ''
    def __init__(self, parent=None):
        super().__init__(parent)

        self.selfmenubar = self.menuBar()
        self.reInitGui()

        self.label = "yo"

    def reInitGui(self):
        self.savedcontents = {}
        self.widget = wandl(PySide.QtGui.QWidget(), PySide.QtGui.QVBoxLayout())
        description = PySide.QtGui.QLineEdit()
        self.widget.layout.addLayout(description_and_label('Description', description))
        description_ok = PySide.QtGui.QPushButton()
        description_ok.setText('OK')

        def lockDescription():
            """ Take a description and on ok hide """
            text = description.text()
            if text:
                description.setEnabled(False)
                self.savedcontents['description'] = description.text()
                self.widget.layout.removeWidget(description_ok)
                description_ok.hide()
            else:
                PySide.QtGui.QMessageBox.critical(self.widget, 'Empty Description',
                'Description box cannot be empty')

        description_ok = okbutt(lockDescription)
        self.widget.layout.addWidget(description_ok)
        self.setCentralWidget(self.widget)
        self.selfmenubar.clear()
        self.initUI()

        dropdownlayout = PySide.QtGui.QHBoxLayout()
        self.dropdown = PySide.QtGui.QComboBox()
        self.dropdown.currentIndexChanged.connect(self.selected_new)
        dropdownlayout.addWidget(self.dropdown)
        addbutton = PySide.QtGui.QPushButton('+')
        addbutton.clicked.connect(self.add_thing)
        dropdownlayout.addWidget(addbutton)


        self.widget.layout.addLayout(dropdownlayout)
        self.things = []

    def update_dropdown(self):
        self.editing_dropdown = True  # Hacky
        for _ in range(self.dropdown.count()):
            self.dropdown.removeItem(0)
        for thing in self.things:
            self.dropdown.addItem(thing.data[self.namevar])
        self.editing_dropdown = False
        self.dropdown.setCurrentIndex(-1)

    def selected_new(self):
        ci = self.dropdown.currentIndex()
        if ci >= 0 and not self.editing_dropdown:
            self.things[ci].show()



    def initUI(self):

        # Initialize menu bar
        menuBar = self.menuBar()
        self.selfmenubar = menuBar
        menuBar.setNativeMenuBar(True)
        self.setMenuBar(menuBar)

        # Initialize menu tabs
        fileMenu = PySide.QtGui.QMenu(menuBar)
        fileMenu.setTitle("File")

        editMenu = PySide.QtGui.QMenu(menuBar)
        editMenu.setTitle("Edit")


        # Give menu tabs actions
        action = fileMenu.addAction('New Exercise', self.reInitGui)
        action.setShortcut(PySide.QtGui.QKeySequence("Ctrl+N"))

        action = fileMenu.addAction('Open...', self.import_data)
        action.setShortcut(PySide.QtGui.QKeySequence("Ctrl+O"))

        fileMenu.addSeparator() # This is a horizontal bar

        action = fileMenu.addAction('Close')
        action.setShortcut(PySide.QtGui.QKeySequence("Ctrl+W"))

        action = fileMenu.addAction('Save', self.write)
        action.setShortcut(PySide.QtGui.QKeySequence("Ctrl+S"))
        self.save = action
        self.save.setEnabled(False)

        action = fileMenu.addAction('Save As...', self.export_data)
        action.setShortcut(PySide.QtGui.QKeySequence("Ctrl+Shift+S"))


        action = editMenu.addAction('Add {}'.format(self.name.capitalize()),
                self.add_thing)
        #action.setShortcut(PySide.QtGui.QKeySequence(self.add_rating"Ctrl+Shift+S"))


        # Give menu bar tabs
        menuBar.addAction(fileMenu.menuAction())
        menuBar.addAction(editMenu.menuAction())


        self.setGeometry(300, 300, 250, 150)
        self.windowtitle = 'Sound Advice Configuration Editor ({})'
        self.setWindowTitle(self.windowtitle.format('New File'))



        self.show()

    def add_thing(self):
        self.subwind(parent=self).exec_()

    def error(self, title, message, error_message=None):
        if error_message:
            PySide.QtGui.QMessageBox.critical(self, title, message.format(error_message))
        else:
            PySide.QtGui.QMessageBox.critical(self, title, message)

    def import_data(self):
        from PySide.QtGui.QFileDialog import getOpenFileName
        jsonFile = getOpenFileName(parent=None,
                                   caption="Open Configuration File",
                                   dir=defaultdir,
                                   filter="JSON files (*.json)")
        print(json.load(open(jsonFile[0], 'r')))
        raise NotImplementedError()
        self.reInitGui()
        if jsonFile[0]:  # If a valid filename has been selected...
            self.filename = jsonFile[0]
            self.setWindowTitle(self.windowtitle.format(os.path.basename(self.filename)))
            self.save.setEnabled(True)
            jsonFile = open(jsonFile[0], 'r')
            try:
                settings = json.load(jsonFile)
                #self.data(settings)
                self.widget.resultsInput.setText(settings['description'])
                for y, x in enumerate(settings['ratings']):
                    self.widget.ratingsWidget.add()
                    print(type(y))
                    print(type(x['name']))
                    self.widget.ratingsWidget.rName.setItemText(y, x['name'])
                    currentwidget = self.widget.ratingsWidget.alltheratings[y]
                    currentwidget.question.setText(x['question'])
                    currentwidget.rType.setCurrentIndex(
                            responses[x['subtype']])
                    if x['subtype'] != "free":
                        currentwidget.options.questionNum.setValue(
                                len(x['options']))
                    if x['options']:
                        for c, d in enumerate(x['options']):
                            cresponse = currentwidget.options.responses[c]
                            cresponse.selection.setText(d[0])
                            cresponse.recode.setValue(d[1])

            except EOFError as err:
                print(err)
                self.error("import failed",
                           "<p>import file failed to open with<br />{}</p>",
                           err)
                return 1
            except KeyError as err:
                self.error("Invalid file",
                           "<b>Import file failed to open with<br />{}</b>",
                           err)

    def export_data(self):
        from PySide.QtGui.QFileDialog import getSaveFileName
        savefilepath = getSaveFileName(parent=None,
                                       caption="hi",
                                       dir=defaultdir,
                                       filter="JSON files(*.json)")[0]
        logger.info('path given to save is {}'.format(savefilepath))
        self.write(savefilepath)

    def write(self, path=None):
        path = path.replace('.json', '')
        if not path:
            path = self.filename
        else:
            self.filename = path

        dirpath = os.path.dirname(os.path.abspath(path))
        for thing in self.things:
            try:
                os.mkdir('{}/preset'.format(dirpath))
            except OSError:
                pass
            thing.write_file(os.path.basename(path), dirpath)

        self.savedcontents.update({
                '{}s'.format(self.name): [thing.data[self.namevar] for thing
                    in self.things]
                })

        self.setWindowTitle(self.windowtitle.format(os.path.basename(path)))
        self.save.setEnabled(True)

        with open('{}.json'.format(path), 'w') as outfile:
            pretty_print = {
                'sort_keys': True,
                'indent': 4,
                'separators': (',', ': ')
            }
            outfile.write(json.dumps(self.savedcontents, **pretty_print))
