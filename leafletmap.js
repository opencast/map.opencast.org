window.onload = function () {
    console.log("Script is running")
    var basemap = L.tileLayer('https://a.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://osm.org/copyright">OpenStreetMap</a> contributors',
        noWrap: false
    });

    $.getJSON("adopters.geojson", function (data) {
         function onEachFeature(features, layer) {

            marker = " ";

            data.features.every(position => {
                if (features.geometry.coordinates[1] == position.geometry.coordinates[1] && features.geometry.coordinates[0] == position.geometry.coordinates[0]){
                   layer.bindPopup("Institutions: " + features.properties.institution + ", " + position.properties.institution);
                } else {
                    layer.bindPopup("Institutions: " + features.properties.institution);
                } 
            });
        }
         var geojson = L.geoJson(data, {

             onEachFeature: onEachFeature
         });

         var map = L.map('my-map', {

            minZoom: 2
        }).fitBounds(geojson.getBounds());
  
        basemap.addTo(map);
        geojson.addTo(map);
    });
};
