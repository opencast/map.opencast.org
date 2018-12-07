window.onload = function () {
    var basemap = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
		attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
	});

var opcIcon = L.icon({
    iconUrl: 'opc.png',

    iconSize:     [30, 30],
    iconAnchor:   [22, 94],
    popupAnchor:  [-3, -76]
});

    $.getJSON("census.geojson", function(data) {

    var geojson = L.geoJson(data, {
      onEachFeature: function (feature, layer) {
        layer.bindPopup(feature.properties.Area_Name);
      }
    });


    var map = L.map('index')
    .fitBounds(geojson.getBounds());


    basemap.addTo(map);
    geojson.addTo(map);
    });

};
