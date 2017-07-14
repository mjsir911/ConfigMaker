#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import super
from builtins import open
from builtins import zip
from future import standard_library
import PySide.QtCore
import PySide.QtGui
import PySide as Py
import sys
import os
import json
import logging

from shared import *

standard_library.install_aliases()

__appname__     = ""
__author__      = "Marco Sirabella"
__copyright__   = ""
__credits__     = ["Marco Sirabella",
                   "Kevin Cole"]  # Authors and bug reporters
__license__     = "GPL"
__version__     = "1.0"
__maintainers__ = "Marco Sirabella"
__email__       = "msirabel@gmail.com"
__status__      = "Prototype"  # "Prototype", "Development" or "Production"
__module__      = ""


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


DEFAULT = {
    'noise':  [{'sample': 1, 'state': True, 'offset': 0, 'level': 0}] * 8,
    'signal': [{'sample': 1, 'state': True, 'offset': 0, 'level': 0}] * 8,
    'step': 2,
    'range': [-5, 5],
    'program': 1,
    'rsize': [200, 250],
    'type': 'preset',
    'targets': [3]
        }

class SubWindow(PySide.QtGui.QDialog):
    maxoptions = 5

    def __init__(self, parent=None, data=DEFAULT):
        logger.debug("data is %s", data)
        self.data = {'type': 'preset'}
        super().__init__(parent)
        self.parent = parent
        self.layout = Py.QtGui.QVBoxLayout()

        self.desc = description_and_label('Scenario Description', Py.QtGui.QLineEdit())
        self.layout.addLayout(self.desc)

        program = Py.QtGui.QSpinBox()
        program.setMinimum(1)
        program.setMaximum(6)
        self.programlayout = description_and_label('Program', program)
        self.programlayout.addStretch(0.5)
        self.program = self.programlayout.inputobj
        del program
        self.layout.addLayout(self.programlayout)
        # self.layout.addLayout(self.programlayout, 0, 1,
        #                      PySide.QtCore.Qt.AlignCenter)

        self.glayout = Py.QtGui.QGridLayout()

        self.datums = []
        # http://mathworld.wolfram.com/TriangleWave.html
        x_equation = lambda t: 8 * abs(round((1 / 8) * (t - 1)) - (1 / 8) * (t - 1))  # noqa
        y_equation = lambda t: 8 * abs(round((1 / 8) * (t - 3)) - (1 / 8) * (t - 3))  # noqa
        # THESE ARE FOR THE EQUATIONS BELOOWWWW
        for i, datum in zip(range(1, 9), zip(data['signal'], data['noise'])):
            """
            Courtesy of the internet, i refined the quartic equation
            Now its a triangle graph, mapping x and y coordinates
            creates a diamond shaped object, which is exactly where we want
            the buttons
              /\    /
             /  \  /   ooh fancy triangle graph
            /    \/
            """
            interior = self.InteriorDatum(datum, parent=self)
            self.datums.append(interior)
            interior.show()
            interior.hide()
            button = Py.QtGui.QPushButton()
            button.setFixedWidth(200)
            button.clicked.connect(interior.show)
            button.setText(str(i))
            xc = x_equation(i)
            yc = y_equation(i)
            # print(xc, yc)
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
        buttonlayout = PySide.QtGui.QHBoxLayout()
        buttonlayout.addWidget(okbutt(self.write))
        buttonlayout.addWidget(okbutt(func=lambda: self.close(),
                                      buttonText='Cancel',
                                      ))
        self.layout.addLayout(buttonlayout)

        self.setLayout(self.layout)

    @classmethod
    def load(cls, parent, fp):
        data = json.load(fp)
        logger.info("loading subfile %s with contents %s", fp.name, data)
        self = cls(parent, data)
        self.exec_()

    def write(self):
        self.data.update({'description': self.desc.inputobj.text(),
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
        if self not in self.parent.things:
            self.parent.things.append(self)
        self.parent.update_dropdown()

    def write_file(self, prefix, pathdir):
        logger.info('writing sub-file %s/%s/%s-%s.json',
                    pathdir,
                    self.data['type'],
                    prefix,
                    self.data['description'])
        with open('{}/{}/{}-{}.json'.format(pathdir,
                                            self.data['type'],
                                            prefix,
                                            self.data['description']
                                            ),
                  'w') as outfile:
            pretty_print = {'sort_keys': True,
                            'indent': 4,
                            'separators': (',', ': ')
                           }
            outfile.write(json.dumps(self.data, **pretty_print))

    class InteriorDatum(Py.QtGui.QWidget):
        def __init__(self, data, parent=None):
            super().__init__(parent)
            self.parent = parent

            layout = Py.QtGui.QVBoxLayout()
            switchlayout = Py.QtGui.QHBoxLayout()
            speakernum = Py.QtGui.QLabel('Speaker Number {0}'
                                         .format(len(self.parent.datums) + 1))
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
            self.signalButton = Py.QtGui.QPushButton('Signal')
            self.signalButton = Py.QtGui.QToolButton()
            self.signalButton.setText('Signal')
            self.noiseButton = Py.QtGui.QPushButton('Noise')
            self.noiseButton = Py.QtGui.QToolButton()
            self.noiseButton.setText('Noise')

            flippy_buttons.addWidget(self.signalButton)
            flippy_buttons.addWidget(self.noiseButton)
            """

            self.signal = self.SignalOrNoise('Signal', data[0], self)
            self.noise = self.SignalOrNoise('Noise', data[1], self)

            # self.signalButton.clicked.connect(self.signal.show)
            # self.noiseButton.clicked.connect(self.noise.show)

            signal_noise_layout = Py.QtGui.QHBoxLayout()

            signal_noise_layout.addWidget(self.signal)
            signal_noise_layout.addWidget(self.noise)

            layout.addLayout(signal_noise_layout)

            self.target = Py.QtGui.QCheckBox()
            targetlayout = Py.QtGui.QHBoxLayout()
            label = Py.QtGui.QLabel('Target:')
            targetlayout.addStretch(0.5)
            targetlayout.addWidget(label)
            targetlayout.addWidget(self.target)
            targetlayout.addStretch(0.5)
            layout.addLayout(targetlayout)

            self.layout = layout

            # layout.addLayout(switchlayout)
            # layout.addLayout(flippy_buttons)
            # self.layout.add
            layout.addLayout(switchlayout)
            self.setLayout(layout)

        def show(self):
            super().show()
            for x in self.parent.datums:
                if x is not self:
                    x.hide()
                # pass
                # self.parent.layout.removeWidget(self)

            self.parent.glayout.addWidget(self, 2, 2)
            self.parent.glayout.indexOf(self)

        def hide(self):
            super().hide()
            self.parent.glayout.removeWidget(self)

        class SignalOrNoise(Py.QtGui.QWidget):

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
                self.layout = Py.QtGui.QVBoxLayout()

                label = Py.QtGui.QLabel(sigornoise)
                self.layout.addWidget(label)

                """
                sample: number
                level: -12 to 12
                offset: in milliseconds
                state: radio button true or false
                """

                self.state = Py.QtGui.QCheckBox()  # state checkbox
                if data['state']:
                    self.state.setCheckState(Py.QtCore.Qt.CheckState.Checked)
                else:
                    self.state.setCheckState(Py.QtCore.Qt.CheckState.Unchecked)
                statelayout = Py.QtGui.QHBoxLayout()
                label = Py.QtGui.QLabel('State:')
                statelayout.addWidget(label)
                statelayout.addWidget(self.state)
                self.layout.addLayout(statelayout)

                self.sampleinput = Py.QtGui.QSpinBox()  # sample spinbox
                self.sampleinput.setMinimum(1)
                self.sampleinput.setValue(data['sample'])
                samplelayout = Py.QtGui.QHBoxLayout()
                label = Py.QtGui.QLabel('Sample:')
                samplelayout.addWidget(label)
                samplelayout.addWidget(self.sampleinput)
                self.layout.addLayout(samplelayout)

                self.levelinput = Py.QtGui.QSpinBox()
                self.levelinput.setMinimum(-50)
                self.levelinput.setMaximum(50)
                self.levelinput.setValue(data['level'])
                levellayout = Py.QtGui.QHBoxLayout()
                label = Py.QtGui.QLabel('Level:')
                levellayout.addWidget(label)
                levellayout.addWidget(self.levelinput)
                self.layout.addLayout(levellayout)

                self.offsetinput = Py.QtGui.QSpinBox()
                self.offsetinput.setValue(data['offset'])
                offsetlayout = Py.QtGui.QHBoxLayout()
                label = Py.QtGui.QLabel('Offset:')
                offsetlayout.addWidget(label)
                offsetlayout.addWidget(self.offsetinput)
                self.layout.addLayout(offsetlayout)

                self.setLayout(self.layout)
                # self.hide()


class MyWindow(BaseWindow):
    name = 'preset'
    namevar = 'description'
    subwind = SubWindow


app = PySide.QtGui.QApplication(sys.argv)
main_window = MyWindow()
main_window.show()
font = app.font()
font.setPointSize(24)
app.setFont(font)
app.exec_()

# if __name__ == '__main__':
#    main()