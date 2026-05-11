def calculate_ticker_sentiment(news_articles):

    ticker_summary = {}

    for article in news_articles:

        sentiment = article["sentiment"].lower()
        confidence = article.get("confidence", 0.5)
        tickers = article.get("tickers", [])

        for ticker in tickers:

            if ticker not in ticker_summary:
                ticker_summary[ticker] = {
                    "positive": 0,
                    "negative": 0,
                    "neutral": 0,
                    "total_mentions": 0,
                    "confidence_total": 0
                }

            ticker_summary[ticker]["total_mentions"] += 1
            ticker_summary[ticker]["confidence_total"] += confidence

            if sentiment == "positive":
                ticker_summary[ticker]["positive"] += 1

            elif sentiment == "negative":
                ticker_summary[ticker]["negative"] += 1

            else:
                ticker_summary[ticker]["neutral"] += 1

    ranked_tickers = {}

    for ticker, data in ticker_summary.items():

        total = data["total_mentions"]

        sentiment_score = (
            (data["positive"] - data["negative"]) / total
        ) * 100

        average_confidence = data["confidence_total"] / total

        if sentiment_score >= 25:
            signal = "Bullish"

        elif sentiment_score <= -25:
            signal = "Bearish"

        else:
            signal = "Neutral"

        ranked_tickers[ticker] = {
            "positive": data["positive"],
            "negative": data["negative"],
            "neutral": data["neutral"],
            "total_mentions": total,
            "ticker_sentiment_score": round(sentiment_score, 2),
            "average_confidence": round(average_confidence, 2),
            "signal": signal
        }

    return ranked_tickers