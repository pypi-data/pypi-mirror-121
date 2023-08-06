import time
from .channel import Channel
import websocket
import threading
import gc
from . import _logging

class WsChannel(Channel):

    def __init__(self, wsUrl) -> None:
        super().__init__()
        self._Url = wsUrl
        self._Handler = []
        self._Ws = None

    def send(self, data):
        if self._Ws is None:
            _logging.error("Should call connect before send message")
            raise Exception("Call the run or runForever before send")
        try:
            self._Ws.send(data)
        except:
            _logging.error("Send message error, please check the connection")

    def connect(self):
        if self._Ws is None:
            self._Ws = websocket.WebSocketApp(self._Url,
                                            on_open=self._onConnected,
                                            on_message=self._onMessage,
                                            on_error=self._onError,
                                            on_close=self._onDisConnected)  

    def disConnect(self):
        pass

    def registeHandler(self, handler):
        self._Handler.append(handler)
        
    def _onMessage(self, ws, message):
        _logging.debug("Receive {}".format(message))
        for _handler in self._Handler:
            _handler.onMessage(ws, message)

    def _onConnected(self, ws):
        _logging.debug("ws connect success")
        for _handler in self._Handler:
            _handler.onConnected(ws)

    def _onDisConnected(self,ws):
        for _handler in self._Handler:
            _handler.onDisconnected(ws)

    def _onError(self, ws, error):
        for _handler in self._Handler:
            _handler.onError(ws, error)

    def run(self):
        self._wsThread = threading.Thread(target=self.runForever, daemon=True)
        self._wsThread.start()

    def runForever(self):
        while True:
            if self._Ws is None:
                raise Exception("Should call the connect before runForever")
            try:
                self._Ws.run_forever()
            except Exception as e:
                gc.collect()
            time.sleep(5)