#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import PySide.QtGui
import PySide.QtCore

from builtins import super

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

class MainWindow(PySide.QtGui.QMainWindow):
    def __init__(self, parent=None):
        super().__init__()

        self.initGUI()

    def initGUI(self):
        self.setWindowTitle("ScribblerSeq")
        self.showMaximized()

        self.setCentralWidget(MainWidget(parent=self))

        with open('style.css', 'r') as fp:
            self.setStyleSheet(fp.read())
        #self.setStyleSheet('* { font-size: 32px; }')

        self.show()


class MainWidget(PySide.QtGui.QGroupBox):
    """ Put main content here """
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setLayout(PySide.QtGui.QHBoxLayout())

        leftlayout = PySide.QtGui.QVBoxLayout()
        rightlayout = PySide.QtGui.QVBoxLayout()
        self.layout().addLayout(leftlayout, 1)
        self.layout().addLayout(rightlayout, 1)

        description_layout = PySide.QtGui.QFormLayout()
        leftlayout.addLayout(description_layout)
        leftlayout.addSpacing(20)

        description_layout.addRow("Ratings &description: ",
                                  PySide.QtGui.QLineEdit())

        self.add_button = PySide.QtGui.QPushButton('Add Question', parent=self)
        leftlayout.addWidget(self.add_button)
        self.add_button.clicked.connect(self.add_subWindow)

        self.things = PySide.QtGui.QListWidget()
        leftlayout.addWidget(self.things)
        self.things.itemDoubleClicked.connect(
                lambda: self.things.selectedItems()[0].widget.show()
                # This is a doozy:
                # this socket, when double clicked, gets the selected
                # double clicked item as a list (even though only one can
                # be selected at a time) and then gets the subwidget, then
                # shows the subwidget
                )


        button_layout = PySide.QtGui.QDialogButtonBox(
                PySide.QtGui.QDialogButtonBox.Save,
                parent=self)
        button_layout.accepted.connect(self.write)
        leftlayout.addWidget(button_layout)

    @property
    def things_actual(self):
        return [self.things.item(i).widget for i in
                range(self.things.count())]

    def add_subWindow(self):
        SubWindow(parent=self).exec_()

    def export_data(self):
        from PySide.QtGui import QFileDialog
        savedir = defaultdir + self.name + 's/'
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

    def write(path, self):
        for i, thing in enumerate(self.things_actual):
            with open('{}/{:02}-{}.json'.format(path, i, thing.data['name']),
                    'r') as fp:
                thing.write_file(fp)


import collections
class SubWindow(PySide.QtGui.QDialog):
    maxoptions = 5
    responses = collections.OrderedDict((
                 ('Radio Buttons', 'radio'),
                 ('Check Boxes', 'check'),
                 ('Free Response', 'free'),
                 ))
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.index = -1

        self.data = {'type': 'rating'}

        self.setLayout(PySide.QtGui.QVBoxLayout())
        input_layout = PySide.QtGui.QFormLayout()
        self.layout().addLayout(input_layout)
        self.name = PySide.QtGui.QLineEdit(parent=self)
        input_layout.addRow('Response id:', self.name)
        self.question = PySide.QtGui.QLineEdit(parent=self)
        input_layout.addRow('Question:', self.question)
        self.rating_type = PySide.QtGui.QComboBox(parent=self)
        input_layout.addRow('Response type:', self.rating_type)
        # Change to radio buttons if dragano dont like the ugliness of this
        self.rating_type.setSizePolicy(PySide.QtGui.QSizePolicy.Expanding,
                                PySide.QtGui.QSizePolicy.Preferred)

        for response_type in self.responses.keys():
            self.rating_type.addItem(response_type)
        self.rating_type.update()

        self.rating_type.currentIndexChanged.connect(self.check)
        self.rating_type.update()

        self.all_responses = []
        self.questionNum = PySide.QtGui.QSpinBox()
        input_layout.addWidget(self.questionNum)
        self.questionNum.setRange(2, self.maxoptions)
        self.questionNum.valueChanged.connect(self.responseCheck)

        response_layout = PySide.QtGui.QVBoxLayout()
        self.layout().addLayout(response_layout)
        for x in range(0, self.maxoptions):
            response = self.Response(x)
            self.all_responses.append(response)
            response_layout.addWidget(response)
        response_layout.addStretch(1)

        button_layout = PySide.QtGui.QDialogButtonBox(
                PySide.QtGui.QDialogButtonBox.Save |
                PySide.QtGui.QDialogButtonBox.Cancel
                )
        self.layout().addWidget(button_layout)
        button_layout.accepted.connect(self.write)
        button_layout.rejected.connect(self.close)

        for button in button_layout.buttons():
            button.setSizePolicy(PySide.QtGui.QSizePolicy(
                PySide.QtGui.QSizePolicy.Expanding,
                PySide.QtGui.QSizePolicy.Expanding)
            )

        self.questionNum.setValue(5)
        self.responseCheck()
        self.check()

    def responseCheck(self):
        for x in self.all_responses:
            x.check(self.questionNum.value())

    def check(self):
        text = self.rating_type.currentText()
        print(self.rating_type.minimumHeight())
        if text == "Radio Buttons":
            self.questionNum.setRange(2, self.maxoptions)
        elif text == "Check Boxes":
            self.questionNum.setRange(1, self.maxoptions)
        elif text == "Free Response":
            self.questionNum.setRange(0, 0)
        else:
            print('error: {}'.format(text))
        self.rating_type.update()

    class Response(PySide.QtGui.QWidget):
        def __init__(self, num, parent=None):
            super().__init__(parent)
            self.parent = parent
            self.layout = PySide.QtGui.QVBoxLayout()
            self.num = num
            #self.hr = PySide.QtGui.QSpacerItem(20, 40, PySide.QtGui.QSizePolicy.Minimum, PySide.QtGui.QSizePolicy.Expanding)
            self.selection = PySide.QtGui.QLineEdit()
            self.selection.setPlaceholderText("Text")
            self.questionNum = PySide.QtGui.QSpinBox()
            self.recode = PySide.QtGui.QSpinBox()
            self.recode.setValue(num + 1)
            self.questionNum.setRange(0, -1)

            self.hbox = PySide.QtGui.QHBoxLayout()
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
        self.data['name'] = self.name.text()
        self.data['subtype'] = self.responses[self.rating_type.currentText()]
        self.data['question'] = self.question.text()
        self.data['options'] = [(x.recode.text(), x.selection.text())
                                for x in self.all_responses if not x.isHidden()]
        self.hide()

        if self not in self.parent.things_actual:
            self.listitem = PySide.QtGui.QListWidgetItem(self.data['name'])
            self.listitem.widget = self
            self.parent.things.addItem(self.listitem)

        else:
            self.listitem.setText(self.data['name'])

    def write_file(self, fp):
        logger.info('writing sub-file %s', fp.name)
        pretty_print = {'sort_keys': True,
                        'indent': 4,
                        'separators': (',', ': ')
                        }
        fp.write(json.dumps(self.data, **pretty_print))

if __name__ == '__main__':
    from sys import argv, exit
    app = PySide.QtGui.QApplication(argv)
    dumbthing = MainWindow(parent=app)
    exit(app.exec_())
