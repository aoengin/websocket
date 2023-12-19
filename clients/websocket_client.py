import websocket
import asyncio
import rel
import time
import sys

counter = 0
num_clients = 1
start_time = 0
is_open = False
active_clients = 0
is_auto = True
in_write = False

def log_and_exit():
    global in_write 
    if not in_write:
        in_write = True
        print("in")
        file1 = open("socketify_websocket_1.txt", "a")
        file1.write(str(counter) + "\n")
        file1.write(str(time.time()) + "\n")
        file1.write(str(start_time) + "\n")
        file1.close()
        sys.exit(0)

def on_message(ws, message):
    global counter
    counter += 1
    global start_time
    if is_open and time.time() - start_time > 20 and not in_write:
        log_and_exit()


def on_open(ws):    
    print("Connection successful.")
    global start_time
    global active_clients
    global counter
    active_clients+=1
    if active_clients == num_clients:
        print("starting the benchmark")
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
