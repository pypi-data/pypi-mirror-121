from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel, QAction, QButtonGroup
from PyQt5.QtCore import QThread, Qt, QPropertyAnimation, pyqtProperty, QPoint, QRect
from PyQt5.QtGui import QColor, QIcon, QPalette
from qtawesome import icon
import cgitb
from utils import *

cgitb.enable(format='text')


# TODO: ͸����ť��
# TODO�� ����Ӧ��ȫ��ק������Сһ���ֱ��ʵȼ�,windows������Ӧ
# TODO�� Introҳ��������ʽ������
# windowsͳһ���嶼��alt+space+X�Ŀ��Ʒ�ʽ
# ��С���䲻����������
# ĳ���¼������˰�ť��resize
# TODO: ��ӰЧ��

class CloseButton(QPushButton):
    def __init__(self, ico=None, text='', p=None):
        super(CloseButton, self).__init__(ico, text, p)

        self.setStyleSheet('''background:transparent;border: 0 solid;width:40px;height:40px''')
        self._color = QColor()

        self.ani_enter = QPropertyAnimation(self, b'color')
        self.ani_enter.setDuration(150)
        self.ani_enter.setStartValue(QColor(255, 255, 255, 0))
        self.ani_enter.setEndValue(QColor(255, 69, 0, 255))

        self.ani_leave = QPropertyAnimation(self, b'color')
        self.ani_leave.setDuration(150)
        self.ani_leave.setStartValue(QColor(255, 69, 0, 255))
        self.ani_leave.setEndValue(QColor(255, 255, 255, 0))

    def get_color(self):
        return self._color

    def set_color(self, col):
        self._color = col
        self.setStyleSheet('''QPushButton{background: rgba(%s, %s, %s, %s); border: 0px solid;}''' % (
            col.red(), col.green(), col.blue(), col.alpha()))

    color = pyqtProperty(QColor, fget=get_color, fset=set_color)

    def enterEvent(self, *args, **kwargs):
        self.ani_enter.start()

    def leaveEvent(self, *args, **kwargs):
        self.ani_leave.start()

    def mousePressEvent(self, *args, **kwargs):
        super(CloseButton, self).mousePressEvent(*args, **kwargs)
        self.setStyleSheet('''background:mediumvioletred;border: 0 solid''')

    def mouseReleaseEvent(self, *args, **kwargs):
        super(CloseButton, self).mouseReleaseEvent(*args, **kwargs)
        self.setStyleSheet('''background:orangered;border: 0 solid''')


class OtherButton(QPushButton):
    def __init__(self, ico=None, text='', p=None):
        super(OtherButton, self).__init__(ico, text, p)

        self.setStyleSheet('''background:transparent;border: 0 solid;width:40px;height:40px''')
        self._color = QColor()

        self.ani_enter = QPropertyAnimation(self, b'color')
        self.ani_enter.setDuration(150)
        self.ani_enter.setStartValue(QColor(255, 255, 255, 0))
        self.ani_enter.setEndValue(QColor(245, 245, 220, 135))

        self.ani_leave = QPropertyAnimation(self, b'color')
        self.ani_leave.setDuration(150)
        self.ani_leave.setStartValue(QColor(245, 245, 220, 135))
        self.ani_leave.setEndValue(QColor(255, 255, 255, 0))

    def get_color(self):
        return self._color

    def set_color(self, col):
        self._color = col
        self.setStyleSheet('''QPushButton{background: rgba(%s, %s, %s, %s); border: 0px solid;}''' % (
            col.red(), col.green(), col.blue(), col.alpha()))

    color = pyqtProperty(QColor, fget=get_color, fset=set_color)

    def showEvent(self, e):
        e.accept()
        self.resize(40, 40)

    def hideEvent(self, e):
        e.accept()
        self.repaint()

    def enterEvent(self, *args, **kwargs):
        self.ani_enter.start()

    def leaveEvent(self, *args, **kwargs):
        self.ani_leave.start()

    def mousePressEvent(self, *args, **kwargs):
        super(OtherButton, self).mousePressEvent(*args, **kwargs)
        self.setStyleSheet('''QPushButton{background-color: rgba(240, 255, 220, 195); border: 0px solid;}''')

    def mouseReleaseEvent(self, *args, **kwargs):
        super(OtherButton, self).mouseReleaseEvent(*args, **kwargs)
        self.setStyleSheet('''QPushButton{background-color: rgba(245, 245, 220, 135); border: 0px solid;}''')


class IntroWidget(QWidget):
    def __init__(self, parent=None):
        super(IntroWidget, self).__init__(parent)


class ShockwaveWidget(QWidget):
    def __init__(self, parent=None):
        super(ShockwaveWidget, self).__init__(parent)

        self.__startPos = None
        self.__endPos = None
        self.__isTracking = False

        self.l_bg = QLabel(self)

        self.btn_close = CloseButton(icon('fa.times', color='azure'), '', self)
        self.btn_mini = OtherButton(icon('fa.minus', color='azure'), '', self)
        self.btn_hint = OtherButton(icon('fa.chevron-down', color='azure'), '', self)

        self.__g_setting()
        self.__s_setting()
        self.__o_setting()

    def __g_setting(self):
        self.resize(500, 500)

        self.l_bg.setGeometry(0, 0, 500, 500)

    def __s_setting(self):
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.l_bg.setStyleSheet('''background:lightblue''')

    def __o_setting(self):
        self.btn_close.clicked.connect(self.close)
        # obj.btn_close.clicked.connect(lambda: systemtrayicon('shutdown -s -t 5'))
        self.btn_mini.clicked.connect(self.showMinimized)

    def geometry_setting(self):
        pass

    def style_setting(self):
        pass

    def other_setting(self):
        pass

    def closeEvent(self, e):
        self.btn_close.setStyleSheet('''background:transparent''')
        self.btn_close.repaint()
        e.accept()

    def resizeEvent(self, e):
        w = self.geometry().width()

        self.l_bg.resize(self.size())

        self.btn_close.move(w - 40, 0)
        self.btn_mini.move(w - 80, 0)
        self.btn_hint.move(w - 120, 0)

    def mouseMoveEvent(self, e):
        try:
            self.__endPos = e.pos() - self.__startPos
            self.move(self.pos() + self.__endPos)
        except TypeError:
            pass

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.__isTracking = True
            self.__startPos = QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.__isTracking = False
            self.__startPos = None
            self.__endPos = None


class FuncWidget(QWidget):
    def __init__(self, desktop_size: QRect, parent=None):
        super(FuncWidget, self).__init__(parent)

        self.desktop_size = desktop_size

        self.__startPos = None
        self.__endPos = None
        self.__isTracking = False

        self.l_bg = QLabel(self)

        self.btn_close = CloseButton(icon('fa.times', color='azure'), '', self)
        self.btn_mini = OtherButton(icon('fa.minus', color='azure'), '', self)
        self.btn_smaller = OtherButton(icon('fa5.minus-square', color='azure'), '', self)
        self.btn_max = OtherButton(icon('fa5.square', color='azure'), '', self)

        self.__g_setting()
        self.__s_setting()
        self.__o_setting()

    def __g_setting(self):
        self.setGeometry(self.desktop_size)

    def __s_setting(self):
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.l_bg.setStyleSheet('''background:lightblue''')

    def __o_setting(self):
        self.btn_max.hide()
        self.btn_max.clicked.connect(self.maximize)

        self.btn_smaller.clicked.connect(self.smaller)

        self.btn_close.clicked.connect(self.close)
        # obj.btn_close.clicked.connect(lambda: systemtrayicon('shutdown -s -t 5'))
        self.btn_mini.clicked.connect(self.minimize)

    def geometry_setting(self):
        pass

    def style_setting(self):
        pass

    def other_setting(self):
        pass

    def smaller(self):
        self.resize(500, 500)
        self.btn_smaller.hide()
        self.btn_max.show()

    def minimize(self):
        self.showMinimized()

    def maximize(self):
        self.btn_max.hide()
        self.btn_smaller.show()
        self.setGeometry(self.desktop_size)

    def closeEvent(self, e):
        self.btn_close.setStyleSheet('''background:transparent''')
        self.btn_close.repaint()
        e.accept()

    def moveEvent(self, e):
        if self.geometry() != self.desktop_size:
            self.resize(500, 500)
            self.btn_max.show()
            self.btn_smaller.hide()

    def resizeEvent(self, e):
        w = self.geometry().width()
        self.l_bg.resize(self.size())

        self.btn_close.move(w - 40, 0)
        self.btn_max.move(w - 80, 0)
        self.btn_smaller.move(w - 80, 0)
        self.btn_mini.move(w - 120, 0)

    def mouseMoveEvent(self, e):
        try:
            self.__endPos = e.pos() - self.__startPos
            self.move(self.pos() + self.__endPos)
        except TypeError:
            pass

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.__isTracking = True
            self.__startPos = QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.__isTracking = False
            self.__startPos = None
            self.__endPos = None
        if self.pos().y() < 0:
            self.maximize()


class InputLineEdit(QLineEdit):
    def __init__(self, parent=None, icon_name='', placeholder=''):
        super(InputLineEdit, self).__init__(parent)
        self.parent = parent
        self.cur = self.cursor()
        self.icon_name = icon_name

        self.setPlaceholderText(placeholder)

        self.action = QAction(self)
        self.action.setIcon(QIcon(icon('%s' % self.icon_name, color='silver')))
        self.addAction(self.action, QLineEdit.LeadingPosition)

        self.setStyleSheet('''
                            QLineEdit{
                                background: transparent;
                                border: 0 solid;
                                border-bottom: 1px solid silver;
                                font-weight:bold;
                                font-family: arial, serif;
                                font-size:18px;
                                color:silver;} 
                            QLineEdit:hover {
                                background: transparent;
                                border: 0 solid;
                                border-bottom: 2px solid silver;
                                font-weight:bold;
                                font-family: arial, serif;
                                font-size:18px;}''')

        self.setFocusPolicy(Qt.ClickFocus)

    def focusInEvent(self, e):
        super(InputLineEdit, self).focusInEvent(e)
        try:
            if self.parent.lw_login_record.current_state():
                lw_login_reverse(self.parent, 'hide')
        except:
            pass
        self.actions()[0].setIcon(QIcon(icon('%s' % self.icon_name, color='skyblue')))
        self.setStyleSheet('''
                            QLineEdit{
                                background: transparent;
                                border: 0 solid;
                                border-bottom: 1px solid skyblue;
                                font-weight:bold;
                                font-family: arial, serif;
                                font-size:18px;}
                            ''')
        self.repaint()

    def focusOutEvent(self, e):
        inside_parent = self.parent.geometry().contains(self.cur.pos())
        if inside_parent:
            super(InputLineEdit, self).focusOutEvent(e)
            self.actions()[0].setIcon(QIcon(icon('%s' % self.icon_name, color='gray')))
            self.setStyleSheet('''
                                        QLineEdit{
                                            background: transparent;
                                            border: 0 solid;
                                            border-bottom: 1px solid silver;
                                            font-weight:bold;
                                            font-family: arial, serif;
                                            font-size:18px;
                                            color:silver;} 
                                        QLineEdit:hover {
                                            background: transparent;
                                            border: 0 solid;
                                            border-bottom: 2px solid silver;
                                            font-weight:bold;
                                            font-family: arial, serif;
                                            font-size:18px;}''')
            self.repaint()


class ElementGroup:
    def __init__(self, p=None):
        self.list_ele = list()

        self.__id_current_ele = 0
        self.num_ele = 0
        self.id_max_ele = 0

    # TODO: ֻ�ܼ�һ��
    # TODO: ֻ�ܼ�FuncButton

    def get_current_id(self):
        return self.__id_current_ele

    def set_current_id(self, new_id):
        self.__id_current_ele = new_id

    def addElement(self, ele):
        self.id_max_ele += 1
        self.num_ele += 1
        ele.setWhatsThis(str(self.id_max_ele))
        self.list_ele.append(ele)

    def addElements(self, list_ele: list):
        for btn in list_ele:
            self.addElement(btn)

    # TODO: �ڴ���


class FuncButton(QPushButton):
    def __init__(self, group: ElementGroup, ico=None, text='', p=None):
        super(FuncButton, self).__init__(ico, text, p)

        self.parent = p
        self.group = group
        self.is_checked = False

        self.widget = None

        self.setStyleSheet('''background:transparent;border: 0 solid;width:40px;height:40px''')
        self._color = QColor()

        self.ani_enter = QPropertyAnimation(self, b'color')
        self.ani_enter.setDuration(150)
        self.ani_enter.setStartValue(QColor(255, 255, 255, 0))
        self.ani_enter.setEndValue(QColor(245, 245, 220, 135))

        self.ani_leave = QPropertyAnimation(self, b'color')
        self.ani_leave.setDuration(150)
        self.ani_leave.setStartValue(QColor(245, 245, 220, 135))
        self.ani_leave.setEndValue(QColor(255, 255, 255, 0))

        self.clicked.connect(self.group_effect)

    def get_color(self):
        return self._color

    def set_color(self, col):
        self._color = col
        self.setStyleSheet('''QPushButton{background: rgba(%s, %s, %s, %s); border: 0px solid;}''' % (
            col.red(), col.green(), col.blue(), col.alpha()))

    color = pyqtProperty(QColor, fget=get_color, fset=set_color)

    def set_widget(self, widget):
        self.widget = widget

    def group_effect(self):
        if self.group.get_current_id():
            self.group.list_ele[self.group.get_current_id() - 1].uncheck()
        self.group.set_current_id(int(self.whatsThis()))
        self.group.list_ele[self.group.get_current_id() - 1].check()

    def check(self):
        self.is_checked = True
        self.widget.show()
        self.setStyleSheet('''background-color: rgba(240, 255, 220, 195); border: 0px solid''')

    def uncheck(self):
        self.is_checked = False
        self.widget.hide()
        self.setStyleSheet('''background: transparent; border: 0px solid''')

    def enterEvent(self, *args, **kwargs):
        if self.is_checked:
            return
        self.ani_enter.start()

    def leaveEvent(self, *args, **kwargs):
        if self.is_checked:
            return
        self.ani_leave.start()

    def mousePressEvent(self, *args, **kwargs):
        if self.is_checked:
            return
        super(FuncButton, self).mousePressEvent(*args, **kwargs)
        self.setStyleSheet('''QPushButton{background-color: rgba(240, 255, 220, 195); border: 0px solid;}''')

    def mouseReleaseEvent(self, *args, **kwargs):
        if self.is_checked:
            return
        super(FuncButton, self).mouseReleaseEvent(*args, **kwargs)
        self.setStyleSheet('''QPushButton{background-color: rgba(245, 245, 220, 135); border: 0px solid;}''')
