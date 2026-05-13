#!/usr/bin/env python3
import sys
import requests

def geocode_osm(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
        "limit": 1,
        "featuretype": "city"
    }
    headers = {
        "User-Agent": "WeatherSkillAgent/1.0"
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        
        if data and len(data) > 0:
            location = data[0]
            return f"{location['lat']},{location['lon']}|{location['display_name']}"
        else:
            return None
    except Exception:
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
        
    address = sys.argv[1]
    result = geocode_osm(address)
    if result:
        print(result)
    else:
        sys.stderr.write(f"Error: Could not geocode address '{address}' via OSM\n")
        sys.exit(1)
