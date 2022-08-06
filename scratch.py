import sys
# sys.path.insert(1, './src/jockmkt_sdk/')
from jockmkt_sdk.client import Client
# import exception
# import objects
# from jm_sockets import sockets
import asyncio
import time
client = Client('5dvS7qravedGv8AeM6Y1nEGTffbKySbc', 'jm_key_mCxk2jho8hhaTgk3')

# for i in range(12):
#     # client.place_order('tdbl_62a17049d93406d730b48ea1b634f119', price=1.1, qty=1)
#     nba_event = client.get_events(start=i, limit=100, league='nba')
#     for i in nba_event:
#         event = client.get_event(i.event_id)

async def main():
    queue = asyncio.Queue()
    list_msgs = []
    global loop
    global client

    async def handle_evt(msg):
        # print('handling event')
        await queue.put(msg)
        # print(msg)

    async def handle_error(message, error, socket):
        print('handling_error')
        await sm.reconnect()


    # sm = await jm_sockets.JockmktSocketClient(loop, client, 'b')
    # await sm.subscribe('account')

    sm = await client.ws_connect(loop, list_msgs, handle_error, callback=queue.put)
    await sm.subscribe('account')
    # sm = await sockets.JockmktSocketManager.create(loop, client, callback=handle_evt)
    await asyncio.sleep(1)
    # await sm.subscribe('games', league='mlb')
    # await asyncio.sleep(1)
    # await sm.subscribe('event', id='evt_629e60b5726370c78750fddb138863b7')
    # counter = 0
    # async def detect_change(old, new):
    #
    last_len = []
    while True:
        await asyncio.sleep(5)
        print(sm.messages)
        # counter += 1
        # print(counter)
        # try:
        #     items = queue.get_nowait()
        # except asyncio.queues.QueueEmpty:
        #     items = None
        # if items is not None:
        #     print(items)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
