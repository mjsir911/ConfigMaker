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




        self.widget = self.MainWidget()
        self.initUI()



        self.setCentralWidget(self.widget)
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

            # Hi
            self.ratingsWidget = self.RatingsWidget(self)
            self.trialsWidget = self.TrialsWidget(self)

            # Make buttons do stuff
            self.ratingsButton.clicked.connect(self.ratingsWidget.show)
            self.trialsButton.clicked.connect(self.trialsWidget.show)


            buttonlayout.addWidget(self.ratingsButton)
            buttonlayout.addWidget(self.trialsButton)


            # Add Widgets to layout
            self.layout.addWidget(self.resultsInput)

            self.layout.addLayout(buttonlayout)
            self.setLayout(self.layout)

        class RatingsWidget(Py.QtGui.QWidget):
            def __init__(self, parent=None):
                super().__init__(parent)
                self.parent = parent

                self.alltheratings = []

                self.layout = Py.QtGui.QVBoxLayout()


                self.rName = Py.QtGui.QComboBox()
                #Set editable
                # Allow duplicates
                # Insert policy
                self.rName.currentIndexChanged.connect(self.change)


                self.layout.addWidget(self.rName)

                self.setLayout(self.layout)
                self.hide()

            class SingularRating(Py.QtGui.QWidget):
                def __init__(self, parent=None):
                    super().__init__(parent)
                    layout = Py.QtGui.QVBoxLayout()

                    self.nameInput = Py.QtGui.QLineEdit()
                    self.nameInput.setPlaceholderText("Name")

                    self.question = Py.QtGui.QLineEdit()
                    self.question.setPlaceholderText("Question")

                    #self.questionNum = Py.QtGui.QSpinBox()
                    #self.questionNum.setRange(1, 5)

                    self.options = self.OptionalOptions(layout, parent=self)

                    self.rType = Py.QtGui.QComboBox()
                    self.rType.addItem("Radio Buttons")
                    self.rType.addItem("Check Boxes")
                    self.rType.addItem("Free Response")
                    self.rType.currentIndexChanged.connect(self.options.check)


                    layout.addWidget(self.nameInput)
                    #layout.addWidget(self.questionNum)
                    layout.addWidget(self.question)
                    layout.addWidget(self.rType)
                    self.setLayout(layout)

                    self.options.check()
                class OptionalOptions(Py.QtGui.QWidget):
                    def __init__(self, playout, parent=None):
                        super().__init__(parent)
                        self.playout = playout
                        self.parent = parent

                        layout = Py.QtGui.QVBoxLayout()

                        questionNum = Py.QtGui.QSpinBox()
                        questionNum.setRange(2, 5)

                        layout.addWidget(questionNum)

                        self.setLayout(layout)

                        self.hide()

                    def check(self):
                        text = self.parent.rType.currentText()
                        if text == "Radio Buttons":
                            self.show()
                        elif text == "Check Boxes":
                            self.show()
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


            def show(self):
                super().show()
                self.parent.layout.addWidget(self)
                self.parent.trialsWidget.hide()
                self.parent.layout.removeWidget(self.parent.trialsWidget)
                self.parent.ratingsButton.setEnabled(False)
                self.parent.trialsButton.setEnabled(True)

            def add(self):

                rating = self.SingularRating()
                for oldrating in self.alltheratings:
                    try:
                        self.layout.removeWidget(oldrating)
                        oldrating.hide()
                    except Exception as e:
                        print(e)
                self.alltheratings.append(rating)
                self.layout.addWidget(rating)
                self.rName.addItem("Question numero uno")

            def change(self):
                for oldrating in self.alltheratings:
                    try:
                        self.layout.removeWidget(oldrating)
                        oldrating.hide()
                    except Exception as e:
                        print(e)
                currentrating = self.alltheratings[self.rName.currentIndex()]
                self.layout.addWidget(currentrating)
                currentrating.show()



        class TrialsWidget(Py.QtGui.QWidget):
            def __init__(self, parent=None):
                super().__init__(parent)
                self.parent = parent

                layout = Py.QtGui.QHBoxLayout()



                self.dropdown = Py.QtGui.QComboBox()
                self.dropdown.addItem("yay!")
                self.dropdown.addItem("Celebrate!")



                layout.addWidget(self.dropdown)

                self.setLayout(layout)
                self.hide()

            def show(self):
                super().show()
                self.parent.layout.addWidget(self)
                self.parent.ratingsWidget.hide()
                self.parent.layout.removeWidget(self.parent.ratingsWidget)
                self.parent.trialsButton.setEnabled(False)
                self.parent.ratingsButton.setEnabled(True)

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
                self.data = self.data(settings)
            except Exception as err:
                self.error("import failed",
                        "<p>import file failed to open with<br />{}</p>", err)
                return 1

    def data(self, dictionary):
        self.description = dictionary['description']
        self.hostname = dictionary['hostname']
        self.ratings = dictionary['ratings']
        self.trials = dictionary['trials']
        self.widget.resultsInput.setText(self.description)





app = PySide.QtGui.QApplication(sys.argv)
main_window = MyWindow()
main_window.show()
app.exec_()

#if __name__ == '__main__':
#    main()
