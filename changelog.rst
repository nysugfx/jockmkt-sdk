=======================
Changelog - jockmkt-sdk
=======================

This changelog will document all changes after and including release **0.2.0** of the Jockmkt-sdk API Wrapper.

Releases follow `semantic versioning <https://semver.org/spec/v2.0.0.html>`_.
The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_.

Docs available at: `Read The Docs <https://jockmkt-sdk.readthedocs.io/en/latest/>`_

Release 0.2.1
#############

``Fixed:``

- Docs

- Event endpoint displaying only 20 results

Release 0.2.0
#############

``Added:``

- Functionality for websockets

``Fixed:``

- ``get_game_logs`` is now fully functional

- ``get_game_logs`` now includes ``statistics`` and ``projected_statistics`` attributes.

- order rate limit handling is fixed -- no order deletions will count towards the rate limit

Release 0.1.0
#############

``Added:``

- functionality for ALL Jockmkt API endpoints

- Automatically fetches an authorization token

- Objects for every relevant request: (i.e. tradeable, entity, event, order, etc.) that contain attributes for all available information.

- Rate limit handling for orders -- the user can place as many orders as they want and the SDK will automatically cache requests if they hit the limit

- Testing

- Event scoring information

- Full docstrings explaining every api request, return value and instance variable

- Full documentation with examples `here <https://jockmkt-sdk.readthedocs.io/en/latest/>`_






