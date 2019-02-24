#!/usr/bin/env python3

import sqlite3
import json
from geopy.geocoders import Nominatim
import os


def getUserInformation():

    locations = []

    cur = sqlite3.connect('user.db').cursor()
    cur.execute('select distinct country, city, organization from user')
    for country, city, organization in cur.fetchall():
        if organization != "None":
            locations.append(compareCache(country, city, organization))
    return locations


def getGeoCode(country, city, organization, dataList):

    geolocator = Nominatim(timeout=10, user_agent='Opencast map generator')
    newLocation = geolocator.geocode(country, city, addressdetails=True) \
        or geolocator.geocode('%s, %s' % (country, city), addressdetails=True)
    if newLocation:
        os.remove("cache.json")
        f = open("cache.json", "a")
        geoLocation = {"country": country, "city": city,
                       "organization": organization,
                       "latitude": newLocation.latitude,
                       "longitude": newLocation.longitude}
        dataList.append(geoLocation)
        f.write(json.dumps(dataList))

        geoLocation = {"country": country,
                       "city": city, "organization": organization,
                       "latitude": newLocation.latitude,
                       "longitude": newLocation.longitude}
        return geoLocation


def convertGeoJson(addresses):

    features = []
    for i in addresses:
        if i is not None:
            print(i)
            features.append({
                "type": "Feature",
                "properties": {
                    'institution': i["organization"]
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [i["longitude"], i["latitude"]]
                }})
    return {"type": "FeatureCollection", "features": features}


def compareCache(country, city, organization):

    check = 0
    with open('cache.json') as data_file:
        if os.stat("cache.json").st_size == 0:
            data = []

            return getGeoCode(country, city, organization, data)
        else:
            data = json.load(data_file)
            for item in data:
                if (city == item["city"] and country == item['country']
                        and organization == item['organization']):
                    check = 1
                    if check == 1:

                        return item
            else:

                return getGeoCode(country, city, organization, data)
            check = 0


def main():
    with open("adopters.geojson", "w") as census:
        census.write(json.dumps(convertGeoJson(getUserInformation())))


if __name__ == '__main__':
    main()
