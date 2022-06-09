import sys
sys.path.insert(1, './src/jockmkt_sdk/')
from client import Client
import exception
import objects
from jm_sockets import sockets
import asyncio
import time
client = Client('<secret>', '<api>')
# print(client.get_ws_topics())

async def main():
    queue = asyncio.Queue()
    global loop
    global client

    async def handle_evt(msg):
        # print('handling event')
        await queue.put(msg)
        # print(msg)

    # sm = await jm_sockets.JockmktSocketClient(loop, client, 'b')
    # await sm.subscribe('account')

    sm = await sockets.JockmktSocketManager.create(loop, client, callback=handle_evt)
    await sm.subscribe('account')
    # await asyncio.sleep(1)
    await sm.subscribe('games', league='mlb')
    # await asyncio.sleep(1)
    await sm.subscribe('event', id='evt_629ecd4c8864714554e8665bdd7f7da8')
    counter = 0
    while True:
        # print('sleeping to keep open')
        await asyncio.sleep(0)

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
