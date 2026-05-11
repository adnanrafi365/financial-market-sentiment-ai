import re

TICKER_MAPPINGS = {
    "APPLE": "AAPL",
    "MICROSOFT": "MSFT",
    "GOOGLE": "GOOGL",
    "AMAZON": "AMZN",
    "TESLA": "TSLA",
    "META": "META",
    "NVIDIA": "NVDA",
    "NETFLIX": "NFLX",
    "AMD": "AMD",
    "INTEL": "INTC",
    "BITCOIN": "BTC",
    "ETHEREUM": "ETH",
    "PALANTIR": "PLTR"
}

def extract_tickers(text):

    found_tickers = []

    text_upper = text.upper()

    for company, ticker in TICKER_MAPPINGS.items():

        pattern = r'\b' + company + r'\b'

        if re.search(pattern, text_upper):

            if ticker not in found_tickers:
                found_tickers.append(ticker)

    return found_tickers