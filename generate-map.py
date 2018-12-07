import sqlite3
import geopy
import sys
from geopy.geocoders import Nominatim
geopy.geocoders.options.default_user_agent = "opc-map"

conn = sqlite3.connect('user.db')
cur = conn.cursor()

def get_latitude(x):
    if x is not None:
        return x.latitude
    else: print("ISNONE")

def get_longitude(x):
  return x.longitude

#get Location as geocode from the db, saved into a list
def getLocation():
    geolocator = Nominatim(timeout = 10)
    geoAdresses = []
    cur.execute("Select distinct country, city FROM user")
    userLocation = cur.fetchone()
    while userLocation is not None:
        userLocation = cur.fetchone()
        #print(userLocation)
        if userLocation is not None:
            userLocationString = ','.join(userLocation)
            geolocate_column = geolocator.geocode(userLocationString, addressdetails=True)
            if geolocate_column is not None:
                latitude = get_latitude(geolocate_column)
                longitude = get_longitude(geolocate_column)
                geoAdress = [longitude, latitude]
                #print(geoAdress)
                geoAdresses.append(geoAdress)
    return geoAdresses

def convertGeoJson(geoAdressList):
        geoJson = {"type": "FeatureCollection","features": []}
        for i in range(len(geoAdressList)):
            feature = {"type": "Feature", "properties": {}, "geometry": {"type": "Point", "coordinates": []}}
            feature["geometry"]["coordinates"] = [geoAdressList[i][0],geoAdressList[i][1]]
            geoJson["features"].append(feature)
        return geoJson

open("census.geojson","w").close()

with open("census.geojson", "a") as census:
   census.write(str(convertGeoJson(getLocation())).replace("'",'"'))

sys.exit()
