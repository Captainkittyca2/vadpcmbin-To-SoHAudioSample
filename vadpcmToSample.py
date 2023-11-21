from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QTabWidget, QLabel, QFileDialog, QSpinBox, QDoubleSpinBox, QCheckBox, QComboBox, QLineEdit, QAction, QPushButton
import sys
import os

class UI(QMainWindow):
    openFile = False
    fileOpen = False
    audioSampledefault = b''
    audioSampledefault2 = b''
    dataa = None
    fname = tuple
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("vadpcmToSample.ui", self)
        self.setFixedSize(340,319)

        self.spinBox = self.findChild(QSpinBox, 'spinBox')
        self.spinBox2 = self.findChild(QSpinBox, 'spinBox_2')
        self.spinBox3 = self.findChild(QSpinBox, 'spinBox_3')
        self.label_3 = self.findChild(QLabel, 'label_3')
        self.label_4 = self.findChild(QLabel, 'label_4')
        self.label_5 = self.findChild(QLabel, 'label_5')
        self.label_6 = self.findChild(QLabel, 'label_6')
        self.pushbutton = self.findChild(QPushButton, 'pushButton')
        self.pushbutton2 = self.findChild(QPushButton, 'pushButton_2')

        self.spinBox.hide()
        self.spinBox2.hide()
        self.spinBox3.hide()
        self.label_3.hide()
        self.label_4.hide()
        self.label_6.hide()
        self.pushbutton2.hide()
        self.pushbutton.pressed.connect(self.Open)
        self.pushbutton2.pressed.connect(self.Convert)
        self.show()
        try:
            fyuyuyle = open("config.bruh", 'rb')
            self.audioSampledefault = fyuyuyle.read(72)
            self.audioSampledefault2 = fyuyuyle.read(150)
        except FileNotFoundError:
            self.firstTime()

    def firstTime(self):
        fnume = QFileDialog.getOpenFileName(self, 'Open a Soh Audio Sample', '', 'SoH Audio Sample (*)')
        if fnume[0]:
            fuyle = open(fnume[0], 'rb+')
            fuyle.seek(4)
            if b'\x50\x4D\x53\x4F' in fuyle.read(4):
                openFile = True
                fuyle.seek(0)
                fayayle = open('config.bruh', 'wb+')
                fayayle.write(fuyle.read(72))
                boi = os.path.getsize(fnume[0]) - 215
                fuyle.seek(71+boi)
                fayayle.write(fuyle.read(156))
                fayayle.close()
                fuyle.close()
                sys.exit()
            else: sys.exit()
        else: sys.exit()


    def Open(self):
        fname = QFileDialog.getOpenFileName(self, 'Open vadpcm.bin File', '', 'vadpcm.bin (*.vadpcm.bin);; All Files (*)')
        if fname[0]:
            if self.fileOpen == False:
                self.fileOpen = True
                self.spinBox.show()
                self.spinBox2.show()
                self.spinBox3.show()
                self.label_3.show()
                self.label_4.show()
                self.label_6.show()
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
                self.spinBox2.hide()
                self.spinBox3.hide()
                self.label_3.hide()
                self.label_4.hide()
                self.label_6.hide()
                self.pushbutton2.hide()
                return
            x = ""
            y = ""
            z = ""
            while ("loop_start" not in x):
                x = foile.readline()
            while ("loop_end" not in y):
                y = foile.readline()
            while ("loop_count" not in z):
                z = foile.readline()
            loop_start = [int(word) for word in x.split() if word.isdigit()][0]
            loop_end = [int(word) for word in y.split() if word.isdigit()][0]
            loop_count = [int(word) for word in z.split() if word.isdigit()][0]
            self.spinBox.setValue(loop_end)
            self.spinBox2.setValue(loop_count)
            self.spinBox3.setValue(loop_start)
    def Convert(self):
        fneme = QFileDialog.getSaveFileName(self, 'Save as SoH audio Sample', '', 'SoH audio Sample (*)')
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
            fyle.write(self.spinBox3.value().to_bytes(2))
            fyle.seek(72+len(self.dataa))
            swep = fyle.read(1)
            swap = fyle.read(1)
            fyle.seek(72+len(self.dataa))
            fyle.write(swap)
            fyle.write(swep)
            fyle.write(b'\x00\x00')
            fyle.write(self.spinBox.value().to_bytes(2))
            fyle.seek(76+len(self.dataa))
            swep = fyle.read(1)
            swap = fyle.read(1)
            fyle.seek(76+len(self.dataa))
            fyle.write(swap)
            fyle.write(swep)
            fyle.write(b'\x00\x00')
            fyle.write(self.spinBox2.value().to_bytes(2))
            fyle.seek(80+len(self.dataa))
            swep = fyle.read(1)
            swap = fyle.read(1)
            fyle.seek(80+len(self.dataa))
            fyle.write(swap)
            fyle.write(swep)
            fyle.write(b'\x00\x00')
            fyle.write(self.audioSampledefault2)
            fyle.close()

if __name__ == '__main__':
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()