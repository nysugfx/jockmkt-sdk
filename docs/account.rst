=======
Account
=======
.. Account Data_

Account data is generated automatically when you call Client.

it can be accessed as follows:

.. currentmodule:: jockmkt_sdk.client

.. automethod:: Client.get_auth_token

.. automethod:: Client.get_account

.. code-block:: python

    client = Client()
    client.get_auth_token(secret_key, api_key)
    account = client.get_account()
    print(account)

Returns a dictionary of account information:

>>> {'DISPLAY_NAME': {'info':
>>>  {'id': 'acct_xxx',
>>>   'object': 'account',
>>>   'tags': [],
>>>   'email': 'xxx@xxx.com',
>>>   'status': 'active',
>>>   'display_name': 'xxx',
>>>   'language': 'en',
>>>   'experience_level': 'expert',
>>>   'created_at': 1614735755967,
>>>   'updated_at': 1649599679285},
>>>  'balances': [{'currency': 'usd',
>>>    'object': 'balance',
>>>    'type': 'fiat',
>>>    'total': 600.00,
>>>    'buying_power': 600.00,
>>>    'pending': 0,
>>>    'updated_at': 1649571297672}],
>>>     # there may also be information about contest balances as well
>>>  'keys': {'secret_key': 'xxx',
>>>   'api_key': 'jm_key_xxx'},
>>>  'token': {'Authorization': 'Bearer xxx'}
>>>        }
>>>    }

.. Account Activity_

Account Activity data is a little bit different.

.. automethod:: Client.get_account_activity

.. code-block:: python

    account_activity = client.get_account_activity()

Returns a list of all account activity, including orders, payouts, event entries, deposits and withdrawals.

Some examples:

.. code-block:: python

    print(type(account_activity))
    for activity in account_activity:
        print(activity)

Returns:

    For example:

        Payout:

>>> {'id': 'aact_6247ed15ed7f8339ead03a510517512c',
>>>    'object': 'account_activity:payout',
>>>    'payouts': [{'tradeable_id': 'tdbl_62452742abe97c136151cae9313fed5d',
>>>                'quantity': 6,
>>>                'price': 1,
>>>                'cost_basis': 27,
>>>                'cost_basis_all_time': 27,
>>>                'proceeds_all_time': 6,
>>>                'tradeable': {objects.Tradeable}, ...]}

A payout is a list of all payouts and respective tradeables from a single event

    Order:

>>> {'id': 'aact_624878935119dbbb29858440504c989e',
>>>  'object': 'account_activity:order',
>>>  'order_id': 'ord_62487893677bd6fec00c68ed47d3a0e2',
>>>  'created_at': 1648916627064,
>>>  'order': {objects.Order}


For more information regarding different types of account activity, please see here:
    `Jock MKT API Account Activity Docs <https://docs.jockmkt.com/#accountactivity>`_
