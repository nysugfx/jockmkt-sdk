import asyncio
import json
import logging
import time
import typing

from ..objects import Game, Event, Tradeable, Entry, Order, Position, PublicOrder, Trade, Balance

import websockets as ws


class JMWebsocketException(Exception):
    """
    a class for JM websocket specific exceptions. Currently not in use.

    """
    pass


class ReconnectWebsocket:
    """
    Class handling the websocket connection

    :ivar log: an instance of logging containing log info about exceptions.
    """
    MAX_RECONNECTS = 5
    AUTH_DICT = {}

    def __init__(self, loop, client, coroutine, error_handler):
        self._loop = loop
        self._coroutine = coroutine
        self._conn = None
        self._client = client
        self._socket = None
        self._reconnect_attempts = 0
        self.log = logging.getLogger(__name__)
        if not error_handler:
            self._error_handler = self.reconnect()
        else:
            self._error_handler = error_handler
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
        authorizes websocket and receives messages
        """
        # print("running")
        async with ws.connect("wss://api.jockmkt.net/streaming/") as socket:
            # print("async with called")
            self._socket = socket
            self._reconnect_attempts = 0
            try:
                await self.send_message(self.AUTH_DICT)
                await self._socket.recv()
                async for message in socket:
                    await self._coroutine(message)

            except ws.ConnectionClosedError as on_close:
                self.log.debug(f'Connection terminated with an error: {on_close}')
                await self._error_handler(message, on_close)

            except Exception as e:
                self.log.debug(f'unknown ws exception: {e}')
                await self._error_handler(message, e)

    async def reconnect(self):
        """
        An error handler is required, so this is a good option! it just attempts to reconnect upon failure
        """
        await self.cancel()
        self._reconnect_attempts += 1
        if self._reconnect_attempts < self.MAX_RECONNECTS:
            wait = self._get_reconnect_wait(self._reconnect_attempts)
            self.log.debug(f'websockets reconnecting. Attempting {self._reconnect_attempts} more times after waiting '
                           f'{wait} seconds')
            self._connect()
        else:
            self.log.error('websocket could not reconnect after 5 attempts.')

    @staticmethod
    def _get_reconnect_wait(attempts):
        wait = [0.1, 3, 10, 30, 60]
        return wait[attempts]

    async def send_message(self, msg, retry_count=0):
        """
        send a message to the websocket (i.e. subscribe or unsubscribe). The user typically should not need to use this.
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
    """
    Create and manage the socket connection.
    """
    PUBLIC_TOPICS = {
        "event_activity": "event_id",
        "event": "event_id",
        "account": None,
        "notification": None,
        "games": "league"
    }

    def __init__(self, iterable):
        """Initialize the SocketManager

        :ivar messages: the iterable to which the user wants to append their messages
        :ivar balances: regularly updated balances each time the balance changes
        """
        self._subscriptions = []
        self.messages = iterable
        self.balances = {}
        self._callback = None
        self._conn = None
        self._loop = None
        self._client = None

    @classmethod
    async def create(cls, loop: asyncio.Event, client, queue: list, exception_handler: typing.Callable,
                     callback: typing.Callable = None):
        """
        create instance of socket manager and reconnect websocket

        """
        self = JockmktSocketManager(queue)
        self._loop = loop
        self._callback = callback
        self._error_handler = exception_handler
        self._conn = ReconnectWebsocket(loop, client, self._recv, self.exception_handler)
        return self

    async def reconnect(self):
        """
        Function that can be passed through the error handler
        """
        await self._conn.reconnect()

    def _wsfeed_case_switcher(self, obj, msg):
        match obj:
            case 'error':
                raise Exception(f'{msg}')
            case 'tradeable':
                return Tradeable(msg[obj])
            case 'game':
                return Game(msg[obj])
            case 'event':
                return Event(msg[obj])
            case 'entry':
                return Entry(msg[obj])
            case 'position':
                return Position(msg[obj])
            case 'order':
                if 'limit_price' in msg[obj]:
                    return Order(msg[obj])
                else:
                    return PublicOrder(msg[obj])
            case 'trade':
                return Trade(msg[obj])
            case 'balance':
                self.balances[msg[obj]['currency']] = msg[obj]['buying_power']
                return Balance(msg[obj])

    async def exception_handler(self, **kwargs):
        """
        Exception handler passed in by the user
        """
        await self._error_handler(**kwargs)

    async def _recv(self, msg):
        """
        handle incoming messages. The user should pass their event handling function in as an arg to callback
        """
        if self.messages is not None:
            messsage = json.loads(msg)
            type = messsage['object']
            obj = self._wsfeed_case_switcher(type, messsage)
            messsage[type] = obj
            self.messages.append(messsage)
        if self._callback is not None:
            # print(msg)
            await self._callback(msg)

    async def subscribe(self, topic: str, id: str = None, league: str = None):
        """
        Subscribe to a chosen topic or event.

        :param topic:  The user's chosen topic. Use client.get_ws_topics() for available topics.
        :type topic:   str, required
        :param id:     The event ID, required if you are subscribing to event or event_activity.
        :type id:      str, optional
        :param league: the league for which the user wants game data, required for 'games' subscription
        :type league:  str, optional
        """
        topics = self.PUBLIC_TOPICS.keys()
        if topic not in topics:
            raise KeyError(f'please choose from the following topics: {list(topics)}')
        self._subscriptions.append((topic, id, league))
        msg = {"action": "subscribe",
               "subscription": {"type": str(topic),
                                'event_id': id,
                                'league': league}}
        await self._conn.send_message(msg)

    async def unsubscribe(self, topic: str, id: str = None, league: str = None):
        """
        unsubscribe method

        :param topic:  The user's chosen topic. Use client.get_ws_topics() for available topics.
        :type topic:   str, required
        :param id:     The event ID, required if you are subscribing to event or event_activity.
        :type id:      str, optional
        :param league: the league for which the user wants game data, required for 'games' subscription
        :type league:  str, optional
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
