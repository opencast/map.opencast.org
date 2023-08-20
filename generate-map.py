#!/usr/bin/env python3

import sqlite3
import json
from geopy.geocoders import Nominatim


data = []
geolocator = Nominatim(timeout=10, user_agent='Opencast map generator')


def get_user_info():
    query = '''
        select organisation_name, department_name,
          country, postal_code, city, street, street_no
        from adopter
        where organisation_name != ''
        '''

    cur = sqlite3.connect('app.db').cursor()
    cur.execute(query)
    for adopter_data in cur.fetchall():
        yield get_geo_info(*adopter_data)


def get_geo_info(organization, department, country, zipcode, city, street,
                 street_no):
    print(f'Requesting: {organization}, {department}'.strip(' ,'))
    addresses = [
            f'{organization}, {street} {street_no} {country} {zipcode} {city}',
            f'{street} {street_no}, {country} {zipcode} {city}',
            f'{country} {zipcode} {city}',
            f'{organization}'
            ]
    for address in addresses:
        address = address.strip(' ,')
        if not address:
            continue
        print(f'  Address: {address}')
        location = geolocator.geocode(address, addressdetails=True)
        print(f'  Location: {location}')
        if location:
            return {"country": country, "city": city,
                    "organization": organization,
                    "department": department,
                    "latitude": location.latitude,
                    "longitude": location.longitude}


def convert_geo_json(addresses):

    features = []
    for address in addresses:
        if address:
            feature = {
                "type": "Feature",
                "properties": {
                    'institution': address['organization']
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [address["longitude"], address["latitude"]]
                }}
            if address['department']:
                feature['properties']['department'] = address['department']
            features.append(feature)
    return {"type": "FeatureCollection", "features": features}


def main():
    geo_data = convert_geo_json(get_user_info())
    with open("adopters.geojson", "w") as f:
        f.write(json.dumps(geo_data))


if __name__ == '__main__':
    main()
