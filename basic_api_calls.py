import requests
from datetime import datetime, timedelta
import keys

class JockAPIException(Exception):
    """
    code -- type -- explanation
    400 -- bad_request -- required parameter not included or typo in required parameter
    401 -- not_authorized -- token is not valid; expired or keys not functioning
    402 -- request_failed -- event status error, user has not joined event, insufficient funds
    404 -- not_found -- incorrect api endpoint
    429 -- rate_limit -- max 10 orders (post, delete) per minute, max 250 other requests per minute. This limit resets at the beginning of every new clock minute (e.g 12:00:00, 12:01:00)
    50x -- internal_error -- request failed due to platform error
    """
    
    def __init__(self, response):
        _error_dict = {
        'bad_request': "try fixing your parameters, or check if you're missing one!",
        'not_authorized': 'Double check your secret keys, or that your auth token is valid',
        'event_status': 'Please wait for the market to open at ...',
        'invalid entry':'', #TODO: create entry to the event
        'not_found': '',
        'rate_limit': 'You have placed too many orders or requests since {}. Please wait until {}.'.format(datetime.now().strftime("%I:%M"), (datetime.now() + timedelta(minutes = 1)).strftime("%I:%M")), #TODO: store the request so that it can be completed at the start of the following minute
    }
        self.code = ""
        self.message = 'unknown error'
        self.helper = ''
        try:
            json_res = response.json()
        except ValueError:
            self.message = response.content
        else:
            if 'error' in json_res:
                self.code = json_res['error']
                self.message = json_res['message']
                self.helper = _error_dict[json_res['error']]
    def _order_error_handler(self):
        pass
        
    def __str__(self):
        return 'JockAPIException {}: {} \n{}'.format(self.code, self.message, self.helper)

class Event:
    def __init__(self, id, name, desc, type, league, status, ipo_start, ipo_end, amt_completed):
        self.id = id
        self.name = name
        self.desc = desc
        self.type = type
        self.status = status
        self.league = league
        self.ipo_start = ipo_start
        self.ipo_end = ipo_end
        self.amt_completed = amt_completed
        self.pnl = None
        self.fees_paid = None
        self.entered = False
        
    def print_event(self):
        print('\nevent_id: ' + self.id, '\nevent_name: ' + self.name, '\ndescription: ' + self.desc, '\ntype: ' + self.type, ' league: ' + self.league, '\nipo_start: ' + str(self.ipo_start), ' ipo_end: ' + str(self.ipo_end), ' amount_completed: ' + str(self.amt_completed), '\n\t profit/loss: ' + str(self.pnl), '  fees_paid: ')


class Client(object):
    API_VERSION = 'v1'
    BASE_URL = 'https://api.jockmkt.net'

    def __init__(self, secret, api_key, request_params = None):
        self.secret = secret
        self.api_key = api_key
        self._request_params = request_params
        self.token = self._get_auth_token()
        self.balance = self._get_account_bal()

    def _create_path(self, path, api_version = None):
        api_version = api_version or self.API_VERSION
        return '/{}/{}'.format(api_version, path)

    def _get_auth_token(self):
            payload = {
                'grant_type' : 'client_credentials',
                'key' : str(self.api_key),
                'secret' : str(self.secret)
            }
            response = requests.post(f'{self.BASE_URL}/{self.API_VERSION}/oauth/tokens', data = payload).json()
            if response['status'] == 'error':
                raise KeyError("Your authorization keys are not valid!")
            else:
                expiration_date = datetime.fromtimestamp(response['token']['expired_at']/1000).strftime("%Y-%m-%d %I:%M %p")
                print(f'\nyour token will expire at: {expiration_date}\n')
            self.token = {'Authorization' : 'Bearer ' + response['token']['access_token']}
            return self.token

    def _request(self, method, path, api_version=None, **kwargs):
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
            response = requests.get('{}{}'.format(self.BASE_URL, full_path), params=kwargs['payload'], headers=self.token)

        if method == 'post':
            if kwargs['data']:
                kwargs['payload'] = kwargs['data']
            elif kwargs['params']:
                kwargs['payload'] = kwargs['params']
            else:
                kwargs['payload'] = {}
            response = requests.post('{}{}'.format(self.BASE_URL, full_path), data=kwargs['payload'], headers=self.token)

        if method == 'delete':
            response = requests.delete('{}{}'.format(self.BASE_URL, full_path), headers=self.token)

        res = self._handle_response(response)
        #TODO: add functionality for response[path]
        return res

    @staticmethod
    def _handle_response(response):
        '''helper to handle api responses and determine errors
        '''
        if not str(response.status_code).startswith('2'):
            raise JockAPIException(response)
        try:
            res = response.json()
            return res
        except ValueError:
            raise JockAPIException('Invalid Response: %s' % response.text)
            
    
    def _get(self, path, api_version=None, **kwargs):
        return self._request('get', path, api_version, **kwargs)

    def _post(self, path, api_version=None, **kwargs):
        return self._request('post', path, api_version, **kwargs)

    def _delete(self, path, api_version=None, **kwargs):
        return self._request('delete', path, api_version, **kwargs)

    def _get_account_bal(self):
        return round(self._get("balances")['balances'][0]['buying_power'], 2)

    def _start_over_100(self):
        """decorator function for requests that require multiple pages of response
        """
        pass

    def get_teams(self, league = None):
        """provides a list of teams for all or chosen leagues that have team structure

        keyword args:
        \tleague -- default: None (Any), or nba, nfl, mlb, nhl, nascar

        note: range default to 1 since there are only 146 total teams 

        TODO: build team class
        """
        if league == None:
            for page in range(1):
                params = {'start': str(page*100), 'limit': '100'}
                return self._get('teams', params = params)
        else:
            params = {'start': '0', 'limit': '100', 'league': league}
            return self._get('teams', params = params)

    def get_some_team(self, team_id):
        """fetch a specific entity based on their entity id

        Keyword args:
        \tteam_id: required (str) e.g "team_8fe94ef0d1f0a00e1285301c4092650f"
        """
        return self._get(f"teams/{team_id}")

    def get_entities(self, qty = 1000, include_team = False, **kwargs):
        """fetch entities (players of any sport)
        
        Keyword args:
        \tleague -- default: Any, or (str) nba, nfl, mlb, nhl, nascar
        \tinclude_team -- default: False (bool), or True to include team info
        \tupdated_after -- default: Any, or (int) ms timestamp (13 digits)
        \tlimit -- default: 1000 #TODO default limits by sports based on # players
        #TODO: build entity class
        """
        params = {}
        response = []
        if 'league' in kwargs:
            params['league'] = kwargs.get('league', "")
        if include_team == True:
            params['include'] = 'team'
        for page in range(int(qty/100)):
            params['start'] = str(page*100)
            params['limit'] = '100'
            res = self._get("entities", params = params)
            for entity in res['entities']:
                response.append(entity)
        return response

    def get_some_entity(self, entity_id, include_team = False):
        """fetch a specific entity based on their entity id

        Keyword args:
        \tentity_id: required (str) e.g en_12d0c14aa5dfd232a0298a737f5a59fc
        \tinclude_team: option, default: False (bool), True includes team information
        """
        if include_team == True:
            params = {'include': 'team'}
        else:
            params = {}

        return self._get(f"entities/{entity_id}", params = params)

    def get_games(self, league = None, qty = 100): 
        """provides a list of teams for all or chosen leagues that have team structure

        keyword args:
        \tleague -- default: None (Any), or nba, nfl, mlb, nhl, nascar
        \tqty -- default: 100 (int), quantity of games the user wishes to see

        TODO: build game class, filter by status etc.
        """
        params = {}
        response = []
        for page in range(int(qty/100)):
            params['start'] = str(page*100)
            params['limit'] = '100'
            if league != None:
                params['league'] = league
            res = self._get('games', params = params)
            for game in res['games']:
                response.append(game)
        return response
    
    def get_some_game(self, game_id):
        """fetch a specific entity based on their entity id

        Keyword args:
        game_id -- required, str, e.g "game_60bb686586eaf95a5e8dafa3823d89cb"
        """
        return self._get(f"games/{game_id}")

    def get_game_logs(self, qty = 100, include_ent = False, include_game = False, include_team = False, **kwargs):
        """fetch game logs

        Keyword args:
        \toptional:
        \tqty -- int, quantity of game logs the user wishes to see
        \tlog_id -- str or list, filter for a specific game log. e.g "gl_60cde7f973f9e00674785e5e144a802b"
        \tentity_id -- str, filter all game logs for a specific player, e.g "en_67c8368a3905f8beee69393ccec854e5"
        \tgame_id -- str, filter all game logs for all players in a specific game, e.g "game_60cde69ee06e791b99ed71e6013fc4a7"
        \tinclude_ent -- bool, if True, returns entity information attached to the game log (entity name, team, etc.)
        \tinclude_game -- bool, if True, returns game information (game name, teams, status)
        \tinclude_team -- bool, if True, returns team information (team name, location, league, etc.)
        """
        params = {}
        include = []
        response = []
        if 'log_id' in kwargs:
            params['id'] = kwargs.get('log_id', '')
        if 'entity_id' in kwargs:
            params['entity_id'] = kwargs.get('entity_id', '')
        if 'game_id' in kwargs:
            params['id'] = kwargs.get('game_id', '')
        if include_game:
            include.append('game')
        if include_ent:
            include.append('entity')
        if include_team:
            include.append('team')
        if len(include) != 0:
            params['include'] = str(include)
        for page in range(int(qty/100)):
            params['start'] = str(page*100)
            params['limit'] = '100'
            print(params)
            res = self._get("game_logs", params = params)
            for log in res['game_logs']:
                response.append(log)
        return response

    def get_upcoming_events(self, qty = 50):
        """Populates event objects with recent and upcoming events

        Keyword args:
        \tqty -- int: default: 50 -- quantity of events the user wishes to populate. No need to adjust this unless your goal is to view historical events
        """
        list_events = []
        data = {}
        for page in range(int(qty/100)):
            if qty <= 100:
                data['start'] = 0 
                data['limit'] = qty
            else:
                data['start'] = str(page*100)
                data['limit'] = str(100)
            res = self._get('events', data=data)
            for event in res['events']:
                if 'horse' not in event['league']:
                    try:
                        amount_completed = event['amount_completed']
                    except:
                        amount_completed = 0
                    list_events.append(Event(event['id'], event['name'], event['description'], event['type'], event['id'], event['status'], datetime.fromtimestamp(int(event['ipo_open_at'])/1000), datetime.fromtimestamp(int(event['live_at_estimated'])/1000), amount_completed))
        return list_events

    def get_some_event(self, event_id, include_games=False, include_payouts=False, include_tradeables=False):
        """fetch a particular event

        Keyword args:
        \tRequired:
        \tevent_id -- str, the event_id for your chosen event, e.g evt_60dbec530d2197a973c5dddcf6f65e12

        \tOptional:
        \tinclude_games -- default: False, include all games that are part of the event
        \tinclude_payouts -- default: False, include the payouts for each rank of an event
        \tinclude_tradeables -- default: False, if True, includes all entities participating in the event (name, fpts, event rank, prices, team, stats, etc.)
        """
        params = {}
        include = []
        if include_games:
            include.append('games')
        if include_payouts:
            include.append('payouts')
        if include_tradeables:
            include.append('tradeables.entity')
        if len(include) != 0:
            params['include'] = str(include)

        return self._get(f"events/{event_id}", params = params)


    def get_event_payouts(self, event_id):
        """get payouts for each rank of an event

        Keyword args:
        \tRequired:
        \tevent_id -- str, the event_id for your chosen event, e.g evt_60dbec530d2197a973c5dddcf6f65e12
        """
        return self._get(f"events/{event_id}/payouts")

    def get_event_games(self, event_id):
        """get all games in an event

        Keyword args:
        \tRequired:
        \tevent_id -- str, the event_id for your chosen event, e.g evt_60dbec530d2197a973c5dddcf6f65e12
        """
        return self._get(f"events/{event_id}/games")

    def get_event_tradeables(self, event_id):
        """get all tradeables in an event

        Keyword args:
        \tRequired:
        \tevent_id -- str, the event_id for your chosen event, e.g evt_60dbec530d2197a973c5dddcf6f65e12
        """
        return self._get(f"events/{event_id}/tradeables")

    def get_entries(self, qty = 100, include_event=False, include_payouts=False, include_tradeables=False):
        """obtain information about events a user has entered

        Keyword args:
        \tOptional:
        \tqty -- default: 50, number of events the user wishes to display
        \tinclude_event -- default: False, include event information
        \tinclude_payouts -- default: False, include the payouts for each rank of an event
        \tinclude_tradeables -- default: False, if True, includes all tradeables participating in the event (id, fpts, event rank, prices, stats, etc.)
        """
        params = {}
        include = []
        response = []
        if include_event:
            include.append('event')
        if include_payouts:
            include.append('payouts')
        if include_tradeables:
            include.append('payouts.tradeable')
        if len(include) != 0:
            params['include'] = str(include)
        for page in range(int(qty/100)):
            params['start'] = str(page*100)
            params['limit'] = '100'
            res = self._get("entries", params = params)
            for entry in res['entries']:
                response.append(entry)

            #TODO: add if loop to display only the most recent few events, and calculate profit and loss for the event (including fees, $ invested, etc.)
        return response
    
    def get_some_entry(self, entry_id, include_event=False, include_payouts=False, include_tradeables=False):
        """obtain information about events a user has entered

        Keyword args:
        \tOptional:
        \tqty -- default: 50, number of events the user wishes to display
        \tinclude_event -- default: False, include event information
        \tinclude_payouts -- default: False, include the payouts for each rank of an event
        \tinclude_tradeables -- default: False, if True, includes all tradeables participating in the event (id, fpts, event rank, prices, stats, etc.)
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

        #TODO: add if loop to display pnl, fees, 
        # probably should be an addition to "Event" class 
        return self._get(f"entries/{entry_id}", params = params)

    def create_entry(self, event_id):
        """create an entry to an event given an event_id e.g evt_60dbec530d2197a973c5dddcf6f65e12
        """
        data = {'event_id': event_id}
        return self._post(f"entries", data = data)

    def place_order(self, id, price, side = 'buy', phase = 'ipo', qty = 1, *args, **kwargs):
        """
        TODO: exception handling, if response to an order is TOO MANY ORDERS, add the order back to the queue
        add functionality for 'market' orders
        add functionality for take_profit/stop_loss
        add functionality for fill or kill/good until
        add functionality to allow user to place order at JockMkt estimated price

        keyword args:
        \tid -- your player's tradeable id, which can be obtained by...
        \tside -- default: buy, buy or sell (sell only available during live trading
        \tphase -- default: ipo or live
        \tqty -- default: 1, number of shares you wish to purchase 
        \tprice -- bid/ask per share. Do not include your fees.

        optional:
        \torder_size -- input a total amount to spend and calculate desired number of shares automatically
        """
        if price > 25:
            price = 25

        if 'order_size' in kwargs:
            size = kwargs.get('order_size', 0)
            print(size)
            qty = size // price
            print(qty)

        price = "{:.2f}".format(price)

        order = {
            'tradeable_id': id,
            'side': side,
            'type': 'limit',
            'phase': phase,
            'quantity': str(qty),
            'limit_price': str(price)
        }

        print(order)
        return self._post('orders', data = order)

#NOTE: the docs for order object > status contain 'outbid' twice

    def get_orders(self, qty = 100, **kwargs):
        """get all of a user's orders
        Keyword args:
        \toptional:
        \tqty -- int, number of orders the user wishes to display
        \tevent_id -- str, orders relating to a specific event
        \tactive -- bool, include only orders marked (created or accepted, not filled, canceled, outbid, or expired)
        \tupdated_after -- int, ms timestamp 13 digits, includes orders only after the timestamp
        """
        params = {}
        response = []
        if 'event_id' in kwargs:
            params['event_id'] = kwargs.get('event_id', '')
        if 'active' in kwargs:
            params['active'] = kwargs.get("active", False)
        if 'updated_after' in kwargs:
            params['updated_after'] = kwargs.get('updated_after', '')
        for page in range(int(qty/100)):
            params['start'] = str(page*100)
            params['limit'] = '100'
            res = self._get('orders', params = params)
            for order in res['orders']:
                response.append(order)

        return response
    def get_some_order(self, order_id):
        """get information about a specific order

         Keyword args:
        \trequired:
        \torder_id -- str, e.g ord_601b5ad6538ec34875ee1687c4a657f8
        """
        return self._get(f"order/{order_id}")

    def delete_order(self, order_id):
        """delete a specific order

        Keyword args:
        \trequired:
        \torder_id -- str, e.g ord_601b5ad6538ec34875ee1687c4a657f8
        """
        return self._delete(f"order/{order_id}")

    def get_positions(self):
        """returns a user's open positions in all current events
        """
        return self._get("positions")

    def get_account_activity(self, qty = 100):
        params = {}
        for page in range(int(qty/100)):
            params['start'] = str(page*100)
            params['limit'] = '100'

            return self._get('account/activity', params = params)
