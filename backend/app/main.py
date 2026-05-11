import logging
import time

from app.market_snapshot import MarketSnapshot
from app.market_insights import generate_market_insights
from app.recommendation_engine import generate_recommendation
from app.stock_data import get_stock_price
from app.trend_analysis import calculate_sentiment_trend
from app.ticker_analytics import calculate_ticker_sentiment
from app.analytics import calculate_market_sentiment
from app.database import engine, SessionLocal
from app.models import NewsArticle
from app.sentiment import analyze_sentiment
from app.entity_extractor import extract_tickers
from fastapi import FastAPI
from app.config import NEWS_API_KEY
from app.news_fetcher import fetch_financial_news

app = FastAPI(
    title="Financial Market Sentiment Intelligence System",
    description="AI-powered financial news sentiment analysis platform",
    version="0.1.0"
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

NewsArticle.metadata.create_all(bind=engine)
MarketSnapshot.metadata.create_all(bind=engine)

@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {
        "message": "Financial Market Sentiment Intelligence System API is running"
    }

@app.get("/health")
def health_check():
    logger.info("Health check endpoint accessed")
    return {
        "status": "healthy"
    }

@app.get("/news")
def get_news():

    start_time = time.time()
    logger.info("News endpoint called")

    news = fetch_financial_news(NEWS_API_KEY)

    if isinstance(news, dict) and news.get("error"):
        logger.error(f"News fetch error: {news['message']}")
        return news

    analyzed_news = []

    for article in news:

        sentiment = analyze_sentiment(article["title"])
        tickers = extract_tickers(article["title"])

        analyzed_news.append({
            "title": article["title"],
            "source": article["source"],
            "published_at": article["published_at"],
            "sentiment": sentiment["label"],
            "confidence": sentiment["score"],
            "tickers": tickers
        })

        db = SessionLocal()

        news_item = NewsArticle(
            title=article["title"],
            source=article["source"],
            published_at=article["published_at"],
            sentiment=sentiment["label"],
            confidence=sentiment["score"]
        )

        db.add(news_item)
        db.commit()
        db.close()

    elapsed_time = round(time.time() - start_time, 2)

    logger.info(f"Analyzed {len(analyzed_news)} news articles in {elapsed_time} seconds")

    return analyzed_news

@app.get("/history")
def get_history():

    logger.info("History endpoint called")

    db = SessionLocal()

    articles = db.query(NewsArticle).all()

    history = []

    for article in articles:
        history.append({
            "id": article.id,
            "title": article.title,
            "source": article.source,
            "published_at": article.published_at,
            "sentiment": article.sentiment,
            "confidence": article.confidence
        })

    db.close()

    logger.info(f"Returned {len(history)} historical records")

    return history

@app.get("/market-analysis")
def market_analysis():

    start_time = time.time()
    logger.info("Market analysis endpoint called")

    news = fetch_financial_news(NEWS_API_KEY)

    if isinstance(news, dict) and news.get("error"):
        logger.error(f"Market analysis error: {news['message']}")
        return news

    analyzed_news = []

    for article in news:

        sentiment = analyze_sentiment(article["title"])

        analyzed_news.append({
            "title": article["title"],
            "sentiment": sentiment["label"],
            "confidence": sentiment["score"]
        })

    analytics = calculate_market_sentiment(analyzed_news)

    analytics["recommendation"] = generate_recommendation(
        analytics["market_sentiment_score"]
    )

    db = SessionLocal()

    snapshot = MarketSnapshot(
        market_sentiment_score=analytics["market_sentiment_score"],
        market_mood=analytics["market_mood"],
        positive_news=analytics["positive_news"],
        negative_news=analytics["negative_news"],
        neutral_news=analytics["neutral_news"],
        volatility_index=analytics["volatility_index"],
        sentiment_strength=analytics["sentiment_strength"]
    )

    db.add(snapshot)
    db.commit()
    db.close()

    elapsed_time = round(time.time() - start_time, 2)

    logger.info(f"Market analysis completed and snapshot saved in {elapsed_time} seconds")

    return analytics

@app.get("/ticker-analysis")
def ticker_analysis():

    logger.info("Ticker analysis endpoint called")

    news = fetch_financial_news(NEWS_API_KEY)

    if isinstance(news, dict) and news.get("error"):
        logger.error(f"Ticker analysis error: {news['message']}")
        return news

    analyzed_news = []

    for article in news:

        sentiment = analyze_sentiment(article["title"])
        tickers = extract_tickers(article["title"])

        analyzed_news.append({
            "title": article["title"],
            "sentiment": sentiment["label"],
            "tickers": tickers
        })

    ticker_data = calculate_ticker_sentiment(analyzed_news)

    logger.info(f"Ticker analysis completed with {len(ticker_data)} tickers detected")

    return ticker_data

@app.get("/sentiment-trend")
def sentiment_trend():

    logger.info("Sentiment trend endpoint called")

    db = SessionLocal()

    articles = db.query(NewsArticle).all()

    trend_data = calculate_sentiment_trend(articles)

    db.close()

    logger.info(f"Returned {len(trend_data)} sentiment trend records")

    return trend_data

@app.get("/stock/{ticker}")
def stock_price(ticker: str):

    logger.info(f"Stock endpoint called for ticker: {ticker.upper()}")

    stock_data = get_stock_price(ticker.upper())

    return stock_data

@app.get("/market-insights")
def market_insights():

    logger.info("Market insights endpoint called")

    market_data = market_analysis()
    ticker_data = ticker_analysis()

    insights = generate_market_insights(
        market_data,
        ticker_data
    )

    logger.info("Market insights generated successfully")

    return {
        "insights": insights
    }