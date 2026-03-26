Usage
==================
Credentials safety
------------------
Avoid exposing credentials in your code. <br>
Instead use a :code:`.env` file:

.. code-block:: python

    API_KEY_ID = "1234"
    API_KEY_TOKEN = "abcdefghijklmnopqrstuvwxyz"


And initiate using:

.. code-block:: python

    from OceanOpsClient import OceanOpsClient
    client = OceanOpsClient.from_env()


This will return:

.. code-block:: python

    API_KEY_ID='1382' API_KEY_TOKEN=SecretStr('**********')
    Process finished with exit code 0

Under no circumstances the client will display your secret token.


Pull a platform
---------------

.. code-block:: python

    from pprint import pprint
    from OceanOpsClient import OceanOpsClient

    wigosID = "0-22000-0-6204817"
    client = OceanOpsClient()
    resp = client.get_platform(ptfWigosId=wigosID)
    pprint(resp)

Validate Passport
-----------------

.. code-block:: python

    from OceanOpsClient import OceanOpsClient
    client = OceanOpsClient()
    passport = "passport_thornton_buoy.json"
    status = client.validate_passport_json(passport)
    print(status)

Push passport
-------------
For pushing a passport you need credentials.
Make sure to have a valid .env file in the repository.

.. code-block:: python

    from pprint import pprint
    from OceanOpsClient import OceanOpsClient

    client = OceanOpsClient.from_env()

    passport = "passport_thornton_buoy.json"
    status = client.validate_passport_json(passport)
    print(status)

    m = client.post_passport(passport, dry_run=True)
    pprint(m)
