from .wsChannel import WsChannel
from threading import Timer
import time
from .channel import ChannelHandler
import json
import netifaces as ni
import sys
from . import _logging
class Device(ChannelHandler):
    def __init__(self, deviceType, deviceId=None, timeout = 20, url="ws://192.168.0.103/ws",deviceIp = None,**kwargs):
        super().__init__()
        self._deviceType = deviceType
        self._deviceId = deviceId
        self._timeout = timeout
        #{
        # "key": {"startTime": xxx, "data": {}, "callback": xxx}
        #}
        self._messageCache = {}
        self._monitor = self.RepeatedTimer(3, self._messageMonitor)
        self._channel = WsChannel(url)
        self._isRunning = False
        self._id = 1
        self._additionalInfo = kwargs
        self._hasRegisted = False
        self._registeCallback = None
        self._ip = deviceIp

    def setChannel(self, channel):
        if self._isRunning:
            raise Exception("SetChannel should be called before connect")
        self._channel = channel 

    def connect(self, callback):
        if self._isRunning:
            return
        self._channel.registeHandler(self)
        self._channel.connect()
        self._channel.run()
        self._registeCallback = callback
        
    """
        method: method name
        params: parameters for jsonrpc
        callback:  callback(result, error),
        in the callback, result or error could be set None
    """    
    def request(self, method, params, callback):
        if self._isRunning is False:
            raise Exception("Please call connect before request")
        params["senderId"] = self._deviceId
        params["senderType"] = self._deviceType
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": self._id
        }
        self._messageCache[self._id] = {
            "startTime": time.time(),
            "data": request,
            "callback": callback
        }
        self._id = self._id + 1
        self._channel.send(json.dumps(request))

    def notify(self, method, params):
        if self._isRunning is False:
            raise Exception("Please call connect before notify")
        params["senderId"] = self._deviceId
        params["senderType"] = self._deviceType
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params
        }
        self._channel.send(json.dumps(request))

    def response(self, originalRequest, id, result, error):
        responseMsg = {
            "jsonrpc": "2.0",
            "id": id,
        }
        deviceInfo = {
            "senderId": originalRequest["params"]["senderId"],
            "senderType": originalRequest["params"]["senderType"],
            "receiverId": originalRequest["params"]["receiverId"],
            "receiverType": originalRequest["params"]["receiverType"]
        }
        if result is None and error is None:
            error = {}
        if result is not None:
            result = {**result, **deviceInfo}
            responseMsg["result"] = result
        else:
            error = {**error, **deviceInfo}
            responseMsg["error"] = error
        self._channel.send(json.dumps(responseMsg))

    def onCommand(self, method, params, id, originalRequest=None):
        pass

    def _messageMonitor(self):
        now = time.time()
        toBeDelete = []
        for item in self._messageCache.items():
            k, v = item
            start = v["startTime"]
            duration = now - start
            if duration > self._timeout:
                if self._channel is not None:
                    self._channel.send(v["data"])
                    v["startTime"] = time.time()
                else:
                    toBeDelete.append(k)
        for k in toBeDelete:
            del self._messageCache[k]


    class RepeatedTimer:
        def __init__(self, interval, function, *args, **kwargs):
            self._timer     = None
            self.interval   = interval
            self.function   = function
            self.args       = args
            self.kwargs     = kwargs
            self.is_running = False
            self.start()

        def _run(self):
            self.is_running = False
            self.start()
            self.function(*self.args, **self.kwargs)

        def start(self):
            if not self.is_running:
                self._timer = Timer(self.interval, self._run)
                self._timer.start()
                self.is_running = True

        def stop(self):
            self._timer.cancel()
            self.is_running = False
    
    def onConnected(self, channelObj):
        _logging.debug("Device connect success")
        registeParams = self._additionalInfo
        registeParams["type"] = self._deviceType    
        if self._deviceId is not None:
            registeParams["id"] = self._deviceId
        if sys.platform == "linux" or sys.platform == "linux2":
            if self._ip is not None:
                registeParams["debugURL"] = self._ip + ":8888"
            else:
                registeParams["debugURL"]= ni.ifaddresses("wlan0")[ni.AF_INET][0]["addr"] + ":8888"
        def callback2(result=None, error=None):
            if result is not None:
                self._deviceId = result.get("id", self._deviceId)
            self._registeCallback(result, error)
            _logging.debug("Device registe result: {}, error: {}".format(result, error))
        self._isRunning = True
        self.request("registe", registeParams, callback2)

    def onDisconnected(self, channelObj):
        pass

    def onMessage(self, channelObj, message):
        jsonMsg = json.loads(message)
        _logging.debug("Device receive: {}".format(jsonMsg))
        if "method" in jsonMsg:
            # is request
            _method = jsonMsg.get("method")
            _params = jsonMsg.get("params", {})
            _id = jsonMsg.get("id", None)
            self.onCommand(_method, _params, _id, jsonMsg)
        elif "result" in jsonMsg or "error" in jsonMsg:
            # is response
            _id = jsonMsg["id"]
            _result = jsonMsg.get("result", None)
            _error = jsonMsg.get("error", None)
            if _id in self._messageCache:
                _cacheRequest = self._messageCache.pop(_id)
                _callbck = _cacheRequest["callback"]
                _callbck(_result, _error)
             

    def onError(self, channelObj, error):
        pass


    
