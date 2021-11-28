==================================
Welcome to kucoin-async-python-sdk
==================================

.. image:: https://img.shields.io/pypi/l/python-kucoin
    :target: https://github.com/Kucoin/kucoin-python-sdk/blob/master/LICENSE

.. image:: https://img.shields.io/badge/python-3.6%2B-green
    :target: https://pypi.org/project/python-kucoin


Features
--------
- Full asyncio support on ALL methods
- Implementation of REST endpoints
- Simple handling of authentication
- Response exception handling
- Implement websockets (note only python 3.6+)

Quick Start
-----------

Register an account with `KuCoin <https://www.kucoin.com/ucenter/signup>`_.

To test on the Sandbox  with `KuCoin Sandbox <https://sandbox.kucoin.com/>`_.

`Generate an API Key <https://www.kucoin.com/account/api>`_
or `Generate an API Key in Sandbox <https://sandbox.kucoin.com/account/api>`_ and enable it.

.. code:: bash

    pip install git+https://github.com/TheoCoombes/kucoin-async-python-sdk.git


Basic Usage
----------
.. code:: python
    
    from kucoin.client import Market, Trade
    import asyncio

    async def main():
        # Market
        client = Market(url='https://api.kucoin.com')

        klines = await client.get_kline('BTC-USDT', '1min')

        # Get KuCoin server's timestamp
        server_time = await client.get_server_timestamp()
        
        # Safe exit client connection
        await client.close()

        # Trade
        api_key = '<api_key>'
        api_secret = '<api_secret>'
        api_passphrase = '<api_passphrase>'

        client = Trade(key='', secret='', passphrase='', is_sandbox=False, url='')

        # Create limit order
        order_id = await client.create_limit_order('BTC-USDT', 'buy', '1', '8000')

        # Create market order
        order_id = await client.create_market_order('BTC-USDT', 'buy', size='1')

        # Cancel limit order
        await client.cancel_order('5bd6e9286d99522a52e458de')

        # Safe close client
        await client.close()
        
        # View original docs for more examples

    if __name__ == "__main__":
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())

Websockets (same as standard library)
----------

.. code:: python

    import asyncio
    from kucoin.client import WsToken
    from kucoin.ws_client import KucoinWsClient


    async def main():
        async def deal_msg(msg):
            if msg['topic'] == '/spotMarket/level2Depth5:BTC-USDT':
                print(msg["data"])
            elif msg['topic'] == '/spotMarket/level2Depth5:KCS-USDT':
                print(f'Get KCS level3:{msg["data"]}')

        # is public
        client = WsToken()
        #is private
        # client = WsToken(key='', secret='', passphrase='', is_sandbox=False, url='')
        # is sandbox
        # client = WsToken(is_sandbox=True)
        ws_client = await KucoinWsClient.create(None, client, deal_msg, private=False)
        # await ws_client.subscribe('/market/ticker:BTC-USDT,ETH-USDT')
        await ws_client.subscribe('/spotMarket/level2Depth5:BTC-USDT,KCS-USDT')
        while True:
            await asyncio.sleep(60, loop=loop)


    if __name__ == "__main__":
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
