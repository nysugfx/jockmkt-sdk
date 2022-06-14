import asyncio
import json
import logging
import time
import typing
from src.jockmkt_sdk.objects import Team, Game, GameLog, Event, Tradeable, Entry, Order, Position, AccountActivity, Entity, \
    _case_switch_ent
import websockets as ws


class JMWebsocketException(Exception):
    pass


class ReconnectWebsocket:
    AUTH_DICT = {}

    def __init__(self, loop, client, coroutine, error_handler):
        self._loop = loop
        self._coroutine = coroutine
        self._conn = None
        self._client = client
        self._socket = None
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
        performs authorizes websocket and receives messages
        """
        print("running")
        keep_waiting = True
        async with ws.connect("wss://api.jockmkt.net/streaming/") as socket:
            print("async with called")
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
        await self.cancel()
        self._connect()

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

    def __init__(self, iterable):
        """Initialize the SocketManager
        """
        self._subscriptions = []
        self.messages = iterable
        self._callback = None
        self._conn = None
        self._loop = None
        self._client = None

    @classmethod
    async def create(cls, loop: asyncio.Event, client, queue: list, exception_handler: typing.Callable,
                     callback: typing.Callable = None):
        """
        create instance of socket manager and reconnect websocket
        **KWARGS uses
        """
        self = JockmktSocketManager(queue)
        self._loop = loop
        self._callback = callback
        self._error_handler = exception_handler
        self._conn = ReconnectWebsocket(loop, client, self._recv, self._error_handler)
        return self

    async def reconnect(self):
        await self._conn.reconnect()

    @staticmethod
    def _wsfeed_case_switcher(obj, msg):
        match obj:
            case 'error':
                raise Exception(f'{msg}')
            case 'tradeable':
                return Tradeable(msg['tradeable'])
            case 'game':
                return Game(msg['game'])
            case 'event':
                return Event(msg['event'])
            case 'entry':
                return Entry(msg['entry'])
            case 'position':
                return Position(msg['position'])
            case 'order':
                return Order(msg['order'])

    async def exception_handler(self, **kwargs):
        await self._error_handler(kwargs)

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
            print('callback')
            await self._callback(msg)

    async def subscribe(self, topic: str, id: str = None, league: str = None):
        """
        self-explanatory
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
