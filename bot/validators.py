from decimal import Decimal

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


def validate_symbol(symbol: str) -> str:
    symbol = symbol.upper().strip()
    if not symbol.endswith("USDT") or len(symbol) < 6:
        raise ValueError("symbol must look like BTCUSDT")
    return symbol


def validate_side(side: str) -> str:
    side = side.upper().strip()
    if side not in VALID_SIDES:
        raise ValueError("side must be BUY or SELL")
    return side


def validate_order_type(order_type: str) -> str:
    order_type = order_type.upper().strip()
    if order_type not in VALID_ORDER_TYPES:
        raise ValueError("order_type must be MARKET or LIMIT")
    return order_type


def validate_quantity(quantity: float) -> float:
    q = Decimal(str(quantity))
    if q <= 0:
        raise ValueError("quantity must be greater than 0")
    return float(q)


def validate_price(price: float | None) -> float | None:
    if price is None:
        return None
    p = Decimal(str(price))
    if p <= 0:
        raise ValueError("price must be greater than 0")
    return float(p)