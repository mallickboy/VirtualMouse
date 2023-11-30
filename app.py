from PyQt5.QtWidgets import QMainWindow,QApplication,QMessageBox
from PyQt5 import QtCore, uic
from PyQt5.Qt import QDesktopServices
from assets.staticIncludes.mouse import controlVM as ctl

class MyGui(QMainWindow):
    def __init__(self):
        super(MyGui,self).__init__()
        uic.loadUi("./assets/windowForms/ui.ui",self)
        self.setFixedSize(520, 600)
        self.show()
        self.pushButton_start.setStyleSheet('background-color: rgba(63, 195, 128,0.8)')
        self.pushButton_start.clicked.connect(self.start)
        self.pushButton_stop.clicked.connect(self.stop)
        self.pushButton_update.clicked.connect(self.update)
        self.plainTextEdit_msg.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.actionClose.triggered.connect(self.close) # triggering the built in close event
        self.actionHelp.triggered.connect(lambda:(self.update_msg_box("Please visit :  https://github.com/mallickboy?tab=repositories ") ,
                                                  QDesktopServices.openUrl(QtCore.QUrl("https://github.com/mallickboy?tab=repositories")))) 
        self.msg=""
        self.line=0
        self.control_map=["Click","Scroll Down","Scroll Up","Right Click","Change Tab","Change Window","Minimize All","Lock Window","Exit Window","Print Window","File Manager","Virtual Keyboard","Press Enter","Game1","Game2","Game3","Game4"]
    def update_msg_box(self,msg):
        print(msg)
        self.line+=1
        self.msg=self.msg+f"\n{self.line} : {msg} "
        self.plainTextEdit_msg.setPlainText(self.msg)
        self.plainTextEdit_msg.verticalScrollBar().setValue(self.plainTextEdit_msg.verticalScrollBar().maximum())
    def start(self):
        self.update_msg_box("Startting the Virtual Mouse")
        self.pushButton_update.setStyleSheet('background-color: rgba(0, 181, 204,1)')
        self.pushButton_stop.setStyleSheet('background-color: rgba(254, 121, 104,1)')
        self.pushButton_update.setEnabled(True)
        self.pushButton_stop.setEnabled(True)
        self.pushButton_start.setEnabled(False)
        self.pushButton_start.setStyleSheet('background-color: rgba(0, 0, 0,0.1)')
        # start()
        self.get_controls()
        self.update_msg_box(ctl.start())
    def get_controls(self):
        def match(item):
            i=0
            for element in self.control_map:
                print(element, "i= ",i)
                if element==item:break
                else:i+=1
            if i==len(self.control_map):i=0 # not found select click
            return i
        
        selected_ctl=[self.comboBox_a1.currentText(), #1st
                      self.comboBox_a4.currentText(), #4th
                      self.comboBox_a3.currentText(),#3rd
                      self.comboBox_a2.currentText()#2nd
                      ]
        selected_sensi=[int(self.comboBox_dpi1.currentText()),
                      int(self.comboBox_dpi2.currentText()),
                      int(self.comboBox_dpi3.currentText()),
                      int(self.comboBox_dpi4.currentText())
                      ]
        selected_ctl_array=[]
        for select in selected_ctl:
            selected_ctl_array.append(match(select))
        self.update_msg_box(f"Controls : {selected_ctl}")
        ctl.update(selected_ctl_array,selected_sensi) # updating backend array
        return selected_ctl    
    def update(self):
        self.get_controls()
        self.update_msg_box("Updating the Virtual Mouse configurations")
    def stop(self):
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
    def closeEvent(self,event): # fixed defined class for close event
        # Ending all process before closing the window
        print("Ending all threads before closing the window")
        self.update_msg_box(ctl.stop())
        try:event.accept()  # Close the window
        except:0

def main():
    app=QApplication([])
    window=MyGui()
    app.exec_()

if __name__=='__main__':
    main()