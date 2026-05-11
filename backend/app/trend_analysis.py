def calculate_sentiment_trend(history_articles):

    trend_data = []

    sentiment_mapping = {
        "positive": 1,
        "neutral": 0,
        "negative": -1
    }

    for article in history_articles:

        sentiment_value = sentiment_mapping.get(
            article.sentiment.lower(),
            0
        )

        trend_data.append({
            "id": article.id,
            "published_at": article.published_at,
            "sentiment": article.sentiment,
            "sentiment_value": sentiment_value,
            "confidence": article.confidence
        })

    return trend_data