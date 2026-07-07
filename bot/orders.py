from .client import BinanceFuturesClient


class OrderService:
    def __init__(self, client: BinanceFuturesClient, logger=None):
        self.client = client
        self.logger = logger

    def create_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float | None = None) -> dict:
        payload = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }
        if order_type == "LIMIT":
            payload["timeInForce"] = "GTC"
            payload["price"] = price
        return self.client.place_order(payload)