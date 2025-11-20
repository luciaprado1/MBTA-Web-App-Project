import requests

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

    # IMPORTANT: realistic User-Agent so Nominatim doesn't block you
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
    }

    resp = requests.get(url, params=params, headers=headers, timeout=10)

    try:
        data = resp.json()
    except Exception:
        # Helpful debug print
        print("DEBUG Nominatim response text:", resp.text[:500])
        raise Exception("Geocoding service returned invalid data.")

    if not data:
        raise Exception("Location not found from geocoding.")

    lat = float(data[0]["lat"])
    lon = float(data[0]["lon"])
    return lat, lon


# -------------------------------
# MBTA API – nearest stop
# -------------------------------

def find_stop_near(place_name: str):
    """
    Given a place name, return (station_name, accessible_bool).
    Raises an Exception if something fails.
    """
    # Step 1: get coordinates
    lat, lon = get_lat_lng(place_name)

    # Step 2: call MBTA API
    url = "https://api-v3.mbta.com/stops"
    params = {
        "filter[latitude]": lat,
        "filter[longitude]": lon,
        "sort": "distance",
    }
    headers = {
        "accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    resp = requests.get(url, params=params, headers=headers, timeout=10)

    try:
        data = resp.json()
    except Exception:
        print("DEBUG MBTA response text:", resp.text[:500])
        raise Exception("MBTA API returned invalid data.")

    if "data" not in data or len(data["data"]) == 0:
        raise Exception("No nearby MBTA stations found.")

    stop = data["data"][0]
    station_name = stop["attributes"]["name"]

    # wheelchair_boarding: 0 = no info, 1 = accessible, 2 = inaccessible
    wb = stop["attributes"].get("wheelchair_boarding", 0)
    accessible = True if wb == 1 else False

    return station_name, accessible
