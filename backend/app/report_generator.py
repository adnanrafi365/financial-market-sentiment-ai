def generate_market_report(market_data, forecast_data, ticker_data, insights_data):

    bullish_assets = []
    bearish_assets = []

    for ticker, data in ticker_data.items():

        if data.get("signal") == "Bullish":
            bullish_assets.append(ticker)

        elif data.get("signal") == "Bearish":
            bearish_assets.append(ticker)

    report = {
        "title": "AI Financial Market Intelligence Report",
        "market_summary": {
            "market_mood": market_data.get("market_mood"),
            "sentiment_score": market_data.get("market_sentiment_score"),
            "recommendation": market_data.get("recommendation"),
            "volatility_index": market_data.get("volatility_index"),
            "sentiment_strength": market_data.get("sentiment_strength")
        },
        "forecast_summary": {
            "forecast": forecast_data.get("forecast"),
            "confidence": forecast_data.get("confidence"),
            "momentum": forecast_data.get("momentum"),
            "risk_level": forecast_data.get("risk_level")
        },
        "ticker_summary": {
            "bullish_assets": bullish_assets,
            "bearish_assets": bearish_assets,
            "total_tickers_detected": len(ticker_data)
        },
        "ai_insights": insights_data.get("insights", [])
    }

    return report