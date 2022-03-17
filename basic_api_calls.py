import requests
from datetime import datetime, timedelta
import json
import keys

from exception import JockAPIException

class Team(object):
    def __init__(self, team_id, location, name, league, abbreviation, sportradar_id):
        self.team_id = team_id
        self.location = location
        self.name = name
        self.league = league
        self.abbreviation = abbreviation
        self.sportradar_id = sportradar_id
    
    def filter_teams(self, **kwargs):
        pass

    def get_team_players(self, **kwargs): # perhaps this should go under Entity
        pass

    def get_team_games(self, **kwargs): # perhaps this should go under Games
        pass

    def get_team_events(self, **kwargs): # perhaps this should go under Event
        pass

class Game(object):
    def __init__(self):
        pass

class GameLog(object):
    def __init__(self):
        pass

class Event(object):
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

class Tradeable(object):
    def __init__(self):
        pass

class Entry(object):
    def __init__(self):
        pass

class Order(object):
    def __init__(self):
        pass

class Position(object):
    def __init__(self):
        pass

class AccountActivity(object):
    def __init__(self):
        pass

class Entity(object): #this got incredibly convoluted fairly quickly. I'm sure there's a better way to do it but by the time I realized that I was mostly done anyways
    def __init__(self, entity):
        self.entity = self._league_filter(entity)

    def _league_filter(self, entity):
        print(entity)
        if entity['league'] == 'nascar':
            self.id = entity['id']
            self.league = 'nascar'
            self.name = entity['name']
            self.first_name = entity['first_name']
            self.last_name = entity['last_name']
            self.status = entity['status']
            self.image_url = entity['image_url']
            self.points_eligible = entity['points_eligible']
            self.in_chase = entity['in_chase']
            if len(entity['cars']) > 1:
                self.car_number = entity['cars'][0]['number']
                self.car_manufacturer = entity['cars'][0]['manufacturer']
                self.car_engine = entity['cars'][0]['engine']
                self.car_sportradar_id = entity['cars'][0]['sportradar_id']
            try:
                self.team_id = entity['current_team_id']
                self.team_name = entity['team']['name']
                self.team_location = entity['team']['location']
                self.team_abbreviation = entity['team']['abbreviation']
            except KeyError:
                self.team_id = None
                self.team_name = None
                self.team_location = None
                self.team_abbreviation = None
            try:
                self.birthday = entity['birthday']
            except:
                self.birthday = None
            try:
                self.birthplace = entity['birth_place']
            except:
                self.birthplace = None
            try:
                self.rookie_year = entity['rookie_year']
            except KeyError:
                self.rookie_year = None
            try:
                self.injury_status = entity['injury']['status']
                self.injury_type = entity['injury']['type']
            except KeyError:
                self.injury = None
            self.updated = entity['updated_at']

        if entity['league'] == 'nhl':
            self.id = entity['id']
            self.league = 'nhl'
            self.name = entity['name']
            self.image_url = entity['image_url']
            self.team_id = entity['current_team_id']
            self.team_name = entity['team']['name']
            self.team_location = entity['team']['location']
            self.team_abbreviation = entity['team']['abbreviation']
            self.first_name = entity['first_name']
            self.preferred_name = entity['preferred_name']
            self.last_name = entity['last_name']
            self.status = entity['status']
            self.position = entity['position']
            self.jersey_number = entity['jersey_number']
            self.handedness = entity['handedness']
            self.height = entity['height']
            self.weight = entity['weight']
            self.birthday = entity['birthdate']
            try:
                self.rookie_year = entity['rookie_year']
            except: 
                self.rookie_year = None
            try:
                self.injury_status = entity['injury']['status']
                self.injury_type = entity['injury']['type']
            except KeyError:
                self.injury = None
            self.updated = entity['updated_at']
            self.sportradar_id = entity['sportradar_id']

        if entity['league'] == 'nfl':
            self.id = entity['id']
            self.league = 'nfl'
            self.name = entity['name']
            self.image_url = entity['image_url']
            try:
                self.team_id = entity['current_team_id']
            except:
                self.team_id = None
            if self.team_id != None:
                self.team_name = entity['team']['name']
                self.team_location = entity['team']['location']
                self.team_abbreviation = entity['team']['abbreviation']
            self.first_name = entity['first_name']
            self.preferred_name = entity['preferred_name']
            self.last_name = entity['last_name']
            self.status = entity['status']
            self.position = entity['position']
            self.jersey_number = entity['jersey_number']
            self.height = entity['height']
            self.weight = entity['weight']
            self.college = entity['college']
            try:
                self.birthday = entity['birthdate']
            except:
                self.birthday = None
            try:
                self.rookie_year = entity['rookie_year']
            except: 
                self.rookie_year = None
            try:
                self.injury_status = entity['injury']['status']
                self.injury_type = entity['injury']['type']
            except KeyError:
                self.injury = None
            self.updated = entity['updated_at']
            self.sportradar_id = entity['sportradar_id']

        if entity['league'] == 'pga':
            self.id = entity['id']
            self.league = 'pga'
            self.name = entity['name']
            self.image_url = entity['image_url']
            self.first_name = entity['first_name']
            self.preferred_name = entity['preferred_name']
            self.last_name = entity['last_name']
            try:
                self.birthdate = entity['birthdate'][:10]
            except:
                self.birthdate = None
            try:
                self.injury_status = entity['injury']['status']
                self.injury_type = entity['injury']['type']
            except KeyError:
                self.injury = None
            self.updated = entity['updated_at']
            self.sportradar_id = entity['sportradar_id']
            if 'college' in entity.keys():
                self.college = entity['college']
            if 'turned_pro' in entity.keys():
                self.turned_pro = entity['turned_pro']
            if 'country' in entity.keys():
                self.country = entity['country']
                
        if entity['league'] == 'mlb':
            self.id = entity['id']
            self.league = 'mlb'
            self.name = entity['name']
            self.image_url = entity['image_url']
            self.team_id = entity['current_team_id']
            self.team_name = entity['team']['name']
            self.team_location = entity['team']['location']
            self.team_abbreviation = entity['team']['abbreviation']
            self.first_name = entity['first_name']
            self.preferred_name = entity['preferred_name']
            self.last_name = entity['last_name']
            self.position = entity['position']
            try:
                self.jersey_number = entity['jersey_number']
            except: 
                self.jersey_number = None
            try:
                self.college = entity['college']
            except:
                self.college = None
            try:
                self.debut = entity['debut']
            except:
                self.debut = None
            self.status = entity['status']
            self.updated = entity['updated_at']
            self.sportradar_id = entity['sportradar_id']
            try:
                self.birthdate = entity['birthdate']
            except:
                self.birthdate = None
            try:
                self.injury_status = entity['injury']['status']
                self.injury_type = entity['injury']['type']
            except KeyError:
                self.injury = None

        if entity['league'] == 'nba':
            self.id = entity['id']
            self.name = entity['name']
            self.league = 'nba'
            self.image_url = entity['image_url']
            try:
                self.team_id = entity['current_team_id']
                self.team_name = entity['team']['name']
                self.team_location = entity['team']['location']
                self.team_abbreviation = entity['team']['abbreviation']
            except:
                self.team_id = None
            self.first_name = entity['first_name']
            self.preferred_name = entity['preferred_name']
            self.last_name = entity['last_name']
            self.position = entity['position']
            self.height = entity['height']
            self.weight = entity['weight']
            try:
                self.jersey_number = entity['jersey_number']
            except:
                self.jersey_number = None
            try:
                self.college = entity['college']
            except:
                self.college = None
            self.birthdate = entity['birthdate']
            try:
                self.rookie_year = entity['rookie_year']
            except:
                self.rookie_year = None
            self.status = entity['status']
            self.updated = entity['updated_at']
            self.sportradar_id = entity['sportradar_id']
            try:
                self.injury_status = entity['injury']['status']
                self.injury_type = entity['injury']['type']
            except KeyError:
                self.injury = None

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

    def get_teams(self, league = None) -> list[Team]: 
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

    def get_some_team(self, team_id) -> Team:
        """fetch a specific entity based on their entity id

        Keyword args:
        \tteam_id: required (str) e.g "team_8fe94ef0d1f0a00e1285301c4092650f"
        """
        return self._get(f"teams/{team_id}")

    def get_entities(self, qty = 1000, include_team = True, **kwargs) -> list[Entity]: #TODO CHANGE INCLUDE TEAM TO ALWAYS BE TRUE, BETTER INTERACTION WITH ENTITY CLASS
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
        entities = []
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
        for i in response:
            print(i)
        for i in response:
            entities.append(Entity(i))
        return entities

    def get_some_entity(self, entity_id: str, include_team = False) -> Entity:
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

    def get_games(self, league = None, qty = 100) -> list: 
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
    
    def get_some_game(self, game_id: str) -> Game:
        """fetch a specific entity based on their entity id

        Keyword args:
        game_id -- required, str, e.g "game_60bb686586eaf95a5e8dafa3823d89cb"
        """
        return self._get(f"games/{game_id}")

    def get_game_logs(self, qty = 100, include_ent = False, include_game = False, include_team = False, **kwargs) -> GameLog:
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

    def get_upcoming_events(self, qty = 50) -> list[Event]:
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

    def get_some_event(self, event_id: str, include_games=False, include_payouts=False, include_tradeables=False) -> Event:
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


    def get_event_payouts(self, event_id: str) -> Event:
        """get payouts for each rank of an event

        Keyword args:
        \tRequired:
        \tevent_id -- str, the event_id for your chosen event, e.g evt_60dbec530d2197a973c5dddcf6f65e12
        """
        return self._get(f"events/{event_id}/payouts")

    def get_event_games(self, event_id: str) -> Game:
        """get all games in an event

        Keyword args:
        \tRequired:
        \tevent_id -- str, the event_id for your chosen event, e.g evt_60dbec530d2197a973c5dddcf6f65e12
        """
        return self._get(f"events/{event_id}/games")

    def get_event_tradeables(self, event_id: str) -> Tradeable:
        """get all tradeables in an event

        Keyword args:
        \tRequired:
        \tevent_id -- str, the event_id for your chosen event, e.g evt_60dbec530d2197a973c5dddcf6f65e12
        """
        return self._get(f"events/{event_id}/tradeables")

    def get_entries(self, qty = 100, include_event=False, include_payouts=False, include_tradeables=False) -> Entry:
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
    
    def get_some_entry(self, entry_id: str, include_event=False, include_payouts=False, include_tradeables=False) -> Entry:
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

    def create_entry(self, event_id: str) -> json:
        """create an entry to an event given an event_id e.g evt_60dbec530d2197a973c5dddcf6f65e12
        """
        data = {'event_id': event_id}
        return self._post(f"entries", data = data)

    def place_order(self, id: str, price: int, side = 'buy', phase = 'ipo', qty = 1, **kwargs) -> json:
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
    def get_some_order(self, order_id: str) -> Order:
        """get information about a specific order

         Keyword args:
        \trequired:
        \torder_id -- str, e.g ord_601b5ad6538ec34875ee1687c4a657f8
        """
        return self._get(f"order/{order_id}")

    def delete_order(self, order_id: str) -> json:
        """delete a specific order

        Keyword args:
        \trequired:
        \torder_id -- str, e.g ord_601b5ad6538ec34875ee1687c4a657f8
        """
        return self._delete(f"order/{order_id}")

    def get_positions(self) -> Position:
        """returns a user's open positions in all current events
        """
        return self._get("positions")

    def get_account_activity(self, qty = 100) -> AccountActivity:
        params = {}
        for page in range(int(qty/100)):
            params['start'] = str(page*100)
            params['limit'] = '100'

            return self._get('account/activity', params = params)

auth = Client(secret = keys.secret, api_key = keys.key)