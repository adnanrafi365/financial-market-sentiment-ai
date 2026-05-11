import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import time

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Financial Market Sentiment Intelligence",
    layout="wide"
)

st.title("📈 Financial Market Sentiment Intelligence System")

st.caption("Live AI-powered market dashboard")

st.subheader("Real-Time AI Financial News Analytics")

refresh_button = st.button("🔄 Refresh Market Data")

market_response = requests.get(f"{API_URL}/market-analysis")
market_data = market_response.json()

insights_response = requests.get(f"{API_URL}/market-insights")
insights_data = insights_response.json()

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

    response = requests.get(f"{API_URL}/stock/{ticker}")

    stock_market_data.append(response.json())

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

for insight in insights_data["insights"]:
    st.info(insight)

st.divider()

st.subheader("Live Multi-Asset Market Data")

stock_df = pd.DataFrame(stock_market_data)

st.dataframe(stock_df, use_container_width=True)

if not stock_df.empty:

    price_fig = px.bar(
        stock_df,
        x="ticker",
        y="current_price",
        title="Live Asset Price Comparison"
    )

    st.plotly_chart(price_fig, use_container_width=True)

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

st.plotly_chart(pie_fig, use_container_width=True)

st.divider()

st.subheader("Historical Sentiment Trend")

trend_response = requests.get(f"{API_URL}/sentiment-trend")
trend_data = trend_response.json()

trend_df = pd.DataFrame(trend_data)

if not trend_df.empty:

    line_fig = px.line(
        trend_df,
        x="id",
        y="sentiment_value",
        title="Historical AI Sentiment Trend"
    )

    st.plotly_chart(line_fig, use_container_width=True)

st.divider()

st.subheader("Latest Financial News")

news_response = requests.get(f"{API_URL}/news")
news_data = news_response.json()

df = pd.DataFrame(news_data)

st.dataframe(df, use_container_width=True)

if refresh_button:
    st.rerun()