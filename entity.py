
class Entity(object):
    def __init__(self, entity):
        self.entity = self._league_filter(entity)

        # for key, value in self.entity.items():
        #     self.key = value    

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
            except KeyError: 
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
            except KeyError:
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
            except KeyError:
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
            except KeyError:
                self.team_id = None
            self.first_name = entity['first_name']
            self.preferred_name = entity['preferred_name']
            self.last_name = entity['last_name']
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