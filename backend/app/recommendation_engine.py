def generate_recommendation(sentiment_score):

    if sentiment_score >= 50:
        return "STRONG BUY"

    elif sentiment_score >= 10:
        return "BUY"

    elif sentiment_score > -10:
        return "HOLD"

    elif sentiment_score > -50:
        return "SELL"

    return "STRONG SELL"