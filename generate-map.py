#!/usr/bin/env python3

import sqlite3
import json
import itertools
from operator import itemgetter
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
    except Exception:
        with open("cache.json", "w+") as data_file:
            # Because of the empty file python converts data to a String, so
            # in line 46 append is not working.
            #  --> In Exception ,,data = []'' to prevent this problem.
            print("FILE IS EMPTY")
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

    sorted_all = sorted(data, key=itemgetter('longitude'))
    grouped_locations = []

    # group all Organizations by long and latitude and save them in a list
    for key, group in (
                       itertools.groupby(sorted_all,
                                         key=lambda each: (each['longitude'],
                                                           each["latitude"]))
    ):
        grouped_locations.append(list(group))

    pooledLoc = []
    # create Location with multiple organizations
    try:
        for k in range(len(grouped_locations)):
            pooledLocation = {"country": grouped_locations[k][0]["country"],
                              "city": grouped_locations[k][0]["city"],
                              "organization": "",
                              "latitude": grouped_locations[k][0]["latitude"],
                              "longitude": grouped_locations[k][0]["longitude"]
                              }
            for grp_location in grouped_locations[k]:
                pooledLocation["organization"] += grp_location["organization"]
                pooledLocation["organization"] += ", "
                pooledLoc.append(pooledLocation)

        for l in range(len(pooledLoc)):
            pooledLoc[l]["organization"] = pooledLoc[l]["organization"][:-2]

        return pooledLoc
    except TypeError:
        return None


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
    except Exception:
        print("FAILED ERROR --> Empty, Not Existing File etc.")
        return getGeoCode(country, city, organization, data)


def main():
    load_datafile()
    convertGeoJson(getUserInformation())
    with open("adopters.geojson", "w") as census:
        census.write(json.dumps(convertGeoJson(fixOverlappingEntries())))


if __name__ == '__main__':
    main()
