import yfinance as yf

def get_stock_price(ticker):

    try:

        stock = yf.Ticker(ticker)

        info = stock.info

        return {
            "ticker": ticker,
            "company": info.get("shortName"),
            "current_price": info.get("currentPrice"),
            "market_cap": info.get("marketCap"),
            "volume": info.get("volume"),
            "previous_close": info.get("previousClose"),
            "open": info.get("open")
        }

    except Exception:

        return {
            "ticker": ticker,
            "error": "Unable to fetch stock data"
        }