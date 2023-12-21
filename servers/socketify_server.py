# socketify_server.py
from socketify import App, OpCode, CompressOptions
import time
import asyncio
import threading
import asyncio
from contextlib import suppress
import sys

# StackOverflow
class Periodic:
    def __init__(self, func, time):
        self.func = func
        self.time = time
        self.is_started = False
        self._task = None

    async def start(self):
        if not self.is_started:
            self.is_started = True
            # Start task to call func periodically:
            self._task = asyncio.create_task(self._run())

    async def stop(self):
        if self.is_started:
            self.is_started = False
            # Stop task and await it stopped:
            self._task.cancel()
            with suppress(asyncio.CancelledError):
                await self._task

    async def _run(self):
        while True:
            await asyncio.sleep(self.time)
            await self.func()

app = App()
counter = 0
first_connection = False
clients = 0
num_of_clients = 16
start_time = time.time()
async def start_streaming_data():   
    global counter
    data = "Continuous data stream: " + str(time.time())
    status = app.publish("stream", data, OpCode.TEXT)
    counter += 1
    if time.time() - start_time > 30:
        sys.exit(0)


p = Periodic(start_streaming_data, 0.000001)

async def ws_open(ws):
    global clients 
    global first_connection
    global start_time
    first_connection = True
    start_time = time.time()
    clients += 1
    print("Client connected")
    ws.subscribe("stream")
    if clients == num_of_clients:
        print("start streaming")
        await p.start()
        
    

async def ws_close(ws, code, reason):
    print(counter)
    print("Client disconnected")
    # print(successful_counter)


app.ws(
    "/*",
    {
        "compression": CompressOptions.DISABLED,
        "max_payload_length": 16 * 1024 * 1024,
        "idle_timeout": 30,
        "open": ws_open,
        "close": ws_close,
    },
)
app.any("/", lambda res, req: res.end("Nothing to see here!"))

app.listen(
    8000,
    lambda config: print("Listening on port ws://localhost:%d now\n" % (config.port)),
)

app.run()


