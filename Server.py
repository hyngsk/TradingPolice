import datetime

from PyQt5 import QtNetwork, QtWebSockets, QtCore

from Controller import Controller


class WSServer(QtCore.QObject):
    # 전역 시그널 변수
    SignalLog = QtCore.pyqtSignal(str)

    def __init__(self, name, mode, parent=None):
        super().__init__(parent)
        self.clients = []
        self.server = QtWebSockets.QWebSocketServer(name, mode, parent)
        self.server.closed.connect(QtCore.QCoreApplication.quit)
        if self.server.listen(QtNetwork.QHostAddress.LocalHost, 5001):
            print(
                f"Connected: {self.server.serverName()} : {self.server.serverAddress().toString()} : {self.server.serverPort()}")
        else:
            print(f"error: {self.server.errorString()}")
        self.server.newConnection.connect(self.onNewConnection)
        print(self.server.isListening())

    @QtCore.pyqtSlot()
    def onNewConnection(self):
        client = self.server.nextPendingConnection()
        client.identifier = QtCore.QUuid.createUuid().toString(QtCore.QUuid.Id128)
        client.textMessageReceived.connect(self.processTextMessage)
        client.binaryMessageReceived.connect(self.processBinaryMessage)
        client.disconnected.connect(self.socketDisconnected)
        self.clients.append(client)
        self.SignalLog.emit(f"[INFO] {datetime.datetime.now()} -- Connected: Client-[{client.identifier}]")

    @QtCore.pyqtSlot(str)
    def processTextMessage(self, message):
        client = self.sender()
        result = None
        if isinstance(client, QtWebSockets.QWebSocket):
            # client.sendTextMessage(message) # 클라이언트로부터 받은 메세지를 다시 클라이언트에게 Echo 전송

            # log 찍는 방법 1. statusChanged 시그널 변수를 이용해 GUI로그창으로 전송
            self.SignalLog.emit(f"[INFO] {datetime.datetime.now()} -- Client- [{client.identifier}] Sent: {type(message)} {str(message)}")
            # get controller instance
            ctr = Controller(client.identifier, str(sage))
            try:
                result = ctr.get_data_from_kw()
            except ctr:
                self.SignalLog.emit(
                    f"[ERROR] {datetime.datetime.now()} -- Client- [{client.identifier}]: Incorrect request")
            # log
            self.SignalLog.emit(
                f"[INFO] {datetime.datetime.now()} -- sent to Client- [{client.identifier}]: {result}")
            # 클라이언트에게 메세지 전송
            return client.sendTextMessage(result)

    @QtCore.pyqtSlot(QtCore.QByteArray)
    def processBinaryMessage(self, message):
        """

        :param message:
        :return:
        """
        client = self.sender()
        if isinstance(client, QtWebSockets.QWebSocket):
            client.sendBinaryMessage(message)
            print(f"[INFO] {datetime.datetime.now()} -- Client- [{client.identifier}]: {message}")

    @QtCore.pyqtSlot()
    def socketDisconnected(self):
        client = self.sender()
        if isinstance(client, QtWebSockets.QWebSocket):
            self.clients.remove(client)
            self.SignalLog.emit(f"[INFO] {datetime.datetime.now()} -- Disconnected: Client-[{client.identifier}]")
            client.deleteLater()
