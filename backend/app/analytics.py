def calculate_market_sentiment(news_articles):

    positive = 0
    negative = 0
    neutral = 0

    for article in news_articles:

        sentiment = article["sentiment"].lower()

        if sentiment == "positive":
            positive += 1

        elif sentiment == "negative":
            negative += 1

        else:
            neutral += 1

    total = positive + negative + neutral

    if total == 0:
        score = 0
    else:
        score = ((positive - negative) / total) * 100

    if score > 20:
        market_mood = "Bullish"

    elif score < -20:
        market_mood = "Bearish"

    else:
        market_mood = "Neutral"

    return {
        "total_articles": total,
        "positive_news": positive,
        "negative_news": negative,
        "neutral_news": neutral,
        "market_sentiment_score": round(score, 2),
        "market_mood": market_mood
    }