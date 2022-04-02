=====
Usage
=====

.. _installation:

Installation
------------

To use jockmkt-sdk, first install it using pip:

.. code-block:: console

    $ pip install jockmkt-sdk

Getting started:
    import the package and generate a Client object

.. autoclass:: jockmkt-sdk.client.Client
.. code-block:: python

    from jockmkt-sdk.client import Client

    secret_key = "<secret_key: xxx>"
    api_key = "<api_key: jm_api_xxx>"

    client = Client(secret_key, api_key)

The client object that you generate here will be used to make all future api calls. It contains a BearerAuth token used in all headers.

Each call is a method within the Client class.


