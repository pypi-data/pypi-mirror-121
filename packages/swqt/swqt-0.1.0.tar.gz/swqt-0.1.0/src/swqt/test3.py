from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MyWidget(QWidget):
    def __init__(self, parent=None):
        super(MyWidget,self).__init__(parent)
        self.btn = QPushButton('ssd', self)
        # self.setStyleSheet("background-color:red;")
        self.setPalette(QPalette(Qt.red)) # 这一句是辅助！着色，区分背景。这一句与self.setStyleSheet("background-color:red;")咋看一样，影响不一样
        self.setAutoFillBackground(True) #这一句是关键！！！自动填充背景
        self.setMinimumSize(100,100) # 这一句是辅助！！因为这个自定义的QWidget默认大小（sizeHint()）是0，看不到！ 不过主窗体使用了布局的话，此句可省略
        #self.setMaximumSize(500, 500)
        #self.setFixesSize(400,200)

        # 做一些别的事情......
        self.do_something()

    def do_something(self):
        pass


    # 如果需要的话，就覆写属性函数：sizeHint（默认尺寸）
    #def sizeHint(self):
    #    return QSize(400, 200)
    # 如果需要的话，就覆写属性函数：minimumSizeHint（最小尺寸）
    #def minimumSizeHint(self):
    #    return QSize(100, 100)




class MyWindow(QWidget):
    def __init__(self, parent=None):
        super(MyWindow,self).__init__(parent)
        self.resize(400,300)
        layout = QGridLayout()

        # 添加自定义部件（MyWidget）
        self.widget = MyWidget() # 这里可以不要self

        # 添加编辑框（QLineEdit）
        self.lineEdit = QLineEdit("0") # 这里可以不要self

        # 放入布局内
        layout.addWidget(self.widget,0,0)
        layout.addWidget(self.lineEdit,1,0)
        self.setLayout(layout)

        self.setWindowTitle("5、完美显示QWidget的派生类")

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show();
    sys.exit(app.exec_())