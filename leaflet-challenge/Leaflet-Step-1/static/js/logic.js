var grey_map = L.tileLayer(
  "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", 
  {
    tileSize: 512,
    maxZoom: 8,
    zoomOffset: -1,
    id: "mapbox/light-v10",
    accessToken: API_KEY
  }
);

var world_map = L.map("world_map", {
  center: [32, -110],
  zoom: 4,
  layers: [grey_map]
});

grey_map.addTo(world_map);

d3.json("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson").then(function(data) {

  function styleInfo(features) {
    return {
      opacity: 1,
      fillOpacity: 0.6,
      fillColor: getColor(features.geometry.coordinates[2]),
      color: "#FFFFFF",
      radius: getRadius(features.properties.mag),
      stroke: true,
      weight: 0.7
    };
  }

  function getColor(depths) {
    switch (true) {
    case depths > 90:
      return "#845EC2";
    case depths > 70:
      return "#D65DB1";
    case depths > 50:
      return "#FF6F91";
    case depths > 30:
      return "#FF9671";
    case depths > 10:
      return "#FFC75F";
    default:
      return "#F9F871";
    }
  }

  function getRadius(mag) {
    if (mag === 0) {
      return 1;
    }

    return mag * 4;
  }
  
  L.geoJson(data, {
    pointToLayer: function(features, coord) {
      return L.circleMarker(coord);
    },
    style: styleInfo,
    onEachFeature: function(features, popup_layer) {
      popup_layer.bindPopup(
        "Magnitude: "
          + features.properties.mag
          + "<br>Depth: "
          + features.geometry.coordinates[2]
          + "<br>Location: "
          + features.properties.place
          + "<br>Time: "
          + features.properties.time
      );
    }
  }).addTo(world_map);

  var map_legend = L.control({
    position: "bottomright"
  });

  map_legend.onAdd = function() {
    var div = L.DomUtil.create("div", "info legend");

    var grading = [-10, 10, 30, 50, 70, 90];

    var color_scheme = [
      "#F9F871",
      "#FFC75F",
      "#FF9671",
      "#FF6F91",
      "#D65DB1",
      "#845EC2"
    ];

    for (var i = 0; i < grading.length; i++) {
      div.innerHTML += "<i style='background: " + color_scheme[i] + "'></i> "
      + grading[i] + (grading[i + 1] ? "&ndash;" + grading[i + 1] + "<br>" : "+");
    }
    return div;
  };

  map_legend.addTo(world_map);
});
