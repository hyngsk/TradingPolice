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
        # Change method name dynamicCall to call
        self.ocx.call = self.ocx.dynamicCall

        self.ocx.call("CommConnect()")

        # OpenAPI+ Event
        self.ocx.OnEventConnect.connect(self.on_event_connect)
        self.ocx.OnReceiveMsg.connect(self.on_receive_msg)
        self.ocx.OnReceiveTrData.connect(self.on_receive_tr_data)
        self.ocx.OnReceiveRealData.connect(self.on_receive_real_data)
        self.ocx.OnReceiveChejanData.connect(self.on_receive_chejan_data)
        self.ocx.OnReceiveConditionVer.connect(self.on_receive_condition_ver)
        self.ocx.OnReceiveTrCondition.connect(self.on_receive_tr_condition)
        self.ocx.OnReceiveRealCondition.connect(self.on_receive_real_condition)

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

    """
    Methods
    """
    def getAcoNo(self):
        """
        ocx에서 계좌 가져오는 메소드 호출
        :return: str(account_num)
        """
        account_num = self.ocx.call("GetLoginInfo(QString)", ["ACCNO"])
        return str(account_num.rstrip(';'))

    def getRData(self):
        return

    def commRqData(self, rq_name, tr_code, prev_next, scr_no):
        return self.ocx.call("CommRqData(QString, QString, Int, QString)", rq_name, tr_code, prev_next, scr_no)
    # ---methods end.
    
    """
    Event Handlers
    """
    def on_event_connect(self, err_code):
        """
        로그인 이벤트
        :param err_code:
        :return: None
        """
        if err_code == 0:
            self.logSignal("로그인 성공")


    def on_receive_msg(self, ):
        pass

    def on_receive_tr_data(self):
        pass

    def on_receive_real_data(self):
        pass

    def on_receive_chejan_data(self):
        pass

    def on_receive_condition_ver(self):
        pass

    def on_receive_tr_condition(self):
        pass

    def on_receive_real_condition(self):
        pass

    # ---events ends.

    @QtCore.pyqtSlot(str)
    def logSignal(self, status):
        """
        전역 서버 상태변수 변경시 로그창 입력
        :param status:
        :return: self.logTextArea.append(status)
        """
        print(status)
        return self.logTextArea.append(status)

    def __del__(self):
        self.__instance = None
