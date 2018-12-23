#!/bin/bash

git checkout master
python generate-map.py

mkdir ~/tmp
mkdir ~/tmp/geomap
cp index.html ~/tmp/geomap
cp adopters.geojson ~/tmp/geomap
cp leafletmap.js ~/tmp/geomap

git checkout gh-pages

cp ~/tmp/geomap/index.html .
cp ~/tmp/geomap/adopters.geojson .
cp ~/tmp/geomap/leafletmap.js .

git add .
git commit -m "testing bash script"
git push origin gh-pages
git checkout master

 rm -rf ~/tmp/geomap
