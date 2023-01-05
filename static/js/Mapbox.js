'use strict';

const center_coordinates=document.querySelector("#map_center")
const center_lat=center_coordinates.dataset.lat; 
const center_long=center_coordinates.dataset.long; 

mapboxgl.accessToken = 'pk.eyJ1IjoiY2hlc25leWJhbCIsImEiOiJjbGMwdXY3eWg0Z2liM3hsY2Uwcm5jcWpwIn0.B2XNvVgPluaaVx9aR3miqw';
const map = new mapboxgl.Map({
  container: 'map', // container ID
  // Choose from Mapbox's core styles, or make your own style with Mapbox Studio
  style: 'mapbox://styles/mapbox/streets-v12', // style URL
  center: [center_long, center_lat],
  zoom: 12 // starting zoom
});

const coordinates=document.querySelectorAll(".coordinates")

console.log("these are coords:", coordinates) //currently just printing div.coordinates but not actual long/lat

const brewery_marker_coords=[]; 

console.log("hi", brewery_marker_coords) // currently printing empty list-this is expected

for (const coordinate of coordinates) {
  let marker_lng=coordinate.dataset.long; 
  let marker_lat=coordinate.dataset.lat;
  brewery_marker_coords.push [marker_lng, marker_lat]; 
};

console.log(brewery_marker_coords) // currently printing empty list-this is not expected

for (const brewery_markers of brewery_marker_coords) {
      new mapboxgl.Marker()
      .setLngLat(brewery_markers)
      .addTo(map) 
  };   


      
  
    



