from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QTabWidget, QLabel, QFileDialog, QSpinBox, QDoubleSpinBox, QCheckBox, QComboBox, QLineEdit, QAction, QPushButton
import sys
import os

class UI(QMainWindow):
    openFile = False
    fileOpen = False
    audioSampledefault = b'\x00\x00\x00\x00\x50\x4D\x53\x4F\x02\x00\x00\x00\xEF\xBE\xAD\xDE\xEF\xBE\xAD\xDE\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    audioSampledefault2 = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x04\x00\x00\x00\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x79\x07\xFC\x06\x87\x06\x19\x06\xB3\x05\x53\x05\xFA\x04\xA7\x04\x80\xF8\xB4\xF1\xC8\xEB\xDB\xE6\x07\xE3\x58\xE0\xD1\xDE\x6B\xDE\x40\x0F\x92\x15\xD2\x1A\xE8\x1E\xC5\x21\x66\x23\xD2\x23\x18\x23\x80\xF9\x52\xF4\x4C\xF0\x45\xED\x1B\xEB\xAC\xE9\xDB\xE8\x8E\xE8\x60\x0E\x54\x13\x0D\x17\xB8\x19\x7B\x1B\x7C\x1C\xDB\x1C\xB5\x1C'
    dataa = None
    fname = tuple
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("vadpcmToSample.ui", self)
        self.setFixedSize(340,319)

        self.spinBox = self.findChild(QSpinBox, 'spinBox')
        self.label_3 = self.findChild(QLabel, 'label_3')
        self.label_5 = self.findChild(QLabel, 'label_5')
        self.pushbutton = self.findChild(QPushButton, 'pushButton')
        self.pushbutton2 = self.findChild(QPushButton, 'pushButton_2')

        self.spinBox.hide()
        self.label_3.hide()
        self.pushbutton2.hide()
        self.pushbutton.pressed.connect(self.Open)
        self.pushbutton2.pressed.connect(self.Convert)
        self.show()

    def Open(self):
        fname = QFileDialog.getOpenFileName(self, 'Open vadpcm.bin File', '', 'vadpcm.bin (*.vadpcm.bin);; All Files (*)')
        if fname[0]:
            if self.fileOpen == False:
                self.fileOpen = True
                self.spinBox.show()
                self.label_3.show()
                self.pushbutton2.show()
            self.fname = fname
            self.label_5.setText(fname[0])
            self.reload()
    def reload(self):
        if self.fileOpen == True:
            file = open(self.fname[0], 'r+b')
            self.dataa = file.read()

            cool = self.fname[0]
            try:
                foile = open(os.path.split(cool)[0]+'/config.toml', 'r')
            except FileNotFoundError:
                self.label_5.setText("Can't Find config.toml file (z64audio generates a config.toml file)")
                self.fileOpen = False
                self.spinBox.hide()
                self.label_3.hide()
                self.pushbutton2.hide()
                return
            y = ""
            while ("loop_end" not in y):
                y = foile.readline()
            loop_end = [int(word) for word in y.split() if word.isdigit()][0]
            self.spinBox.setValue(loop_end)
    def Convert(self):
        fneme = QFileDialog.getSaveFileName(self, 'Save as SoH audio Sample', '', '')
        if fneme[0]:
            fyle = open(fneme[0], 'wb+')
            fyle.write(self.audioSampledefault)
            fyle.seek(68)
            fyle.write(len(self.dataa).to_bytes(2))
            fyle.seek(68)
            swep = fyle.read(1)
            swap = fyle.read(1)
            fyle.seek(68)
            fyle.write(swap)
            fyle.write(swep)
            fyle.seek(72)
            fyle.write(self.dataa)
            fyle.write(b'\x00\x00\x00\x00')
            fyle.write(self.spinBox.value().to_bytes(2))
            fyle.seek(76+len(self.dataa))
            swep = fyle.read(1)
            swap = fyle.read(1)
            fyle.seek(76+len(self.dataa))
            fyle.write(swap)
            fyle.write(swep)
            fyle.write(self.audioSampledefault2)
            fyle.close()

if __name__ == '__main__':
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()

