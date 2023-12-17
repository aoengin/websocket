# socketify_server.py
from socketify import App, OpCode, CompressOptions
import time
import asyncio
app = App()
counter = 0
async def ws_open(ws):
    print("Client connected")
    ws.subscribe("stream")
    await asyncio.sleep(0.1)
    await start_streaming_data(ws)
    

async def ws_close(ws, code, reason):
    print("Client disconnected")

async def start_streaming_data(ws):    
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