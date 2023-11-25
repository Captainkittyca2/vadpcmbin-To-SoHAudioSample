from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QTabWidget, QLabel, QFileDialog, QSpinBox, QDoubleSpinBox, QCheckBox, QComboBox, QLineEdit, QAction, QPushButton
import sys
import os

class UI(QMainWindow):
    openFile = False
    fileOpen = False
    audioSampledefault = b''
    audioSampledefault2 = b''
    sustime = b''
    fileOrd = b''
    fileType1 = ''
    fileType2 = ''
    SampleOpen = False
    dataa = None
    fname = tuple
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("vadpcmToSample.ui", self)
        self.setFixedSize(340,319)

        self.spinBox = self.findChild(QSpinBox, 'spinBox')
        self.spinBox3 = self.findChild(QSpinBox, 'spinBox_3')
        self.dspinbox = self.findChild(QDoubleSpinBox, 'doubleSpinBox_2')
        self.dspinbox2 = self.findChild(QDoubleSpinBox, 'doubleSpinBox')
        self.label_3 = self.findChild(QLabel, 'label_3')
        self.label_4 = self.findChild(QLabel, 'label_4')
        self.label_5 = self.findChild(QLabel, 'label_5')
        self.label_6 = self.findChild(QLabel, 'label_6')
        self.checkbox = self.findChild(QCheckBox, 'checkBox')
        self.pushbutton = self.findChild(QPushButton, 'pushButton')
        self.pushbutton2 = self.findChild(QPushButton, 'pushButton_2')
        self.tToggle = self.findChild(QPushButton, 'SecondsSamples')
        self.sampleRate = self.findChild(QComboBox, 'comboBox')

        self.spinBox.hide()
        self.spinBox3.hide()
        self.dspinbox.hide()
        self.dspinbox2.hide()
        self.checkbox.hide()
        self.label_3.hide()
        self.label_4.hide()
        self.label_6.hide()
        self.pushbutton2.hide()
        self.tToggle.hide()
        self.sampleRate.hide()
        self.checkbox.clicked.connect(self.Looop)
        self.pushbutton.pressed.connect(self.Open)
        self.pushbutton2.pressed.connect(self.Convert)
        self.sampleRate.currentIndexChanged.connect(self.samRate)
        self.tToggle.pressed.connect(self.SampleSecond)
        self.show()
        try:
            fyuyuyle = open("config.bruh", 'rb')
            self.audioSampledefault = fyuyuyle.read(72)
            self.audioSampledefault2 = fyuyuyle.read(144)
            self.sustime = fyuyuyle.read(1)
            self.sampleRate.setCurrentIndex(int(ord(fyuyuyle.read(1)))) 
            self.fileOrd = fyuyuyle.read(1)
            fyuyuyle.close()
            if self.sustime == b'':
                self.firstTime()
            self.priority()
        except FileNotFoundError:
            self.firstTime()
        except TypeError:
            self.firstTime()

    def firstTime(self):
        fnume = QFileDialog.getOpenFileName(self, 'Open a sfx/voice SoH Audio Sample', '', 'SoH Audio Sample (*)')
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
                fayayle.write((0).to_bytes())
                fayayle.write((4).to_bytes())
                fayayle.write((0).to_bytes())
                fayayle.close()
                fuyle.close()
                sys.exit()
            else: sys.exit()
        else: sys.exit()


    def Open(self):
        fname = QFileDialog.getOpenFileName(self, 'Open a vadpcm.bin or SoH Audio Sample File', '', self.fileType1 + ';; ' + self.fileType2)
        if fname[0]:
            if self.fileOpen == False:
                self.fileOpen = True
                self.checkbox.show()
                self.label_3.show()
                self.label_4.show()
                self.label_6.show()
                self.pushbutton2.show()
                self.sampleRate.show()
                self.tToggle.show()
            self.fname = fname
            self.label_5.setText(fname[0])
            self.reload()

    def reload(self):
        if self.fileOpen == True:
            file = open(self.fname[0], 'r+b')
            file.seek(4)
            if b'\x50\x4D\x53\x4F' in file.read(4):
                self.SampleOpen = True
                self.fileOrd = b'\x01'
                file.seek(0)
                self.dataa = file.read()
                file.seek(68)
                longth = int.from_bytes(file.read(4), byteorder='little')
                file.seek(longth+72)
                loop_start = int.from_bytes(file.read(4), byteorder='little')
                loop_end = int.from_bytes(file.read(4), byteorder='little')
                loop_count = int.from_bytes(file.read(4), byteorder='little')
            else:
                self.SampleOpen = False
                self.fileOrd = b'\x00'
                file.seek(0)
                self.dataa = file.read()
                cool = self.fname[0]
                try:
                    foile = open(os.path.split(cool)[0]+'/config.toml', 'r')
                except FileNotFoundError:
                    self.label_5.setText("Can't Find config.toml file (z64audio generates a config.toml file)")
                    self.fileOpen = False
                    self.spinBox.hide()
                    self.spinBox3.hide()
                    self.dspinbox.hide()
                    self.dspinbox2.hide()
                    self.checkbox.hide()
                    self.label_3.hide()
                    self.label_4.hide()
                    self.label_6.hide()
                    self.pushbutton2.hide()
                    self.sampleRate.hide()
                    self.tToggle.hide()
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
            if loop_count != 0:
                self.checkbox.setChecked(True)
            else: self.checkbox.setChecked(False)
            self.Looop()
            if self.sustime == b'\x00':
                self.spinBox.show()
                self.spinBox3.show()
                self.spinBox.setValue(loop_end)
                self.spinBox3.setValue(loop_start)
            elif self.sustime == b'\x01':
                self.dspinbox.show()
                self.dspinbox2.show()
                self.dspinbox.setValue(loop_end/int(self.sampleRate.currentText()))
                self.dspinbox2.setValue(loop_start/int(self.sampleRate.currentText()))
            self.priority()

    def Looop(self):
        if self.checkbox.isChecked() == True:
            self.spinBox3.setEnabled(True)
            self.dspinbox2.setEnabled(True)
        else:
            self.spinBox3.setEnabled(False)
            self.dspinbox2.setEnabled(False)

    def SampleSecond(self):
        fchat = open('config.bruh', 'rb+')
        fchat.seek(216)
        secOrSam = fchat.read(1)
        fchat.seek(216)
        if secOrSam == b'\x00':
            fchat.write((1).to_bytes(1))
            self.sustime = b'\x01'
            self.dspinbox.show()
            self.dspinbox2.show()
            self.spinBox.hide()
            self.spinBox3.hide()
            self.dspinbox2.setValue(self.spinBox3.value()/int(self.sampleRate.currentText()))
            self.dspinbox.setValue(self.spinBox.value()/int(self.sampleRate.currentText()))
        else:
            fchat.write((0).to_bytes(1))
            self.sustime = b'\x00'
            self.spinBox.show()
            self.spinBox3.show()
            self.dspinbox.hide()
            self.dspinbox2.hide()
            self.spinBox3.setValue(int(self.dspinbox2.value()*int(self.sampleRate.currentText())))
            self.spinBox.setValue(int(self.dspinbox.value()*int(self.sampleRate.currentText())))
        fchat.close()

    def samRate(self):
        fchat = open('config.bruh', 'rb+')
        fchat.seek(217)
        fchat.write((self.sampleRate.currentIndex()).to_bytes())
        fchat.close()

    def priority(self):
        fchat = open('config.bruh', 'rb+')
        fchat.seek(218)
        if self.fileOrd == b'\x01':
            fchat.write((1).to_bytes())
            self.fileType1 = 'SoH Audio Sample (*)'
            self.fileType2 = 'vadpcm.bin (*.vadpcm.bin)'
        else:
            fchat.write((0).to_bytes())
            self.fileType1 = 'vadpcm.bin (*.vadpcm.bin)'
            self.fileType2 = 'SoH Audio Sample (*)'
        fchat.close()

    def Convert(self):
        fneme = QFileDialog.getSaveFileName(self, 'Save as SoH audio Sample', '', 'SoH audio Sample (*)')
        if fneme[0]:
            fyle = open(fneme[0], 'wb+')
            if self.SampleOpen == True:
                fyle.write(self.dataa)
                fyle.seek(68)
                longth = int.from_bytes(fyle.read(4), byteorder='little')
                fyle.seek(longth+72)
                if self.sustime == b'\x00':
                    fyle.write(self.spinBox3.value().to_bytes(4, byteorder='little'))
                else: fyle.write(int(self.dspinbox2.value()*int(self.sampleRate.currentText())).to_bytes(4, byteorder='little'))
                if self.sustime == b'\x00':
                    fyle.write(self.spinBox.value().to_bytes(4, byteorder='little'))
                else: fyle.write(int(self.dspinbox.value()*int(self.sampleRate.currentText())).to_bytes(4, byteorder='little'))
                soup = int(self.checkbox.isChecked())
                fyle.write(int(soup).to_bytes(2, byteorder='little'))
                fyle.write(b'\x00\x00')
                fyle.close()
            else:
                fyle.write(self.audioSampledefault)
                fyle.seek(68)
                fyle.write(len(self.dataa).to_bytes(4, byteorder='little'))
                fyle.write(self.dataa)
                if self.sustime == b'\x00':
                    fyle.write(self.spinBox3.value().to_bytes(4, byteorder='little'))
                else: fyle.write(int(self.dspinbox2.value()*int(self.sampleRate.currentText())).to_bytes(4, byteorder='little'))
                if self.sustime == b'\x00':
                    fyle.write(self.spinBox.value().to_bytes(4, byteorder='little'))
                else: fyle.write(int(self.dspinbox.value()*int(self.sampleRate.currentText())).to_bytes(4, byteorder='little'))
                soup = int(self.checkbox.isChecked())
                fyle.write(int(soup).to_bytes(2, byteorder='little'))
                fyle.write(b'\x00\x00')
                fyle.write(self.audioSampledefault2)
                fyle.close()

if __name__ == '__main__':
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()