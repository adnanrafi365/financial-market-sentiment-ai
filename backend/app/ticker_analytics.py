def calculate_ticker_sentiment(news_articles):

    ticker_summary = {}

    for article in news_articles:

        sentiment = article["sentiment"].lower()
        tickers = article.get("tickers", [])

        for ticker in tickers:

            if ticker not in ticker_summary:
                ticker_summary[ticker] = {
                    "positive": 0,
                    "negative": 0,
                    "neutral": 0,
                    "total_mentions": 0
                }

            ticker_summary[ticker]["total_mentions"] += 1

            if sentiment == "positive":
                ticker_summary[ticker]["positive"] += 1
            elif sentiment == "negative":
                ticker_summary[ticker]["negative"] += 1
            else:
                ticker_summary[ticker]["neutral"] += 1

    return ticker_summary