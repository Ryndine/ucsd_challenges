// Add a number of base maps to choose from.
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

var satellite_map = L.tileLayer(
  "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", 
  {
    tileSize: 512,
    maxZoom: 8,
    zoomOffset: -1,
    id: "mapbox/satellite-v9",
    accessToken: API_KEY
  }
);

var outdoor_map = L.tileLayer(
  "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", 
  {
  tileSize: 512,
  maxZoom: 8,
  zoomOffset: -1,
  id: "mapbox/outdoors-v11",
  accessToken: API_KEY
  }
);

var world_map = L.map("world_map", {
  center: [32, -110],
  zoom: 4,
  layers: [grey_map, satellite_map, outdoor_map]
});

grey_map.addTo(world_map);

var tectonic_plate_layer = new L.LayerGroup();
var earthquake_layer = new L.LayerGroup();

var base_maps = {
  Grayscale: grey_map,
  Satellite: satellite_map,
  Outdoors: outdoor_map
};

var overlays = {
  "Tectonic Plate Data": tectonic_plate_layer,
  "Earthquake Data": earthquake_layer
};

L.control
  .layers(base_maps, overlays)
  .addTo(world_map);

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
    pointToLayer: function(feature, coord) {
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
  }).addTo(earthquake_layer);
  
  earthquake_layer.addTo(world_map);

  var legend = L.control({
    position: "bottomright"
  });

  legend.onAdd = function() {
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

  legend.addTo(world_map);

  d3.json("https://raw.githubusercontent.com/fraxen/tectonicplates/master/GeoJSON/PB2002_plates.json").then(function(tectonic_plate_data) {
      L.geoJson(tectonic_plate_data, {
        color: "black",
        weight: 1.5
      })
      .addTo(tectonic_plate_layer);

      tectonic_plate_layer.addTo(world_map);
    });
});
