#!/usr/bin/env python3

import sqlite3
import json
from geopy.geocoders import Nominatim


def getUserInformation():
    geolocator = Nominatim(timeout=10, user_agent='Opencast map generator')

    cur = sqlite3.connect('user.db').cursor()
    cur.execute('select distinct country, city, organization from user')
    for country, city, organization in cur.fetchall():
        location = geolocator.geocode({'country': country, 'city': city},
                                      addressdetails=True)
        print((country, city), '->', location)
        if location:
            yield (location.latitude, location.longitude, organization)


def convertGeoJson(addresses):
    features = []
    for lat, lon, org in addresses:
        features.append({
            "type": "Feature",
            "properties": {
                'institution': org,
            },
            "geometry": {
                "type": "Point",
                "coordinates": [lat, lon]
            }})
    return {"type": "FeatureCollection", "features": features}


def main():
    with open("adopters.geojson", "w") as census:
        census.write(json.dumps(convertGeoJson(getUserInformation())))


if __name__ == '__main__':
    main()
