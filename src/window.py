import logging
from PyQt4 import QtGui, QtCore

class TestWindow(QtGui.QWidget):
  
    def __init__(self):
        super(TestWindow, self).__init__()

        self.logger = logging.getLogger('root')
        self.logger.info('__init__()')
        self.initUI()

    def initUI(self):

        self.label = QtGui.QLabel("Ubuntu", self)

        self.comboBox = QtGui.QComboBox(self)
        self.comboBox.addItem("Ubuntu")
        self.comboBox.addItem("Mandriva")
        self.comboBox.addItem("Fedora")
        self.comboBox.addItem("Red Hat")
        self.comboBox.addItem("Gentoo")

        self.label.move(55, 40)
        self.comboBox.move(50, 60)

        self.connect(self.comboBox, QtCore.SIGNAL('activated(QString)'),
            self.onActivated)

        self.checkBox = QtGui.QCheckBox('Add Windows', self)
        self.checkBox.setFocusPolicy(QtCore.Qt.NoFocus)
        self.checkBox.move(10, 10)
#        self.checkBox.toggle()

        self.connect(self.checkBox, QtCore.SIGNAL('stateChanged(int)'),
            self.changeTitle)

        self.setGeometry(250, 200, 350, 250)
        self.setWindowTitle('QComboBox')

    def changeTitle(self, value):
      
        self.logger.debug('changeTitle() ... Title >>%s<<' % (value))
        
        if self.checkBox.isChecked():
            self.comboBox.addItem("Windows")
        else:
            self.comboBox.clear()
            self.comboBox.addItem("Ubuntu")
            self.comboBox.addItem("Mandriva")
            self.comboBox.addItem("Fedora")
            self.comboBox.addItem("Red Hat")
            self.comboBox.addItem("Gentoo")

    def onActivated(self, text):
      
        self.logger.debug('onActivated() ... Activated >>%s<< ... ' % (text))

        self.label.setText(text)
        self.label.adjustSize()

