window.onload = function () {
  var basemap = L.tileLayer('https://a.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://osm.org/copyright">OpenStreetMap</a> contributors',
    noWrap: false
  });

  fetch('adopters.geojson')
    .then(response => response.json())
    .then(data => {
      function onEachFeature(feature, layer) {
        let description = `<b>${feature.properties.institution}</b>`;
        if (feature.properties.department) {
          description += `<br />${feature.properties.department}`
        }
        layer.bindPopup(description);
      }
      var geojson = L.geoJson(data, {
        onEachFeature: onEachFeature
      });

      var map = L.map('map',{
        minZoom: 2
      })
        .fitBounds(geojson.getBounds());

      basemap.addTo(map);
      geojson.addTo(map);
    });
};
