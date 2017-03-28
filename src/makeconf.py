#!/usr/bin/env python
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


responses = {'radio' : 0, 'check' : 1, 'free' : 2}

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

        action = fileMenu.addAction('Save', self.save)
        action.setShortcut(Py.QtGui.QKeySequence("Ctrl+S"))

        action = fileMenu.addAction('Save As...', self.export_data)
        action.setShortcut(Py.QtGui.QKeySequence("Ctrl+Shift+S"))


        action = editMenu.addAction('Add Rating', self.widget.ratingsWidget.add)
        #action.setShortcut(Py.QtGui.QKeySequence("Ctrl+Shift+S"))

        action = editMenu.addAction('Add Trial', self.widget.trialsWidget.add)


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
        self.reInitGui()
        if jsonFile[0]:  # If a valid filename has been selected...
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
                            currentwidget.options.responses[c].selection.setText(d[0])

                # Done with ratings



                for num, trial in enumerate(settings['trials']):
                    self.widget.trialsWidget.add()
                    # Description
                    # Program
                    # Target
                    """Noise"""
                    trial_object = self.widget.trialsWidget.dropdown_list[-1]
                    for speaker, signal, noise in zip(trial_object.datums, trial['signal'], trial['noise']):
                        s_noise = speaker.noise
                        s_sig = speaker.signal

                        s_noise.sampleinput.setValue(noise['sample']),
                        s_noise.levelinput.setValue(noise['level']),
                        s_noise.offsetinput.setValue(noise['offset']),
                        s_noise.state.setChecked(noise['state']),

                        s_sig.sampleinput.setValue(signal['sample']),
                        s_sig.levelinput.setValue(signal['level']),
                        s_sig.offsetinput.setValue(signal['offset']),
                        s_sig.state.setChecked(signal['state']),



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
                                                    filter="JSON files(*.json)")[0]
        self.write(savefilepath)

    def save(self):
        if self.opened:
            self.write(self.opened)

    def write(self, path):
        data = {}
        data['description'] = self.widget.resultsInput.text()
        data['ratings'] = []
        for num, x in enumerate(self.widget.ratingsWidget.alltheratings):
            ratings = {}

            ratings['name'] = self.widget.ratingsWidget.rName.itemText(num)
            ratings['question'] = x.question.text()
            if x.rType.currentText() == "Free Response":
                subtype = "free"
            elif x.rType.currentText() == "Check Boxes":
                subtype = "check"
            elif x.rType.currentText() == "Radio Buttons":
                subtype = "radio"
            else:
                print(x.rType.currentText())
            ratings['subtype'] = subtype

            ratings['options'] = []

            if subtype is not "free":
                print('not free')
                for option in x.options.responses:
                    print('for opt in responses')
                    if not option.isHidden():
                        print('if not hid')
                        ratings['options'].append(option.selection.text())
                        print(option.selection.text())
            else:
                ratings['options'] = None


            del subtype
            data['ratings'].append(ratings)

        # Done with ratings

        data['trials'] = []

        for trial in self.widget.trialsWidget.dropdown_list:
            data['trials'].append({})


            json_trial = data['trials'][-1]
            #WIP
            json_trial['description'] = "description work in progress"
            json_trial['program'] = 1
            json_trial['targets'] = [1]

            #END OF WIP
            noise = json_trial['noise'] = []
            sig = json_trial['signal'] = []
            for speaker in trial.datums:
                s_noise = speaker.noise
                s_sig = speaker.signal

                noise.append({
                    'sample' : s_noise.sampleinput.value(),
                    'level' : s_noise.levelinput.value(),
                    'offset' : s_noise.offsetinput.value(),
                    'state' : s_noise.state.isChecked(),
                    })
                sig.append({
                    'sample' : s_sig.sampleinput.value(),
                    'level' : s_sig.levelinput.value(),
                    'offset' : s_sig.offsetinput.value(),
                    'state' : s_sig.state.isChecked(),
                    })






        with open(path, 'w') as outfile:
            pretty_print={'sort_keys':True, 'indent':4, 'separators':(',', ': ')}
            outfile.write(json.dumps(data, **pretty_print))


app = PySide.QtGui.QApplication(sys.argv)
main_window = MyWindow()
main_window.show()
font = app.font()
font.setPointSize(24)
app.setFont(font)
app.exec_()

#if __name__ == '__main__':
#    main()
