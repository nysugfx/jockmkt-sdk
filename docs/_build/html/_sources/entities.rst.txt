===========================
Entities & Entity Endpoints
===========================
Entity Endpoints:

.. autoclass:: jockmkt-sdk.client.Client
    :members: get_entities, get_entity

.. code-block:: python

    entities = client.get_entities()
    entity = client.get_entity(entity_id="en_6025693d374b384994316c1e13f40416")

These methods return league-specific entity objects. Entities is a list of them, entity returns information about one specific entity.

.. code-block:: python

    for entity in entities:
        print(type(entity))
        print(entity)

Returns:

.. object:: object.NBAEntity

.. object:: {'entity_id': 'en_0066178b3093f39afbd80612d1b1f04d',
        'league': 'nba',
        'name': "E'Twaun Moore",
        'first_name': "E'Twaun",
        'last_name': 'Moore',
        'updated_at': 1644963000678,
        'news': {},
        'team_id': 'team_11fd5bd23ac17bb67b4d4008cb64583e',
        'team': {'team_id': 'team_11fd5bd23ac17bb67b4d4008cb64583e',
                'location': 'Orlando',
                'name': 'Magic',
                'league': 'nba',
                'abbreviation': 'ORL'},
        'preferred_name': "E'Twaun",
        'position': 'SG',
        'height': 75,
        'weight': 191,
        'jersey_number': '55',
        'college': '55',
        'birthdate': '1989-02-25',
        'rookie_year': 2011,
        'status': 'inactive',
        'injury_status': 'out',
        'injury_type': 'Knee'}

    >>> object.NFLEntity

    >>> {'entity_id': 'en_0163a8ae7659f447a5493ee42b56be05',
        'league': 'nfl',
        'name': 'Brandon Bolden',
        'first_name': 'Brandon',
        'last_name': 'Bolden',
        'updated_at': 1648650568742,
        'news': {},
        'team_id': 'team_c80dd7c0b4258453ea79cee1a585d3ca',
        'team': {'team_id': 'team_c80dd7c0b4258453ea79cee1a585d3ca',
                'location': 'Las Vegas',
                'name': 'Raiders',
                'league': 'nfl',
                'abbreviation': 'LV'},
        'preferred_name': 'Brandon',
        'position': 'RB',
        'height': 71,
        'weight': 220,
        'jersey_number': '0',
        'college': 'Ole Miss',
        'birthdate': '1990-01-26',
        'rookie_year': 2012,
        'status': 'active',
        'injury_status': None,
        'injury_type': None}
.. autoclass:: jockmkt-sdk.objects.Entity
.. inheritance-diagram:: jockmkt-sdk.objects.Entity
    :parts: 1


