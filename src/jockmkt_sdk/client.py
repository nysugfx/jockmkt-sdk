import requests
import json
from datetime import datetime
from .exception import JockAPIException
from .objects import Team, Game, GameLog, Event, Tradeable, Entry, Order, Position, AccountActivity, Entity, \
    _case_switch_ent


class Client(object):
    """The user should initialize an instance of this class and then call .get_auth_token(secret, api_key) to use other
    class methods.

    :ivar ACCOUNT: The user's account information, including their balances and the auth token they generate.
    """
    API_VERSION = 'v1'
    BASE_URL = 'https://api.jockmkt.net'
    _AUTH_TOKEN = {}
    _EXPIRATION = None
    LEAGUES = ['nba', 'nfl', 'nhl', 'pga', 'mlb', 'nascar']
    MLB_SCORING = {'at_bat': 0.5, 'single': 2.5, 'double': 3, 'triple': 3.5, 'home_run': 4, 'walk': 2, 'run': 2,
                   'rbi': 2, 'stolen_base': 3, 'strikeout': -1}
    NFL_SCORING = {'pass_yards': 0.04, 'pass_td': 4, 'int_thrown': -3, 'rush_yards': 0.1, 'rush_td': 6, 'reception': 1,
                   'receiving_yards': 0.1, 'receiving_td': 6, 'return_td': 6, 'two_pt_conversion': 2, 'fumble_lost': -3,
                   '100_yd_passing_bonus': 1, '100_yd_rushing_bonus': 3, '100_yd_receiving_bonus': 3}
    NBA_SCORING = {'point': 1, '10_pt_bonus': 1.5, '3pm': 0.5, 'rebound': 1.25, 'assist': 1.5, 'steal': 2, 'block': 2,
                   'turnover': -0.5, 'missed_fg': -0.5}
    NHL_SCORING = {'goal': 8.5, 'assist': 5, 'shot_on_goal': 1.5, 'blocked_shot': 2, 'shorthanded_pt': 2,
                   'shootout_goal': 1.5, 'hat_trick': 3, '3_plus_blocks': 3, '3_plus_pts': 3, 'penalty_mins': -0.5,
                   'hits': 1, 'goalie_win': 6, 'goalie_save': 0.5, 'goal_allowed': -3.5, 'ot_loss': 2,
                   '35_plus_saves': 3, 'shutout': 4}
    PGA_SCORING = {'win': 5, 'albatross': 4, 'eagle': 3, 'birdie': 2, 'par': 1, 'bogey': 0, 'double_bogey': -1,
                   'triple_bogey': -2, 'quadruple_bogey': -3, 'quintuple_bogey': -4}
    NASCAR_SCORING = {'lap_complete': 1, 'position': -1, 'win': 10, 'start_bonus': 40}
    ACCOUNT = {}

    def __init__(self, request_params=None):
        self._request_params = request_params

    def _create_path(self, path, api_version=None):
        """generates a path for self._request
        """
        api_version = api_version or self.API_VERSION
        return '/{}/{}'.format(api_version, path)

    @staticmethod
    def get_auth_token(secret_key: str, api_key: str) -> dict:
        """obtains the user's auth token using provided api and secret keys, generating a BearerAuth header. It also allows the user to call .get_account to retreive relevant information about their accounts, including balances etc.

        :param secret_key: The user's Jock MKT provided secret key.
        :type secret_key:  str, required
        :param api_key:    The user's api key, starting with jm\_key\_
        :type api_key:     str, required
        """
        payload = {
            'grant_type': 'client_credentials',
            'key': str(api_key),
            'secret': str(secret_key)
        }

        response = requests.post(f'{Client.BASE_URL}/{Client.API_VERSION}/oauth/tokens', data=payload).json()
        print(response)
        if response['status'] == 'error':
            raise KeyError("Your authorization keys are not valid!")

        expiry = response['token']['expired_at']/1000
        print('Your token will expire at:', datetime.fromtimestamp(expiry).strftime("%Y-%m-%d %H:%M %p"))
        Client._EXPIRATION = expiry
        Client._AUTH_TOKEN = {'Authorization': 'Bearer ' + response['token']['access_token']}

        account = requests.get(f'{Client.BASE_URL}/{Client.API_VERSION}/account', headers=Client._AUTH_TOKEN).json()
        acct = account['account']
        balance = requests.get(f'{Client.BASE_URL}/{Client.API_VERSION}/balances', headers=Client._AUTH_TOKEN).json()
        bal = balance['balances']

        account_dict = {
            acct['display_name']: {
                'info': acct,
                'balances': bal,
                'keys': {'secret_key': secret_key, 'api_key': api_key},
                'token': Client._AUTH_TOKEN
            }
        }
        Client.ACCOUNT = account_dict

    def _request(self, method, path, api_version=None, **kwargs) -> dict:
        """method by which all requests are made
        """
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
                                    headers=self._AUTH_TOKEN)

        if method == 'post':
            if kwargs['data']:
                kwargs['payload'] = kwargs['data']
            elif kwargs['params']:
                kwargs['payload'] = kwargs['params']
            else:
                kwargs['payload'] = {}
            response = requests.post('{}{}'.format(self.BASE_URL, full_path), data=kwargs['payload'],
                                     headers=self._AUTH_TOKEN)

        if method == 'delete':
            response = requests.delete('{}{}'.format(self.BASE_URL, full_path), headers=self._AUTH_TOKEN)

        res = self._handle_response(response)
        return res

    @staticmethod
    def _handle_response(json_response):
        """helper to handle api responses and determine exceptions
        """
        if not str(json_response.status_code).startswith('2'):
            raise JockAPIException(json_response)
        try:
            res = json_response.json()
            return res
        except ValueError:
            raise JockAPIException('Invalid Response: %s' % json_response.text)

    def _throttle_requests(self, func):
        """method designed to throttle certain user requests
        """
        pass

    def _get(self, path, api_version=None, **kwargs):
        """method for get requests
        """
        return self._request('get', path, api_version, **kwargs)

    def _post(self, path, api_version=None, **kwargs):
        """method for post requests
        """
        return self._request('post', path, api_version, **kwargs)

    def _delete(self, path, api_version=None, **kwargs):
        """method for delete requests, used exclusively for order deletion
        """
        return self._request('delete', path, api_version, **kwargs)

    def _get_account_bal(self):
        """method retreiving user's USD balance
        """
        return self._get("balances")['balances']

    def get_account(self):
        """
        method for retreiving a user's account information. Must be run AFTER get_auth_token.

        :returns: a dict of relevant account information
        :rtype:   dict
        """
        return self.ACCOUNT

    def get_scoring(self, league):
        """
        method to retreive information about scoring for different league events

        :param league: the league for which you'd like to retreive scoring
        :type league:  str, required

        :returns:      scoring information for the chosen league
        :rtype:        dict
        """
        scoring_dict = {'mlb': self.MLB_SCORING,
                        'nhl': self.NHL_SCORING,
                        'nba': self.NBA_SCORING,
                        'pga': self.PGA_SCORING,
                        'nfl': self.NFL_SCORING,
                        'nascar': self.NASCAR_SCORING}

        return scoring_dict[league]

    def get_teams(self, start: int = 0, league: str = None) -> list[Team]:
        """provides a list of teams for all or chosen leagues that have team structure.
        displays only the first page, the user can paginate via:

        :param start: Which page the user wants to display. Default: 0 (first 100 teams)
        :type start: int, optional
        :param league: which league the user is searching for teams, one of: ['nba', 'nfl', 'nhl', 'pga', 'mlb', 'nascar']
        :type league: str, optional

        :returns: a list of Team objects
        :rtype: list[Team]
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
        """fetch a specific team based on their team id

        :param team_id: a team id, starting with team\_ (e.g. "team_8fe94ef0d1f0a00e1285301c4092650f")
        :type team_id: str, required

        :returns: a dictionary with team information
        :rtype: objects.Team
        """
        team = self._get(f"teams/{team_id}")['team']
        return Team(team)

    def get_entities(self, start: int = 0, limit: int = 100, include_team: bool = True, league: str = None) \
            -> list[Entity]:
        """fetch entities (players of any sport). The user will have to paginate.

        :param start: page at which the user wants to start their search, default: 0 (first page of entities)
        :type start: int, optional
        :param limit: number of entities the user wants to display, default: 100 (displays 100 entities)
        :type limit: int, optional
        :param include_team: include team information for the entity, default: False
        :type include_team: bool, optional
        :param league: filter by league, must be one of: ['nba', 'nfl', 'nhl', 'pga', 'mlb', 'nascar']
        :type league: str, optional

        :return: a list of league-specific Entity objects
        :rtype: list[objects.Entity]
        """
        params = {}
        entities = []
        if league is not None:
            params['league'] = league
        if include_team:
            params['include'] = 'team'
        params['start'] = start * limit
        params['limit'] = limit
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

        :param entity_id: The chosen entity's id (e.g "en_9af7d442f918404feced51d877989aa0")
        :type entity_id: str, required
        :param include_team: include team information for the entity, default: False
        :type include_team: bool, optional

        :returns: a league-specific entity object, one of: :class:`objects.NBAEntity`, :class:`objects.NFLEntity`, :class:`objects.NHLEntity`, :class:`objects.NascarEntity`, :class:`objects.PGAEntity`, :class:`MLBEntity` which are all children of the :class:`objects.Entity`
        :rtype: objects.Entity

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

        :param start: page at which the user wants to start their search, default: 0 (first page of games)
        :type start: int, optioanl
        :param limit: number of entities the user wants to display, default: 100 (displays 100 recent and upcoming games)
        :type limit: int, optional
        :param league: filter by league, must be one of: ['nba', 'nfl', 'nhl', 'pga', 'mlb', 'nascar']
        :type league: str, optional

        :returns: A list of :class:`objects.Game` objects
        :rtype: list

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

        :param game_id: a string of the game id (e.g. "game_60bb686586eaf95a5e8dafa3823d89cb")
        :type game_id: str, required

        :returns: a :class:`objects.Game` object, containing the relevant fields
        :rtype: objects.Game

        """
        return Game(self._get(f"games/{game_id}")['game'])

    def get_game_logs(self, start: int = 0, limit: int = 100, log_id: str = None, entity_id: str = None,
                      game_id: str = None, include_ent: bool = False, include_game: bool = False,
                      include_team: bool = False) -> list[GameLog]:
        """fetch game logs

        :param start: Page at which the user wants to start their search, default: 0
            (first page of game_logs)
        :type start: int, optional
        :param limit: Number of entities the user wants to display, default: 100 (displays 100 game_logs)
        :type limit: int, optional
        :param log_id: Filter for a specific log or list of logs
            (e.g. "gl_60cde7f973f9e00674785e5e144a802b")
        :type log_id: str or list of str, optional
        :param entity_id: Filter all game logs for a specific player,
            (e.g. "en_67c8368a3905f8beee69393ccec854e5")
        :type entity_id: str, optional
        :param game_id: filter all game logs for all players in a specific game,
            (e.g. "game_60cde69ee06e791b99ed71e6013fc4a7")
        :type game_id: str, optional
        :param include_ent: Returns entity information attached to the game log (entity name, team, etc.)
        :type include_ent: bool, optional
        :param include_game: Returns game information (game name, teams, status)
        :type include_game: bool, optional
        :param include_team: Returns team information (team name, location, league, etc.)
        :type include_team: bool, optional

        :returns: a list of :class:`objects.GameLogs`, containing scoring information for a player in a specific game
        :rtype: objects.GameLog

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

        :param start: Page at which the user wants to start their search, default: 0 (first page of events)
        :type start: int, optional
        :param limit: Number of entities the user wants to display,
            default: 25 (displays 25 recent and upcoming events)
        :type limit: int, optional
        :param league: Filter by league, must be one of: ['nba', 'nfl', 'nhl', 'pga', 'mlb', 'nascar']
        :type league: str, optional
        :param include_sims: Will return all events, including Horse Sims for test use
        :type include_sims: bool, optional

        :returns: list of :class:`objects.Events`, containing the event_id and information for each
        :rtype: list[objects.Event]

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

        :param event_id: The event_id for your chosen event, (e.g. evt_60dbec530d2197a973c5dddcf6f65e12)
        :type event_id: str, required

        :returns: An :class:`objects.Event`, including its payouts, tradeables and games
        :rtype: objects.Event

        """
        params = {}
        include = ['tradeables.entity', 'games', 'payouts']
        params['include'] = str(include)
        res = self._get(f"events/{event_id}", params=params)
        return Event(res['event'])

    def get_event_payouts(self, event_id: str) -> dict:  # should this be appended to the event object itself?
        """get payouts for each rank of an event

        :param event_id: The event_id for your chosen event, (e.g. evt_60dbec530d2197a973c5dddcf6f65e12)
        :type event_id: str, required

        :returns: a dictionary of the chosen event's payouts
        :rtype: dict

        """
        return self._get(f"events/{event_id}/payouts")

    def get_event_games(self, event_id: str) -> list[Game]:
        """get all games in an event

        :param event_id: the event_id for your chosen event, (e.g. evt_60dbec530d2197a973c5dddcf6f65e12)
        :type event_id: str, required

        :returns: a list of event-relevant :class:`objects.Game` objects
        :rtype: list[objects.Game]

        """
        games = []
        res = self._get(f"events/{event_id}/games")
        for game in res['games']:
            games.append(Game(game))
        return games

    def get_event_tradeables(self, event_id: str) -> list[Tradeable]:
        """get all tradeables in an event

        :param event_id: The event_id for your chosen event, (e.g. evt_60dbec530d2197a973c5dddcf6f65e12)
        :type event_id: str, required

        :returns: a list of :class:`objects.Tradeable` objects participating in the chosen event
        :rtype: list[objects.Tradeable]

        """
        res = self._get(f"events/{event_id}/tradeables")
        tradeables = []
        for tdbl in res['tradeables']:
            tradeables.append(Tradeable(tdbl))
        return tradeables

    def get_entries(self, start: int = 0, limit: int = 10, include_payouts: bool = False,
                    include_tradeables: bool = False) -> list[Entry]:
        """obtain information about events a user has entered

        :param start: Page at which the user wants to start their search,
            default: 0 (first page of entries)
        :type start: int, optional
        :param limit: Number of entities the user wants to display, default: 10 (displays 10 recent
            and upcoming entries)
        :type limit: int, optional
        :param include_payouts: Option to include payouts of completed entries, default: False
        :type include_payouts: bool, optional
        :param include_tradeables: Option to include entry-relevant :class:`objects.Tradeable` objects
        :type include_tradeables: bool, optional

        :returns: A list of :class:`objects.Entry` objects
        :rtype: object.Entity

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
        return response_list

    def get_entry(self, entry_id: str, include_event: bool = False, include_payouts: bool = False,
                  include_tradeables: bool = False) -> Entry:
        """Method to obtain information about an event that a user has entered

        :param entry_id: The entry_id for which the user wishes to get information
            (e.g. evt_60dbec530d2197a973c5dddcf6f65e12)
        :type entry_id: str, required
        :param include_event: Include :class:`objects.Event` information related to the entry
        :type include_event: bool, optional
        :param include_payouts: Include payouts for the user's holdings of a completed event
        :type include_payouts: bool, optional
        :param include_tradeables: Include relevant event :class:`object.Tradeable` objects
        :type include_tradeables: bool, optional

        :returns: a list of :class:`objects.Entry` objects, containing the user's chosen fields
        :rtype: objects.Entity

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

    def create_entry(self, event_id: str) -> dict:
        """create an entry to an event given an event_id e.g. evt_60dbec530d2197a973c5dddcf6f65e12
        """
        return self._post(f"entries", data={'event_id': event_id})

    def place_order(self, id: str, price: int, side: str = 'buy', phase: str = 'ipo', qty: int = 1, **kwargs) -> dict:
        """
        Places an order of the user's chosen tradeable (player) and the chosen price. It defaults to  buy 1 share
        during the ipo phase. The user may specify an amount of money they want to buy and automatically buy x shares at
        the chosen price (param: order_size), such that the total cost is less than their specified amount. If the user
        wants to make a live they must specify phase='live', or if they want to sell a share side='sell'.

        :param id: The chosen player's tradeable id, obtained by calling a Tradeable object
        :type id: str, required
        :param price: The user's chosen price at which to place their order
        :type price: int, required
        :param side: default: 'buy' - the user must specify 'sell' if they wish to sell
        :type side: str, optional
        :param phase: default: 'ipo' - If the Event.status is 'ipo', should be ipo, else specify 'live'
        :type phase: str, optional
        :param qty: default: 1 - The desired number of shares the user wants to buy, the user may specify order_size instead.
        :type qty: int, optional
        :param order_size: The user can specify the total amount they wish to spend on shares of a player. Calculated by: (order_size)//price (it will always round down)
        :type order_size: int, optional

        :returns: A json response with information about the order that was sent

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

    def get_orders(self, start: int = 0, limit: int = 100, event_id: str = None, active: bool = False,
                   updated_after: int = None):
        """Get all of a user's orders. The user is required to paginate if they want to see more than 1 page

        :param start: Page at which the user wants to start their search, default: 0 (first page of entities)
        :type start: int, optional
        :param limit: Number of entities the user wants to display, default: 100 (displays 100 entities)
        :type limit: int, optional
        :param event_id: the event_id for your chosen event, (e.g. evt_60dbec530d2197a973c5dddcf6f65e12)
        :type event_id: str, optional
        :param active: Whether to display only orders that are active (either created or accepted),
            default = False
        :type active: bool, optional
        :param updated_after: filter orders updated after 13 digit epoch timestamp (orders with fills,
            partial fills, cancellations, outbids, etc. after that time)
        :type updated_after: int, optional

        :returns: a list of :class:`objects.Order` objects
        :rtype: objects.Order

        """
        params = {'start': start * limit, 'limit': limit}
        orders = []
        if event_id is not None:
            params['event_id'] = str(event_id)
        if active:
            params['active'] = 'true'
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

        :param order_id: Order id for which the user is searching `(e.g. ord_601b5ad6538ec34875ee1687c4a657f8)`
        :type order_id: str, required

        :returns: :class:`objects.Order`
        :rtype: Order

        """
        return Order(self._get(f"orders/{order_id}")['order'])

    def delete_order(self, order_id: str) -> dict:
        """delete a specific order

        :param order_id: order id for which the user is attempting to delete
            (e.g. ord_601b5ad6538ec34875ee1687c4a657f8)
        :type order_id: str, required

        :returns: json response with information about the order deletion

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
        """
        returns a user's most recent account activity

        :param start: the page of account activity which the user wants to display,
            default = 0 (first page of responses)
        :type start: int, optional
        :param limit: the quantitiy of account activity objects the user wants to see, default = 100
        :type limit: int, optional

        :returns: a list of :class:`objects.AccountActivity`
        :rtype: list[AccountActivity]

        """
        params = {'start': str(start * limit), 'limit': limit}
        activity_res = self._get('account/activity', params=params)
        acct_activity = []
        for aact in activity_res['activity']:
            acct_activity.append(AccountActivity(aact))
        return acct_activity
