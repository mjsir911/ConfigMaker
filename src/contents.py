#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
        self.trialsButton = Py.QtGui.QPushButton("Trials")
        self.trialsButton = Py.QtGui.QToolButton()
        self.trialsButton.setText("Trials")
        # Hi
        self.ratingsWidget = RatingsWidget(self)
        self.trialsWidget = TrialsWidget(self)
        # Make buttons do stuff
        self.ratingsButton.clicked.connect(self.ratingsWidget.show)
        self.trialsButton.clicked.connect(self.trialsWidget.show)

        labelgroup.addWidget(desclabel)
        labelgroup.addWidget(self.resultsInput)
        self.layout.addLayout(labelgroup)
        buttonlayout.addWidget(self.ratingsButton)
        buttonlayout.addWidget(self.trialsButton)
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
        self.parent.trialsWidget.hide()
        self.parent.layout.removeWidget(self.parent.trialsWidget)
        self.parent.ratingsButton.setEnabled(False)
        self.parent.trialsButton.setEnabled(True)

    def add(self):
        rating = SingularRating()
        for oldrating in self.alltheratings:
            try:
                self.layout.removeWidget(oldrating)
                oldrating.hide()
            except Exception as e:
                print(e)
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


class TrialsWidget(Py.QtGui.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.dropdown_list = []
        self.layout = Py.QtGui.QVBoxLayout()
        self.dropdown = Py.QtGui.QComboBox()
        self.dropdown.currentIndexChanged.connect(self.change)
        self.dropdown.hide()
        self.layout.addWidget(self.dropdown)
        self.setLayout(self.layout)
        self.hide()

    def show(self):
        super().show()
        self.parent.layout.addWidget(self)
        self.parent.ratingsWidget.hide()
        self.parent.layout.removeWidget(self.parent.ratingsWidget)
        self.parent.trialsButton.setEnabled(False)
        self.parent.ratingsButton.setEnabled(True)

    def add(self):
        self.show()
        self.dropdown.show()
        self.dropdown.addItem("Trial {}".format(self.dropdown.count() + 1))
        self.dropdown.setCurrentIndex(self.dropdown.count() - 1)
        try:
            #print('remove old')
            self.layout.removeWidget(self.currentwidge)
            self.currentwidge.hide()
        except AttributeError as e:
            #print(e, 'hi')
            pass
        self.currentwidge = speakergrid = SpeakerGrid()
        self.dropdown_list.append(speakergrid)
        self.layout.addWidget(speakergrid)

    def change(self):
        dropdown = self.dropdown
        current = dropdown.currentIndex()
        for widget in self.dropdown_list:
            if widget is not self.dropdown_list[current]:
                self.layout.removeWidget(widget)
                widget.hide()
            else:
                self.currentwidge = widget
        try:
            self.layout.addWidget(self.currentwidge)
            self.currentwidge.show()
        except:
            pass
        print(self.dropdown_list)
        print(current)

class SpeakerGrid(Py.QtGui.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = Py.QtGui.QVBoxLayout()

        programlayout = Py.QtGui.QHBoxLayout()
        self.program = Py.QtGui.QSpinBox()
        self.program.setMinimum(1)
        self.program.setMaximum(6)
        plabel = Py.QtGui.QLabel("Program: ")
        programlayout.addStretch(0.5)
        programlayout.addWidget(plabel)
        programlayout.addWidget(self.program)
        programlayout.addStretch(0.5)
        self.layout.addLayout(programlayout)

        self.glayout = Py.QtGui.QGridLayout()

        self.datums = []
        #http://mathworld.wolfram.com/TriangleWave.html
        x_equation = lambda t: 8 * abs(round((1 / 8) * (t - 1)) - (1 / 8) * (t - 1))
        y_equation = lambda t: 8 * abs(round((1 / 8) * (t - 3)) - (1 / 8) * (t - 3))
        # THESE ARE FOR THE EQUATIONS BELOOWWWW
        for testest in range(1, 9):
            """
            Courtesy of the internet, i refined the quartic equation
            Now its a triangle graph, mapping x and y coordinates
            creates a diamond shaped object, which is exactly where we want
            the buttons
              /\    /
             /  \  /   ooh fancy triangle graph
            /    \/
            """
            interior = InteriorDatum(parent=self)
            self.datums.append(interior)
            interior.show()
            interior.hide()
            button = Py.QtGui.QPushButton()
            button.setFixedWidth(200)
            button.clicked.connect(interior.show)
            button.setText(str(testest))
            xc = x_equation(testest)
            yc = y_equation(testest)
            #print(xc, yc)
            self.glayout.addWidget(button, xc, yc)

        """ In case of emergency, break quotes
        self.layout.addWidget(button, 0, 2)
        self.layout.addWidget(button, 1, 1)
        self.layout.addWidget(button, 2, 0)
        self.layout.addWidget(button, 3, 1)
        self.layout.addWidget(button, 4, 2)
        self.layout.addWidget(button, 3, 3)
        self.layout.addWidget(button, 2, 4)
        self.layout.addWidget(button, 1, 3)
        """
        self.layout.addLayout(self.glayout)
        self.setLayout(self.layout)

class InteriorDatum(Py.QtGui.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        layout = Py.QtGui.QVBoxLayout()
        switchlayout = Py.QtGui.QHBoxLayout()
        #print(type(self.parent.datums))
        #desclabel = Py.QtGui.QLabel("Description" + str(len(self.parent.datums)) + "after")
        speakernum = Py.QtGui.QLabel("Speaker Number " + str(len(self.parent.datums) + 1))
        layout.addWidget(speakernum)



        """
        flippy_buttons = Py.QtGui.QHBoxLayout()
        flippy_buttons.setSpacing(-0.1)
        self.signalButton = Py.QtGui.QPushButton("Signal")
        self.signalButton = Py.QtGui.QToolButton()
        self.signalButton.setText("Signal")
        self.noiseButton = Py.QtGui.QPushButton("Noise")
        self.noiseButton = Py.QtGui.QToolButton()
        self.noiseButton.setText("Noise")

        flippy_buttons.addWidget(self.signalButton)
        flippy_buttons.addWidget(self.noiseButton)
        """



        self.signal = SignalOrNoise("Signal", self)
        self.noise = SignalOrNoise("Noise", self)

        #self.signalButton.clicked.connect(self.signal.show)
        #self.noiseButton.clicked.connect(self.noise.show)

        signal_noise_layout = Py.QtGui.QHBoxLayout()

        signal_noise_layout.addWidget(self.signal)
        signal_noise_layout.addWidget(self.noise)

        layout.addLayout(signal_noise_layout)

        self.target = Py.QtGui.QCheckBox()
        targetlayout = Py.QtGui.QHBoxLayout()
        label = Py.QtGui.QLabel("Target:")
        targetlayout.addWidget(label)
        targetlayout.addWidget(self.target)
        layout.addLayout(targetlayout)

        self.layout = layout

        #layout.addLayout(switchlayout)
        #self.parent.layout.addWidget(desclabel, 2, 2)
        #layout.addWidget(desclabel)
        #layout.addLayout(flippy_buttons)
        #self.layout.add
        layout.addLayout(switchlayout)
        self.setLayout(layout)

    def show(self):
        super().show()
        #print('hi' + str(self.parent.datums.index(self)))
        for x in self.parent.datums:
            if x is not self:
                x.hide()
            #pass
            #self.parent.layout.removeWidget(self)

        self.parent.glayout.addWidget(self, 2, 2)
        self.parent.glayout.indexOf(self)

    def hide(self):
        super().hide()
        #print(self.parent)
        #print(type(self.parent))
        self.parent.glayout.removeWidget(self)



class SignalOrNoise(Py.QtGui.QWidget):
    def buttonclick(self):
        self.parent.datums
        for datum in self.parent.datums:
            if datum is not self:
                pass
                "make button not blue"
    def __init__(self, sigornoise, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.toggle = sigornoise
        self.layout = Py.QtGui.QVBoxLayout()

        label = Py.QtGui.QLabel(sigornoise)
        self.layout.addWidget(label)

        """
        sample: number
        level: -12 to 12
        offset: in milliseconds
        state: radio button true or false
        """


        self.state = Py.QtGui.QCheckBox()
        self.state.setCheckState(Py.QtCore.Qt.Checked)
        statelayout = Py.QtGui.QHBoxLayout()
        label = Py.QtGui.QLabel("State")
        statelayout.addWidget(label)
        statelayout.addWidget(self.state)
        self.layout.addLayout(statelayout)

        self.sampleinput = Py.QtGui.QSpinBox()
        self.sampleinput.setMinimum(1)
        samplelayout = Py.QtGui.QHBoxLayout()
        label = Py.QtGui.QLabel("Sample")
        samplelayout.addWidget(label)
        samplelayout.addWidget(self.sampleinput)
        self.layout.addLayout(samplelayout)

        self.levelinput = Py.QtGui.QSpinBox()
        self.levelinput.setMinimum(-50)
        self.levelinput.setMaximum(50)
        levellayout = Py.QtGui.QHBoxLayout()
        label = Py.QtGui.QLabel("Level")
        levellayout.addWidget(label)
        levellayout.addWidget(self.levelinput)
        self.layout.addLayout(levellayout)

        self.offsetinput = Py.QtGui.QSpinBox()
        offsetlayout = Py.QtGui.QHBoxLayout()
        label = Py.QtGui.QLabel("Offset(ms)")
        offsetlayout.addWidget(label)
        offsetlayout.addWidget(self.offsetinput)
        self.layout.addLayout(offsetlayout)

        self.setLayout(self.layout)
        #self.hide()
