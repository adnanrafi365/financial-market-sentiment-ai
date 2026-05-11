import streamlit as st
import requests
import pandas as pd
import plotly.express as px
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

st.caption("Live AI-powered market dashboard")

st.subheader("Real-Time AI Financial News Analytics")

refresh_button = st.button("🔄 Refresh Market Data")

market_data = fetch_api("/market-analysis")
insights_data = fetch_api("/market-insights")
trend_data = fetch_api("/sentiment-trend")
news_data = fetch_api("/news")

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

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Articles",
    market_data["total_articles"]
)

col2.metric(
    "Positive News",
    market_data["positive_news"]
)

col3.metric(
    "Negative News",
    market_data["negative_news"]
)

col4.metric(
    "Market Mood",
    market_data["market_mood"]
)

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
        title="Live Asset Price Comparison"
    )

    st.plotly_chart(price_fig, width="stretch")
else:
    st.warning("Stock market data is currently unavailable.")

st.divider()

st.subheader("Market Sentiment Score")

st.metric(
    "Sentiment Score",
    market_data["market_sentiment_score"]
)

st.metric(
    "AI Recommendation",
    market_data["recommendation"]
)

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
    title="Market Sentiment Distribution"
)

st.plotly_chart(pie_fig, width="stretch")

st.divider()

st.subheader("Historical Sentiment Trend")

if trend_data is not None:
    trend_df = pd.DataFrame(trend_data)

    if not trend_df.empty:
        line_fig = px.line(
            trend_df,
            x="id",
            y="sentiment_value",
            title="Historical AI Sentiment Trend"
        )

        st.plotly_chart(line_fig, width="stretch")
    else:
        st.warning("No historical sentiment data available yet.")
else:
    st.warning("Sentiment trend data is currently unavailable.")

st.divider()

st.subheader("Latest Financial News")

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