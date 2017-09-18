#!/usr/bin/env python3
# vim: set fileencoding=utf-8:
# vim: set expandtab:

import PySide.QtGui
import PySide.QtCore

from builtins import super

import os
import re
import json
import logging

import pathlib2

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

        self.saveButton = PySide.QtGui.QAction('Save',
                                                self,
                                                shortcut=PySide.QtGui.QKeySequence.Save,
                                                statusTip="Save the file to the already saved file",
                                                triggered=self.saveFile,
                                                enabled=False,
        )
        fileMenu.addAction(self.saveButton)

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
        self.centralWidget().write()
    def saveAsFile(self):
        self.centralWidget().export_data()
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
        if not os.path.exists(savedir):
            os.mkdir(savedir)

        pattern = re.compile(savedir + ".+")  # At least one character beyond
        attempted = False
        self.filename = ""

        while not pattern.match(self.filename):
            self.filename = QFileDialog.getExistingDirectory(self,
                                                             caption="Export Config File",
                                                             dir=savedir,
                                                             )
            attempted = True
            if attempted and not pattern.match(self.filename):
                message  = """<p>Directory choice not allowed.</p>"""
                message += """<p>Try again.</p>"""
                box = PySide.QtGui.QMessageBox()
                box.setIcon(PySide.QtGui.QMessageBox.Warning)
                box.setWindowTitle("Invalid directory")
                box.setText("<strong>Invalid directory</strong>")
                box.setInformativeText(message.replace(" ", "&nbsp;"))
                box.setStandardButtons(PySide.QtGui.QMessageBox.Ok)
                box.exec_()

        print self.filename
        if not self.filename:
            return
        self.parent.saveButton.setEnabled(True)
        """
        savefilepath = QFileDialog.getSaveFileName(parent=None,
                                                   caption='Export Config File',
                                                   dir=savedir,
                                                   filter='JSON files(*.json)'
                                                   )[0]
                                                   """
        logger.info('path given to save is "%s"', self.filename)
        self.write(save_as=True)

    def write(self, save_as=False):
        path = pathlib2.Path(self.filename)
        import shutil
        import tempfile

        logger.info("Hello i am write")
        def warn():
            box = PySide.QtGui.QMessageBox()
            box.setIcon(PySide.QtGui.QMessageBox.Warning)
            box.setWindowTitle("Directory not empty")
            box.setText("<strong>Directory not empty</strong>")
            box.setInformativeText("""The directory {} is not empty. continue?
                    This will wipe out everything""".format(path))
            box.setStandardButtons(PySide.QtGui.QMessageBox.Save |
                    PySide.QtGui.QMessageBox.Cancel)
            box.setDefaultButton(PySide.QtGui.QMessageBox.Cancel)
            return box.exec_()

        files_exist_in_directory = bool(tuple(path.iterdir()))
        if files_exist_in_directory:
            if save_as:
                if warn() == PySide.QtGui.QMessageBox.Cancel:
                    return self.export_data()
            oldstuff = tempfile.mkdtemp(suffix="ConfigMaker", prefix='{}-'.format(path.name))
            os.rmdir(oldstuff) # To be copied to later
            shutil.move(path, oldstuff)
            # Oh also dont mess up this section cuz right here all the user's
            # contents are in ram in both places
            logger.info('Moving old contents to %s', oldstuff)
            os.mkdir(path)

        # NOTE: if users start opening up multiple windows, implement a lock
        # file

        logger.info('saving to path "%s"', self.filename)
        for i, thing in enumerate(self.things_actual):
            with open('{}/{:02}-{}.json'.format(path, i + 1,
                thing.data[self.namevar]), 'w') as fp:
                thing.write_file(fp)

        self.parent.setWindowTitle(self.parent.windowtitle.format(path.name))

        with open('{}/00-index.json'.format(path), 'w') as outfile:
            outfile.write(json.dumps(self.savedcontents, **pretty_print))
