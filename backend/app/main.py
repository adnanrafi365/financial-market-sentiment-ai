from app.database import engine, SessionLocal
from app.models import NewsArticle
from app.sentiment import analyze_sentiment
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

        analyzed_news.append({
            "title": article["title"],
            "source": article["source"],
            "published_at": article["published_at"],
            "sentiment": sentiment["label"],
            "confidence": sentiment["score"]
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