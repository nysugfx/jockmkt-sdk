=======
Account
=======

Account data is generated automatically when you call Client.

it can be accessed as follows:

.. autoclass:: jockmkt-sdk.client.Client
    :members: _get_account_balance, _get_account,
    :annotation: called automatically upon initialization

.. code-block:: python

    client = Client(secret, api_key)
    balance = client.balance
    account = client.account

    print(balance)
    print(account)

Returns USD balance:

>>>        500.00

Returns account info:

>>> {'id': 'acct_xxx',
    'object': 'account',
    'tags': [],
    'email': 'nysu.gfx@gmail.com',
    'status': 'active',
    'display_name': 'adf',
    'language': 'en',
    'experience_level': 'expert',
    'created_at': 1614735755967,
    'updated_at': 1648916924545}

Account Activity data is a little bit different.

.. autoclass:: jockmkt-sdk.client.Client
    .. automethod:: get_account_activity

.. code-block:: python

    account_activity = client.get_account_activity()

Returns a list of all account activity, including orders, payouts, event entries, deposits and withdrawals.

Some examples:

.. code-block:: python

    print(type(account_activity))
    for activity in account_activity:
        print(activity)

Returns:

>>> <class 'list'> <- returns a list of AccountActivity objects

For example:

    Payout:

>>> {'id': 'aact_6247ed15ed7f8339ead03a510517512c',
    'object': 'account_activity:payout',
    'payouts': [{'tradeable_id': 'tdbl_62452742abe97c136151cae9313fed5d',
                'quantity': 6,
                'price': 1,
                'cost_basis': 27,
                'cost_basis_all_time': 27,
                'proceeds_all_time': 6,
                'tradeable': {objects.Tradeable}, ...]}

                account_activity:payout is a list of all payouts and respective tradeables from a single event

    Order:
>>> {'id': 'aact_624878935119dbbb29858440504c989e',
    'object': 'account_activity:order',
    'order_id': 'ord_62487893677bd6fec00c68ed47d3a0e2',
    'created_at': 1648916627064,
    'order': {objects.Order}

For more information regarding different types of account activity, please see here:
    `Jock MKT API Account Activity Docs <https://docs.jockmkt.com/#accountactivity>`_
