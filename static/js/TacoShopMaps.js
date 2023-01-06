'use strict';

//information to center the map based on selected brewery
const tacoshop_center_coordinates=document.querySelector("#taco_map_center")
const center_lat=tacoshop_center_coordinates.dataset.lat; 
const center_long=tacoshop_center_coordinates.dataset.long; 

console.log(center_long, center_lat)

mapboxgl.accessToken = 'pk.eyJ1IjoiY2hlc25leWJhbCIsImEiOiJjbGMwdXY3eWg0Z2liM3hsY2Uwcm5jcWpwIn0.B2XNvVgPluaaVx9aR3miqw';
const map = new mapboxgl.Map({
  container: 'map', // container ID
  style: 'mapbox://styles/mapbox/streets-v12', // style URL
  center: [center_long, center_lat],
  zoom: 12 // starting zoom
});

map.addControl(new mapboxgl.NavigationControl());


//pulls name, longitude, latitude from html for use with markers
const coordinates=document.querySelectorAll(".taco_coordinates")

const tacoshop_marker_list=[]; 

//adds information to tacoshop_marker_list to be used by markers
for (const coordinate of coordinates) {
  let tacoshop_name=coordinate.dataset.taco_name; //this should be the property/key
  let marker_lng=coordinate.dataset.taco_long; //long and lat should be a list as the value
  let marker_lat=coordinate.dataset.taco_lat; //long and lat should be a list as the value
  tacoshop_marker_list.push([tacoshop_name, marker_lng, marker_lat]); // establishing objects/dict property = value
};

//creates markers on the map with tacoshop name
for (const tacoshop of tacoshop_marker_list) {
      let marker= new mapboxgl.Marker({
        color: '#A13D2D',
        }).setLngLat([tacoshop[1], tacoshop[2]])
        .setPopup(new mapboxgl.Popup().setHTML(tacoshop[0]))
        .addTo(map); 
  };   


