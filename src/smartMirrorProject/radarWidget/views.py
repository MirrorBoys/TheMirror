from django.http import JsonResponse
import requests

def get_lat_lon(placename):
    url = f"https://api.pdok.nl/bzk/locatieserver/search/v3_1/free?q={placename}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data["response"]["docs"]:
            centroide_ll = data["response"]["docs"][0]["centroide_ll"]
            lon, lat = map(float, centroide_ll.strip("POINT()").split())
            return lon, lat
        else:
            return None
    except Exception:
        return None

def fetch_coordinates(request, placename):
    """
    API endpoint to fetch coordinates of a given placename.
    """
    coordinates = get_lat_lon(placename)
    if coordinates:
        return JsonResponse({"latitude": coordinates[1], "longitude": coordinates[0], "placename": placename})
    else:
        return JsonResponse({"error": "Coordinates not found"}, status=404)
