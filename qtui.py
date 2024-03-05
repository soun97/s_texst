import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType("MARKET_TIME.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.start_time_edit: QTimeEdit
        self.end_time_edit: QTimeEdit

        self.okButton: QPushButton
        self.okButton.clicked.connect(self.buttonClick)

    def buttonClick(self):
        print(self.start_time_edit.time())
        print(self.end_time_edit.time())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()