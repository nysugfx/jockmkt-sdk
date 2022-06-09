import sys
sys.path.insert(1, './src/jockmkt_sdk/')
from client import Client
import exception
import objects
from jm_sockets import sockets
import asyncio
import time
client = Client('--', '--')
# print(client.get_ws_topics())

async def main():
    queue = asyncio.Queue()
    list_msgs = []
    global loop
    global client

    async def handle_evt(msg):
        # print('handling event')
        await queue.put(msg)
        # print(msg)

    # sm = await jm_sockets.JockmktSocketClient(loop, client, 'b')
    # await sm.subscribe('account')

    sm = await client.ws_connect(loop, list_msgs, callback=queue.put)
    await sm.subscribe('account')
    # sm = await sockets.JockmktSocketManager.create(loop, client, callback=handle_evt)
    # await sm.subscribe('account')®
    # await asyncio.sleep(1)
    await sm.subscribe('games', league='mlb')
    # await asyncio.sleep(1)
    await sm.subscribe('event', id='evt_629e60b5726370c78750fddb138863b7')
    counter = 0
    while True:
        await asyncio.sleep(0)
        # if len(sm.messages)>0:
        #     print(sm.messages)

        counter += 1
        # print(counter)
        try:
            items = queue.get_nowait()
        except asyncio.queues.QueueEmpty:
            items = None
        if items is not None:
            print(items)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
