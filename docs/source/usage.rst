=======================
Usage & Getting Started
=======================
.. automodule:: jockmkt_sdk.client

Installation
============

To use jockmkt-sdk, first install it using pip:

.. code-block:: console

    $ pip install jockmkt-sdk

Getting started:

    import the package and generate a Client object instance

.. autoclass:: Client

.. code-block:: python

    from jockmkt_sdk.client import Client

    secret_key = "<secret_key: xxx>"
    api_key = "<api_key: jm_api_xxx>"

    # Initialize an instance of the client class:
    client = Client()

    # Get your authorization token
    client.get_auth_token(secret_key, api_key)


You are creating an instance of the Client class and generating an auth-token,
which you will use for all future api calls.

Each call is a method within the Client class.

For example:

.. code-block:: python

    client.get_events()

    client.get_entities()

    client.get_orders()
