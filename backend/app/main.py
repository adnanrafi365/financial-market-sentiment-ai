from fastapi import FastAPI

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