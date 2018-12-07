#!/bin/bash

git checkout master
python generate-map py

mkdir ~/tmp
mkdir ~/tmp/geomap
cp mymap.html ~/tmp/geomap
cp census.geojson ~/tmp/geomap
cp leafletmap.js ~/tmp/geomap

git checkout gh-pages

cp map.opencast.org/mymap.html .
cp map.opencast.org/census.geojson .
cp map.opencast.org/leafletmap.js .

git add .
git commit -m "testing bash script"
git push origin gh-pages
git checkout master

 rm -rf ~/tmp/geomap