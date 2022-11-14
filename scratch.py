import sys
sys.path.insert(1, './src/jockmkt_sdk/')
from client import Client
import exception
import objects
import json
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
    queue = asyncio.Queue(-1)
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

    sm = await client.ws_connect(loop, list_msgs, handle_error, callback=queue.put)
    await sm.subscribe('account')
    print('subscribed to acct')
    # sm = await sockets.JockmktSocketManager.create(loop, client, callback=handle_evt)
    await sm.subscribe('games', league='pga')
    print('subscribed to game')
    await sm.subscribe('event_activity', id='evt_636b33d2014f61ebbe8c5dd468c8ebab')
    print('event activity subscribed')
    await sm.subscribe('event', id='evt_636b33d2014f61ebbe8c5dd468c8ebab')
    print('event subscribe')
    # counter = 0
    # async def detect_change(old, new):
    #
    last_len = []
    while True:
        await asyncio.sleep(0)
        # print(sm.messages)
        d = await queue.get()
        print(d)
        # counter += 1
        # print(counter)
        # try:
        #     items = queue.get_nowait()
        # except asyncio.queues.QueueEmpty:
        #     items = None
        # if items is not None:
        #     print(items)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
