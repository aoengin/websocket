import asyncio
from websockets.sync.client import connect
import time
import sys
from signal import SIGINT, SIGTERM

start_time = 0
counter = 0
num_of_clients = 1

def log_and_exit(websocket):
    print(counter)
    print(time.time())
    print(start_time)
    websocket.close()
    sys.exit(0)


async def hello():
    global counter
    global start_time
    with connect("ws://localhost:8000") as websocket:
        start_time = time.time()
        while True:
            message = websocket.recv()
            if message is not None:
                counter+=1
            if time.time() - start_time > 20:
                log_and_exit(websocket)

async def main():
    tasks = [0] * num_of_clients
    for i in range(num_of_clients):
        tasks[i] = asyncio.create_task(hello())
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Received exit, exiting")