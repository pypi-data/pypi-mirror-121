from .position import Position


class Trader:
    def __init__(self, /, market):
        self.market = market

        self.balance = None
        self.available_balance = None

        self.balance2 = None
        self.available_balance2 = None

        self.leverage = None
        self.position = Position()
        self.position.trader = self
        self.orders = None
        self.pnl = None
        self.upnl = None

    async def change_leverage(self, leverage):
        await self.market.bot.client.change_leverage_all(
            market_id=self.market.id,
            leverage=leverage,
        )

    async def get_trader_status(self):
        await self.market.bot.client.get_trader_status(
            timestamp=self.market.bot.client.timestamp(),
            market_id=self.market.id,
        )

    def on_update(self):
        pass
