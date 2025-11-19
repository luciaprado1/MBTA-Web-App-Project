import os
import requests
from dotenv import load_dotenv

# Load .env file (MBTA_API_KEY and MAPBOX_TOKEN)
load_dotenv()

MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MBTA_API_KEY = os.getenv("MBTA_API_KEY")

if MAPBOX_TOKEN is None:
    raise RuntimeError("MAPBOX_TOKEN is not set. Check your .env file.")

if MBTA_API_KEY is None:
    raise RuntimeError("MBTA_API_KEY is not set. Check your .env file.")

MAPBOX_BASE_URL = "https://api.mapbox.com/search/searchbox/v1/forward"
MBTA_STOPS_URL = "https://api-v3.mbta.com/stops"


def get_json(url, params=None):
    """
    Helper to send a GET request and return JSON.
    """
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json()


def get_lat_lon(place_name):
    """
    Given a place name (e.g. 'Boston Common'),
    return (lat, lon) using Mapbox Searchbox API.
    """
    params = {
        "q": place_name,
        "access_token": MAPBOX_TOKEN,
        "limit": 1,
    }

    data = get_json(MAPBOX_BASE_URL, params=params)
    features = data.get("features", [])
    if not features:
        return None, None

    # Searchbox returns center as [lon, lat]
    center = features[0]["geometry"]["coordinates"]
    lon, lat = center[0], center[1]
    return lat, lon


def get_nearest_station(lat, lon):
    """
    Given latitude and longitude, return (station_name, accessibility_string).
    Uses MBTA /stops endpoint.
    """
    params = {
        "api_key": MBTA_API_KEY,
        "sort": "distance",
        "filter[latitude]": lat,
        "filter[longitude]": lon,
        "page[limit]": 1,
    }

    data = get_json(MBTA_STOPS_URL, params=params)
    stops = data.get("data", [])
    if not stops:
        return None, None

    stop = stops[0]
    attrs = stop["attributes"]
    name = attrs["name"]
    wheelchair = attrs.get("wheelchair_boarding")

    if wheelchair == 1:
        access = "Wheelchair accessible"
    elif wheelchair == 2:
        access = "Not wheelchair accessible"
    else:
        access = "Accessibility unknown"

    return name, access


def find_stop_near(place_name):
    """
    Given a place name, combine Mapbox + MBTA to
    return (nearest_stop_name, accessibility).
    """
    lat, lon = get_lat_lon(place_name)
    if lat is None or lon is None:
        return None, None

    return get_nearest_station(lat, lon)


# Simple tests you can run directly
if __name__ == "__main__":
    test_place = "Boston Common"
    print("Testing with:", test_place)
    lat, lon = get_lat_lon(test_place)
    print("Coordinates:", (lat, lon))
    station, access = find_stop_near(test_place)
    print("Nearest station:", station)
    print("Accessibility:", access)


