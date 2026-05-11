def calculate_market_sentiment(news_articles):

    positive = 0
    negative = 0
    neutral = 0

    positive_confidence = 0
    negative_confidence = 0
    neutral_confidence = 0

    for article in news_articles:

        sentiment = article["sentiment"].lower()

        confidence = article.get("confidence", 0.5)

        if sentiment == "positive":
            positive += 1
            positive_confidence += confidence

        elif sentiment == "negative":
            negative += 1
            negative_confidence += confidence

        else:
            neutral += 1
            neutral_confidence += confidence

    total = positive + negative + neutral

    if total == 0:
        score = 0

    else:
        weighted_positive = positive * (
            positive_confidence / max(positive, 1)
        )

        weighted_negative = negative * (
            negative_confidence / max(negative, 1)
        )

        score = (
            (weighted_positive - weighted_negative)
            / total
        ) * 100

    if score >= 35:
        market_mood = "Strong Bullish"

    elif score >= 15:
        market_mood = "Bullish"

    elif score <= -35:
        market_mood = "Strong Bearish"

    elif score <= -15:
        market_mood = "Bearish"

    else:
        market_mood = "Neutral"

    volatility_index = round(
        abs(positive - negative) / max(total, 1) * 100,
        2
    )

    sentiment_strength = round(
        (
            positive_confidence +
            negative_confidence +
            neutral_confidence
        ) / max(total, 1),
        2
    )

    return {
        "total_articles": total,
        "positive_news": positive,
        "negative_news": negative,
        "neutral_news": neutral,
        "market_sentiment_score": round(score, 2),
        "market_mood": market_mood,
        "volatility_index": volatility_index,
        "sentiment_strength": sentiment_strength
    }