from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from pynput.keyboard import Controller, KeyCode
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QDialog,QProgressBar, QPushButton)
from random import randint
import time
from datetime import datetime
import serial,wmi


def Press_Keyboard(hex_code):
    keyboard = Controller()
    keyboard.press(KeyCode.from_vk(hex_code))


def main(volume_level):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == "Spotify.exe":
                volume.SetMasterVolume(round((volume_level/1023),2), None)

def brightnessSetting(brightness):
    wmi.WMI(namespace='wmi').WmiMonitorBrightnessMethods()[0].WmiSetBrightness(brightness, 0) 


def mapValue(inVal,inmin,inmax,outmin,outmax):
    outVal = 0
    if(inVal < 0):outVal = 0
    elif(inVal > inmax):outVal = outmax
    else:outVal = round((outmax - outmin) / (inmax - inmin) * inVal)
    return outVal


def map_range(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min



port = serial.Serial("COM7", baudrate = 9600, timeout=1)
time.sleep(1.2)


class External(QThread):
    countChanged = pyqtSignal(str)
    def run(self):
        while True:
                data = "" 
                while(port.readable()):
                        veri = str(port.read(), 'utf-8')
                        if("x" == veri):pass
                        elif ("c" == veri):break
                        else:data = data + veri
                time.sleep(0.015)
                port.reset_input_buffer()
                self.countChanged.emit(data)




class Ui_Form(QDialog):
        def __init__(self):
                super().__init__()
                self.setupUi()
                self.ldr_Val = 1
                self.ptc_Val = 1
                self.pot_Val = 1
                self.but_Val = 1
                self.brigh_level = 0
                self.volume_level = 0
                self.nt1 = datetime.now()
                self.nt2 = datetime.now()

        def setupUi(self):

                self.resize(1104, 759)
                self.setStyleSheet("background-color: rgb(235, 235, 235);")

                self.shape_LDR = QtWidgets.QLabel(self)
                self.shape_LDR.setGeometry(QtCore.QRect(80, 100, 171, 171))
                self.shape_LDR.setStyleSheet("border-radius: 85px;\n""background-color: rgb(255, 255,255);\n""border: 3px solid black;")

                self.slider_LDR = QtWidgets.QSlider(self)
                self.slider_LDR.setGeometry(QtCore.QRect(40, 330, 271, 41))
                self.slider_LDR.setStyleSheet("background-color: rgb(195, 255, 178);")
                self.slider_LDR.setMaximum(100)
                self.slider_LDR.setOrientation(QtCore.Qt.Horizontal)

                self.text_LDR = QtWidgets.QLineEdit(self)
                self.text_LDR.setGeometry(QtCore.QRect(70, 430, 221, 61))
                font = QtGui.QFont()
                font.setPointSize(18)
                font.setBold(True)
                font.setWeight(75)
                self.text_LDR.setFont(font)
                self.text_LDR.setStyleSheet("background-color: rgb(184, 192, 196);")
                self.text_LDR.setAlignment(QtCore.Qt.AlignCenter)
                self.text_LDR.setReadOnly(True)

                self.name_1 = QtWidgets.QLabel(self)
                self.name_1.setGeometry(QtCore.QRect(60, 30, 211, 41))
                font = QtGui.QFont()
                font.setPointSize(20)
                font.setBold(True)
                font.setWeight(75)
                self.name_1.setFont(font)
                self.name_1.setLayoutDirection(QtCore.Qt.RightToLeft)
                self.name_1.setAlignment(QtCore.Qt.AlignCenter)

                self.but_LDR = QtWidgets.QPushButton(self)
                self.but_LDR.setGeometry(QtCore.QRect(80, 530, 201, 41))
                font = QtGui.QFont()
                font.setPointSize(14)
                font.setBold(True)
                font.setWeight(75)
                self.but_LDR.setFont(font)

                self.name_2 = QtWidgets.QLabel(self)
                self.name_2.setGeometry(QtCore.QRect(440, 30, 211, 41))
                font = QtGui.QFont()
                font.setPointSize(20)
                font.setBold(True)
                font.setWeight(75)
                self.name_2.setFont(font)
                self.name_2.setLayoutDirection(QtCore.Qt.RightToLeft)
                self.name_2.setAlignment(QtCore.Qt.AlignCenter)

                self.shape_PTC = QtWidgets.QLabel(self)
                self.shape_PTC.setGeometry(QtCore.QRect(460, 100, 171, 171))
                self.shape_PTC.setStyleSheet("border-radius: 85px;\n""background-color: rgb(255, 255,255);\n""border: 3px solid black;\n""border: 1px solid black;")

                self.butt_PTC = QtWidgets.QPushButton(self)
                self.butt_PTC.setGeometry(QtCore.QRect(460, 530, 201, 41))
                font = QtGui.QFont()
                font.setPointSize(14)
                font.setBold(True)
                font.setWeight(75)
                self.butt_PTC.setFont(font)

                self.text_PTC = QtWidgets.QLineEdit(self)
                self.text_PTC.setGeometry(QtCore.QRect(450, 430, 221, 61))
                font = QtGui.QFont()
                font.setPointSize(18)
                font.setBold(True)
                font.setWeight(75)
                self.text_PTC.setFont(font)
                self.text_PTC.setStyleSheet("background-color: rgb(184, 192, 196);")
                self.text_PTC.setAlignment(QtCore.Qt.AlignCenter)
                self.text_PTC.setReadOnly(True)

                self.slider_PTC = QtWidgets.QSlider(self)
                self.slider_PTC.setGeometry(QtCore.QRect(420, 330, 271, 41))
                self.slider_PTC.setStyleSheet("background-color: rgb(195, 255, 178);")
                self.slider_PTC.setMaximum(1023)
                self.slider_PTC.setOrientation(QtCore.Qt.Horizontal)


                self.but_POT = QtWidgets.QPushButton(self)
                self.but_POT.setGeometry(QtCore.QRect(830, 640, 201, 41))
                font = QtGui.QFont()
                font.setPointSize(14)
                font.setBold(True)
                font.setWeight(75)
                self.but_POT.setFont(font)

                self.text_POT = QtWidgets.QLineEdit(self)
                self.text_POT.setGeometry(QtCore.QRect(820, 560, 221, 61))
                font = QtGui.QFont()
                font.setPointSize(18)
                font.setBold(True)
                font.setWeight(75)
                self.text_POT.setFont(font)
                self.text_POT.setStyleSheet("background-color: rgb(184, 192, 196);")
                self.text_POT.setAlignment(QtCore.Qt.AlignCenter)
                self.text_POT.setReadOnly(True)

                self.name_3 = QtWidgets.QLabel(self)
                self.name_3.setGeometry(QtCore.QRect(800, 30, 211, 41))
                font = QtGui.QFont()
                font.setPointSize(20)
                font.setBold(True)
                font.setWeight(75)
                self.name_3.setFont(font)
                self.name_3.setLayoutDirection(QtCore.Qt.RightToLeft)
                self.name_3.setAlignment(QtCore.Qt.AlignCenter)

                self.slider_POT = QtWidgets.QSlider(self)
                self.slider_POT.setGeometry(QtCore.QRect(790, 490, 271, 41))
                self.slider_POT.setStyleSheet("background-color: rgb(195, 255, 178);")
                self.slider_POT.setMaximum(1023)
                self.slider_POT.setOrientation(QtCore.Qt.Horizontal)

                self.shape_3 = QtWidgets.QLabel(self)
                self.shape_3.setGeometry(QtCore.QRect(860, 100, 101, 101))
                self.shape_3.setStyleSheet("border-radius: 50px;\n""background-color: rgb(255, 255,255);\n""border: 3px solid black;")

                self.dial_POT = QtWidgets.QDial(self)
                self.dial_POT.setGeometry(QtCore.QRect(790, 240, 241, 201))
                self.dial_POT.setRange(0,1023)
                self.dial_POT.setNotchesVisible(True)

                self.calc = External()
                self.calc.countChanged.connect(self.serialData)
                self.calc.start()

                self.retranslateUi()
                self.show()   
                #QtCore.QMetaObject.connectSlotsByName(self)

                
        def retranslateUi(self):
                self.setWindowTitle("Controller")
                self.name_1.setText("LDR")
                self.but_LDR.setText("LDR")
                self.name_2.setText("PTC")
                self.butt_PTC.setText("PTC")
                self.but_POT.setText("POT")
                self.name_3.setText("POT")


        def serialData(self,val):
                #print(val)
                try:
                        text = val.split(".")
                        self.ldr_Val = int(text[0]) #mapValue(int(text[0]), 400, 1000, 0, 100)
                        self.ptc_Val = int(text[1])
                        self.pot_Val = int(text[2])
                        self.but_Val = text[3]
                        self.LDR_Func()
                        self.PTC_Func()
                        self.POT_Func()
                        self.BUT_Func()
                        self.nt2 = datetime.now()

                except: 
                       pass


        def LDR_Func(self):
                if(self.ldr_Val > 7):
                        self.text_LDR.setText("% " + str(self.ldr_Val))
                        self.slider_LDR.setValue(self.ldr_Val)
                        if(self.brigh_level > 12):
                                self.brigh_level = 0
                                brightnessSetting(self.ldr_Val)
                        self.brigh_level = self.brigh_level + 1
                        self.shape_LDR.setStyleSheet("border-radius: 85px;\n""background-color: rgb({}, {}, {});\n""border: 3px solid black;".format(int(self.ldr_Val*2.55),int(self.ldr_Val*2.55),int(self.ldr_Val*2.55)))

        def PTC_Func(self):
                self.text_PTC.setText(str(int(self.ptc_Val/4)) + " °C")
                self.slider_PTC.setValue(self.ptc_Val)
                self.shape_PTC.setStyleSheet("border-radius: 85px;\n""background-color: rgb({},0,0);\n""border: 1px solid black;".format(self.ptc_Val))
        
        def POT_Func(self):
                if(self.volume_level > 2):
                        self.volume_level = 0
                        main(self.pot_Val)

                self.volume_level = self.volume_level + 1
                self.text_POT.setText("% " +str(map_range(self.pot_Val,0,1025,0,100)))
                self.dial_POT.setValue(self.pot_Val)
                self.slider_POT.setValue(self.pot_Val)                

        def BUT_Func(self):
                diff_time = self.nt2 - self.nt1
                if(self.nt1 == 0 or (diff_time.microseconds)>100000):
                        self.nt1 = datetime.now()
                        if(self.but_Val == "s"):
                                Press_Keyboard(0xB3)
                        elif(self.but_Val == "f"):
                                Press_Keyboard(0xB0)
                        elif(self.but_Val == "b"):
                                Press_Keyboard(0xB1)

if __name__ == "__main__":
        import sys
        app = QApplication(sys.argv)
        window = Ui_Form()
        sys.exit(app.exec_())