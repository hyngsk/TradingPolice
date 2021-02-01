import sys

from PyQt5 import QtWidgets, QtWebSockets

from Kiwoom import Kiwoom
from Server import WSServer

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    KWAPI = Kiwoom.instance()

    server = WSServer("My Socket", QtWebSockets.QWebSocketServer.NonSecureMode)
    server.SignalLog.connect(KWAPI.logSignal)

    sys.exit(app.exec_())
