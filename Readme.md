**# Binance SOL/USDT Order Book Tracker**

This script connects to Binance's public API and WebSocket to maintain a real-time order book for any trading pair. It stores the top 20 levels of bids and asks in a CSV file (`orderbook.csv`) that gets updated continuously.

**## Features**

- Fetches an initial snapshot of the order book from Binance REST API.
- Maintains a live order book using Binance's WebSocket depth stream (`@depth@100ms`).
- Stores the top 20 bids and asks into a CSV file (`orderbook.csv`) in real time.
- Uses `ujson` for fast JSON processing and `SortedContainers` for efficient sorted order book management.

**## Requirements**

- Python 3.7+
- Dependencies:
  - `aiohttp`
  - `websockets`
  - `ujson`
  - `sortedcontainers`

Install the required packages using pip:

```bash
pip install aiohttp websockets ujson sortedcontainers

**Next Steps**
Add a local db to track all top levels.
