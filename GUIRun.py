import os
import sys
import time
import pymongo
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from GUI import Ui_Detect
from Detect import CheckFrames
from RoundProgress import Progress

if len(sys.argv) < 3:
    parameter1 = ""
    parameter2 = ""
else:
    parameter1 = sys.argv[1]
    parameter2 = sys.argv[2]

class CheckFramesGUI(QWidget, Ui_Detect):

    def __init__(self):
        super(CheckFramesGUI, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('./badcheck.png'))
        self.setWindowFlags(Qt.FramelessWindowHint)  # 去边框
        self.setAttribute(Qt.WA_TranslucentBackground) # 设置窗口背景透明
        self.center()
        self.groupBox.hide()
        self.toolButton_2.hide()
        self.pushButton_2.hide()
        self.pushButton_4.hide()

        self.stackedWidget.setCurrentIndex(0)

        self.stack = QStackedWidget()
        self.stack.setStyleSheet("border: none;")
        self.stack.setMinimumSize(QtCore.QSize(110, 110))
        self.stack.setMaximumSize(QtCore.QSize(110, 110))
        self.paint = Progress()
        self.stack.addWidget(self.paint)
        self.horizontalLayout.addWidget(self.stack)

        self.pushButton.clicked.connect(self.buttonclick)
        self.pushButton_1.clicked.connect(self.buttonclick1)
        self.pushButton_2.clicked.connect(self.buttonclick2)
        self.pushButton_3.clicked.connect(self.buttonclick3)
        self.pushButton_4.clicked.connect(self.buttonclick4)
        self.pushButton_5.clicked.connect(self.buttonclick)
        self.toolButton.clicked.connect(self.showDialog)
        self.minButton.clicked.connect(self.ShowMininizedWindow)
        self.maxButton.clicked.connect(self.ShowRestoreWindow)
        self.closeButton.clicked.connect(self.CloseWindow)
        self.setAcceptDrops(True)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def dragEnterEvent(self, event):
        self.toolButton.hide()
        self.toolButton_2.show()
    #    self.toolButton.setStyleSheet("color: #5481FF;background: #EDF2FF;border: 1px solid #5481FF;border-radius: 4px;padding-top: 159px;padding-bottom:154px;")
        self.skinButton.setStyleSheet("image: url(:/icons/15.svg);")
        self.minButton.setStyleSheet("image: url(:/icons/19.svg);")
        self.maxButton.setStyleSheet("image: url(:/icons/17.svg);")
        self.closeButton.setStyleSheet("image: url(:/icons/11.svg);")
        event.accept()

    def dragLeaveEvent(self, event):
        self.toolButton.show()
        self.toolButton_2.hide()
    #    self.toolButton.setStyleSheet("#toolButton{border: 1px solid #D4D4D4;border-radius: 4px;background-color: rgb(250, 250, 250);color: #8D9EA7;padding-top: 159px;padding-bottom:154px;}"
    #                                  "#toolButton:hover{color: #5481FF;background: #EDF2FF;border: 1px solid #5481FF;border-radius: 4px;padding-top: 159px;padding-bottom:154px;}")
        self.skinButton.setStyleSheet("#skinButton{border-image: url(:/icons/14.svg)}#skinButton:hover{border-image: url(:/icons/15.svg)}")
        self.minButton.setStyleSheet("#minButton{border-image: url(:/icons/18.svg)}#minButton:hover{border-image: url(:/icons/19.svg)}")
        self.maxButton.setStyleSheet("#maxButton{border-image: url(:/icons/16.svg)}#maxButton:hover{border-image: url(:/icons/17.svg)}")
        self.closeButton.setStyleSheet("#closeButton{border-image: url(:/icons/10.svg)}#closeButton:hover{border-image: url(:/icons/11.svg)}")

    def dropEvent(self, event):
        self.toolButton.show()
        self.toolButton_2.hide()
    #    self.toolButton.setStyleSheet(
    #        "#toolButton{border: 1px solid #D4D4D4;border-radius: 4px;background-color: rgb(250, 250, 250);color: #8D9EA7;padding-top: 159px;padding-bottom:154px;}"
    #        "#toolButton:hover{color: #5481FF;background: #EDF2FF;border: 1px solid #5481FF;border-radius: 4px;padding-top: 159px;padding-bottom:154px;}")
        self.skinButton.setStyleSheet("#skinButton{border-image: url(:/icons/14.svg)}#skinButton:hover{border-image: url(:/icons/15.svg)}")
        self.minButton.setStyleSheet("#minButton{border-image: url(:/icons/18.svg)}#minButton:hover{border-image: url(:/icons/19.svg)}")
        self.maxButton.setStyleSheet("#maxButton{border-image: url(:/icons/16.svg)}#maxButton:hover{border-image: url(:/icons/17.svg)}")
        self.closeButton.setStyleSheet("#closeButton{border-image: url(:/icons/10.svg)}#closeButton:hover{border-image: url(:/icons/11.svg)}")
        path = (event.mimeData().urls())[0].toLocalFile()
        detect = CheckFrames()
        try:
            if path.split('.')[-1] == 'exr':
                path = os.path.dirname(path)
                Lost, Bad, Data, totalText, lostframenum, badframenum, totalnormalText = detect.Singlepath(path)
            elif os.listdir(path)[-1].split('.')[-1] == ('exr' or 'db'):
                Lost, Bad, Data, totalText, lostframenum, badframenum, totalnormalText = detect.Singlepath(path)
            else:
                Lost, Bad, Data, totalText, lostframenum, badframenum, totalnormalText = detect.Multipath(path)

            if Lost == "<p style = 'margin: 5px'>    暂未发现异常帧\n" and Bad == "<p style = 'margin: 5px'>    暂未发现异常帧\n":
                self.stackedWidget.setCurrentIndex(1)
                self.timer = QTimer()
                self.timer.start(1500)
                self.timer.timeout.connect(self.progressRuntime1)

                self.label_16.setText("检测的" + totalnormalText + "帧中，暂未发现异常帧")
                Data.update({"工号": parameter1})
                Data.update({"检测人": parameter2})
                myclient = pymongo.MongoClient('mongodb://localhost:27017/')
                mydb = myclient['framecheck']
                mydb['detail'].insert_one(Data)
            elif Lost == "文件路径中有中文名称，请检查重新上传":
                self.groupBox.show()
                self.stackedWidget.setCurrentIndex(0)

                self.label_17.setText(Lost)
                Data.update({"工号": parameter1})
                Data.update({"检测人": parameter2})
                myclient = pymongo.MongoClient('mongodb://localhost:27017/')
                mydb = myclient['framecheck']
                mydb['detail'].insert_one(Data)
                self.timer = QTimer()
                self.timer.start(3000)
                self.timer.timeout.connect(self.runtime)
            else:
                self.pushButton_1.show()
                self.pushButton_2.hide()
                self.groupBox_9.show()
                self.pushButton_3.show()
                self.pushButton_4.hide()
                self.groupBox_10.show()
                self.stackedWidget.setCurrentIndex(1)
                self.timer = QTimer()
                self.timer.start(1500)
                self.timer.timeout.connect(self.progressRuntime2)

                self.label_8.setText(totalText)
                self.label_9.setText("检测路径：" + path.replace('/', '\\'))
                self.label_11.setText("缺帧（" + lostframenum + "帧）")
                self.label_12.setText(Lost)
                self.label_14.setText("坏帧（" + badframenum + "帧）")
                self.label_15.setText(Bad)
                Data.update({"工号": parameter1})
                Data.update({"检测人": parameter2})
                myclient = pymongo.MongoClient('mongodb://localhost:27017/')
                mydb = myclient['framecheck']
                mydb['detail'].insert_one(Data)
        except NotADirectoryError:
            Text = "不要拖入除exr文件类型以外的文件，请检查重新上传"
            Time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            Data = {"工号": "", "检测人": "", "检测时间": Time, "检测路径": path, "检测失败": "不要拖入除exr文件类型以外的文件，请检查重新上传！"}
            self.groupBox.show()
            self.stackedWidget.setCurrentIndex(0)
            self.timer = QTimer()
            self.timer.start(3000)
            self.timer.timeout.connect(self.runtime)

            self.label_17.setText(Text)
            Data.update({"工号": parameter1})
            Data.update({"检测人": parameter2})
            myclient = pymongo.MongoClient('mongodb://localhost:27017/')
            mydb = myclient['framecheck']
            mydb['detail'].insert_one(Data)
        except IndexError:
            Text = "文件夹为空"
            Time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            Data = {"工号": "", "检测人": "", "检测时间": Time, "检测路径": path, "检测失败": "文件夹为空！"}
            self.groupBox.show()
            self.stackedWidget.setCurrentIndex(0)
            self.timer = QTimer()
            self.timer.start(3000)
            self.timer.timeout.connect(self.runtime)

            self.label_17.setText(Text)
            Data.update({"工号": parameter1})
            Data.update({"检测人": parameter2})
            myclient = pymongo.MongoClient('mongodb://localhost:27017/')
            mydb = myclient['framecheck']
            mydb['detail'].insert_one(Data)

    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, '打开文件', 'C:/Users/huangzh/Desktop/Bad frame')
        if fname[0]:
            path = os.path.dirname(fname[0])
            detect = CheckFrames()
            Lost, Bad, Data, totalText, lostframenum, badframenum, totalnormalText = detect.Singlepath(path)
            if Lost == "<p style = 'margin: 5px'>    暂未发现异常帧\n" and Bad == "<p style = 'margin: 5px'>    暂未发现异常帧\n":
                self.stackedWidget.setCurrentIndex(1)
                self.timer = QTimer()
                self.timer.start(1500)
                self.timer.timeout.connect(self.progressRuntime1)

                self.label_16.setText("检测的" + totalnormalText + "帧中，暂未发现异常帧")
                Data.update({"工号": parameter1})
                Data.update({"检测人": parameter2})
                myclient = pymongo.MongoClient('mongodb://localhost:27017/')
                mydb = myclient['framecheck']
                mydb['detail'].insert_one(Data)
            elif Lost == "文件路径中有中文名称，请检查重新上传":
                self.groupBox.show()
                self.stackedWidget.setCurrentIndex(0)
                self.timer = QTimer()
                self.timer.start(3000)
                self.timer.timeout.connect(self.runtime)

                self.label_17.setText(Lost)
                Data.update({"工号": parameter1})
                Data.update({"检测人": parameter2})
                myclient = pymongo.MongoClient('mongodb://localhost:27017/')
                mydb = myclient['framecheck']
                mydb['detail'].insert_one(Data)
            else:
                self.pushButton_1.show()
                self.pushButton_2.hide()
                self.groupBox_9.show()
                self.pushButton_3.show()
                self.pushButton_4.hide()
                self.groupBox_10.show()
                self.stackedWidget.setCurrentIndex(1)
                self.timer = QTimer()
                self.timer.start(1500)
                self.timer.timeout.connect(self.progressRuntime2)

                self.label_8.setText(totalText)
                self.label_9.setText("检测路径：" + path.replace('/', '\\'))
                self.label_11.setText("缺帧（" + lostframenum + "帧）")
                self.label_12.setText('\n' + Lost)
                self.label_14.setText("坏帧（" + badframenum + "帧）")
                self.label_15.setText('\n' + Bad)
                Data.update({"工号": parameter1})
                Data.update({"检测人": parameter2})
                myclient = pymongo.MongoClient('mongodb://localhost:27017/')
                mydb = myclient['framecheck']
                mydb['detail'].insert_one(Data)

    def buttonclick(self):
        self.stackedWidget.setCurrentIndex(0)

    def buttonclick1(self):
        self.pushButton_1.hide()
        self.pushButton_2.show()
        self.groupBox_9.hide()

    def buttonclick2(self):
        self.pushButton_1.show()
        self.pushButton_2.hide()
        self.groupBox_9.show()

    def buttonclick3(self):
        self.pushButton_3.hide()
        self.pushButton_4.show()
        self.groupBox_10.hide()

    def buttonclick4(self):
        self.pushButton_3.show()
        self.pushButton_4.hide()
        self.groupBox_10.show()

    def runtime(self):
        self.timer.stop()
        self.groupBox.hide()

    def progressRuntime1(self):
        self.timer.stop()
        self.stackedWidget.setCurrentIndex(3)

    def progressRuntime2(self):
        self.timer.stop()
        self.stackedWidget.setCurrentIndex(2)

    def ShowMininizedWindow(self):
        self.showMinimized()

    def ShowMaximizedWindow(self):
        self.showMaximized()

    def ShowRestoreWindow(self):
        if self.isMaximized():
            self.showNormal()
            self.maxButton.setStyleSheet("#maxButton{border-image: url(:/icons/16.svg)}#maxButton:hover{border-image: url(:/icons/17.svg)}")
        else:
            self.showMaximized()
            self.maxButton.setStyleSheet("#maxButton{border-image: url(:/icons/12.svg)}#maxButton:hover{border-image: url(:/icons/13.svg)}")

    def CloseWindow(self):
        self.close()

    def mouseDoubleClickEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.ShowRestoreWindow()
            event.accept()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.isPressed = True
            self.startPos = event.globalPos() - self.pos()
            event.accept()

    def mouseReleaseEvent(self, event):
        self.isPressed = False

    def mouseMoveEvent(self, event):
        try:
            if self.isPressed:
                if self.isMaximized:
                    self.showNormal()
                    self.maxButton.setStyleSheet(
                        "#maxButton{border-image: url(:/icons/16.svg)}#maxButton:hover{border-image: url(:/icons/17.svg)}")
                self.move(event.globalPos() - self.startPos)
                event.accept()
        except:
            pass

if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    checkframes = CheckFramesGUI()
    checkframes.show()
    sys.exit(app.exec_())
