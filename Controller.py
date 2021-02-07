import json

from Kiwoom import Kiwoom



class Controller:

    def __init__(self, client, message, **kwargs):
        super().__init__()
        self.k = json.loads(message)
        self.request = {"client": client, "func": self.k["func"], "param": self.k["param"]}
        print(f'get message type[{type(self.request)}] : {json.dumps(self.request, indent=4)} from client - [{self.request["client"]}]')
        self.conn = Kiwoom.instance()

    def getAcoNo(self):
        """
        ocx에서 계좌 가져오는 메소드 호출
        :return: str(account_num)
        """
        # 함수 매핑 데코레이터 만들어서 사용할 예정
        # 아직 none used
        account_num = self.conn.getLoginInfo("ACCNO")
        return str(account_num.rstrip(';'))

    def get_data_from_kw(self):

        if str(self.request["func"][0]) == 'getaccno':
            return self.conn.getLoginInfo("ACCNO").rstrip(';')
            """
            아래는 실행 안되는 코드
            """
        elif str(self.request["func"]) == 'getrdata':
            print(f'##[{self.request["message"]}]## get Real data, param is {[x for x in self.request["param"]]}')
            return self.conn.getRData([x for x in self.request["param"]])
        else:
            return ""
