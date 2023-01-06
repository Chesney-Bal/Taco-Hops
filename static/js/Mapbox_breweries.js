'use strict';

//information to center the map based on original search term location
const center_coordinates=document.querySelector("#map_center")
const center_lat=center_coordinates.dataset.lat; 
const center_long=center_coordinates.dataset.long; 

mapboxgl.accessToken = 'pk.eyJ1IjoiY2hlc25leWJhbCIsImEiOiJjbGMwdXY3eWg0Z2liM3hsY2Uwcm5jcWpwIn0.B2XNvVgPluaaVx9aR3miqw';
const map = new mapboxgl.Map({
  container: 'map', // container ID
  style: 'mapbox://styles/mapbox/streets-v12', // style URL
  center: [center_long, center_lat],
  zoom: 12 // starting zoom
});

map.addControl(new mapboxgl.NavigationControl());

//pulls name, longitude, latitude from html for use with markers
const coordinates=document.querySelectorAll(".coordinates")

const brewery_marker_list=[]; 

//adds information to brewery_marker_list to be used by markers
for (const coordinate of coordinates) {
  let brewery_name=coordinate.dataset.name; //this should be the property/key
  let marker_lng=coordinate.dataset.long; //long and lat should be a list as the value
  let marker_lat=coordinate.dataset.lat; //long and lat should be a list as the value
  brewery_marker_list.push([brewery_name, marker_lng, marker_lat]); // establishing objects/dict property = value
};

//creates markers on the map with brewery name
for (const brewery of brewery_marker_list) {
      let marker= new mapboxgl.Marker({
        color: '#FFD700',
        }).setLngLat([brewery[1], brewery[2]])
        .setPopup(new mapboxgl.Popup().setHTML(brewery[0]))
        .addTo(map); 
  };   

  




