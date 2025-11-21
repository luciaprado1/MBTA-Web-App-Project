import requests
import os
 

# Load MBTA API key from environment variable
from dotenv import load_dotenv
load_dotenv()
MBTA_API_KEY = os.getenv("MBTA_API_KEY")

if not MBTA_API_KEY: 
    raise RuntimeError("Missing MBTA_API_KEY")


# -------------------------------
# Geocoding with Nominatim
# -------------------------------

def get_lat_lng(place_name: str):
    """
    Convert a place name into (lat, lon) using Nominatim.
    Raises an Exception if something goes wrong.
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": place_name,
        "format": "json",
        "limit": 1,
    }

    headers = {
        "User-Agent": "MBTA Helper App - OIM Course"
    }

    resp = requests.get(url, params=params, headers=headers, timeout=10)

    try:
        data = resp.json()
    except Exception:
        # Helpful debug print
        print("DEBUG Nominatim response:", resp.text[:300])
        raise Exception("Geocoding returned invalida data and JSON response.")

    if not data:
        raise Exception("Geocoding did not found location.")

    lat = float(data[0]["lat"])
    lon = float(data[0]["lon"])
    return lat, lon


def get_json(url, params=None):
    """Returms JSON from the MBTA API"""
    headers = {
        "accept":"application/json"
    }

    resp= requests.get(url,params=params, headers=headers,timeout=10)

    try:
        return resp.json()
    except Exception:
        print("Debug MBTA response:", resp.text[:300])
        raise Exception("MBTA API returned invalid JSON")

# -------------------------------
# MBTA API – nearest stop
# -------------------------------

def find_nearest_station(lat: float, lon: float):
    """
    Given a place name, return (station_name, accessible_str).
    Raises an Exception if something fails.
    """
    #Step 1: Set up the url and parameters
    url = "https://api-v3.mbta.com/stops"
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
    attributes = first ["attributes"]
    name = attributes["name"]
    wheelchair = attributes["wheelchair_boarding"]

    if wheelchair == 1:
        accessible = "Wheelchair accessible"
    elif wheelchair == 2:
        accessible = "Not wheelchair accessible"
    else:
        accessible = "Accessibility unknown"

    stop_id = first["id"]
    return name, accessible, stop_id 


def find_stop_near(place_name: str):
    """Main function: returns (station, accessibility)."""
    lat, lon = get_lat_lng(place_name)
    name, accessible, stop_id = find_nearest_station(lat, lon)
    return name, accessible, stop_id, lat, lon

#WOW factor - including the time of each bus in the station
def time_to_next_arrival(stop_id):
    """Returns next arrival time for the mode of transportation """
    url = "https://api-v3.mbta.com/predictions"
    params={
        "api_key": MBTA_API_KEY,
        "filter[stop]":stop_id,
        "sort": "arrival_time"
    }
    data = get_json(url, params)
    time_predictions = data.get("data", [])

    if not time_predictions:
        return None,None
    
    attrs = time_predictions[0]["attributes"]
    arrival_str = attrs.get("arrival_time")

    if not arrival_str:
        return None, None
    
    from datetime import datetime, timezone 

    arrival = datetime.fromisoformat(arrival_str.replace("Z","+00:00"))
    now = datetime.now(timezone.utc)
    minutes= round ((arrival - now).total_seconds() / 60)
    arrival_time_str= arrival.strftime("%I:%M %p")
    return arrival_time_str, minutes
    
if __name__ == "__main__":
    print("Testing with: Boston Common")
    lat, lon = get_lat_lng("Boston Common")
    print("Coordinates:", (lat, lon))
    station, accessible, stop_id, lat, lon = find_stop_near("Boston Common")
    print("Nearest station:", station)
    print("Accessibility:", accessible)



