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



