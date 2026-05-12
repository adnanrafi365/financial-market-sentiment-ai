import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def train_market_model(snapshots):

    if len(snapshots) < 10:
        return {
            "error": True,
            "message": "Not enough historical data to train ML model. Please generate at least 10 market snapshots."
        }

    data = []

    for snapshot in snapshots:

        target = 1 if snapshot.market_sentiment_score > 0 else 0

        data.append({
            "sentiment_score": snapshot.market_sentiment_score,
            "volatility": snapshot.volatility_index,
            "sentiment_strength": snapshot.sentiment_strength,
            "target": target
        })

    df = pd.DataFrame(data)

    if df["target"].nunique() < 2:
        return {
            "error": True,
            "message": "ML model needs both bullish and bearish/neutral examples before training."
        }

    X = df[
        [
            "sentiment_score",
            "volatility",
            "sentiment_strength"
        ]
    ]

    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = LogisticRegression()

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    latest_data = X.tail(1)

    future_prediction = model.predict(latest_data)[0]

    probability = model.predict_proba(latest_data)[0]

    bearish_probability = round(probability[0] * 100, 2)
    bullish_probability = round(probability[1] * 100, 2)

    outlook = (
        "Bullish"
        if future_prediction == 1
        else "Bearish"
    )

    return {
        "model_accuracy": round(accuracy * 100, 2),
        "predicted_market_direction": outlook,
        "bullish_probability": bullish_probability,
        "bearish_probability": bearish_probability,
        "training_samples": len(df)
    }