import asyncio

from autobahn.asyncio.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory

import time
import sys
counter = 0
num_clients = 16
start_time = 0
is_open = False

def log_and_exit():
    print(counter)
    print(time.time())
    print(start_time)
    sys.exit(0)

class MyClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    def onConnecting(self, transport_details):
        print("Connecting; transport details: {}".format(transport_details))
        return None  

    def onOpen(self):
        global start_time
        start_time = time.time()
        global is_open
        is_open = True
        print("WebSocket connection open.")
        
        

    def onMessage(self, payload, isBinary):
        global counter        
        counter += 1
        global start_time
        if is_open and time.time() - start_time > 20:
            log_and_exit()

    def onClose(self, wasClean, code, reason):
        print("Closing the connection.")

if __name__ == '__main__':
    factories = [0] * num_clients
    for i in range(num_clients):
        factories[i] = WebSocketClientFactory("ws://127.0.0.1:8000")
        factories[i].protocol = MyClientProtocol

    loop = asyncio.get_event_loop()
    coros = [0] * num_clients
    for l in range(num_clients):
        coros[l] = loop.create_connection(factories[i], '127.0.0.1', 8000)
    
    for m in range(num_clients):
        loop.run_until_complete(coros[m])
    loop.run_forever()
    loop.close()