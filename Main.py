import sys

from PyQt5 import QtWidgets, QtWebSockets

from Kiwoom import Kiwoom
from Server import WSServer

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = Kiwoom.instance()

    server = WSServer("My Socket", QtWebSockets.QWebSocketServer.NonSecureMode)
    server.statusChanged.connect(ex.on_status_changed)

    sys.exit(app.exec_())
