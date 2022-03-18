#league filtering now done in Client class using if/else statements

class Entity(object):
    def __init__(self, entity):
        self.entity = self._populate_universal_fields(entity)
 
    def _populate_universal_fields(self, entity):
        self.id = entity['id']
        self.league = entity['league']
        self.name = entity['name']
        self.first_name = entity['first_name']
        self.last_name = entity['last_name']
        self.image_url = entity['image_url']
        self.updated_at = entity['updated_at']
        self.full_ent_dict = entity
        
class nbaEntity(Entity):
    def __init__(self, entity):
        Entity.__init__(self, entity)
        try:
            self.team_id = entity['current_team_id']
            self.team_name = entity['team']['name']
            self.team_location = entity['team']['location']
            self.team_abbreviation = entity['team']['abbreviation']
        except KeyError:
            self.team_id = None
        self.preferred_name = entity['preferred_name']
        self.position = entity['position']
        self.height = entity['height']
        self.weight = entity['weight']
        try:
            self.jersey_number = entity['jersey_number']
        except KeyError:
            self.jersey_number = None
        try:
            self.college = entity['college']
        except KeyError:
            self.college = None
        self.birthdate = entity['birthdate']
        try:
            self.rookie_year = entity['rookie_year']
        except KeyError:
            self.rookie_year = None
        self.status = entity['status']
        self.updated = entity['updated_at']
        self.sportradar_id = entity['sportradar_id']
        try:
            self.injury_status = entity['injury']['status']
            self.injury_type = entity['injury']['type']
        except KeyError:
            self.injury = None

class nflEntity(Entity):
    def __init__(self, entity):
        Entity.__init__(self, entity)
        try:
            self.team_id = entity['current_team_id']
        except KeyError:
            self.team_id = None
        if self.team_id != None:
            self.team_name = entity['team']['name']
            self.team_location = entity['team']['location']
            self.team_abbreviation = entity['team']['abbreviation']
        self.preferred_name = entity['preferred_name']
        self.status = entity['status']
        self.position = entity['position']
        self.jersey_number = entity['jersey_number']
        self.height = entity['height']
        self.weight = entity['weight']
        self.college = entity['college']
        try:
            self.birthday = entity['birthdate']
        except KeyError:
            self.birthday = None
        try:
            self.rookie_year = entity['rookie_year']
        except KeyError: 
            self.rookie_year = None
        try:
            self.injury_status = entity['injury']['status']
            self.injury_type = entity['injury']['type']
        except KeyError:
            self.injury = None
        self.sportradar_id = entity['sportradar_id']
    
class nascarEntity(Entity):
    def __init__(self, entity):
        Entity.__init__(self, entity)
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
        except KeyError:
            self.birthday = None
        try:
            self.birthplace = entity['birth_place']
        except KeyError:
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

class nhlEntity(Entity):
    def __init__(self, entity):
        Entity.__init__(self, entity)
        self.team_id = entity['current_team_id']
        self.team_name = entity['team']['name']
        self.team_location = entity['team']['location']
        self.team_abbreviation = entity['team']['abbreviation']
        self.preferred_name = entity['preferred_name']
        self.status = entity['status']
        self.position = entity['position']
        self.jersey_number = entity['jersey_number']
        self.handedness = entity['handedness']
        self.height = entity['height']
        self.weight = entity['weight']
        self.birthday = entity['birthdate']
        try:
            self.rookie_year = entity['rookie_year']
        except KeyError: 
            self.rookie_year = None
        try:
            self.injury_status = entity['injury']['status']
            self.injury_type = entity['injury']['type']
        except KeyError:
            self.injury = None
        self.sportradar_id = entity['sportradar_id']

class pgaEntity(Entity):
    def __init__(self, entity):
        Entity.__init__(self, entity)
        # print('pga object!')
        # for key in entity:
        #     self.__dict__[key] = entity[key]
        #     if type(entity[key]) == dict:
        #         for k in entity[key]:
        #             self.__dict__[key + '_' + k] = entity[key][k]

        self.preferred_name = entity['preferred_name']
        try:
            self.birthdate = entity['birthdate'][:10]
        except KeyError:
            self.birthdate = None
        try:
            self.injury_status = entity['injury']['status']
            self.injury_type = entity['injury']['type']
        except KeyError:
            self.injury = None
        self.sportradar_id = entity['sportradar_id']
        try:
            self.college = entity['college']
        except:
            self.college = None
        try:
            self.turned_pro = entity['turned_pro']
        except:
            self.turned_pro = None
        try:
            self.country = entity['country']
        except:
            self.country = None

class mlbEntity(Entity):
    def __init__(self, entity):
        Entity.__init__(self, entity)
        self.team_id = entity['current_team_id']
        self.team_name = entity['team']['name']
        self.team_location = entity['team']['location']
        self.team_abbreviation = entity['team']['abbreviation']
        self.preferred_name = entity['preferred_name']
        self.position = entity['position']
        try:
            self.jersey_number = entity['jersey_number']
        except KeyError: 
            self.jersey_number = None
        try:
            self.college = entity['college']
        except KeyError:
            self.college = None
        try:
            self.debut = entity['debut']
        except KeyError:
            self.debut = None
        self.status = entity['status']
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

