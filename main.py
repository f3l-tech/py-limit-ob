import asyncio
import aiohttp
import websockets
import ujson as json
import csv
from sortedcontainers import SortedDict

symbol = "solusdt"
depth_snapshot_url = f"https://api.binance.com/api/v3/depth?symbol={symbol.upper()}&limit=1000"
depth_stream_url = f"wss://stream.binance.com:9443/ws/{symbol}@depth@100ms"
order_book = {
    "bids": SortedDict(lambda x: -x),
    "asks": SortedDict()
}

def apply_orderbook_update(update):
    for side_key, updates in [("bids", update["bids"]), ("asks", update["asks"])]:
        side = order_book[side_key]
        for price_str, qty_str in updates:
            price = float(price_str)
            qty = float(qty_str)
            if qty == 0.0:
                side.pop(price, None)
            else:
                side[price] = qty

def orderbook_to_rows(levels=20):
    bids = list(order_book["bids"].items())[:levels]
    asks = list(order_book["asks"].items())[:levels]
    rows = []
    for i in range(levels):
        bid_price, bid_qty = bids[i] if i < len(bids) else ("", "")
        ask_price, ask_qty = asks[i] if i < len(asks) else ("", "")
        rows.append({
            "bid_price": bid_price,
            "bid_qty": bid_qty,
            "ask_price": ask_price,
            "ask_qty": ask_qty
        })
    return rows

async def initialize_orderbook():
    async with aiohttp.ClientSession() as session:
        async with session.get(depth_snapshot_url) as resp:
            data = await resp.json()
            apply_orderbook_update({"bids": data["bids"], "asks": data["asks"]})

async def stream_orderbook():
    await initialize_orderbook()
    print("Initialized local order book from snapshot.")
    async with websockets.connect(depth_stream_url) as websocket:
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            apply_orderbook_update({"bids": data["b"], "asks": data["a"]})
            rows = orderbook_to_rows(levels=20)
            with open("orderbook.csv", "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["bid_price", "bid_qty", "ask_price", "ask_qty"])
                writer.writeheader()
                writer.writerows(rows)

if __name__ == "__main__":
    asyncio.run(stream_orderbook())