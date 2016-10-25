#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import PySide.QtCore
import PySide.QtGui
import PySide as Py
import sys
import json
import contents as mainWidget

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



class MyWindow(PySide.QtGui.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)




        self.widget = mainWidget.MainWidget()
        self.initUI()



        self.setCentralWidget(self.widget)
        self.label = "yo"

    def reInitGui(self):
        self.widget = mainWidget.MainWidget()
        self.setCentralWidget(self.widget)
        self.selfmenubar.clear()
        self.initUI()

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

        action = fileMenu.addAction('Save')
        action.setShortcut(Py.QtGui.QKeySequence("Ctrl+S"))

        action = fileMenu.addAction('Save As...', self.import_data)
        action.setShortcut(Py.QtGui.QKeySequence("Ctrl+Shift+S"))


        action = editMenu.addAction('Add Rating', self.widget.ratingsWidget.add)
        #action.setShortcut(Py.QtGui.QKeySequence("Ctrl+Shift+S"))

        action = editMenu.addAction('Add Trial', self.import_data)


        # Give menu bar tabs
        menuBar.addAction(fileMenu.menuAction())
        menuBar.addAction(editMenu.menuAction())


        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Sound Advice Configuration Editor')



        self.show()

    def error(self, title, message, error_message=None):
        if error_message:
            Py.QtGui.QMessageBox.critical(self, title, message.format(error_message))
        else:
            Py.QtGui.QMessageBox.critical(self, title, message)

    def import_data(self):
        jsonFile = Py.QtGui.QFileDialog.getOpenFileName(parent=None,
                                              caption="Open Configuration File",
                                              #dir=appDataPath,
                                              filter="JSON files (*.json)")
        if jsonFile[0]:  # If a valid filename has been selected...
            jsonFile = open(jsonFile[0], 'r')
            try:
                settings = json.load(jsonFile)
                self.data(settings)
            except EOFError as err:
                self.error("import failed",
                        "<p>import file failed to open with<br />{}</p>", err)
                return 1

    def data(self, dictionary):
        self.description = dictionary['description']
        self.hostname = dictionary['hostname']
        self.trials = dictionary['trials']
        self.widget.resultsInput.setText(self.description)
        responses = {'radio' : 0, 'check' : 1, 'free' : 2}
        for y, x in enumerate(dictionary['ratings']):
            self.widget.ratingsWidget.add()
            self.widget.ratingsWidget.rName.setItemText(y, x['name'])
            currentwidget = self.widget.ratingsWidget.alltheratings[y]
            currentwidget.question.setText(x['question'])
            currentwidget.rType.setCurrentIndex(
                    responses[x['subtype']])
            if x['subtype'] != "free":
                currentwidget.options.questionNum.setValue(
                        len(x['options']))
            #print(len(currentwidget.options.responses))
            if x['options']:
                for c, d in enumerate(x['options']):
                    currentwidget.options.responses[c].selection.setText(d)







app = PySide.QtGui.QApplication(sys.argv)
main_window = MyWindow()
main_window.show()
app.exec_()

#if __name__ == '__main__':
#    main()
