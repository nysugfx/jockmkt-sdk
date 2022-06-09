import asyncio
import json
import logging
import time

import websockets as ws


class JMWebsocketException(Exception):
    pass


class ReconnectWebsocket:
    MAX_RECONNECTS = 5
    MAX_RECONNECT_SECS = 60
    MAX_RECONNECT_WAIT = 0.1
    TIMEOUT = 10
    PROTOCOL_VERSION = "1.0.0"
    AUTH_DICT = {}

    def __init__(self, loop, client, coroutine, private=False):
        self._loop = loop
        self._log = logging.getLogger(__name__)
        self._coroutine = coroutine
        self._reconnect_attempts = 0
        self._conn = None
        self._ws_details = None
        self._connect_id = None
        self._client = client
        self._private = private
        self._last_ping = None
        self._socket = None
        self.__build_auth_dict(client.ws_token_generator())
        self._connect()

    def __build_auth_dict(self, token):
        """
        builds the dictionary necessary for the websocket authorization
        """
        auth_dict = {"action": "authenticate", "authentication": {"type": "token", "token": token}}
        self.AUTH_DICT = auth_dict
        return auth_dict

    def _connect(self):
        """
        instantiates a singular websocket task
        """
        print("connecting")
        self._conn = asyncio.ensure_future(self._run(), loop=self._loop)

    async def _run(self):
        """
        performs authorizes websocket and receives messages
        """
        print("running")
        keep_waiting = True
        async with ws.connect("wss://api.jockmkt.net/streaming/") as socket:
            print("async with called")
            self._socket = socket
            self._reconnect_attempts = 0
            await self.send_message(self.AUTH_DICT)
            await self._socket.recv()
            async for message in socket:
                await self._coroutine(message)

            # try:
            #     while keep_waiting:
            #         print("waiting")
            #         try:
            #             evt = await self._socket.recv()
            #             print('evt', evt)
            #         except asyncio.TimeoutError:
            #             self._log.debug(f"no message in {self._get_ws_ping_timeout()} seconds")
            #             await self.send_ping()
            #         except asyncio.CancelledError:
            #             self._log.debug("cancelled error")
            #             await self._socket.ping()
            #         else:
            #             try:
            #                 evt_obj = json.loads(evt)
            #             except ValueError:
            #                 pass
            #             else:
            #                 await self._coroutine(evt_obj)
            # except ws.ConnectionClosed:
            #     keep_waiting = False
            #     await self._reconnect()
            # except Exception as e:
            #     self._log.debug(f"ws exception:{e}")
            #     keep_waiting = False
            #     await self._reconnect()

    def _get_ws_ping_timeout(self):
        pass
        if not self._ws_details:
            raise Exception("Unknown Websocket details")

        ping_timeout = 10
        return ping_timeout

    async def _reconnect(self):
        """
        not yet implemented
        """
        await self.cancel()
        self._reconnect_attempts += 1
        if self._reconnect_attempts < self.MAX_RECONNECTS:
            self._log.debug(f"Websocket reconnecting. {self.MAX_RECONNECTS - self._reconnect_attempts} attempts left.")
            self._get_reconnect_wait(self._reconnect_attempts)

        else:
            self._log.error(f"websocket could not reconnect after {self._reconnect_attempts} attempts")
            pass

    @staticmethod
    def _get_reconnect_wait(attempts):
        wait_times = [1, 10, 50, 100]
        return wait_times[attempts]

    async def send_message(self, msg, retry_count=0):
        """
        send a message to the websocket (i.e. subscribe or unsubscribe)
        """
        if not self._socket:
            if retry_count < 5:
                await asyncio.sleep(1)
                await self.send_message(msg, retry_count + 1)
        else:
            await self._socket.send(json.dumps(msg))

    async def cancel(self):
        """
        cancels the instance of websocket connection
        """
        try:
            self._conn.cancel()
        except asyncio.CancelledError:
            pass


class JockmktSocketManager:
    PUBLIC_TOPICS = {
        "event_activity": "event_id",
        "event": "event_id",
        "account": None,
        "notification": None,
        "games": "league"
    }

    def __init__(self):
        """Initialize the SocketManager
        """
        self._subscriptions = []
        self._callback = None
        self._conn = None
        self._loop = None
        self._client = None
        self._private = False
        self._log = logging.getLogger(__name__)

    @classmethod
    async def create(cls, loop, client, callback, private=False):
        """
        create instance of socket manager and reconnect websocket
        """
        self = JockmktSocketManager()
        self._loop = loop
        self._private = private
        self._callback = callback
        self._conn = ReconnectWebsocket(loop, client, self._recv, private)
        return self

    async def _recv(self, msg):
        """
        handle incoming messages. The user should pass their event handling function in as an arg to callback
        """
        await self._callback(msg)

    async def subscribe(self, topic, id=None, league=None):
        """
        self explanatory
        """
        topics = self.PUBLIC_TOPICS.keys()
        if topic not in topics:
            print(f'please choose from the following topics: {topics}')
            return
        self._subscriptions.append((topic, id, league))
        msg = {"action": "subscribe",
               "subscription": {"type": str(topic),
                                'event_id': id,
                                'league': league}}
        await self._conn.send_message(msg)

    async def unsubscribe(self, topic, id=None, league=None):
        """
        unsubscribe method
        """
        msg = {"action": "unsubscribe",
               "subscription": {"topic": topic,
                                "event_id": str(id),
                                "league": str(league)}}
        await self._conn.send_message(msg)

    async def unsubscribe_all(self):
        """
        unsubscribe all method
        """
        for i in self._subscriptions:
            await self.unsubscribe(topic=i[0], id=i[1], league=i[2])
