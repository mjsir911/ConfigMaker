#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PySide.QtGui
import PySide.QtCore

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

class MainWidget(shared.MainWidget):
    """ Put main content here """
    name = 'ratings'
    thing = 'question' # I really dont want to go down this path again
    namevar = 'name'
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.subwind = SubWindow

        self.setLayout(PySide.QtGui.QVBoxLayout())

        description_layout = PySide.QtGui.QFormLayout()
        self.layout().addLayout(description_layout)
        #self.layout().addSpacing(20)

        self.description = PySide.QtGui.QLineEdit()
        self.description.setSizePolicy(PySide.QtGui.QSizePolicy.MinimumExpanding,
                PySide.QtGui.QSizePolicy.Fixed)
        self.description.setMinimumWidth(10 * self.size().width()) # TODO: make better
        description_layout.addRow("Ratings &description: ",
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
        self.savedcontents['description'] = self.description.text()
        self.savedcontents['instructions'] = self.instruction.text()
        super().write()

    def update(self):
        pass

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
        shared.logger.debug("data is %s", data)
        self.data = {'type': 'preset'}
        super().__init__(parent)
        self.parent = parent
        self.setLayout(PySide.QtGui.QVBoxLayout())

        description_layout = PySide.QtGui.QFormLayout()
        self.layout().addLayout(description_layout)
        self.description = PySide.QtGui.QLineEdit()
        description_layout.addRow("Scenario &Description",
                                  self.description)

        self.program = PySide.QtGui.QSpinBox()
        self.program.setMinimum(1)
        self.program.setMaximum(6)
        description_layout.addRow("Program", self.program)

        # self.layout.addLayout(self.programlayout, 0, 1,
        #                      PySide.QtCore.Qt.AlignCenter)

        self.glayout = PySide.QtGui.QGridLayout()

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
            button = PySide.QtGui.QPushButton()
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
        self.layout().addLayout(self.glayout)

        button_layout = PySide.QtGui.QDialogButtonBox(
                PySide.QtGui.QDialogButtonBox.Save |\
                PySide.QtGui.QDialogButtonBox.Cancel,
                parent=self)

        button_layout.accepted.connect(self.write)
        button_layout.rejected.connect(self.close)
        self.layout().addWidget(button_layout)

    @classmethod
    def load(cls, parent, fp):
        data = json.load(fp)
        shared.logger.info("loading subfile %s with contents %s", fp.name, data)
        self = cls(parent, data)
        self.exec_()

    def write(self):
        self.data.update({'description': self.description.text(),
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

    def write_file(self, fp):
        shared.logger.info('writing sub-file %s', fp.name)
        pretty_print = {'sort_keys': True,
                        'indent': 4,
                        'separators': (',', ': ')
                        }
        fp.write(json.dumps(self.data, **pretty_print))

    class InteriorDatum(PySide.QtGui.QWidget):
        def __init__(self, data, parent=None):
            super().__init__(parent)
            self.parent = parent

            layout = PySide.QtGui.QVBoxLayout()
            switchlayout = PySide.QtGui.QHBoxLayout()
            speakernum = PySide.QtGui.QLabel('Speaker Number {0}'
                                         .format(len(self.parent.datums) + 1))
            f = PySide.QtGui.QFont()
            f.setWeight(PySide.QtGui.QFont.Black)
            speakernum.setFont(f)
            speakerhead = PySide.QtGui.QHBoxLayout()
            speakerhead.addStretch(0.5)
            speakerhead.addWidget(speakernum)
            speakerhead.addStretch(0.5)
            layout.addLayout(speakerhead)

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

            layout.addLayout(signal_noise_layout)

            self.target = PySide.QtGui.QCheckBox()
            targetlayout = PySide.QtGui.QHBoxLayout()
            label = PySide.QtGui.QLabel('Target:')
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
                self.layout = PySide.QtGui.QVBoxLayout()

                label = PySide.QtGui.QLabel(sigornoise)
                self.layout.addWidget(label)

                """
                sample: number
                level: -12 to 12
                offset: in milliseconds
                state: radio button true or false
                """

                self.state = PySide.QtGui.QCheckBox()  # state checkbox
                if data['state']:
                    self.state.setCheckState(PySide.QtCore.Qt.CheckState.Checked)
                else:
                    self.state.setCheckState(PySide.QtCore.Qt.CheckState.Unchecked)
                statelayout = PySide.QtGui.QHBoxLayout()
                label = PySide.QtGui.QLabel('State:')
                statelayout.addWidget(label)
                statelayout.addWidget(self.state)
                self.layout.addLayout(statelayout)

                self.sampleinput = PySide.QtGui.QSpinBox()  # sample spinbox
                self.sampleinput.setMinimum(1)
                self.sampleinput.setValue(data['sample'])
                samplelayout = PySide.QtGui.QHBoxLayout()
                label = PySide.QtGui.QLabel('Sample:')
                samplelayout.addWidget(label)
                samplelayout.addWidget(self.sampleinput)
                self.layout.addLayout(samplelayout)

                self.levelinput = PySide.QtGui.QSpinBox()
                self.levelinput.setMinimum(-50)
                self.levelinput.setMaximum(50)
                self.levelinput.setValue(data['level'])
                levellayout = PySide.QtGui.QHBoxLayout()
                label = PySide.QtGui.QLabel('Level:')
                levellayout.addWidget(label)
                levellayout.addWidget(self.levelinput)
                self.layout.addLayout(levellayout)

                self.offsetinput = PySide.QtGui.QSpinBox()
                self.offsetinput.setValue(data['offset'])
                offsetlayout = PySide.QtGui.QHBoxLayout()
                label = PySide.QtGui.QLabel('Offset:')
                offsetlayout.addWidget(label)
                offsetlayout.addWidget(self.offsetinput)
                self.layout.addLayout(offsetlayout)

                self.setLayout(self.layout)
                # self.hide()

if __name__ == '__main__':
    from sys import argv, exit
    app = PySide.QtGui.QApplication(argv)
    dumbthing = shared.MainWindow(MainWidget, parent=app)
    exit(app.exec_())
