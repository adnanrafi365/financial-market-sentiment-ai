def generate_market_insights(market_data, ticker_data):

    insights = []

    score = market_data["market_sentiment_score"]

    if score >= 50:
        insights.append("Overall market sentiment is strongly bullish.")

    elif score >= 10:
        insights.append("Market sentiment is moderately positive.")

    elif score <= -50:
        insights.append("Market sentiment is extremely bearish.")

    elif score <= -10:
        insights.append("Market sentiment is moderately bearish.")

    else:
        insights.append("Market sentiment is neutral.")

    bullish_assets = []
    bearish_assets = []

    for ticker, data in ticker_data.items():

        positive = data["positive"]
        negative = data["negative"]

        if positive > negative:
            bullish_assets.append(ticker)

        elif negative > positive:
            bearish_assets.append(ticker)

    insights.append(
        f"Bullish assets detected: {', '.join(bullish_assets) if bullish_assets else 'None'}"
    )

    insights.append(
        f"Bearish assets detected: {', '.join(bearish_assets) if bearish_assets else 'None'}"
    )

    volatility_score = abs(score)

    if volatility_score >= 60:
        risk = "HIGH RISK"

    elif volatility_score >= 30:
        risk = "MEDIUM RISK"

    else:
        risk = "LOW RISK"

    insights.append(f"Current market volatility risk: {risk}")

    return insights