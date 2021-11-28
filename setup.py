#!/usr/bin/python
# -*- coding:utf-8 -*-

from setuptools import setup

setup(
    name='async-kucoin-python',
    version='v1.0.9',
    packages=['kucoin_async', 'kucoin_async/base_request', 'kucoin_async/margin', 'kucoin_async/market', 'kucoin_async/trade', 'kucoin_async/user',
              'kucoin_async/websocket', 'kucoin_async/ws_token'],
    license="MIT",
    author='Theo',
    author_email="theocoombes06@gmail.com",
    url='https://github.com/TheoCoombes/kucoin-async-python-sdk',
    description="Asynchronous wrapper for KuCoin's API. Forked from Kucoin/kucoin-python-sdk",
    install_requires=['aiohttp', 'websockets'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
