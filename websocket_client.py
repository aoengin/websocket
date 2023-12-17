import websocket
import asyncio
import rel
import time
import sys

num_of_messages = 32
counter = 0

num_clients = 16
start_time = 0
is_open = False
active_clients = 0
def log_and_exit():
    print(counter)
    print(time.time())
    print(start_time)
    sys.exit(0)

def on_message(ws, message):
    global counter
    counter += 1
    global start_time
    if is_open and time.time() - start_time > 20:
        log_and_exit()


def on_open(ws):    
    print("Connection successful.")
    global start_time
    global active_clients
    global counter
    active_clients+=1
    if active_clients == num_clients:
        start_time = time.time()
        counter = 0
    global is_open
    is_open = True
    

if __name__ == "__main__":
    ws_list = [0] * num_clients
    for i in range(num_clients):
        ws_list[i] = websocket.WebSocketApp("ws://localhost:8000",
                                on_open = on_open,
                                on_message=on_message)
    for ws in ws_list:
        ws.run_forever(dispatcher=rel, reconnect=5) 
    rel.signal(2, rel.abort)
    rel.dispatch()


    
    
