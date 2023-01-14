'use strict';

//information to center the map based on users location
const center_coordinates=document.querySelector("#map_center")
const center_lat=center_coordinates.dataset.lat; 
const center_long=center_coordinates.dataset.long; 

//establishes map on page
mapboxgl.accessToken = 'pk.eyJ1IjoiY2hlc25leWJhbCIsImEiOiJjbGMwdXY3eWg0Z2liM3hsY2Uwcm5jcWpwIn0.B2XNvVgPluaaVx9aR3miqw';
const map = new mapboxgl.Map({
  container: 'map', // container ID
  style: 'mapbox://styles/mapbox/streets-v12', // style URL
  center: [center_long, center_lat],
  zoom: 10 // starting zoom
});


map.addControl(new mapboxgl.NavigationControl());

//pulls name, and coordinates from html for use with markers
const fav_B_coordinates=document.querySelectorAll(".fav_brewery_info")

const fav_B_marker_list=[]

//adds information to fav_B_marker_list to be used by markers
for (const fav_B_coordinate of fav_B_coordinates) {
  const fav_brewery_name=fav_B_coordinate.dataset.favName;
  const fav_brewery_long=fav_B_coordinate.dataset.fav_brewery_long;
  const fav_brewery_lat=fav_B_coordinate.dataset.fav_brewery_lat;
  fav_B_marker_list.push([fav_brewery_name, fav_brewery_long, fav_brewery_lat]);
};

//printing undefined even after tried convertin to String()
//jinja in users_details.html accurately displaying string on website
//this is impacting info on the marker popup
console.log(fav_B_marker_list[0][0]) 

//creates markers on the map with fav_brewery name
for (const fav_brewery of fav_B_marker_list) {
  let marker= new mapboxgl.Marker({
    color: '#FFD700',
  }).setLngLat([fav_brewery[1], fav_brewery[2]])
  .setPopup(new mapboxgl.Popup({
    closeButton: false,
    closeOnClick: true,
  }).setHTML((fav_brewery[0])))
  .addTo(map);
  };
  

