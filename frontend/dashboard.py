import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

API_URL = "http://backend:8000"

def fetch_api(endpoint):

    try:
        response = requests.get(
            f"{API_URL}{endpoint}",
            timeout=15
        )

        data = response.json()

        if isinstance(data, dict) and data.get("error"):
            st.error(data["message"])
            return None

        return data

    except requests.exceptions.ConnectionError:
        st.error("Unable to connect to backend API. Please make sure the backend server is running.")
        return None

    except requests.exceptions.Timeout:
        st.error("Backend API request timed out. Please try again.")
        return None

    except Exception as e:
        st.error(f"Unexpected frontend error: {str(e)}")
        return None


st.set_page_config(
    page_title="Financial Market Sentiment Intelligence",
    layout="wide"
)

st.title("📈 Financial Market Sentiment Intelligence System")

st.caption("Institutional-style AI market sentiment and multi-asset intelligence dashboard")

refresh_button = st.button("🔄 Refresh Market Data")

market_data = fetch_api("/market-analysis")
forecast_data = fetch_api("/market-forecast")
insights_data = fetch_api("/market-insights")
trend_data = fetch_api("/sentiment-trend")
news_data = fetch_api("/news")
ticker_data = fetch_api("/ticker-analysis")
ml_prediction_data = fetch_api("/ml-prediction")

copilot_question = st.text_input(
    "Ask the AI Financial Copilot",
    placeholder="What is the market mood?"
)

if market_data is None:
    st.stop()

tracked_stocks = [
    "AAPL",
    "TSLA",
    "MSFT",
    "NVDA",
    "AMZN",
    "BTC-USD"
]

stock_market_data = []

for ticker in tracked_stocks:

    stock_data = fetch_api(f"/stock/{ticker}")

    if stock_data is not None:
        stock_market_data.append(stock_data)

st.subheader("Executive Market Overview")

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("Total Articles", market_data["total_articles"])
col2.metric("Positive", market_data["positive_news"])
col3.metric("Negative", market_data["negative_news"])
col4.metric("Neutral", market_data["neutral_news"])
col5.metric("Market Mood", market_data["market_mood"])
col6.metric("AI Signal", market_data["recommendation"])

st.divider()

st.subheader("Market Risk & Sentiment Strength")

risk_col1, risk_col2, risk_col3 = st.columns(3)

risk_col1.metric(
    "Sentiment Score",
    market_data["market_sentiment_score"]
)

risk_col2.metric(
    "Volatility Index",
    market_data.get("volatility_index", "N/A")
)

risk_col3.metric(
    "Sentiment Strength",
    market_data.get("sentiment_strength", "N/A")
)

gauge_fig = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=market_data["market_sentiment_score"],
        title={"text": "Market Sentiment Gauge"},
        gauge={
            "axis": {"range": [-100, 100]},
            "bar": {"color": "white"},
            "steps": [
                {"range": [-100, -35], "color": "#8B0000"},
                {"range": [-35, -15], "color": "#B22222"},
                {"range": [-15, 15], "color": "#444444"},
                {"range": [15, 35], "color": "#228B22"},
                {"range": [35, 100], "color": "#006400"}
            ],
        }
    )
)

st.plotly_chart(gauge_fig, width="stretch")

st.divider()

st.subheader("AI Market Forecast")

if forecast_data is not None:

    f1, f2, f3, f4 = st.columns(4)

    f1.metric("Forecast", forecast_data["forecast"])
    f2.metric("Confidence", forecast_data["confidence"])
    f3.metric("Momentum", forecast_data["momentum"])
    f4.metric("Risk Level", forecast_data["risk_level"])

    forecast_detail_col1, forecast_detail_col2, forecast_detail_col3 = st.columns(3)

    forecast_detail_col1.metric(
        "Average Sentiment",
        forecast_data.get("average_sentiment_score", "N/A")
    )

    forecast_detail_col2.metric(
        "Latest Sentiment",
        forecast_data.get("latest_sentiment_score", "N/A")
    )

    forecast_detail_col3.metric(
        "Average Volatility",
        forecast_data.get("average_volatility", "N/A")
    )

    confidence_fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=forecast_data["confidence"],
            title={"text": "Forecast Confidence"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "white"},
                "steps": [
                    {"range": [0, 30], "color": "#444444"},
                    {"range": [30, 70], "color": "#B8860B"},
                    {"range": [70, 100], "color": "#006400"}
                ],
            }
        )
    )

    st.plotly_chart(confidence_fig, width="stretch")

else:
    st.warning("AI market forecast is currently unavailable.")

st.divider()

st.subheader("AI Market Insights")

if insights_data is not None:
    for insight in insights_data["insights"]:
        st.info(insight)
else:
    st.warning("AI market insights are currently unavailable.")

st.divider()

st.subheader("Live Multi-Asset Market Data")

stock_df = pd.DataFrame(stock_market_data)

if not stock_df.empty:

    st.dataframe(stock_df, width="stretch")

    price_fig = px.bar(
        stock_df,
        x="ticker",
        y="current_price",
        title="Live Asset Price Comparison",
        text="current_price"
    )

    st.plotly_chart(price_fig, width="stretch")

    if "volume" in stock_df.columns:
        volume_fig = px.bar(
            stock_df,
            x="ticker",
            y="volume",
            title="Trading Volume Comparison"
        )

        st.plotly_chart(volume_fig, width="stretch")

else:
    st.warning("Stock market data is currently unavailable.")

st.divider()

st.subheader("Sentiment Distribution")

sentiment_counts = {
    "Positive": market_data["positive_news"],
    "Negative": market_data["negative_news"],
    "Neutral": market_data["neutral_news"]
}

chart_df = pd.DataFrame({
    "Sentiment": sentiment_counts.keys(),
    "Count": sentiment_counts.values()
})

pie_fig = px.pie(
    chart_df,
    values="Count",
    names="Sentiment",
    title="Market Sentiment Distribution",
    hole=0.4
)

st.plotly_chart(pie_fig, width="stretch")

bar_fig = px.bar(
    chart_df,
    x="Sentiment",
    y="Count",
    title="Sentiment Count Breakdown",
    text="Count"
)

st.plotly_chart(bar_fig, width="stretch")

st.divider()

st.subheader("AI Machine Learning Prediction Engine")

if ml_prediction_data is not None:

    ml_col1, ml_col2, ml_col3, ml_col4 = st.columns(4)

    ml_col1.metric(
        "Predicted Direction",
        ml_prediction_data.get(
            "predicted_market_direction",
            "N/A"
        )
    )

    ml_col2.metric(
        "Model Accuracy",
        ml_prediction_data.get(
            "model_accuracy",
            "N/A"
        )
    )

    ml_col3.metric(
        "Bullish Probability",
        ml_prediction_data.get(
            "bullish_probability",
            "N/A"
        )
    )

    ml_col4.metric(
        "Bearish Probability",
        ml_prediction_data.get(
            "bearish_probability",
            "N/A"
        )
    )

    st.metric(
        "Training Samples",
        ml_prediction_data.get(
            "training_samples",
            "N/A"
        )
    )

    if "bullish_probability" in ml_prediction_data and "bearish_probability" in ml_prediction_data:

        probability_df = pd.DataFrame({
            "Direction": [
                "Bullish",
                "Bearish"
            ],
            "Probability": [
                ml_prediction_data["bullish_probability"],
                ml_prediction_data["bearish_probability"]
            ]
        })

        probability_fig = px.bar(
            probability_df,
            x="Direction",
            y="Probability",
            title="ML Market Direction Probability",
            text="Probability"
        )

        st.plotly_chart(
            probability_fig,
            width="stretch"
        )

else:
    st.warning("ML prediction engine data unavailable.")

st.divider()

st.subheader("Institutional Ticker Intelligence")

if ticker_data is not None and len(ticker_data) > 0:

    ticker_rows = []

    for ticker, data in ticker_data.items():

        ticker_rows.append({
            "Ticker": ticker,
            "Signal": data["signal"],
            "Sentiment Score": data["ticker_sentiment_score"],
            "Mentions": data["total_mentions"],
            "Confidence": data["average_confidence"],
            "Positive": data["positive"],
            "Negative": data["negative"],
            "Neutral": data["neutral"]
        })

    ticker_df = pd.DataFrame(ticker_rows)

    ticker_df = ticker_df.sort_values(
        by="Sentiment Score",
        ascending=False
    )

    st.dataframe(
        ticker_df,
        width="stretch"
    )

    heatmap_fig = px.treemap(
        ticker_df,
        path=["Signal", "Ticker"],
        values="Mentions",
        color="Sentiment Score",
        color_continuous_scale="RdYlGn",
        title="Ticker Intelligence Heatmap"
    )

    st.plotly_chart(
        heatmap_fig,
        width="stretch"
    )

    bullish_df = ticker_df[
        ticker_df["Signal"] == "Bullish"
    ]

    bearish_df = ticker_df[
        ticker_df["Signal"] == "Bearish"
    ]

    col_bullish, col_bearish = st.columns(2)

    with col_bullish:

        st.subheader("Top Bullish Assets")

        if not bullish_df.empty:
            st.dataframe(
                bullish_df,
                width="stretch"
            )
        else:
            st.info("No bullish assets detected.")

    with col_bearish:

        st.subheader("Top Bearish Assets")

        if not bearish_df.empty:
            st.dataframe(
                bearish_df,
                width="stretch"
            )
        else:
            st.info("No bearish assets detected.")

else:
    st.warning("No ticker intelligence data available.")

st.divider()

st.subheader("Historical Sentiment Trend")

if trend_data is not None:
    trend_df = pd.DataFrame(trend_data)

    if not trend_df.empty:
        line_fig = px.line(
            trend_df,
            x="id",
            y="sentiment_value",
            title="Historical AI Sentiment Trend",
            markers=True
        )

        st.plotly_chart(line_fig, width="stretch")
    else:
        st.warning("No historical sentiment data available yet.")
else:
    st.warning("Sentiment trend data is currently unavailable.")

st.divider()

st.subheader("AI Financial Copilot")

if copilot_question:

    encoded_question = copilot_question.replace(
        " ",
        "%20"
    )

    copilot_response = fetch_api(
        f"/copilot?question={encoded_question}"
    )

    if copilot_response is not None:

        st.success(
            copilot_response.get(
                "answer",
                "No response generated."
            )
        )

        st.json(copilot_response)

st.subheader("Latest Financial News Intelligence Feed")

if news_data is not None:
    df = pd.DataFrame(news_data)

    if not df.empty:
        st.dataframe(df, width="stretch")
    else:
        st.warning("No financial news available right now.")
else:
    st.warning("Latest financial news is currently unavailable.")

if refresh_button:
    st.rerun()