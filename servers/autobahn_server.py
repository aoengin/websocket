import asyncio
from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol, \
    listenWS
import time
import sys

from twisted.internet import reactor

counter = 0
start_time = time.time()
class BroadcastServerProtocol(WebSocketServerProtocol):

    def onOpen(self):
        global start_time
        self.factory.register(self)
        start_time = time.time()

    def onMessage(self, payload, isBinary):
        if not isBinary:
            msg = "{} from {}".format(payload.decode('utf8'), self.peer)
            self.factory.broadcast(msg)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)


class BroadcastServerFactory(WebSocketServerFactory):

    """
    Simple broadcast server broadcasting any message it receives to all
    currently connected clients.
    """

    def __init__(self, url):
        WebSocketServerFactory.__init__(self, url)
        self.clients = []
        self.tickcount = 0
        self.tick()

    def tick(self):
        self.tickcount += 1
        self.broadcast("tick %d from server" % self.tickcount)
        reactor.callLater(0, self.tick)

    def register(self, client):
        global counter
        if client not in self.clients:
            print("registered client {}".format(client.peer))
            counter = 0
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            print("unregistered client {}".format(client.peer))
            self.clients.remove(client)
            print(counter)

    def broadcast(self, msg):
        global counter
        global start_time
        if time.time() - start_time > 30:
            reactor.stop()
        for c in self.clients:
            try:
                counter += 1
                c.sendMessage(msg.encode('utf8'))
            except:
                print("Connection lost.")

if __name__ == '__main__':

    ServerFactory = BroadcastServerFactory
    # ServerFactory = BroadcastPreparedServerFactory

    factory = ServerFactory("ws://127.0.0.1:8000")
    factory.protocol = BroadcastServerProtocol
    listenWS(factory)

    reactor.listenTCP(8080, factory)

    reactor.run()