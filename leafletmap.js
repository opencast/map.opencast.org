window.onload = function () {
    console.log("Script is running")
    var basemap = L.tileLayer('https://a.tile.openstreetmap.org/{z}/{x}/{y}.png', {
		attribution: '&copy; <a href="https://osm.org/copyright">OpenStreetMap</a> contributors',
        noWrap: true
	});

    $.getJSON("census.geojson", function(data) {

    var geojson = L.geoJson(data, {
      onEachFeature: function (feature, layer) {
        layer.bindPopup(feature.properties.Area_Name);
      }
    });

    var map = L.map('my-map')
    .fitBounds(geojson.getBounds());

    basemap.addTo(map);
    geojson.addTo(map);
$(window).on("resize", function () {
     $("#my-map").height($(window).height()); map.invalidateSize(); }).trigger("resize");
    });
};
