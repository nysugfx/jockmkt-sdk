def _case_switch_ent(entity: dict):
    match entity['league']:
        case 'nba':
            return NBAEntity(entity)
        case 'nfl':
            return NFLEntity(entity)
        case 'nhl':
            return NHLEntity(entity)
        case 'pga':
            return PGAEntity(entity)
        case 'mlb':
            return MLBEntity(entity)
        case 'nascar':
            return NASCAREntity(entity)


class Entity(object):
    def __init__(self, entity: dict):
        self._populate_universal_fields(entity)

    def _populate_universal_fields(self, entity):
        self.entity_id = entity.get('id')
        self.league = entity.get('league')
        self.name = entity.get('name')
        self.first_name = entity.get('first_name')
        self.last_name = entity.get('last_name')
        self.updated_at = entity.get('updated_at')
        self.news = entity.get('latest_news', {})

    def __repr__(self):
        return str(self.__dict__) + '\n'

    def __str__(self):
        return str(self.__dict__) + '\n'


class NBAEntity(Entity):
    def __init__(self, entity):
        super().__init__(entity)
        self.team_id = entity.get('current_team_id')
        team = entity.get('team', {})  # turn this into a Team object, and do so for all team sports
        self.team = Team(team)
        self.preferred_name = entity.get('preferred_name')
        self.position = entity.get('position')
        self.height = entity.get('height')
        self.weight = entity.get('weight')
        self.jersey_number = entity.get('jersey_number')
        self.college = entity.get('college')
        self.birthdate = entity.get('birthdate')
        self.rookie_year = entity.get('rookie_year')
        self.status = entity.get('status')
        injury = entity.get('injury', {})
        self.injury_status = injury.get('status')
        self.injury_type = injury.get('type')


class NFLEntity(Entity):
    def __init__(self, entity):
        super().__init__(entity)
        self.team_id = entity.get('current_team_id')
        team = entity.get('team', {})
        self.team = Team(team)
        self.preferred_name = entity.get('preferred_name')
        self.position = entity.get('position')
        self.height = entity.get('height')
        self.weight = entity.get('weight')
        self.jersey_number = entity.get('jersey_number')
        self.college = entity.get('college')
        self.birthdate = entity.get('birthdate')
        self.rookie_year = entity.get('rookie_year')
        self.status = entity.get('status')
        injury = entity.get('injury', {})
        self.injury_status = injury.get('status')
        self.injury_type = injury.get('type')


class NASCAREntity(Entity):
    def __init__(self, entity):
        super().__init__(entity)
        self.team_id = entity.get('current_team_id')
        team = entity.get('team', {})
        self.team = Team(team)
        self.points_eligible = entity.get('points_eligible', False)
        self.in_chase = entity.get('in_chase', False)
        self.cars = entity.get("cars", [])
        self.birthday = entity.get('birthday')
        self.birthplace = entity.get('birth_place')
        self.rookie_year = entity.get('rookie_year')
        self.status = entity.get('status')
        injury = entity.get('injury', {})
        self.injury_status = injury.get('status')
        self.injury_type = injury.get('type')


class NHLEntity(Entity):
    def __init__(self, entity):
        super().__init__(entity)
        self.team_id = entity.get('current_team_id')
        team = entity.get('team', {})
        self.team = Team(team)
        self.preferred_name = entity.get('preferred_name')
        self.position = entity.get('position')
        self.height = entity.get('height')
        self.weight = entity.get('weight')
        self.jersey_number = entity.get('jersey_number')
        self.handedness = entity['handedness']
        self.rookie_year = entity.get('rookie_year')
        self.status = entity.get('status')
        injury = entity.get('injury', {})
        self.injury_status = injury.get('status')
        self.injury_type = injury.get('type')


class PGAEntity(Entity):
    def __init__(self, entity):
        super().__init__(entity)
        self.preferred_name = entity.get('preferred_name')
        birthday = entity.get('birthdate', None)
        if birthday is not None:
            self.birthdate = birthday[:10]
        else:
            self.birthdate = birthday
        self.height = entity.get('height')
        self.weight = entity.get('weight')
        self.college = entity.get('college')
        self.rookie_year = entity.get('turned_pro')
        self.country = entity.get('country')
        injury = entity.get('injury', {})
        self.injury_status = injury.get('status')
        self.injury_type = injury.get('type')


class MLBEntity(Entity):
    def __init__(self, entity):
        super().__init__(entity)
        self.team_id = entity.get('current_team_id')
        team = entity.get('team', {})
        self.team = Team(team)
        self.preferred_name = entity.get('preferred_name')
        self.position = entity.get('position')
        self.jersey_number = entity.get('jersey_number')
        self.college = entity.get('college')
        self.debut = entity.get('debut')
        self.status = entity.get('status')
        self.birthdate = entity.get('birthdate')
        injury = entity.get('injury', {})
        self.injury_status = injury.get('status')
        self.injury_type = injury.get('type')


class Team(object):
    def __init__(self, team):
        self.team_id = team.get('id')
        self.location = team.get('location')
        self.name = team.get('name')
        self.league = team.get('league')
        self.abbreviation = team.get('abbreviation')

    def filter_teams(self, **kwargs):
        pass

    def get_team_players(self, **kwargs):  # perhaps this should go under Entity
        pass

    def get_team_games(self, **kwargs):  # perhaps this should go under Games
        pass

    def get_team_events(self, **kwargs):  # perhaps this should go under Event
        pass

    def available_attributes(self):
        print({key for key in self.__dict__.keys()})

    def __repr__(self):
        return str(self.__dict__) + '\n'

    def __str__(self):
        return str(self.__dict__) + '\n'


class Game(object):
    """
    Games differ significantly, and you can expect significantly different information under "state" depending on the
    league. See docs for more info, or use self.print_game to get an idea of what the keys are.
    """

    def __init__(self, game: dict):
        self.game_id = game.get('id')
        self.game_name = game.get('name')
        self.league = game.get('league')
        self.start = game.get('scheduled_start')
        self.venue = game.get('venue')
        self.status = game.get('status')
        self.amount_completed = game.get('amount_completed')
        self.state = game.get('state')
        self.weather = game.get('weather')
        self._populate_team_info(game)

    def _populate_team_info(self, game: dict):
        home = game.get('home', {})
        for key in home:
            self.__dict__['home_' + key] = home[key]
        away = game.get('away', {})
        for key in away:
            self.__dict__['away_' + key] = away[key]

    def update_team_names(self, team_id):
        pass

    def available_attributes(self):
        print({key for key in self.__dict__.keys()})

    def __repr__(self):
        return str(self.__dict__) + '\n'

    def __str__(self):
        return str(self.__dict__) + '\n'


class GameLog(object):
    """
    different leagues will return different dictionaries of stats/projected. There is currently no league identifier.
    """

    def __init__(self, game_log):
        self.id = game_log.get('id')
        self.entity_id = game_log.get('entity_id')
        self.game_id = game_log.get('game_id')
        self.team_id = game_log.get('team_id')
        self.scheduled_start = game_log.get('scheduled_start')
        self.updated_at = game_log.get('updated_at')
        projected_stats = game_log.get('projected_stats', {'league': None})
        for key in projected_stats:
            self.__dict__['projected_' + key] = projected_stats[key]
        stats = game_log.get('stats', {'league': None})
        for k in stats:
            self.__dict__['actual_' + k] = stats[k]
        self.league = stats.get('league', projected_stats.get('league'))
        entity = game_log.get('entity', {})
        self.entity = _case_switch_ent(entity)
        game = game_log.get('game', {})
        self.game = Game(game)
        team = game_log.get('team', {})
        self.team = Team(team)

    def available_attributes(self):
        print({key for key in self.__dict__.keys()})

    def __repr__(self):
        return str(self.__dict__) + '\n'

    def __str__(self):
        return str(self.__dict__) + '\n'

#

class Event(object):
    def __init__(self, event):
        self.event_id = event.get('id')
        self.name = event.get('name')
        self.description = event.get('description')
        self.type = event.get('type')
        self.status = event.get('status')
        self.league = event.get('league')
        self.ipo_start = event.get('ipo_open_at')
        self.ipo_end = event.get('live_at_estimated')
        self.amt_completed = event.get('amount_completed')
        self.updated_at = event.get('updated_at')
        self.payouts = event.get('payouts', [])
        games = event.get('games', {})
        self.games = []
        for game in games:
            self.games.append(Game(game))
        tradeables = event.get('tradeables', {})
        self.tradeables = []
        for tdbl in tradeables:
            self.tradeables.append(Tradeable(tdbl))
        self.contest = event.get('contest', {})

    def _is_entered(self):
        pass

    def available_attributes(self):
        print({key for key in self.__dict__.keys()})

    def __repr__(self):
        return str(self.__dict__) + '\n'

    def __str__(self):
        return str(self.__dict__) + "\n"


class Tradeable(object):  # may be worth somehow implementing an auto-updating system for this
    def __init__(self, tradeable):
        self.tradeable_id = tradeable.get('id')
        self.league = tradeable.get('league')
        self.entity_id = tradeable.get('entity_id')
        self.event_id = tradeable.get('event_id')
        self.game_id = tradeable.get('focus_game_id')
        points = tradeable.get('points', {})
        self.fpts_proj_pregame = points.get('projected')
        self.fpts_proj_live = points.get('projected_live')
        self.fpts_scored = points.get('scored')
        price = tradeable.get('price', {})
        self.ipo = price.get('ipo')
        self.high = price.get('high')
        self.low = price.get('low')
        self.last = price.get('last')
        self.estimated = price.get('estimated')
        self.bid = price.get('bid')
        self.ask = price.get('ask')
        self.final = price.get('final')
        stats = tradeable.get('stats', {})
        if type(stats) != dict and len(stats) > 0:
            for key in stats[0]:
                self.__dict__[key] = stats[0][key]
        else:
            for key in stats:
                self.__dict__[key] = stats[key]
        entity = tradeable.get('entity', {'league': tradeable['league']})
        self.name = entity.get('name')
        self.entity = _case_switch_ent(entity)

    def available_attributes(self):
        print({key for key in self.__dict__.keys()})

    def __repr__(self):
        return str(self.__dict__) + '\n'

    def __str__(self):
        return str(self.__dict__) + '\n'


class Entry(object):
    def __init__(self, entry):
        self.entry_id = entry.get('id')
        self.event_id = entry.get('event_id')
        leaderboard = entry.get('leaderboard')
        self.leaderboard_position = leaderboard.get('position')
        self.profit = leaderboard.get('amount')
        self.updated_at = entry.get('updated_at')
        self.favorites = entry.get('favorites')  # interact this with tradeable lookup
        event = entry.get('event', {})
        self.event = Event(event)
        self.payouts = entry.get('payouts')

    def available_attributes(self):
        print({key for key in self.__dict__.keys()})

    def __repr__(self):
        return str(self.__dict__) + '\n'

    def __str__(self):
        return str(self.__dict__) + '\n'


class Position(object):
    def __init__(self, position):
        self.tradeable_id = position.get('tradeable_id')
        self.event_id = position.get('event_id')
        self.bought_count = position.get('bought_count')
        self.buy_interest = position.get('buy_interest')
        self.sell_interest = position.get('sell_interest')
        self.quantity_owned = position.get('quantity')
        self.cost_basis = position.get('cost_basis')
        self.proceeds = position.get('proceeds')
        self.cost_basis_all_time = position.get('cost_basis_all_time')
        self.proceeds_all_time = position.get("proceeds_all_time")
        self.updated_at = position.get('updated_at')

    def available_attributes(self):
        print({key for key in self.__dict__.keys()})

    def __repr__(self):
        return str(self.__dict__) + '\n'

    def __str__(self):
        return str(self.__dict__) + '\n'


class Order(object):
    def __init__(self, order):
        self.order_id = order.get('id')
        self.tradeable_id = order.get('tradeable_id')
        self.entity_id = order.get('entity_id')
        self.event_id = order.get('event_id')
        self.status = order.get('status')
        self.side = order.get('side')
        self.type = order.get('type')
        self.phase = order.get('phase')
        self.quantity = order.get('quantity')
        self.limit_price = order.get('limit_price')
        self.cost_basis = order.get('cost_basis', 0)
        self.fee_paid = order.get('fee_paid', 0)
        self.filled_quantity = order.get('filled_quantity', 0)
        self.created_at = order.get('created_at')
        self.accepted_at = order.get('accepted_at')
        self.updated_at = order.get('updated_at')
        self.filled_at = order.get('filled_at')
        self.cancellation_requested_at = order.get('cancellation_requested_at')

    def available_attributes(self):
        print({key for key in self.__dict__.keys()})

    def __repr__(self):
        return str(self.__dict__) + '\n'

    def __str__(self):
        return str(self.__dict__) + '\n'


class AccountActivity(object):  # will need to get more advanced with the way aact objects are handled in future
    def __init__(self, aact):
        for key in aact:
            if key == 'event':
                self.__dict__[key] = Event(aact[key])
            elif key == 'order':
                self.__dict__[key] = Order(aact[key])
            else:
                self.__dict__[key] = aact[key]

    def available_attributes(self):
        print({key for key in self.__dict__.keys()})

    def __repr__(self):
        return str(self.__dict__) + '\n'

    def __str__(self):
        return str(self.__dict__) + '\n'
