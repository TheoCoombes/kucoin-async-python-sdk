from kucoin_async.margin.margin import MarginData
from kucoin_async.market.market import MarketData
from kucoin_async.trade.trade import TradeData
from kucoin_async.user.user import UserData
from kucoin_async.ws_token.token import GetToken


class User(UserData):
    pass


class Trade(TradeData):
    pass


class Market(MarketData):
    pass


class Margin(MarginData):
    pass


class WsToken(GetToken):
    pass


