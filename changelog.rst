=======================
Changelog - jockmkt-sdk
=======================

This changelog will document all changes after and including release **0.2.0** of the Jockmkt-sdk API Wrapper.

Releases follow `semantic versioning <https://semver.org/spec/v2.0.0.html>`_.
The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_.

Docs available at: `Read The Docs <https://jockmkt-sdk.readthedocs.io/en/latest/>`_

Release 0.2.7
#############

``ADDED:``

- Added current_shares attribute to Event object

Release 0.2.6
#############

``ADDED:``

- Added sold count to position object

Release 0.2.5
#############

``FIXED:``

- Order placing fixed

Release 0.2.4
#############

``FIXED:``

- Decimal rounding error for pricing

- Github Actions

Release 0.2.3
#############

``skipped, versioning typo!``

Release 0.2.2
#############

``Added:``

- Order response is now an Order object.
    - added direction and time_in_force instance variables

- Balance object

- 'insufficient_funds' and 'mixed_position' message in exception handling

- 'updated_at' attribute for Tradeable objects

``Fixed:``

- Order prices are now formatted using Decimal rather than ``"{0:.2f}".format()`` which was causing the occasional bug.

- ``.place_order()`` input typing was corrected

- Order object is correctly parsed from 'account' websocket endpoint

- kwargs are correctly unpacked in websocket error_handler

``Changed:``

- place_order args adjusted order of positional args:
    - tradeable_id, price, **qty: int = 1**, ...)
    - should not break any code

- Orders can now be placed like so (you do not need qty as a keyword argument):

```
client.place_order('tradeable_id', price, qty)
```


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






