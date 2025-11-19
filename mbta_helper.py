import os
import requests
from dotenv import load_dotenv

load_dotenv()

MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MBTA_API_KEY = os.getenv("MBTA_API_KEY")

MAPBOX_BASE_URL = "https://api.mapbox.com/search/searchbox/v1/forward"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"


def get_json(url: str, params: dict = None):
    """Return parsed JSON from a URL request."""
    response = requests.get(url, params=params)
    print ("REQUEST URL:", response.url)  # DEBUG
    response.raise_for_status()
    return response.json()


def get_lat_lon(place_name: str):
    """Convert a place name into (lat, lon) using Mapbox."""
    params = {
        "q": place_name,
        "access_token": MAPBOX_TOKEN,
        "limit": 1,
    }

    data = get_json(MAPBOX_BASE_URL, params=params)
    features = data.get("features", [])

    if not features:
        return None, None

    center = features[0]["geometry"]["coordinates"]
    lon, lat = center[0], center[1]
    return lat, lon


def get_nearest_station(lat, lon):
    """Return the closest MBTA station name and wheelchair accessibility."""
    url = MBTA_BASE_URL
    params = {
        "api_key": MBTA_API_KEY,
        "sort": "distance",
        "filter[latitude]": lat,
        "filter[longitude]": lon,
    }

    data = get_json(url, params=params)
    stops = data.get("data", [])

    if not stops:
        return None, None

    first = stops[0]
    name = first["attributes"]["name"]
    wheelchair = first["attributes"]["wheelchair_boarding"]

    if wheelchair == 1:
        accessible = "Wheelchair accessible"
    elif wheelchair == 2:
        accessible = "Not wheelchair accessible"
    else:
        accessible = "Accessibility unknown"

    return name, accessible


def find_stop_near(place_name: str):
    """Main function: returns (station, accessibility)."""
    lat, lon = get_lat_lon(place_name)

    if lat is None:
        return None, None

    return get_nearest_station(lat, lon)
if __name__ == "__main__":
    print("Testing with: Boston Common")
    lat, lon = get_lat_lon("Boston Common")
    print("Coordinates:", (lat, lon))
    station, accessible = find_stop_near("Boston Common")
    print("Nearest station:", station)
    print("Accessibility:", accessible)



# hola prueba 