from autobahn.asyncio.websocket import create_client_agent
from twisted.internet import task
import time
import struct
import asyncio
counter = 0
agent_num = 10
async def main():
    """
    Using the 'agent' interface to talk to the echo server (run
    ../echo/server.py for the server, for example)
    """
    agents = [0] * agent_num
    for i in range(agent_num):
        agents[i] = create_client_agent()
    options = {
        "headers": {
            "x-foo": "bar",
        }
    }

    protos = [0] * agent_num
    for k in range(agent_num):
        protos[k] = await agents[k].open("ws://localhost:8000", options)

    
    
    def got_message(*args, **kw):
        global counter
        counter += 1

    for l in range(agent_num):
        protos[l].on('message', got_message)
    for m in range(agent_num):
        await protos[m].is_open

    
    
    print(time.time())
    
    async def send_message(protos):
        for i in range(32):
            for proto in protos:
                proto.sendMessage(b"")
    
    async def print_counter():
        await asyncio.sleep(1)
        global counter
        print(counter)
    data = [0] * agent_num
    for a in range(agent_num):
        data[a] = asyncio.create_task(send_message(protos))

    print_counter = asyncio.create_task(print_counter())
    
    for o in range(agent_num):
        await data[o]
    await print_counter
    
    # print(float(struct.unpack('!d', last_timestamp)[0]))
    
    # print(counter / (float(struct.unpack('!d', last_timestamp)[0]) - first_timestamp))

if __name__ == "__main__":
    asyncio.run(main)