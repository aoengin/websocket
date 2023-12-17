# socketify_server.py
from socketify import App, OpCode, CompressOptions
import time
import asyncio
import threading
app = App()
counter = 0
first_connection = False
async def ws_open(ws):
    global first_connection
    first_connection = True
    print("Client connected")
    ws.subscribe("stream")
    start_streaming_data()
    

async def ws_close(ws, code, reason):
    print("Client disconnected")

def start_streaming_data():   
    while True:
        global counter
        counter += 1
        data = "Continuous data stream: " + str(time.time())
        app.publish("stream", data, OpCode.TEXT)

app.ws(
    "/*",
    {
        "compression": CompressOptions.DISABLED,
        "max_payload_length": 16 * 1024 * 1024,
        "idle_timeout": 12,
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

