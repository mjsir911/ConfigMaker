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


responses = {'radio' : 0, 'check' : 1, 'free' : 2}
def description_and_label(text, inputobj):
    layout = PySide.QtGui.QHBoxLayout()
    label  = PySide.QtGui.QLabel(text)
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
    if button is None:
        button = PySide.QtGui.QPushButton(buttonText)
    else:
        if button.text() is not "":
            button.setText(buttonText)
    button.clicked.connect(func)
    return button

class MyWindow(PySide.QtGui.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)



        #self.widget.ratingsWidget = SubWindow()


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
        addbutton = Py.QtGui.QPushButton('+')
        addbutton.clicked.connect(self.add_rating)
        dropdownlayout.addWidget(addbutton)


        self.widget.layout.addLayout(dropdownlayout)

        self.ratings = []

    def update_dropdown(self):
        self.editing_dropdown = True  # Hacky
        for _ in range(self.dropdown.count()):
            self.dropdown.removeItem(0)
        for rating in self.ratings:
            self.dropdown.addItem(rating.name.inputobj.text())
        self.editing_dropdown = False
        self.dropdown.setCurrentIndex(-1)

    def selected_new(self):
        ci = self.dropdown.currentIndex()
        if ci >= 0 and not self.editing_dropdown:
            self.ratings[ci].show()



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
        action.setShortcut(Py.QtGui.QKeySequence("Ctrl+N"))

        action = fileMenu.addAction('Open...', self.import_data)
        action.setShortcut(Py.QtGui.QKeySequence("Ctrl+O"))

        fileMenu.addSeparator() # This is a horizontal bar

        action = fileMenu.addAction('Close')
        action.setShortcut(Py.QtGui.QKeySequence("Ctrl+W"))

        action = fileMenu.addAction('Save', self.write)
        action.setShortcut(Py.QtGui.QKeySequence("Ctrl+S"))
        self.save = action
        self.save.setEnabled(False)

        action = fileMenu.addAction('Save As...', self.export_data)
        action.setShortcut(Py.QtGui.QKeySequence("Ctrl+Shift+S"))


        action = editMenu.addAction('Add Rating', self.add_rating)
        #action.setShortcut(Py.QtGui.QKeySequence(self.add_rating"Ctrl+Shift+S"))


        # Give menu bar tabs
        menuBar.addAction(fileMenu.menuAction())
        menuBar.addAction(editMenu.menuAction())


        self.setGeometry(300, 300, 250, 150)
        self.windowtitle = 'Sound Advice Configuration Editor ({})'
        self.setWindowTitle(self.windowtitle.format('New File'))



        self.show()

    def add_rating(self):
        newrating = SubWindow(parent=self)
        self.ratings.append(newrating)
        newrating.exec_()

    def error(self, title, message, error_message=None):
        if error_message:
            Py.QtGui.QMessageBox.critical(self, title, message.format(error_message))
        else:
            Py.QtGui.QMessageBox.critical(self, title, message)

    def import_data(self):
        jsonFile = Py.QtGui.QFileDialog.getOpenFileName(parent=None,
                                              caption="Open Configuration File",
                                              dir=os.path.expanduser('~/Code/dragana/Sound Advice/Presets/'),
                                              filter="JSON files (*.json)")
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
                        "<p>import file failed to open with<br />{}</p>", err)
                return 1
            except KeyError as err:
                self.error("Invalid file",
                        "<b>Import file failed to open with<br />{}</b>", err)

    def export_data(self):
        savefilepath = Py.QtGui.QFileDialog.getSaveFileName(parent=None,
                                                      caption="hi",
                                                      dir=os.path.expanduser('~/Code/dragana/Sound Advice/Presets/'),
                                                      filter="JSON files(*.json)")[0]
        self.write(savefilepath)

    def write(self, path=None):
        if not path:
            path = self.filename
        else:
            self.filename = path

        dirpath = os.path.dirname(os.path.abspath(path))
        for rating in self.ratings:
            rating.write_file(dirpath)

        self.savedcontents.update({
                'ratings': ['{}.json'.format(rating.data['name']) for  rating in self.ratings]
                })

        self.setWindowTitle(self.windowtitle.format(os.path.basename(path)))
        self.save.setEnabled(True)

        with open(path, 'w') as outfile:
            pretty_print = {'sort_keys':True, 'indent':4, 'separators':(',', ': ')}
            outfile.write(json.dumps(self.savedcontents, **pretty_print))


responses = {
        'Radio Buttons': "radio",
        "Check Boxes": 'check',
        "Free Response": 'free'
        }
class SubWindow(PySide.QtGui.QDialog):
    maxoptions = 5
    def __init__(self, parent=None):
        self.data = {'type': 'rating'}
        super().__init__(parent)
        self.layout = Py.QtGui.QVBoxLayout()
        self.name = description_and_label('Column Heading', Py.QtGui.QLineEdit())
        self.layout.addLayout(self.name)
        self.question = description_and_label('Question', Py.QtGui.QLineEdit())
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

        self.layout.addWidget(okbutt(self.write))
        self.responseCheck()
        self.setLayout(self.layout)
        self.check()

    def responseCheck(self):
        for x in self.responses:
            x.check(self.questionNum.value())

    def check(self):
        text = self.rType.currentText()
        if text == "Radio Buttons":
            self.questionNum.setRange(2, self.maxoptions)
        elif text == "Check Boxes":
            self.questionNum.setRange(1, self.maxoptions)
        elif text == "Free Response":
            self.questionNum.setRange(0, 0)
        else:
            print(text)

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

    def write(self):
        self.data['name'] = self.name.inputobj.text()
        self.data['subtype'] = responses[self.rType.currentText()]
        self.data['question'] = self.question.inputobj.text()
        self.data['options'] = [(x.selection.text(), x.recode.value()) for x in self.responses if not x.isHidden()]
        self.hide()
        self.parent.update_dropdown()

    def write_file(self, pathdir):
        with open('{}/{}.json'.format(pathdir, self.data['name']), 'w') as outfile:
            pretty_print = {'sort_keys':True, 'indent':4, 'separators':(',', ': ')}
            outfile.write(json.dumps(self.data, **pretty_print))
            # Multiple ratings with same name



app = PySide.QtGui.QApplication(sys.argv)
main_window = MyWindow()
main_window.show()
font = app.font()
font.setPointSize(24)
app.setFont(font)
app.exec_()

#if __name__ == '__main__':
#    main()
