import asyncio

from autobahn.asyncio.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory

import time
import sys
import random
import sys

counter = 0
num_clients = 2
clients = 0
start_time = 0
param1 = 0
is_open = False
in_write = False
def log_and_exit():
    global in_write 
    if not in_write:
        in_write = True
        print("in")
        file1 = open("results/socketify_autows_multiple_console_2.txt", "a")
        file1.write(str(counter) + "\n")
        file1.write(str(time.time()) + "\n")
        file1.write(str(start_time) + "\n")
        file1.close()
        sys.exit(0)

class MyClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    def onConnecting(self, transport_details):
        print("Connecting; transport details: {}".format(transport_details))
        return None  

    def onOpen(self):
        global start_time
        global clients
        global counter
        start_time = time.time()
        clients += 1
        if clients == num_clients:
            counter = 0
            start_time = time.time()
        global is_open
        is_open = True
        print("WebSocket connection open.")
        
        

    async def onMessage(self, payload, isBinary):
        global counter        
        counter += 1
        global start_time
        global param1
        if time.time() - start_time > 20 and is_open and not in_write:
            await asyncio.sleep(param1)
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
    param1 = float(sys.argv[1])
    loop.run_forever()
    loop.close()