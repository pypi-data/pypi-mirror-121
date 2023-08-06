from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QApplication, QButtonGroup, QWidget, QLineEdit, QGraphicsDropShadowEffect
import sys
from qtawesome import icon
from swqt import ShockwaveWidget, InputLineEdit, FuncButton, ElementGroup, FuncWidget


class MyWindow(QWidget):
    def __init__(self, size: QRect, parent=None):
        super(MyWindow, self).__init__(parent)
        self.resize(400, 300)

        # 添加原生QWidget
        self.widget = QWidget(self)  # 注意QWidget(self) 内的self!!
        self.widget.setGeometry(10, 10, 380, 250)
        self.widget.setStyleSheet("background-color:grey;")

        # 添加编辑框（QLineEdit）
        self.lineEdit = QLineEdit("0", self)  # 注意QLineEdit("0",self) 内的self!!
        self.lineEdit.setGeometry(10, 270, 380, 20)


class Main(FuncWidget):
    def __init__(self, size):
        super(Main, self).__init__(size)

        # self.setGeometry(size)

        self.g_btn = ElementGroup(self)

        self.a = FuncButton(self.g_btn, icon('fa.times', color='azure'), 'a', self)
        self.b = FuncButton(self.g_btn, icon('fa.times', color='azure'), 'b', self)
        self.c = FuncButton(self.g_btn, icon('fa.times', color='azure'), 'C', self)
        self.d = FuncButton(self.g_btn, icon('fa.times', color='azure'), 'D', self)

        self.effect_shadow = QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(0, 0)  # 偏移
        self.effect_shadow.setBlurRadius(20)  # 阴影半径
        self.effect_shadow.setColor(Qt.gray)  # 阴影颜色
        self.l_bg.setGraphicsEffect(self.effect_shadow)

        self.wa = QWidget(self)
        self.wb = QWidget(self)
        self.wc = QWidget(self)
        self.wd = QWidget(self)

        self.g_btn.addElements([self.a, self.b, self.c, self.d])

        self.a.set_widget(self.wa)
        self.b.set_widget(self.wb)
        self.c.set_widget(self.wc)
        self.d.set_widget(self.wd)

        self.a.setGeometry(0, 0, 50, 50)
        self.b.setGeometry(0, 50, 50, 50)
        self.c.setGeometry(0, 100, 50, 50)
        self.d.setGeometry(0, 150, 50, 50)

        self.wa.setGeometry(50, 0, 100, 100)
        self.wb.setGeometry(50, 0, 100, 100)
        self.wc.setGeometry(50, 0, 100, 100)
        self.wd.setGeometry(50, 0, 100, 100)


app = QApplication(sys.argv)
m = Main(app.desktop().screenGeometry())
m.show()
sys.exit(app.exec_())
