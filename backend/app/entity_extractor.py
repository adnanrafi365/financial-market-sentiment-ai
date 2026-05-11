import re

TICKER_MAPPINGS = {

    "APPLE": "AAPL",
    "IPHONE": "AAPL",

    "MICROSOFT": "MSFT",
    "WINDOWS": "MSFT",
    "OPENAI": "MSFT",
    "CHATGPT": "MSFT",

    "GOOGLE": "GOOGL",
    "ALPHABET": "GOOGL",
    "YOUTUBE": "GOOGL",

    "AMAZON": "AMZN",
    "AWS": "AMZN",

    "TESLA": "TSLA",
    "ELON MUSK": "TSLA",

    "META": "META",
    "FACEBOOK": "META",
    "INSTAGRAM": "META",

    "NVIDIA": "NVDA",
    "AI CHIP": "NVDA",

    "NETFLIX": "NFLX",

    "AMD": "AMD",

    "INTEL": "INTC",

    "BITCOIN": "BTC",
    "BTC": "BTC",

    "ETHEREUM": "ETH",
    "ETH": "ETH",

    "PALANTIR": "PLTR",

    "DELL": "DELL",

    "ARAMCO": "2222.SR",

    "GOLDMAN SACHS": "GS",

    "JPMORGAN": "JPM",

    "MORGAN STANLEY": "MS",

    "BANK OF AMERICA": "BAC",

    "CITIGROUP": "C",

    "UBER": "UBER",

    "AIRBNB": "ABNB",

    "COINBASE": "COIN",

    "ROBINHOOD": "HOOD",

    "WALMART": "WMT",

    "COSTCO": "COST",

    "DISNEY": "DIS",

    "NIKE": "NKE",

    "COCA COLA": "KO",

    "PEPSI": "PEP",

    "MCDONALDS": "MCD",

    "STARBUCKS": "SBUX"
}

def extract_tickers(text):

    found_tickers = []

    text_upper = text.upper()

    for keyword, ticker in TICKER_MAPPINGS.items():

        pattern = r'\b' + re.escape(keyword) + r'\b'

        if re.search(pattern, text_upper):

            if ticker not in found_tickers:
                found_tickers.append(ticker)

    explicit_tickers = re.findall(
        r'\b[A-Z]{2,5}\b',
        text_upper
    )

    known_tickers = set(TICKER_MAPPINGS.values())

    for ticker in explicit_tickers:

        if ticker in known_tickers:

            if ticker not in found_tickers:
                found_tickers.append(ticker)

    return found_tickers