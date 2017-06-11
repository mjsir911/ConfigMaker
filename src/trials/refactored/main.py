#!/usr/bin/env python3
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


def description_and_label(text, inputobj):
    layout = PySide.QtGui.QHBoxLayout()
    layout.setAlignment(PySide.QtCore.Qt.AlignCenter)
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
        addbutton.clicked.connect(self.add_trial)
        dropdownlayout.addWidget(addbutton)


        self.widget.layout.addLayout(dropdownlayout)
        self.trials = []

    def update_dropdown(self):
        self.editing_dropdown = True  # Hacky
        for _ in range(self.dropdown.count()):
            self.dropdown.removeItem(0)
        for trial in self.trials:
            self.dropdown.addItem(trial.desc.inputobj.text())
        self.editing_dropdown = False
        self.dropdown.setCurrentIndex(-1)

    def selected_new(self):
        ci = self.dropdown.currentIndex()
        if ci >= 0 and not self.editing_dropdown:
            self.trials[ci].show()



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


        action = editMenu.addAction('Add Trial', self.add_trial)
        #action.setShortcut(Py.QtGui.QKeySequence(self.add_rating"Ctrl+Shift+S"))


        # Give menu bar tabs
        menuBar.addAction(fileMenu.menuAction())
        menuBar.addAction(editMenu.menuAction())


        self.setGeometry(300, 300, 250, 150)
        self.windowtitle = 'Sound Advice Configuration Editor ({})'
        self.setWindowTitle(self.windowtitle.format('New File'))



        self.show()

    def add_trial(self):
        newtrial = SubWindow(parent=self)
        self.trials.append(newtrial)
        newtrial.exec_()

    def error(self, title, message, error_message=None):
        if error_message:
            Py.QtGui.QMessageBox.critical(self, title, message.format(error_message))
        else:
            Py.QtGui.QMessageBox.critical(self, title, message)

    def import_data(self):
        raise NotImplementedError()
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
        for trial in self.trials:
            trial.write_file(dirpath)

        self.savedcontents.update({
                'trials': ['{}.json'.format(trial.data['description']) for  trial in
                    self.trials]
                })

        self.setWindowTitle(self.windowtitle.format(os.path.basename(path)))
        self.save.setEnabled(True)

        with open(path, 'w') as outfile:
            pretty_print = {'sort_keys':True, 'indent':4, 'separators':(',', ': ')}
            outfile.write(json.dumps(self.savedcontents, **pretty_print))


class SubWindow(PySide.QtGui.QDialog):
    maxoptions = 5
    def __init__(self, parent=None):
        self.data = {'type': 'trial'}
        super().__init__(parent)
        self.parent = parent
        self.layout = Py.QtGui.QVBoxLayout()

        self.desc = description_and_label('Description', Py.QtGui.QLineEdit())
        self.layout.addLayout(self.desc)

        program = Py.QtGui.QSpinBox()
        program.setMinimum(1)
        program.setMaximum(6)
        self.programlayout = description_and_label('Program: ', program)
        self.programlayout.addStretch(0.5)
        self.program = self.programlayout.inputobj
        del program
        self.layout.addLayout(self.programlayout)
        #self.layout.addLayout(self.programlayout, 0, 1, PySide.QtCore.Qt.AlignCenter)

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
            interior = self.InteriorDatum(parent=self)
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
        self.layout.addWidget(okbutt(self.write))

        self.setLayout(self.layout)

    def write(self):
        self.data.update({
            'description': self.desc.inputobj.text(),
            'program': self.program.value(),
            'targets': [3],
            'step': 2,
            'range': [-5, 5],
            'rsize': [200, 250],
            })

        self.data['noise'] = noise = []
        self.data['signal'] = signal = []
        for datum in self.datums:
            # these are all interior datums
            signal.append({
                'sample': datum.signal.sampleinput.value(),
                'level': datum.signal.levelinput.value(),
                'offset': datum.signal.offsetinput.value(),
                'state': datum.signal.state.isChecked(),
                })
            noise.append({
                'sample': datum.noise.sampleinput.value(),
                'level': datum.noise.levelinput.value(),
                'offset': datum.noise.offsetinput.value(),
                'state': datum.noise.state.isChecked(),
                })




        self.hide()
        self.parent.update_dropdown()

    def write_file(self, pathdir):
        with open('{}/{}.json'.format(pathdir, self.data['description']), 'w') as outfile:
            pretty_print = {'sort_keys':True, 'indent':4, 'separators':(',', ': ')}
            outfile.write(json.dumps(self.data, **pretty_print))

    class InteriorDatum(Py.QtGui.QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.parent = parent

            layout = Py.QtGui.QVBoxLayout()
            switchlayout = Py.QtGui.QHBoxLayout()
            #print(type(self.parent.datums))
            #desclabel = Py.QtGui.QLabel("Description" + str(len(self.parent.datums)) + "after")
            speakernum = Py.QtGui.QLabel("Speaker Number " + str(len(self.parent.datums) + 1))
            f = Py.QtGui.QFont()
            f.setWeight(Py.QtGui.QFont.Black)
            speakernum.setFont(f)
            speakerhead = Py.QtGui.QHBoxLayout()
            speakerhead.addStretch(0.5)
            speakerhead.addWidget(speakernum)
            speakerhead.addStretch(0.5)
            layout.addLayout(speakerhead)



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



            self.signal = self.SignalOrNoise("Signal", self)
            self.noise = self.SignalOrNoise("Noise", self)

            #self.signalButton.clicked.connect(self.signal.show)
            #self.noiseButton.clicked.connect(self.noise.show)

            signal_noise_layout = Py.QtGui.QHBoxLayout()

            signal_noise_layout.addWidget(self.signal)
            signal_noise_layout.addWidget(self.noise)

            layout.addLayout(signal_noise_layout)

            self.target = Py.QtGui.QCheckBox()
            targetlayout = Py.QtGui.QHBoxLayout()
            label = Py.QtGui.QLabel("Target:")
            targetlayout.addStretch(0.5)
            targetlayout.addWidget(label)
            targetlayout.addWidget(self.target)
            targetlayout.addStretch(0.5)
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
                label = Py.QtGui.QLabel("State:")
                statelayout.addWidget(label)
                statelayout.addWidget(self.state)
                self.layout.addLayout(statelayout)

                self.sampleinput = Py.QtGui.QSpinBox()
                self.sampleinput.setMinimum(1)
                samplelayout = Py.QtGui.QHBoxLayout()
                label = Py.QtGui.QLabel("Sample:")
                samplelayout.addWidget(label)
                samplelayout.addWidget(self.sampleinput)
                self.layout.addLayout(samplelayout)

                self.levelinput = Py.QtGui.QSpinBox()
                self.levelinput.setMinimum(-50)
                self.levelinput.setMaximum(50)
                levellayout = Py.QtGui.QHBoxLayout()
                label = Py.QtGui.QLabel("Level:")
                levellayout.addWidget(label)
                levellayout.addWidget(self.levelinput)
                self.layout.addLayout(levellayout)

                self.offsetinput = Py.QtGui.QSpinBox()
                offsetlayout = Py.QtGui.QHBoxLayout()
                label = Py.QtGui.QLabel("Offset(ms):")
                offsetlayout.addWidget(label)
                offsetlayout.addWidget(self.offsetinput)
                self.layout.addLayout(offsetlayout)

                self.setLayout(self.layout)
                #self.hide()



app = PySide.QtGui.QApplication(sys.argv)
main_window = MyWindow()
main_window.show()
font = app.font()
font.setPointSize(24)
app.setFont(font)
app.exec_()

#if __name__ == '__main__':
#    main()
