# kucoin-async-python-sdk

## Features
- Full asyncio support on ALL methods
- Drop-in replacement for the [existing client](https://github.com/Kucoin/kucoin-python-sdk).
- Implementation of REST endpoints
- Simple handling of authentication
- Response exception handling
- Websockets support

## Quick Start
- Register an account with [KuCoin](https://www.kucoin.com/ucenter/signup>) or the [KuCoin Sandbox](https://sandbox.kucoin.com/>).
- Generate an [API Key](https://www.kucoin.com/account/api) ([Sandbox](https://sandbox.kucoin.com/account/api)).
- Install the library:
```bash
pip install git+https://github.com/TheoCoombes/kucoin-async-python-sdk.git
```

## Note
To avoid errors, you have to close the client session after use:
```py
await client.close()
```

## Basic Usage
```py
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


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```
View the [original repo](https://github.com/Kucoin/kucoin-python-sdk) for more examples, adding `await` before method calls.

## Websockets (same as standard library)
```py
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
```
