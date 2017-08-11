#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import PySide.QtGui
import PySide.QtCore

from builtins import super

import os
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

pretty_print = {'sort_keys': True, 'indent': 4, 'separators': (',', ': ')}

class MainWindow(PySide.QtGui.QMainWindow):
    windowtitle = 'Sound Advice Configuration Editor ({})'
    def __init__(self, widget, parent=None):
        super().__init__()
        self.widget = widget

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.windowtitle.format('New File'))
        self.showMaximized()

        #menubar stuff
        fileMenu = self.menuBar().addMenu("&File")

        fileMenu.addAction(PySide.QtGui.QAction('New Exercise',
                                                 self,
                                                 shortcut=PySide.QtGui.QKeySequence.New,
                                                 statusTip="Create a new file",
                                                 triggered=self.newFile,
        ))

        fileMenu.addAction(PySide.QtGui.QAction('Open...',
                                                 self,
                                                 shortcut=PySide.QtGui.QKeySequence.Open,
                                                 statusTip="Open an existing file",
                                                 triggered=self.openFile,
        ))

        #####self.setStyleSheet('* { font-size: 32px; }')

        fileMenu.addSeparator() # This is a horizontal bar

        fileMenu.addAction(PySide.QtGui.QAction('Close',
                                                 self,
                                                 shortcut=PySide.QtGui.QKeySequence.Close,
                                                 statusTip="Close window",
                                                 triggered=self.closeWindow,
        ))

        self.save = PySide.QtGui.QAction('Save',
                                         self,
                                         shortcut=PySide.QtGui.QKeySequence.Save,
                                         statusTip="Save the file to the already saved file",
                                         triggered=self.saveFile,
                                         enabled=False,
        )
        fileMenu.addAction(self.save)

        fileMenu.addAction(PySide.QtGui.QAction('Save As...',
                                                 self,
                                                 shortcut=PySide.QtGui.QKeySequence.SaveAs,
                                                 statusTip="Save file as new document",
                                                 triggered=self.saveAsFile,
        ))


        self.newFile()

        self.setCentralWidget(self.widget(parent=self))

        with open(os.path.dirname(os.path.abspath(__file__)) + '/style.css', 'r') as fp:
            self.setStyleSheet(fp.read())


        self.show()

    def newFile(self):
        self.editMenu = self.menuBar().addMenu("&Edit")
    def openFile(self):
        raise NotImplementedError()
    def saveFile(self):
        raise NotImplementedError()
    def saveAsFile(self):
        raise NotImplementedError()
    def closeWindow(self):
        raise NotImplementedError()

class MainWidget(PySide.QtGui.QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.savedcontents = {}

    @property
    def things_actual(self):
        return [self.things.item(i).widget for i in
                range(self.things.count())]

    def add_subWindow(self):
        self.subwind(parent=self).exec_()

    def export_data(self):
        from PySide.QtGui import QFileDialog
        savedir = defaultdir + self.name + '/'
        try:
            os.mkdir(savedir)
        except OSError:
            pass

        savefilepath = QFileDialog.getExistingDirectory(self,
                                                        caption="Export Config File",
                                                        dir=savedir,
                                                        )
        """
        savefilepath = QFileDialog.getSaveFileName(parent=None,
                                                   caption='Export Config File',
                                                   dir=savedir,
                                                   filter='JSON files(*.json)'
                                                   )[0]
                                                   """
        logger.info('path given to save is "%s"', savefilepath)
        self.write(savefilepath)

    def write(self, path=None):
        if not path:
            path = self.filename
        else:
            self.filename = path

        for i, thing in enumerate(self.things_actual):
            with open('{}/{:02}-{}.json'.format(path, i + 1,
                thing.data[self.namevar]), 'w') as fp:
                thing.write_file(fp)

        self.parent.setWindowTitle(self.parent.windowtitle.format(os.path.basename(path)))

        with open('{}/00-index.json'.format(path), 'w') as outfile:
            outfile.write(json.dumps(self.savedcontents, **pretty_print))
