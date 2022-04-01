import requests
import json
from exception import JockAPIException
from objects import Team, Game, GameLog, Event, Tradeable, Entry, Order, Position, AccountActivity, Entity, \
    _case_switch_ent


class Client(object):
    API_VERSION = 'v1'
    BASE_URL = 'https://api.jockmkt.net'
    _AUTH_TOKEN = {}

    def __init__(self, secret, api_key, request_params=None):
        self.secret = secret
        self.api_key = api_key
        self._request_params = request_params
        _AUTH_TOKEN = self._get_auth_token()
        self.balance = self._get_account_bal()

    def _create_path(self, path, api_version=None):
        api_version = api_version or self.API_VERSION
        return '/{}/{}'.format(api_version, path)

    def _get_auth_token(self):
        payload = {
            'grant_type': 'client_credentials',
            'key': str(self.api_key),
            'secret': str(self.secret)
        }
        response = requests.post(f'{self.BASE_URL}/{self.API_VERSION}/oauth/tokens', data=payload).json()
        if response['status'] == 'error':
            raise KeyError("Your authorization keys are not valid!")
        self.token = {'Authorization': 'Bearer ' + response['token']['access_token']}
        return self.token

    def _request(self, method, path, api_version=None, **kwargs) -> json:
        if self._request_params:
            kwargs.update(self._request_params)
        kwargs['data'] = kwargs.get('data', {})
        kwargs['params'] = kwargs.get('params', {})

        full_path = self._create_path(path, api_version)

        if method == 'get':
            if kwargs['data']:
                kwargs['payload'] = kwargs['data']
            elif kwargs['params']:
                kwargs['payload'] = kwargs['params']
            else:
                kwargs['payload'] = {}
            response = requests.get('{}{}'.format(self.BASE_URL, full_path), params=kwargs['payload'],
                                    headers=self.token)

        if method == 'post':
            if kwargs['data']:
                kwargs['payload'] = kwargs['data']
            elif kwargs['params']:
                kwargs['payload'] = kwargs['params']
            else:
                kwargs['payload'] = {}
            response = requests.post('{}{}'.format(self.BASE_URL, full_path), data=kwargs['payload'],
                                     headers=self.token)

        if method == 'delete':
            response = requests.delete('{}{}'.format(self.BASE_URL, full_path), headers=self.token)

        res = self._handle_response(response)
        return res

    @staticmethod
    def _handle_response(json_response):
        """helper to handle api responses and determine errors
        """
        if not str(json_response.status_code).startswith('2'):
            raise JockAPIException(json_response)
        try:
            res = json_response.json()
            return res
        except ValueError:
            raise JockAPIException('Invalid Response: %s' % json_response.text)

    def _throttle_requests(self, func):
        pass

    def _get(self, path, api_version=None, **kwargs):
        return self._request('get', path, api_version, **kwargs)

    def _post(self, path, api_version=None, **kwargs):
        return self._request('post', path, api_version, **kwargs)

    def _delete(self, path, api_version=None, **kwargs):
        return self._request('delete', path, api_version, **kwargs)

    def _get_account_bal(self):
        return round(self._get("balances")['balances'][0]['buying_power'], 2)

    def get_teams(self, start: int = 0, league: str = None) -> list[Team]:
        """provides a list of teams for all or chosen leagues that have team structure.
        displays only the first page, the user can paginate via:
        for i in range(n):
            get_teams(league = x, start = i)

        keyword args:
            start -- default: 0 (first 100 responses)
            league -- default: None (Any), or nba, nfl, mlb, nhl, nascar (lowercase)
        """
        teams = []
        params = {'start': str(start * 100), 'limit': '100'}
        if league is not None:
            params['league'] = league
        res = self._get('teams', params=params)
        print('status: ' + res['status'])
        print('start: ' + str(res['start']))
        print('limit: ' + str(res['limit']))
        print('count: ' + str(res['count']))
        for team in res['teams']:
            teams.append(Team(team))
        return teams

    def get_team(self, team_id: str) -> Team:
        """fetch a specific entity based on their entity id

        Keyword args:
            team_id: required (str) e.g. "team_8fe94ef0d1f0a00e1285301c4092650f"
        """
        team = self._get(f"teams/{team_id}")['team']
        return Team(team)

    def get_entities(self, start: int = 0, include_team: bool = True, league: str = None) -> list[Entity]:
        """fetch entities (players of any sport)
        the user will have to paginate i.e.
            for i in range(n):
                get_entities(start=i)
        
        Keyword args:
            start -- default: 0 (first 100 responses)
            include_team -- default: True (bool), or False to drop team info
            league -- default: Any, or (str) nba, nfl, mlb, nhl, nascar, pga
        """

        params = {}
        entities = []
        if league is not None:
            params['league'] = league
        if include_team:
            params['include'] = 'team'
        params['start'] = start
        params['limit'] = '100'
        res = self._get("entities", params=params)
        print('status: ' + res['status'])
        print('start: ' + str(res['start']))
        print('limit: ' + str(res['limit']))
        print('count: ' + str(res['count']))
        for entity in res['entities']:
            entities.append(_case_switch_ent(entity))
        return entities

    def get_entity(self, entity_id: str, include_team: bool = False) -> Entity:
        """fetch a specific entity based on their entity id

        Keyword args:
            entity_id: required (str) e.g. en_12d0c14aa5dfd232a0298a737f5a59fc
            include_team: option, default: False (bool), True includes team information
        """
        if include_team:
            params = {'include': 'team'}
        else:
            params = {}
        ent = self._get(f"entities/{entity_id}", params=params)['entity']
        return _case_switch_ent(ent)

    def get_games(self, start: int = 0, limit: int = 100, league: str = None) -> list[Game]:
        """provides a list of teams for all or chosen leagues that have team structure
        the user will have to paginate.
        i.e. for i in range(n):
                get_games(start=i)

        keyword args:
            start -- default: 0 (int), which page of games the user wishes to see
            limit -- default: 100, displays chosen number of relevant events
            league -- default: None (Any), or nba, nfl, mlb, nhl, nascar, pga
        """
        params = {}
        response = []
        params['start'] = start * limit
        params['limit'] = limit
        if league is not None:
            params['league'] = league
        res = self._get('games', params=params)
        print('status: ' + res['status'])
        print('start: ' + str(res['start']))
        print('limit: ' + str(res['limit']))
        print('count: ' + str(res['count']))
        for game in res['games']:
            response.append(Game(game))
        return response

    def get_game(self, game_id: str) -> Game:
        """fetch a specific entity based on their entity id

        Keyword args:
        game_id -- required, str, e.g. "game_60bb686586eaf95a5e8dafa3823d89cb"
        """
        return Game(self._get(f"games/{game_id}")['game'])

    def get_game_logs(self, start: int = 0, limit: int = 100, log_id: str = None, entity_id: str = None,
                      game_id: str = None, include_ent: bool = False, include_game: bool = False,
                      include_team: bool = False) -> list[GameLog]:
        """fetch game logs

        Keyword args:
        Optional:
            start -- default: 0 (int), which page of games the user wishes to see
            limit -- default: 100, displays chosen number of most recent logs, max 100
            log_id -- str or list, filter for a specific game log. e.g. "gl_60cde7f973f9e00674785e5e144a802b"
            entity_id -- str, filter all game logs for a specific player, e.g. "en_67c8368a3905f8beee69393ccec854e5"
            game_id -- str, filter all game logs for all players in a specific game,
            e.g. "game_60cde69ee06e791b99ed71e6013fc4a7"
            include_ent -- bool, if True, returns entity information attached to the game log (entity name, team, etc.)
            include_game -- bool, if True, returns game information (game name, teams, status)
            include_team -- bool, if True, returns team information (team name, location, league, etc.)
        """
        params = {}
        include = []
        response = []
        if log_id is not None:
            params['id'] = log_id
        if entity_id is not None:
            params['entity_id'] = entity_id
        if game_id is not None:
            params['game_id'] = game_id
        if include_game:
            include.append('game')  # can be computationally costly for golf events, be careful
        if include_ent:
            include.append('entity')
        if include_team:
            include.append('team')
        if len(include) != 0:
            params['include'] = str(include)
        params['start'] = start * limit
        params['limit'] = limit
        res = self._get("game_logs", params=params)
        print('status: ' + res['status'])
        print('start: ' + str(res['start']))
        print('limit: ' + str(res['limit']))
        print('count: ' + str(res['count']))
        for log in res['game_logs']:
            print(log)
            response.append(GameLog(log))
        return response

    def get_events(self, start: int = 0, limit: int = 25, league: str = None, include_sims: bool = False) \
            -> list[Event]:
        """Populates event objects with recent and upcoming events

        Keyword args:
            start -- default: 0 (int), which page of games the user wishes to see
            limit -- default: 25, displays chosen number recent and upcoming events
            league -- default: None (Any), or nba, nfl, mlb, nhl, nascar, pga
            include_sims -- default: False (bool), if True, will return Horse Sims for test use
        """
        list_events = []
        data = {'start': str(start * limit), 'limit': limit}
        if league is not None:
            data['league'] = league
        res = self._get('events', data=data)
        for event in res['events']:
            if event['league'] != 'simulated_horse_racing':
                list_events.append(Event(event))
            elif include_sims:
                list_events.append(Event(event))
        return list_events

    def get_event(self, event_id: str) -> Event:
        """fetch a particular event, by default includes games, payouts and tradeables. This is easier than
        pulling payouts, tradeables, and games separately

        Keyword args:
        Required:
            event_id -- str, the event_id for your chosen event, e.g. evt_60dbec530d2197a973c5dddcf6f65e12
        """
        params = {}
        include = ['tradeables.entity', 'games', 'payouts']
        params['include'] = str(include)
        res = self._get(f"events/{event_id}", params=params)
        return Event(res['event'])

    def get_event_payouts(self, event_id: str) -> json:  # should this be appended to the event object itself?
        """get payouts for each rank of an event

        Keyword args:
        Required:
            event_id -- str, the event_id for your chosen event, e.g. evt_60dbec530d2197a973c5dddcf6f65e12
        """
        return self._get(f"events/{event_id}/payouts")

    def get_event_games(self, event_id: str) -> list[Game]:
        """get all games in an event

        Keyword args:
        Required:
            event_id -- str, the event_id for your chosen event, e.g. evt_60dbec530d2197a973c5dddcf6f65e12
        """
        games = []
        res = self._get(f"events/{event_id}/games")
        for game in res['games']:
            games.append(Game(game))
        return games

    def get_event_tradeables(self, event_id: str) -> list[Tradeable]:
        """get all tradeables in an event

        Keyword args:
        Required:
            event_id -- str, the event_id for your chosen event, e.g. evt_60dbec530d2197a973c5dddcf6f65e12
        """
        res = self._get(f"events/{event_id}/tradeables")
        tradeables = []
        for tdbl in res['tradeables']:
            tradeables.append(Tradeable(tdbl))
        return tradeables

    def get_entries(self, start: int = 0, limit: int = 10, include_payouts: bool = False,
                    include_tradeables: bool = False) -> list[Entry]:
        """obtain information about events a user has entered

        Keyword args:
        Optional:
            start -- default: 0 (int), which page of games the user wishes to see
            limit -- default: 10 (int), how many recent entries the user would like to see
            include_payouts -- default: False, include the payouts for each rank of an event
            include_tradeables -- default: False, if True, includes all tradeables participating in the event
            (id, fpts, event rank, prices, stats, etc.)
        """
        params = {'start': start * limit, 'limit': limit}
        include = ['event']
        if include_payouts:
            include.append('payouts')
        if include_tradeables:
            include.append('payouts.tradeable')
        params['include'] = str(include)
        print(params)
        response_list = []
        res = self._get("entries", params=params)
        print('status: ' + res['status'])
        print('start: ' + str(res['start']))
        print('limit: ' + str(res['limit']))
        print('count: ' + str(res['count']))
        for entry in res['entries']:
            response_list.append(entry)

            # potential todo: add if loop to display only the most recent few events, and calculate profit and loss
            #  for the event (including fees, $ invested, etc.)
        return response_list

    def calculate_pnl(self, entry_id: str):
        pass

    def get_entry(self, entry_id: str, include_event=False, include_payouts=False,
                  include_tradeables=False) -> Entry:
        """obtain information about events a user has entered

        Keyword args:
        Optional:
            qty -- default: 50, number of events the user wishes to display
            include_event -- default: False, include event information
            include_payouts -- default: False, include the payouts for each rank of an event (only displayed post-event)
            include_tradeables -- default: False, if True, includes all tradeables participating in the event
            (only displayed post-event)
            (provides information about positions/payouts and their underlying tradeables)
        """
        params = {}
        include = []
        if include_event:
            include.append('event')
        if include_payouts:
            include.append('payouts')
        if include_tradeables:
            include.append('payouts.tradeable')
        if len(include) != 0:
            params['include'] = str(include)
        print(params)
        entry = self._get(f"entries/{entry_id}", params=params)
        print(entry)
        return Entry(entry['entry'])

    def create_entry(self, event_id: str) -> json:
        """create an entry to an event given an event_id e.g. evt_60dbec530d2197a973c5dddcf6f65e12
        """
        return self._post(f"entries", data={'event_id': event_id})

    _order_cache = []

    # @staticmethod
    # def _order_counter(self, func):
    #     def _helper(*args, **kwargs):
    #         pass
    #     pass

    def place_order(self, id: str, price: int, side: str = 'buy', phase: str = 'ipo', qty: int = 1, **kwargs) -> json:
        """
        TODO: exception handling, if response to an order is TOO MANY ORDERS, add the order back to the queue
        add functionality for 'market' orders
        add functionality for take_profit/stop_loss
        add functionality for fill or kill/good until
        add functionality to allow user to place order at JockMkt estimated price

        keyword args:
            id -- your player's tradeable id, which can be obtained by...
            side -- default: buy, buy or sell (sell only available during live trading
            phase -- default: ipo or live
            qty -- default: 1, number of shares you wish to purchase
            price -- bid/ask per share. Do not include your fees.

        optional:
            order_size -- input a total amount to spend and calculate desired number of shares automatically
        """
        if price > 25:
            price = 25

        if 'order_size' in kwargs:
            size = kwargs.get('order_size', 0)
            qty = size // price

        price = "{:.2f}".format(price)

        order = {'tradeable_id': id, 'side': side, 'type': 'limit', 'phase': phase, 'quantity': str(qty),
                 'limit_price': str(price)}
        order_response = self._post('orders', data=order)
        print(order_response)

        return order_response

    # NOTE: the docs for order object > status contain 'outbid' twice

    def get_orders(self, start=0, limit: int = 100, event_id: str = None, active: bool = False,
                   updated_after: int = None):
        """get all of a user's orders
        Keyword args:
        optional:
            qty -- int, number of orders the user wishes to display
            event_id -- str, orders relating to a specific event
            active -- bool, include only orders marked (created or accepted, not filled, canceled, outbid, or expired)
            updated_after -- int, ms timestamp 13 digits, includes orders only after the timestamp
        """
        params = {'start': start * limit, 'limit': limit}
        orders = []
        if event_id is not None:
            params['event_id'] = str(event_id)
        if active:
            params['active'] = str(True)
        if updated_after is not None:
            params['updated_after'] = str(updated_after)
        orders_response = self._get('orders', params=params)
        print('status: ' + orders_response['status'])
        print('start: ' + str(orders_response['start']))
        print('limit: ' + str(orders_response['limit']))
        print('count: ' + str(orders_response['count']))
        for order in orders_response['orders']:
            orders.append(Order(order))
        return orders

    def get_order(self, order_id: str) -> Order:
        """get information about a specific order

        Keyword args:
        required:
            order_id -- str, e.g. ord_601b5ad6538ec34875ee1687c4a657f8
        """
        return Order(self._get(f"orders/{order_id}")['order'])

    def delete_order(self, order_id: str) -> json:
        """delete a specific order

        Keyword args:
        required:
            order_id -- str, e.g. ord_601b5ad6538ec34875ee1687c4a657f8
        """
        deletion_res = self._delete(f"orders/{order_id}")
        if deletion_res['status'] == 'success':
            print('order successfully canceled')
        print(deletion_res)
        return deletion_res

    def get_positions(self) -> list[Position]:
        """returns a user's open positions in all current events
        """
        positions = []
        positions_res = self._get("positions")
        print('status: ' + positions_res['status'])
        print('count: ' + str(positions_res['count']))
        for position in positions_res['positions']:
            positions.append(Position(position))
        return positions

    def get_account_activity(self, start: int = 0, limit: int = 100) -> list[AccountActivity]:
        params = {'start': str(start * limit), 'limit': limit}
        activity_res = self._get('account/activity', params=params)
        acct_activity = []
        for aact in activity_res['activity']:
            acct_activity.append(AccountActivity(aact))
        return acct_activity

    @staticmethod
    def fetch_all(func, pages: int) -> object:
        pass
