from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
from PyQt5.uic import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import subprocess
import sys
mainwindow,cal = loadUiType('ui.ui')
class MainWindow(cal,mainwindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setupUi(self)

        self.pushButton_2.clicked.connect(self.a)
        self.pushButton_4.clicked.connect(self.b)

    def a(self):
        subprocess.call('PCL.exe')
    def b(self):
        subprocess.call('HMCL.exe')
    def c(self):
        subprocess.call('MinecraftInstaller.msi')
    def d(self):
        subprocess.call('Java1.8.291install.exe')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainclass = MainWindow()
    mainclass.show()
    app.exec_()