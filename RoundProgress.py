import sys
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget

class Progress(QWidget):

    def __init__(self):
        super(Progress, self).__init__()
        self.persent = 0
        self.my_thread = MyThread()
        self.my_thread.my_signal.connect(self.progressUpdate)
        self.my_thread.start()

    def progressUpdate(self, p):
        self.persent = p

    def paintEvent(self, event):
        rotateAngle = 360 * self.persent / 100
        # 启用反锯齿, 平移坐标轴中心, 等比例缩放
        painter = QPainter(self)  # 6
        painter.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.TextAntialiasing)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QBrush(QColor("#5F89FF")))
        painter.drawEllipse(3, 3, 100, 100)
        painter.setBrush(QBrush(QColor("#e3ebff")))
        painter.drawEllipse(5, 5, 96, 96)
        gradient = QConicalGradient(50, 50, 91)  # 3
        gradient.setColorAt(0, QColor("#95BBFF"))
        gradient.setColorAt(1, QColor("#5C86FF"))
        self.pen = QPen()
        self.pen.setBrush(gradient)
        self.pen.setWidth(8)
        self.pen.setCapStyle(Qt.RoundCap)
        painter.setPen(self.pen)
        painter.drawArc(QtCore.QRectF(4, 4, 98, 98), (90 - 0) * 16, -rotateAngle * 16)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        painter.setFont(font)
        painter.setPen(QColor("#5481FF"))
        painter.drawText(QtCore.QRectF(4, 4, 98, 98), Qt.AlignCenter, "%d%%" % self.persent)
        self.update()

class MyThread(QThread):
    my_signal = pyqtSignal(int)
    p = 0
    def __init__(self):
        super(MyThread, self).__init__()

    def run(self):
        while True:
            self.my_signal.emit(self.p)
            self.msleep(1500)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    progress = Progress()
    progress.show()
    sys.exit(app.exec_())