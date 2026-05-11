from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class NewsArticle(Base):
    __tablename__ = "news_articles"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    source = Column(String, nullable=False)

    published_at = Column(String, nullable=False)

    sentiment = Column(String, nullable=False)

    confidence = Column(Float, nullable=False)