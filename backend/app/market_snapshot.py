from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from app.database import Base

class MarketSnapshot(Base):

    __tablename__ = "market_snapshots"

    id = Column(Integer, primary_key=True, index=True)

    market_sentiment_score = Column(Float)

    market_mood = Column(String)

    positive_news = Column(Integer)

    negative_news = Column(Integer)

    neutral_news = Column(Integer)

    volatility_index = Column(Float)

    sentiment_strength = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)