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

NewsArticle.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {
        "message": "Financial Market Sentiment Intelligence System API is running"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

@app.get("/news")
def get_news():

    news = fetch_financial_news(NEWS_API_KEY)

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

    return analyzed_news

@app.get("/history")
def get_history():

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

    return history

@app.get("/market-analysis")
def market_analysis():

    news = fetch_financial_news(NEWS_API_KEY)

    analyzed_news = []

    for article in news:

        sentiment = analyze_sentiment(article["title"])

        analyzed_news.append({
            "title": article["title"],
            "sentiment": sentiment["label"]
        })

    analytics = calculate_market_sentiment(analyzed_news)

    return analytics

@app.get("/ticker-analysis")
def ticker_analysis():

    news = fetch_financial_news(NEWS_API_KEY)

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

    return ticker_data

@app.get("/sentiment-trend")
def sentiment_trend():

    db = SessionLocal()

    articles = db.query(NewsArticle).all()

    trend_data = calculate_sentiment_trend(articles)

    db.close()

    return trend_data