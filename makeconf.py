#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import PySide.QtCore
import PySide.QtGui
import PySide as Py
import sys
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





class MyWindow(PySide.QtGui.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)




        self.initUI()



        widget = self.MainWidget()
        self.setCentralWidget(widget)
        self.label = "yo"

    class MainWidget(PySide.QtGui.QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)


            self.layout = Py.QtGui.QVBoxLayout()
            # Actual content inside window

            self.resultsInput = Py.QtGui.QLineEdit()
            self.resultsInput.setPlaceholderText("Description")
            #self.resultsInput.setPlaceholderText(Py.QtGui.QApplication.translate("mainWindow", "Username", None, Py.QtGui.QApplication.UnicodeUTF8)) # Why translate when you could not?

            # Sub layouts inside of layouts!
            buttonlayout = Py.QtGui.QHBoxLayout()
            buttonlayout.setSpacing(-0.1)

            self.ratingsButton = Py.QtGui.QPushButton("Ratings")
            self.ratingsButton = Py.QtGui.QToolButton()
            self.ratingsButton.setText("Ratings")

            self.trialsButton = Py.QtGui.QPushButton("Trials")
            self.trialsButton = Py.QtGui.QToolButton()
            self.trialsButton.setText("Trials")

            # Some baaad stuff
            #buttons = {'ratings': self.ratingsButton, 'trials' : self.trialsButton}
            #self.ratingswidget = self.RatingsWidget(self.layout, buttons)
            #self.trialswidget = self.TrialsWidget(self.layout, buttons)
            #self.ratingswidget.other = self.trialswidget
            #self.trialswidget.other = self.ratingswidget
            #ratingswidget.paintMenu()

            # Make buttons do stuff
            self.ratingsButton.clicked.connect(self.paintRatingsWidget)
            #self.trialsButton.clicked.connect(self.trialswidget.paintMenu)
            self.trialsButton.clicked.connect(self.paintTrialsWidget)


            buttonlayout.addWidget(self.ratingsButton)
            buttonlayout.addWidget(self.trialsButton)


            # Add Widgets to layout
            self.layout.addWidget(self.resultsInput)

            self.layout.addLayout(buttonlayout)
            self.setLayout(self.layout)

        # I may want to incorporate both of these into the same class
        def paintRatingsWidget(self):
            self.ratingsWidget = Py.QtGui.QWidget()
            ratingsLayout = Py.QtGui.QHBoxLayout()



            self.dropdown = Py.QtGui.QComboBox()
            self.dropdown.addItem("will this work?")
            self.dropdown.addItem("I hope")



            ratingsLayout.addWidget(self.dropdown)

            self.ratingsWidget.setLayout(ratingsLayout)

            try:
                self.trialsWidget.deleteLater()
                self.layout.removeWidget(self.trialsWidget)
            except Exception as e:
                print(e)
            self.ratingsButton.setEnabled(False)
            self.trialsButton.setEnabled(True)
            self.layout.addWidget(self.ratingsWidget)

        def paintTrialsWidget(self):
            self.trialsWidget = Py.QtGui.QWidget()
            ratingsLayout = Py.QtGui.QHBoxLayout()



            self.dropdown = Py.QtGui.QComboBox()
            self.dropdown.addItem("yay!")
            self.dropdown.addItem("Celebrate!")



            ratingsLayout.addWidget(self.dropdown)

            self.trialsWidget.setLayout(ratingsLayout)

            try:
                self.ratingsWidget.deleteLater()
                self.layout.removeWidget(self.ratingsWidget)
            except Exception as e:
                print(e)
            self.trialsButton.setEnabled(False)
            self.ratingsButton.setEnabled(True)
            self.layout.addWidget(self.trialsWidget)

    def initUI(self):

        # Initialize menu bar
        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(True)
        self.setMenuBar(menuBar)

        # Initialize menu tabs
        fileMenu = PySide.QtGui.QMenu(menuBar)
        fileMenu.setTitle("File")

        editMenu = PySide.QtGui.QMenu(menuBar)
        editMenu.setTitle("Edit")


        # Give menu tabs actions
        action = fileMenu.addAction('New Exercise', self.import_data)
        action.setShortcut(Py.QtGui.QKeySequence("Ctrl+N"))

        action = fileMenu.addAction('Open...', self.import_data)
        action.setShortcut(Py.QtGui.QKeySequence("Ctrl+O"))

        fileMenu.addSeparator() # This is a horizontal bar

        action = fileMenu.addAction('Close', self.import_data)
        action.setShortcut(Py.QtGui.QKeySequence("Ctrl+W"))

        action = fileMenu.addAction('Save', self.import_data)
        action.setShortcut(Py.QtGui.QKeySequence("Ctrl+S"))

        action = fileMenu.addAction('Save As...', self.import_data)
        action.setShortcut(Py.QtGui.QKeySequence("Ctrl+Shift+S"))


        action = editMenu.addAction('Add Rating', self.import_data)
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
                self.data = self.Data(settings)
                print('hostname is {}'.format(self.data.hostname))
            except Exception as err:
                self.error("import failed",
                        "<p>import file failed to open with<br />{}</p>", err)
                return 1

    class Data():
        # set base data
        description = ""
        hostname = ""
        ratings = {}
        trials = {}

        def __init__(self, dictionary):
            self.description = dictionary['description']
            self.hostname = dictionary['hostname']
            self.ratings = dictionary['ratings']
            self.trials = dictionary['trials']




app = PySide.QtGui.QApplication(sys.argv)
main_window = MyWindow()
main_window.show()
app.exec_()

#if __name__ == '__main__':
#    main()
