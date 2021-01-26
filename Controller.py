import json

from Kiwoom import Kiwoom


class Controller:

    def __init__(self, client, message, **kwargs):
        super().__init__()

        self.k = json.loads(message)
        self.request = {"client": client, "message": self.k["message"], "param": self.k["param"]}
        print(
            f'get message type[{type(self.request)}] : {json.dumps(self.request, indent=4)} from client - [{self.request["client"]}]')

        self.conn = Kiwoom.instance()

    def getDataFromKW(self):

        if str(self.request["message"]) == 'getaccno':
            return self.conn.getAcoNo()
        elif str(self.request["message"]) == 'getrdata':
            print(f'##[{self.request["message"]}]## get Real data, param is {[x for x in self.request["param"]]}')
            return self.conn.getRData([x for x in self.request["param"]])
        else:
            return ""
