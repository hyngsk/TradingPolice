from PyQt5 import QtCore
from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtWidgets import QTextEdit, QMainWindow


class SingletonInstance(object):
    __instance = None

    @classmethod
    def __getInstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kwargs):
        cls.__instance = cls(*args, **kwargs)
        cls.instance = cls.__getInstance
        return cls.__instance


class Kiwoom(QMainWindow, SingletonInstance):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Kiwoom Login
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.dynamicCall("CommConnect()")

        # OpenAPI+ Event
        self.ocx.OnEventConnect.connect(self.event_connect)

        self.setWindowTitle("Gui-App")
        self.setGeometry(150, 150, 800, 600)

        # 필요없으면 삭제
        # btn1 = QPushButton("계좌 얻기", self)
        # btn1.move(190, 20)
        # btn1.clicked.connect(self.getAcoNo)

        self.logTextArea = QTextEdit(self)
        self.logTextArea.setGeometry(10, 10, 780, 580)
        # show gui
        self.show()

    def getAcoNo(self):
        """
        ocx에서 계좌 가져오는 메소드 호출
        :return: str(account_num)
        """
        account_num = self.ocx.dynamicCall("GetLoginInfo(QString)", ["ACCNO"])
        return str(account_num.rstrip(';'))

    def event_connect(self, err_code):
        """
        로그인 이벤트
        :param err_code:
        :return: None
        """
        if err_code == 0:
            self.logTextArea.append("로그인 성공")

    @QtCore.pyqtSlot(str)
    def on_status_changed(self, status):
        """
        전역 서버 상태변수 변경시 로그창 입력
        :param status:
        :return: self.logTextArea.append(status)
        """
        return self.logTextArea.append(status)

    def __del__(self):
        self.__instance = None

