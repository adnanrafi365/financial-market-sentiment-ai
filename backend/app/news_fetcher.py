import requests

NEWS_API_URL = "https://newsapi.org/v2/top-headlines"


def fetch_financial_news(api_key: str):

    if not api_key:
        return {
            "error": True,
            "message": "Missing NewsAPI key. Please set NEWS_API_KEY in environment variables."
        }

    params = {
        "category": "business",
        "language": "en",
        "pageSize": 10,
        "apiKey": api_key
    }

    try:
        response = requests.get(
            NEWS_API_URL,
            params=params,
            timeout=10
        )

        if response.status_code == 401:
            return {
                "error": True,
                "message": "Invalid or unauthorized NewsAPI key."
            }

        if response.status_code == 429:
            return {
                "error": True,
                "message": "NewsAPI rate limit exceeded. Please try again later."
            }

        if response.status_code != 200:
            return {
                "error": True,
                "message": "Failed to fetch news from NewsAPI.",
                "status_code": response.status_code
            }

        data = response.json()

        articles = data.get("articles", [])

        if not articles:
            return {
                "error": True,
                "message": "No financial news articles found."
            }

        cleaned_articles = []

        for article in articles:
            title = article.get("title")

            if not title:
                continue

            cleaned_articles.append({
                "title": title,
                "source": article.get("source", {}).get("name", "Unknown"),
                "published_at": article.get("publishedAt", "Unknown"),
                "url": article.get("url", "")
            })

        if not cleaned_articles:
            return {
                "error": True,
                "message": "No valid news headlines found."
            }

        return cleaned_articles

    except requests.exceptions.Timeout:
        return {
            "error": True,
            "message": "NewsAPI request timed out."
        }

    except requests.exceptions.ConnectionError:
        return {
            "error": True,
            "message": "Network connection error while fetching news."
        }

    except Exception as e:
        return {
            "error": True,
            "message": f"Unexpected error while fetching news: {str(e)}"
        }