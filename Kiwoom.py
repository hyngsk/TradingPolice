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

    # 4) GetLoginInfo
    def getLoginInfo(self, tag):
        """
        원형 : BSTR GetLoginInfo(BSTR sTag)
        설명 : 로그인한 사용자 정보를 반환한다.
        입력값 : BSTR sTag : 사용자 정보 구분 TAG값 (비고)
        반환값 : TAG값에 따른 데이터 반환
        비고 :
            BSTRsTag에 들어 갈 수 있는 값은 아래와 같음
            "ACCOUNT_CNT" – 전체 계좌 개수를 반환한다.
            "ACCNO" – 전체 계좌를 반환한다. 계좌별 구분은 ';'이다.
            "USER_ID" - 사용자 ID를 반환한다.
            "USER_NAME" – 사용자명을 반환한다.
            "KEY_BSECGB" – 키보드보안 해지여부. 0:정상, 1:해지
            "FIREW_SECGB" – 방화벽 설정 여부. 0:미설정, 1:설정, 2:해지
            Ex) openApi.GetLoginInfo("ACCOUNT_CNT");
        """
        return self.ocx.call("GetLoginInfo(QString)", tag)

    def commRqData(self, rq_name, tr_code, prev_next, scr_no):
        # return self.ocx.call("CommRqData(QString, QString, int, QString)", "opt10001_req", "opt10001", 0, "0101")
        self.logSignal(f'{rq_name}, {tr_code}, {prev_next}, {scr_no}')
        result = None
        """
        # RqName 데이터 타입을 배열로 받아 아래 commRqData로 받아온 값을 
        self.ocx.call("CommRqData(QString, QString, Int, QString)", str(rq_name), str(tr_code), int(prev_next), str(scr_no))
        # getCommData 로 요청 값들 배열에 저장 후 리턴
        result = self.getCommData(tr_code, rq_name, prev_next, scr_no)
        """

        return result

    def getCommData(self, tr_code, rq_name, index, item):
        data = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)",
                                    tr_code, rq_name, index, item)
        return data.strip()

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

    def on_receive_tr_data(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
        
        """
        구현중,,
        """
        print("리시브로 들어옴")
        if rqname == "opt10001_req":
            name = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode, recordname, 0, "종목명")
            volume = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode, recordname, 0, "거래량")
            numStocks = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode, recordname, 0,
                                                "상장주식")
            prices = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode, recordname, 0, "시가")
            self.text_edit.append("종목명:" + name.strip())
            self.text_edit.append("거래량:" + volume.strip())
            self.text_edit.append("상장주식:" + numStocks.strip())
            self.text_edit.append("시가:" + prices.strip())

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
