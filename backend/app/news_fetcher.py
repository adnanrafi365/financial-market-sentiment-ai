import requests

NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

def fetch_financial_news(api_key: str):

    params = {
        "category": "business",
        "language": "en",
        "pageSize": 10,
        "apiKey": api_key
    }

    response = requests.get(NEWS_API_URL, params=params)

    if response.status_code != 200:
        return {
            "error": "Failed to fetch news",
            "status_code": response.status_code
        }

    data = response.json()

    articles = []

    for article in data.get("articles", []):
        articles.append({
            "title": article.get("title"),
            "source": article.get("source", {}).get("name"),
            "published_at": article.get("publishedAt"),
            "url": article.get("url")
        })

    return articles