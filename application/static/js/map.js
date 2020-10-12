var month = 1
var day = 1
var hour = 0
var months = { 1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December" };
var mymap = L.map('mapid').setView([60.172097, 24.941249], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: "&copy; <a href=&quot;http://osm.org/copyright&quot;>OpenStreetMap</a> contributors",
  maxZoom: 18,
  id: 'mapbox/streets-v11',
  tileSize: 512,
  zoomOffset: -1
}).addTo(mymap)
mymap.setZoom(10)
var url = `/map_features?geojson=${month}_${day}_${hour}_late_per_station.geojson`
var set_map_values = function () {
  url = `/map_features?geojson=${month}_${day}_${hour}_late_per_station.geojson`


  $.ajax({
    type: "GET",
    url: url,
    dataType: 'json',
    success: function (response) {
      var geojsonMarkerOptions = function (late) {
        var late_prc = late * 100

        if (0 <= late_prc & late_prc <= 10)
          return {
            radius: 8,
            fillColor: "#ffffcc",
            color: "#000",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.6
          }
        else if (10 <= late_prc & late_prc <= 20)
          return {
            radius: 8,
            fillColor: "#ffeda0",
            color: "#000",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.6
          }
        else if (20 <= late_prc & late_prc <= 30)
          return {
            radius: 8,
            fillColor: "#fed976",
            color: "#000",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.6
          }
        else if (30 <= late_prc & late_prc <= 40)
          return {
            radius: 8,
            fillColor: "#feb24c",
            color: "#000",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.6
          }
        else if (40 <= late_prc & late_prc <= 50) 
        return {
          radius: 8,
          fillColor: "#fd8d3c",
          color: "#000",
          weight: 1,
          opacity: 1,
          fillOpacity: 0.6
        }
        else if (50 <= late_prc & late_prc <= 60) 
        return {
          radius: 8,
          fillColor: "#fc4e2a",
          color: "#000",
          weight: 1,
          opacity: 1,
          fillOpacity: 0.6
        }
        else if (60 <= late_prc & late_prc <= 70) 
        return {
          radius: 8,
          fillColor: "#e31a1c",
          color: "#000",
          weight: 1,
          opacity: 1,
          fillOpacity: 0.6
        }
        else if (70 <= late_prc & late_prc <= 80)
          return {
            radius: 8,
            fillColor: "#bd0026",
            color: "#000",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.6
          }
        else if (80 <= late_prc & late_prc <= 90)
          return {
            radius: 8,
            fillColor: "#800026",
            color: "#000",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.6
          }
        else {
          return {
            radius: 8,
            fillColor: "#000000",
            color: "#000",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.6
          }

        }

      };
      mymap.removeLayer(geojsonLayer)
     geojsonLayer = L.geoJSON(response, {
        pointToLayer: function (feature, latlng) {
          return L.circleMarker(latlng, geojsonMarkerOptions(feature.properties.late_prc));
        }
      }).addTo(mymap);
      $("#info").fadeOut(500);
    }
  });

}


$.ajax({
  type: "GET",
  url: url,
  dataType: 'json',
  success: function (response) {

     var geojsonMarkerOptions = function() {
            return {
            radius: 8,
            fillColor: "#ffffcc",
            color: "#000",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.6
          }
        }


  geojsonLayer = L.geoJSON(response, {
      pointToLayer: function (feature, latlng) {
        return L.circleMarker(latlng, geojsonMarkerOptions);
      }
    }).addTo(mymap);
    $("#info").fadeOut(500);
  }
});

var slider_month = document.getElementById("month");
month = slider_month.value
document.getElementById("month_text").innerHTML = months[month];
set_map_values()

var slider_day = document.getElementById("day");
day = slider_day.value
document.getElementById("day_text").innerHTML = day;
set_map_values()

var slider_hour = document.getElementById("hour");
hour = slider_hour.value
document.getElementById("hour_text").innerHTML = hour;
set_map_values()


// Update the current slider value (each time you drag the slider handle)
slider_month.oninput = function () {
  month = this.value;
  document.getElementById("month_text").innerHTML = months[month];
  set_map_values()
}

slider_day.oninput = function () {
  day = this.value;
  document.getElementById("day_text").innerHTML = day;
  set_map_values()

}

slider_hour.oninput = function () {
  hour = this.value;
  document.getElementById("hour_text").innerHTML = hour;
  set_map_values()

} 
