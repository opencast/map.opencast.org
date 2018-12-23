
import sqlite3
import json
import geopy
import sys
from geopy.geocoders import Nominatim
from time import sleep

def getUserInformation():
    geolocator = Nominatim(timeout = 10)

    cur.execute("Select distinct country, city, organization FROM user")

    allUsersDict = json.loads(json.dumps(cur.fetchall()))
    allUsersGeoCode = []
    k = 0
    for i in range(len(allUsersDict)):
        geolocate_column = geolocator.geocode(allUsersDict[i][0]+ " " + allUsersDict[i][1], addressdetails=True)
        sleep(0.075)
        k = k + 1
        print(k)
        latitude = geolocate_column.latitude if geolocate_column is not None else None
        longitude = geolocate_column.longitude if geolocate_column is not None else None
        if latitude or longitude is not None:
            allUsersGeoCode.append([latitude, longitude, allUsersDict[i][2]])

    #print(allUsersGeoCode)
    return allUsersGeoCode

def convertGeoJson(geoAdressList):
        geoJson = {"type": "FeatureCollection","features": []}
        for i in range(len(geoAdressList)):
            feature = {"type": "Feature", "properties": {}, "geometry": {"type": "Point", "coordinates": []}}
            feature["geometry"]["coordinates"] = [geoAdressList[i][1],geoAdressList[i][0]]
            feature['properties'] = {'institution' : geoAdressList[i][2]}
            geoJson["features"].append(feature)
        return geoJson

conn = sqlite3.connect('/Users/danielkaiser/tmp/user.db')
cur = conn.cursor()
geopy.geocoders.options.default_user_agent = "opc-map"

open("census.geojson","w").close()

with open("census.geojson", "a") as census:
   #census.write(str(convertGeoJson(getUserInformation())).replace("'",'"'))
   census.write(json.dumps(convertGeoJson(getUserInformation())))

sys.exit()
