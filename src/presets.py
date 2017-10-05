#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PySide.QtGui
import PySide.QtCore

import json

from builtins import super

import shared

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

from inspect import currentframe
def debug(frame):
    import inspect
    frameinfo = inspect.getframeinfo(frame)
    shared.logger.debug("%s:%s", frameinfo.filename, frameinfo.lineno)

class MainWidget(shared.MainWidget):
    """ Put main content here """
    name = 'presets'
    thing = 'trial' # I really dont want to go down this path again
    namevar = 'description'
    DEFAULT = {namevar: ''}
    def __init__(self, parent=None, data=DEFAULT):
        super().__init__(parent=parent)
        self.savedcontent = data.copy()
        self.subwind = SubWindow

        self.setLayout(PySide.QtGui.QVBoxLayout())

        description_layout = PySide.QtGui.QFormLayout()
        self.layout().addLayout(description_layout)
        # self.layout().addSpacing(20)

        self.description = PySide.QtGui.QLineEdit()
        self.description.setText(self.savedcontent['description'])
        self.description.setPlaceholderText("Scenario")
        self.description.setSizePolicy(
            PySide.QtGui.QSizePolicy.MinimumExpanding,
            PySide.QtGui.QSizePolicy.Fixed
        )
        self.description.setMinimumWidth(10 * self.size().width())
        # TODO: make better
        description_layout.addRow("Scenario &description: ",
                                  self.description)

        self.add_button = PySide.QtGui.QPushButton(
            'Add {}'.format(self.thing),
            parent=self
        )
        self.layout().addWidget(self.add_button)
        self.add_button.clicked.connect(self.add_subWindow)

        self.parent.editMenu.addAction(PySide.QtGui.QAction('Add {}'.format(self.thing),
                                                 self,
                                                 statusTip="Add a new {}".format(self.thing),
                                                 triggered=self.add_subWindow,
        ))

        self.layout().addWidget(PySide.QtGui.QLabel("Double click an entry below to edit:"))
        # Thanks kevin for good wording on that



        self.things = PySide.QtGui.QListWidget()
        self.layout().addWidget(self.things)
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
        button_layout.buttons()[0].setText('Save as')
        # Change first (and only) button from Save => Save as
        button_layout.accepted.connect(self.export_data)
        self.layout().addWidget(button_layout)

        self.update()

    def write(self):
        if self.description.text() == "":
            self.description.setText(self.description.placeholderText())
        self.savedcontents['description'] = self.description.text()
        super().write()

    def update(self):
        pass

from UI import LocalizationPane
import math
class FancyCircle(LocalizationPane.ControlPane):
    def __init__(self, *args):
        shared.logger.debug("Creating circle")
        super().__init__(*args)
        self.signal.hide()
        self.noise.hide()

        for i in range(8):
            for button in ('louder', 'softer'):
                self.speakers[i][button].hide()
            self.speakers[i]['select'].setStyleSheet(self.style.format('red'))
        shared.logger.debug("finishing fancy circle")

    def paintEvent(self, event):
        shared.logger.debug("fancy circle paint event")
        """
        Draw / position the audio source buttons
        MONKEYPATCHING
        """

        #super(PySide.QtCore.ControlPane, self).paintEvent(event)  # Draw the normal grey box
        super().paintEvent(event)
############################################################################

        sizeX, sizeY = [55] * 2
        self.speaker1.setGeometry(self.compass[0][0] - (sizeX // 2),
                                  self.compass[0][1] - (sizeY // 2),
                                  sizeX, sizeY)
        self.speaker2.setGeometry(self.compass[1][0] - (sizeX // 2),
                                  self.compass[1][1] - (sizeY // 2),
                                  sizeX, sizeY)
        self.speaker3.setGeometry(self.compass[2][0] - (sizeX // 2),
                                  self.compass[2][1] - (sizeY // 2),
                                  sizeX, sizeY)
        self.speaker4.setGeometry(self.compass[3][0] - (sizeX // 2),
                                  self.compass[3][1] - (sizeY // 2),
                                  sizeX, sizeY)
        self.speaker5.setGeometry(self.compass[4][0] - (sizeX // 2),
                                  self.compass[4][1] - (sizeY // 2),
                                  sizeX, sizeY)
        self.speaker6.setGeometry(self.compass[5][0] - (sizeX // 2),
                                  self.compass[5][1] - (sizeY // 2),
                                  sizeX, sizeY)
        self.speaker7.setGeometry(self.compass[6][0] - (sizeX // 2),
                                  self.compass[6][1] - (sizeY // 2),
                                  sizeX, sizeY)
        self.speaker8.setGeometry(self.compass[7][0] - (sizeX // 2),
                                  self.compass[7][1] - (sizeY // 2),
                                  sizeX, sizeY)

        signalX, signalY = 10,              self.height - 90
        noiseX,  noiseY  = self.width - 95, self.height - 90

class SubWindow(PySide.QtGui.QDialog):
    maxoptions = 5

    DEFAULT = {
        'description': '',
        'noise':  [{'sample': 1, 'state': False, 'offset': 0, 'level': 0}] * 8,
        'signal': [{'sample': 1, 'state': False, 'offset': 0, 'level': 0}] * 8,
        'step': 3,
        'range': [-12, 12],
        'program': 1,
        'rsize': [104, 104],
        'type': 'preset',
        'targets': [3]
            }

    def __init__(self, parent=None, data=DEFAULT):
        shared.logger.debug("data is %s", data)
        self.parent = parent
        self.num = self.parent.things.count() + 1
        self.data = data.copy()
        super().__init__(parent)
        self.setLayout(PySide.QtGui.QVBoxLayout())

        description_layout = PySide.QtGui.QFormLayout()
        self.layout().addLayout(description_layout)
        self.description = PySide.QtGui.QLineEdit()
        self.description.setPlaceholderText("Trial {}".format(self.num))
        self.description.setMinimumWidth(10 * self.size().width())
        self.description.setText(self.data['description'])
        # TODO: make better
        description_layout.addRow("Trial &Description:",
                                  self.description)

        self.program = PySide.QtGui.QSpinBox()
        self.program.setMinimum(0)
        self.program.setMaximum(6)
        self.program.setValue(self.data['program'])
        self.program.setSizePolicy(PySide.QtGui.QSizePolicy(
                PySide.QtGui.QSizePolicy.Maximum,
                PySide.QtGui.QSizePolicy.Maximum)
            )
        label1 = PySide.QtGui.QLabel("Program:")
        label1.setSizePolicy(PySide.QtGui.QSizePolicy(
                PySide.QtGui.QSizePolicy.Maximum,
                PySide.QtGui.QSizePolicy.Maximum)
            )
        program_layout = PySide.QtGui.QHBoxLayout()
        program_layout.addWidget(label1)
        program_layout.addWidget(self.program)
        program_layout.addWidget(PySide.QtGui.QLabel(
        "0 = client's choice of program. 1 to 6 = assigned [requested] program"))
        description_layout.addRow(program_layout)

        # self.layout.addLayout(self.programlayout, 0, 1,
        #                      PySide.QtCore.Qt.AlignCenter)

        self.fancy_circle = FancyCircle()
        self.layout().addWidget(self.fancy_circle)

        self.datums = []
        for button, datum in zip(self.fancy_circle.speakers, zip(data['signal'], data['noise'])):
            shared.logger.debug("Adding widget x")
            interior = self.InteriorDatum(datum, parent=self)
            self.datums.append(interior)
            interior.show()
            interior.hide()

            button['select'].clicked.connect(interior.show)

        debug(currentframe())


        button_layout = PySide.QtGui.QDialogButtonBox(
                PySide.QtGui.QDialogButtonBox.Save |\
                PySide.QtGui.QDialogButtonBox.Cancel,
                parent=self)

        debug(currentframe())
        for button in button_layout.buttons():
            button.setSizePolicy(PySide.QtGui.QSizePolicy(
                PySide.QtGui.QSizePolicy.MinimumExpanding,
                PySide.QtGui.QSizePolicy.MinimumExpanding)
            )

        debug(currentframe())
        button_layout.accepted.connect(self.write)
        button_layout.rejected.connect(self.close)
        self.layout().addWidget(button_layout)

        self.showMaximized()
        debug(currentframe())

    @classmethod
    def load(cls, parent, fp):
        data = json.load(fp)
        shared.logger.info("loading subfile %s with contents %s", fp.name, data)
        self = cls(parent, data)
        self.exec_()

    def write(self):
        if self.description.text() == "":
            self.description.setText(self.description.placeholderText())

        self.data.update({'description': self.description.text(),
                          'program': self.program.value(),
                          })

            sub.target.isChecked()]
        self.data['targets'] = [sub.num for sub in self.datums if

        self.data['noise'] = noise = []
        self.data['signal'] = signal = []
        for datum in self.datums:
            # these are all interior datums
            signal.append({'sample': datum.signal.sampleinput.value(),
                           'level': datum.signal.levelinput.value(),
                           'offset': datum.signal.offsetinput.value(),
                           'state': datum.signal.state.isChecked(),
                           })
            noise.append({'sample': datum.noise.sampleinput.value(),
                          'level': datum.noise.levelinput.value(),
                          'offset': datum.noise.offsetinput.value(),
                          'state': datum.noise.state.isChecked(),
                          })

        self.hide()

        if self not in self.parent.things_actual:
            self.listitem = PySide.QtGui.QListWidgetItem(self.data['description'])
            self.listitem.widget = self
            self.parent.things.addItem(self.listitem)

        else:
            self.listitem.setText(self.data['description'])

        self.parent.update()

    def write_file(self, fp):
        shared.logger.info('writing sub-file %s', fp.name)
        pretty_print = {'sort_keys': True,
                        'indent': 4,
                        'separators': (',', ': ')
                        }
        fp.write(json.dumps(self.data, **pretty_print))

    class InteriorDatum(PySide.QtGui.QDialog):
        def __init__(self, data, parent=None):
            super().__init__(parent)
            self.parent = parent

            self.setLayout(PySide.QtGui.QVBoxLayout())

            switchlayout = PySide.QtGui.QHBoxLayout()
            self.num = len(self.parent.datums) + 1
            speakernum = PySide.QtGui.QLabel('Loudspeaker {0}'.format(self.num))
            f = PySide.QtGui.QFont()
            f.setWeight(PySide.QtGui.QFont.Black)
            speakernum.setFont(f)
            speakerhead = PySide.QtGui.QHBoxLayout()
            speakerhead.addStretch(0.5)
            speakerhead.addWidget(speakernum)
            speakerhead.addStretch(0.5)
            self.layout().addLayout(speakerhead)

            """
            flippy_buttons = PySide.QtGui.QHBoxLayout()
            flippy_buttons.setSpacing(-0.1)
            self.signalButton = PySide.QtGui.QPushButton('Signal')
            self.signalButton = PySide.QtGui.QToolButton()
            self.signalButton.setText('Signal')
            self.noiseButton = PySide.QtGui.QPushButton('Noise')
            self.noiseButton = PySide.QtGui.QToolButton()
            self.noiseButton.setText('Noise')

            flippy_buttons.addWidget(self.signalButton)
            flippy_buttons.addWidget(self.noiseButton)
            """

            self.signal = self.SignalOrNoise('Signal', data[0], self)
            self.noise = self.SignalOrNoise('Noise', data[1], self)

            # self.signalButton.clicked.connect(self.signal.show)
            # self.noiseButton.clicked.connect(self.noise.show)

            signal_noise_layout = PySide.QtGui.QHBoxLayout()

            signal_noise_layout.addWidget(self.signal)
            signal_noise_layout.addWidget(self.noise)

            self.layout().addLayout(signal_noise_layout)

            self.target = PySide.QtGui.QCheckBox()
            targetlayout = PySide.QtGui.QHBoxLayout()
            label = PySide.QtGui.QLabel('Target:')
            targetlayout.addStretch(0.5)
            targetlayout.addWidget(label)
            targetlayout.addWidget(self.target)
            targetlayout.addStretch(0.5)
            self.layout().addLayout(targetlayout)


            # layout.addLayout(switchlayout)
            # layout.addLayout(flippy_buttons)
            # self.layout.add
            self.layout().addLayout(switchlayout)

            button_layout = PySide.QtGui.QDialogButtonBox(
                    PySide.QtGui.QDialogButtonBox.Save |\
                    PySide.QtGui.QDialogButtonBox.Cancel,
                    parent=self)

            for button in button_layout.buttons():
                button.setSizePolicy(PySide.QtGui.QSizePolicy(
                    PySide.QtGui.QSizePolicy.MinimumExpanding,
                    PySide.QtGui.QSizePolicy.MinimumExpanding)
                    )

            button_layout.accepted.connect(self.write)
            button_layout.rejected.connect(self.close)
            self.layout().addWidget(button_layout)

        def write(self):
            button = self.parent.fancy_circle.speakers[self.num - 1]['select']
            button.setStyleSheet(self.parent.fancy_circle.style.format('green'))
            self.hide()

        def show(self):
            super().show()
            for x in self.parent.datums:
                if x is not self:
                    x.hide()
                # pass
                # self.parent.layout.removeWidget(self)

            #self.parent.glayout.addWidget(self, 2, 2) # XXX
            #self.parent.glayout.indexOf(self) # XXX

        def hide(self):
            super().hide()
            #self.parent.glayout.removeWidget(self) # XXX

        class SignalOrNoise(PySide.QtGui.QWidget):

            def buttonclick(self):
                self.parent.datums
                for datum in self.parent.datums:
                    if datum is not self:
                        pass
                        'make button not blue'

            def __init__(self, sigornoise, data, parent=None):
                super().__init__(parent)
                self.parent = parent
                self.toggle = sigornoise
                self.setLayout(PySide.QtGui.QFormLayout())

                label = PySide.QtGui.QLabel(sigornoise)
                self.layout().addRow(label)
                label.setAlignment(PySide.QtCore.Qt.AlignHCenter)
                label.setProperty('class', 'list_header') # This is pretty cool


                """
                sample: number
                level: -12 to 12
                offset: in milliseconds
                state: radio button true or false
                """


                self.state = PySide.QtGui.QCheckBox()  # state checkbox

                self.state.setCheckState(
                                         PySide.QtCore.Qt.CheckState.Checked
                                         if data['state'] else
                                         PySide.QtCore.Qt.CheckState.Unchecked
                                         )

                self.layout().addRow("Active:", self.state)

                self.sampleinput = PySide.QtGui.QSpinBox()  # sample spinbox
                self.sampleinput.setMinimum(1)
                self.sampleinput.setValue(data['sample'])
                self.layout().addRow("Sample:", self.sampleinput)


                self.levelinput = PySide.QtGui.QSpinBox()
                self.levelinput.setMinimum(-50)
                self.levelinput.setMaximum(50)
                self.levelinput.setValue(data['level'])
                self.layout().addRow("Gain (dB):", self.levelinput)

                self.offsetinput = PySide.QtGui.QSpinBox()
                self.offsetinput.setValue(data['offset'])
                self.offsetinput.setEnabled(False)
                self.layout().addRow("Offset (sec):", self.offsetinput)

                # self.hide()

if __name__ == '__main__':
    from sys import argv, exit
    app = PySide.QtGui.QApplication(argv)
    dumbthing = shared.MainWindow(MainWidget, parent=app)
    exit(app.exec_())
