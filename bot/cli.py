import os
import argparse
from dotenv import load_dotenv

from .client import BinanceFuturesClient
from .orders import OrderService
from .validators import validate_symbol, validate_side, validate_order_type, validate_quantity, validate_price
from .logging_config import setup_logging


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--side", required=True)
    parser.add_argument("--type", dest="order_type", required=True)
    parser.add_argument("--quantity", required=True, type=float)
    parser.add_argument("--price", type=float, default=None)
    args = parser.parse_args()

    logger = setup_logging()

    try:
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        order_type = validate_order_type(args.order_type)
        quantity = validate_quantity(args.quantity)
        price = validate_price(args.price)
        if order_type == "LIMIT" and price is None:
            raise ValueError("price is required for LIMIT orders")

        api_key = os.getenv("BINANCE_API_KEY", "")
        api_secret = os.getenv("BINANCE_API_SECRET", "")
        if not api_key or not api_secret:
            raise RuntimeError("Set BINANCE_API_KEY and BINANCE_API_SECRET in .env")

        client = BinanceFuturesClient(api_key, api_secret, logger=logger)
        service = OrderService(client, logger=logger)

        print("Order request summary")
        print(f"symbol={symbol}, side={side}, type={order_type}, quantity={quantity}, price={price}")

        response = service.create_order(symbol, side, order_type, quantity, price)

        print("Order response details")
        print(f"orderId={response.get('orderId')}")
        print(f"status={response.get('status')}")
        print(f"executedQty={response.get('executedQty')}")
        print(f"avgPrice={response.get('avgPrice', 'N/A')}")
        print("Success: order placed successfully")
    except Exception as e:
        logger.error(str(e))
        print(f"Failure: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()