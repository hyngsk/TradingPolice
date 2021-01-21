import datetime

from PyQt5 import QtNetwork, QtWebSockets, QtCore

from Kiwoom import Kiwoom


class WSServer(QtCore.QObject):
    # 전역 시그널 변수
    statusChanged = QtCore.pyqtSignal(str)

    def __init__(self, name, mode, parent=None):
        super().__init__(parent)
        self.clients = []
        self.server = QtWebSockets.QWebSocketServer(name, mode, parent)
        self.server.closed.connect(QtCore.QCoreApplication.quit)
        if self.server.listen(QtNetwork.QHostAddress.LocalHost, 5001):
            print(
                "Connected: {} : {} : {}".format(
                    self.server.serverName(),
                    self.server.serverAddress().toString(),
                    self.server.serverPort(),
                )
            )
        else:
            print("error: {}".format(self.server.errorString()))
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
        self.statusChanged.emit("Connected: client-{}".format(client.identifier))

    @QtCore.pyqtSlot(str)
    def processTextMessage(self, message):
        client = self.sender()
        if isinstance(client, QtWebSockets.QWebSocket):

            # client.sendTextMessage(message) # 클라이언트로부터 받은 메세지를 다시 클라이언트에게 Echo 전송

            # log 찍는 방법 1. statusChanged 시그널 변수를 이용해 GUI로그창으로 전송
            self.statusChanged.emit("Client-[{}] Send: {}".format(client.identifier, message))
            if message == 'getaccno':
                accno = Kiwoom.instance().getAcoNo()
                print(accno)
                # log 찍는 방법 2. App 싱글톤을 호출해 logTextArea를 직접 컨트롤
                Kiwoom.instance().logTextArea.append(
                    "[Log] {} -- Client- {}: {}".format(datetime.datetime.now(), client.identifier,
                                                        "계좌번호: " + accno))
                # 클라이언트에게 메세지 전송
                client.sendTextMessage(accno)

    @QtCore.pyqtSlot(QtCore.QByteArray)
    def processBinaryMessage(self, message):
        """

        :param message:
        :return:
        """
        client = self.sender()
        if isinstance(client, QtWebSockets.QWebSocket):
            client.sendBinaryMessage(message)
            print("Client-{}: {}".format(client.identifier, message))

    @QtCore.pyqtSlot()
    def socketDisconnected(self):
        client = self.sender()
        if isinstance(client, QtWebSockets.QWebSocket):
            self.clients.remove(client)
            self.statusChanged.emit("Disconnected: client-{}".format(client.identifier))
            client.deleteLater()
