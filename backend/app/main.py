from app.sentiment import analyze_sentiment
from fastapi import FastAPI
from app.config import NEWS_API_KEY
from app.news_fetcher import fetch_financial_news

app = FastAPI(
    title="Financial Market Sentiment Intelligence System",
    description="AI-powered financial news sentiment analysis platform",
    version="0.1.0"
)

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

        analyzed_news.append({
            "title": article["title"],
            "source": article["source"],
            "published_at": article["published_at"],
            "sentiment": sentiment["label"],
            "confidence": sentiment["score"]
        })

    return analyzed_news