#!/usr/bin/env python3

import sqlite3
import json
from geopy.geocoders import Nominatim

global geolocator
geolocator = Nominatim(timeout=10, user_agent='Opencast map generator')


# load the file only ones
def load_datafile():

    global data

    try:
        with open("cache.json", "r") as data_file:
            data = data_file.read()
            data = json.loads(data)
    except FileNotFoundError and ValueError:
        data = []


def getUserInformation():

    cur = sqlite3.connect('user.db').cursor()
    cur.execute('select distinct country, city, organization from user')
    for country, city, organization in cur.fetchall():
        if organization != "None":
            yield compareCache(country, city, organization)


def getGeoCode(country, city, organization, dataList):

    # Location with geocode true ->
    # add it to the cache and return geoLocation object
    newLocation = geolocator.geocode('%s, %s' %
                                     (country, city), addressdetails=True)
    if newLocation:
        geoLocation = {"country": country, "city": city,
                       "organization": organization,
                       "latitude": newLocation.latitude,
                       "longitude": newLocation.longitude}
        dataList.append(geoLocation)
        with open("cache.json", "w") as f:
            f.write(json.dumps(dataList))
        print(geoLocation)
        return geoLocation


def fixOverlappingEntries():

    locations = {}

    for organization in data:
        key = (organization['longitude'], organization['latitude'])
        # check if we already encountered this location
        if locations.get(key):
            locations[key]['organization'] += ', ' \
                + organization['organization']
        else:
            locations[key] = organization
    return locations.values()


def convertGeoJson(addresses):

    features = []
    for address in addresses:
        if address is not None:
            # print(address)
            features.append({
                "type": "Feature",
                "properties": {
                    'institution': address["organization"]
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [address["longitude"], address["latitude"]]
                }})
    return {"type": "FeatureCollection", "features": features}


def compareCache(country, city, organization):

    try:
        for item in data:
            if (city == item["city"] and country == item['country']
                    and organization == item['organization']):
                print("USER LOADED FROM CACHE")
                print(item)
                return item
        else:
            print("NEW USER NOT IN CACHE")
            return getGeoCode(country, city, organization, data)
    except TypeError and FileNotFoundError:
        print("FAILED ERROR")
        return getGeoCode(country, city, organization, data)


def main():
    load_datafile()
    convertGeoJson(getUserInformation())
    with open("adopters.geojson", "w") as census:
        census.write(json.dumps(convertGeoJson(fixOverlappingEntries())))


if __name__ == '__main__':
    main()
