def generate_copilot_response(question, market_data, forecast_data, ticker_data):

    question_lower = question.lower()

    if "market" in question_lower or "overall" in question_lower:
        return (
            f"The current market mood is {market_data.get('market_mood')}. "
            f"The sentiment score is {market_data.get('market_sentiment_score')}, "
            f"with a recommendation of {market_data.get('recommendation')}. "
            f"The forecast is {forecast_data.get('forecast')} with "
            f"{forecast_data.get('confidence')}% confidence."
        )

    if "risk" in question_lower or "volatility" in question_lower:
        return (
            f"The current risk level is {forecast_data.get('risk_level')}. "
            f"The average volatility is {forecast_data.get('average_volatility')}, "
            f"and the volatility index is {market_data.get('volatility_index')}."
        )

    if "bullish" in question_lower:
        bullish_assets = []

        for ticker, data in ticker_data.items():
            if data.get("signal") == "Bullish":
                bullish_assets.append(ticker)

        if bullish_assets:
            return f"The currently bullish assets are: {', '.join(bullish_assets)}."

        return "No clearly bullish assets are detected right now."

    if "bearish" in question_lower:
        bearish_assets = []

        for ticker, data in ticker_data.items():
            if data.get("signal") == "Bearish":
                bearish_assets.append(ticker)

        if bearish_assets:
            return f"The currently bearish assets are: {', '.join(bearish_assets)}."

        return "No clearly bearish assets are detected right now."

    return (
        "Based on current data, the system is tracking market sentiment, "
        "forecast confidence, volatility, ticker intelligence, and financial news. "
        "Try asking about market mood, bullish assets, bearish assets, or risk level."
    )