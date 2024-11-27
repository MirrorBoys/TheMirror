import feedparser
from django.http import JsonResponse

def fetch_news(request, numberOfArticles):
    """
    Fetches the latest news articles from the NU.nl RSS feed and returns them as a JSON response.

    Args:
        request: The HTTP request object.
        numberOfArticles (int): The number of news articles to fetch.

    Returns:
        JsonResponse: A JSON response containing the latest news articles with their titles and links.
    """
    feed_url = "https://www.nu.nl/rss"
    feed = feedparser.parse(feed_url)
    newsData = {
        "articles": []
        }

    for entry in feed.entries[:numberOfArticles]:
        newsData["articles"].append(
            {
                "title": entry.title,
                "link": entry.link
            }
        )

    return JsonResponse(newsData)
