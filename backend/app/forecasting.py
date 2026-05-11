def generate_market_forecast(snapshots):

    if not snapshots:
        return {
            "forecast": "Insufficient data",
            "confidence": 0,
            "momentum": "Unknown",
            "risk_level": "Unknown",
            "message": "Not enough historical market snapshots available for forecasting."
        }

    recent_snapshots = snapshots[-5:]

    scores = [
        snapshot.market_sentiment_score
        for snapshot in recent_snapshots
    ]

    volatility_values = [
        snapshot.volatility_index
        for snapshot in recent_snapshots
    ]

    average_score = sum(scores) / len(scores)
    latest_score = scores[-1]
    first_score = scores[0]

    momentum_value = latest_score - first_score

    if momentum_value > 10:
        momentum = "Improving"
    elif momentum_value < -10:
        momentum = "Weakening"
    else:
        momentum = "Stable"

    average_volatility = sum(volatility_values) / len(volatility_values)

    if average_volatility >= 60:
        risk_level = "High"
    elif average_volatility >= 30:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    if average_score >= 20 and momentum != "Weakening":
        forecast = "Bullish Outlook"
    elif average_score <= -20 and momentum != "Improving":
        forecast = "Bearish Outlook"
    else:
        forecast = "Neutral / Mixed Outlook"

    confidence = min(
        100,
        round(abs(average_score) + average_volatility / 2, 2)
    )

    return {
        "forecast": forecast,
        "confidence": confidence,
        "momentum": momentum,
        "risk_level": risk_level,
        "average_sentiment_score": round(average_score, 2),
        "latest_sentiment_score": round(latest_score, 2),
        "average_volatility": round(average_volatility, 2),
        "snapshots_used": len(recent_snapshots)
    }