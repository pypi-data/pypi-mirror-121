from abc import ABC, abstractmethod

class Channel(ABC):
    @abstractmethod
    def send(self, data):
        pass

    # @abstractmethod
    # def recv(self):
    #     pass

    # @abstractmethod
    # def onMessage(self, callback):
    #     pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disConnect(self):
        pass

    # @abstractmethod
    # def onDisconnect(self, callback):
    #     pass

    # @abstractmethod
    # def onConnect(self, callback):
    #     pass

    @abstractmethod
    def registeHandler(self, handler):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def runForever(self):
        pass


class ChannelHandler:
    def onConnected(self, channelObj):
        pass

    def onDisconnected(self, channelObj):
        pass

    def onMessage(self,channelObj, message):
        pass

    def onError(self,channelObj,error):
        pass

