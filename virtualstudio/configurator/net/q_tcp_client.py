
import socket

from PyQt5.QtCore import QThread, QMutex

from virtualstudio.common.net.messagetools import *
from virtualstudio.common.logging import logengine


class TCPClient(QThread):

    def __init__(self, address="127.0.0.1", port=4233):
        super().__init__()

        self.address = address
        self.port = port

        self.sock = None
        self.timeout: Optional[float] = None
        self.running = False

        self.sendLock = QMutex ()
        self.socketLock = QMutex ()

        self.messageStub = None

        self.logger = logengine.getLogger()

    def __str__(self):
        return "TCP Client connected to " + str(self.address) + ":" + str(self.port)

    def setTimeout(self, timeout: Optional[float]):
        self.timeout = timeout
        if self.sock is not None:
            self.sock.settimeout(timeout)

    def requestStop(self):
        self.running = False

    def run(self) -> None:
        self.running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)

        self.sock.connect((self.address, self.port))
        self.messageStub = None
        try:
            while self.running:

                length = self.sock.recv(4)
                while len(length) < 4:
                    length += self.sock.recv(4 - len(length))  # 16 kb buffer
                pkglen = getInt(length, start=0)
                data = bytearray()
                while len(data) < pkglen:
                    data += self.sock.recv(pkglen - len(data))

                self.logger.debug("Message Recieved: {:08X} {}".format(getInt(length, start=0), str(data)))
                self.onMessageRecv(data)

        except ConnectionAbortedError:
            pass # Socket closed by another thread
        except Exception as ex:
            self.logger.exception(ex)
        finally:
            self.sock.close()

    def onMessageRecv(self, message: bytes):
        pass

    def sendMessage(self, message: bytes):
        with self.socketLock:
            if self.sock is not None:
                messages = disassembleMessage(message)
                self.sendLock.acquire()
                try:
                    for packet in messages:
                        self.sock.sendall(packet)
                finally:
                    self.sendLock.release()

    def closeConnection(self):
        self.sock.close()

