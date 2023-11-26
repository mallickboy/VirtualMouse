import typing
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QWidget
from mouse import controlVM as ctl

class MyGui(QMainWindow):
    def __init__(self):
        super(MyGui,self).__init__()
        uic.loadUi("./assets/ui.ui",self)
        self.setFixedSize(520, 600)
        self.show()
        self.pushButton_start.setStyleSheet('background-color: rgba(63, 195, 128,0.8)')
        self.pushButton_start.clicked.connect(self.start)
        self.pushButton_stop.clicked.connect(self.stop)
        self.pushButton_update.clicked.connect(self.update)
        self.plainTextEdit_msg.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.msg=""
        self.line=0

    def update_msg_box(self,msg):
        print(msg)
        self.line+=1
        self.msg=self.msg+f"\n{self.line} : {msg} "
        self.plainTextEdit_msg.setPlainText(self.msg)
        self.plainTextEdit_msg.verticalScrollBar().setValue(self.plainTextEdit_msg.verticalScrollBar().maximum())
    def start(self):
        # self.line+=1
        # self.msg=self.msg+f"\n{self.line} : Startting the Virtual Mouse"
        # print("start")
        # self.plainTextEdit_msg.setPlainText(self.msg)
        # self.plainTextEdit_msg.verticalScrollBar().setValue(self.plainTextEdit_msg.verticalScrollBar().maximum())
        self.update_msg_box("Startting the Virtual Mouse")
        self.pushButton_update.setStyleSheet('background-color: rgba(0, 181, 204,1)')
        self.pushButton_stop.setStyleSheet('background-color: rgba(254, 121, 104,1)')
        self.pushButton_update.setEnabled(True)
        self.pushButton_stop.setEnabled(True)
        self.pushButton_start.setEnabled(False)
        self.pushButton_start.setStyleSheet('background-color: rgba(0, 0, 0,0.1)')
        # start()
        self.update_msg_box(ctl.start())
    def update(self):
        # self.line+=1
        # self.msg=self.msg+f"\n{self.line} : Updating the Virtual Mouse configurations"
        # print("update")
        # self.plainTextEdit_msg.setPlainText(self.msg)
        # self.plainTextEdit_msg.verticalScrollBar().setValue(self.plainTextEdit_msg.verticalScrollBar().maximum())
        self.update_msg_box("Updating the Virtual Mouse configurations")
    def stop(self):
        # self.line+=1
        # self.msg=self.msg+f"\n{self.line} : Stoping the Virtual Mouse"
        # print("stop")
        # self.plainTextEdit_msg.setPlainText(self.msg)
        # self.plainTextEdit_msg.verticalScrollBar().setValue(self.plainTextEdit_msg.verticalScrollBar().maximum())
        self.update_msg_box("Stoping the Virtual Mouse")
        self.pushButton_update.setStyleSheet('background-color: rgba(0,0,0,0.1)')
        self.pushButton_stop.setStyleSheet('background-color: rgba(0,0,0,0.1)')
        self.pushButton_start.setStyleSheet('background-color: rgba(63, 195, 128,0.8)')
        self.pushButton_start.setEnabled(True)
        self.pushButton_update.setEnabled(False)
        self.pushButton_stop.setEnabled(False)
        self.update_msg_box(ctl.stop())
        
    def login(self):
        print("Button clicked")
        if self.lineEdit.text()=="Tamal" and self.lineEdit_2.text()=="113344" :
            self.textEdit.setEnabled(True)
            self.pushButton_2.setEnabled(True)
        else:
            message=QMessageBox()
            message.setText("Invalid Login")
            message.exec_()
            self.textEdit.setEnabled(False)
            self.pushButton_2.setEnabled(False)
    def messageSection(self,msg):
        message=QMessageBox()
        message.setText(msg)
        message.exec_()


def main():
    app=QApplication([])
    window=MyGui()
    app.exec_()

if __name__=='__main__':
    main()