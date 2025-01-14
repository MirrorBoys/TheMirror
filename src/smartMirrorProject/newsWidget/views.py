import feedparser
from django.http import JsonResponse
import requests


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
    newsData = {"articles": []}

    try:
        # Check if the feed URL is accessible
        response = requests.get(feed_url, timeout=5)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        # Parse the RSS feed
        feed = feedparser.parse(response.content)
        for entry in feed.entries[:numberOfArticles]:
            newsData["articles"].append({"title": entry.title, "link": entry.link})
    except requests.exceptions.RequestException as e:
        # Handle exceptions for the HTTP request
        return JsonResponse(
            {
                "error": "Failed to fetch news articles. Please try again later.",
                "details": str(e),
            },
            status=500,
        )
    except Exception as e:
        # Handle any other exceptions
        return JsonResponse(
            {"error": "An unexpected error occurred.", "details": str(e)}, status=500
        )

    return JsonResponse(newsData)
