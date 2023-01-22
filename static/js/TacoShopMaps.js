'use strict';
//MAP FEATURE//
//information to center the map based on selected brewery
const tacoshop_center_coordinates=document.querySelector("#taco_map_center")
const center_lat=tacoshop_center_coordinates.dataset.lat; 
const center_long=tacoshop_center_coordinates.dataset.long; 
const center_brewery_name=tacoshop_center_coordinates.dataset.nearby_brewery_name;


//establishes map on page
mapboxgl.accessToken = 'pk.eyJ1IjoiY2hlc25leWJhbCIsImEiOiJjbGMwdXY3eWg0Z2liM3hsY2Uwcm5jcWpwIn0.B2XNvVgPluaaVx9aR3miqw';
const map = new mapboxgl.Map({
  container: 'map', // container ID
  style: 'mapbox://styles/mapbox/streets-v12', // style URL
  center: [center_long, center_lat],
  zoom: 12 // starting zoom  
});


//adds navigation controls to map for user to zoom in or out
map.addControl(new mapboxgl.NavigationControl());

// Add geolocate control to the map.
//Initialize the Geolocate Control
const geolocate = new mapboxgl.GeolocateControl({
  positionOptions: {
      enableHighAccuracy: true
  },
  // When active the map will receive updates to the device's location as it changes.
  trackUserLocation: true,
  // Draw an arrow next to the location dot to indicate which direction the device is heading.
  showUserHeading: true,
  showUserLocation: true,
});

//adds geolocation feature on map
map.addControl(geolocate);
geolocate.on('geolocate', () => {
})


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
        .setPopup(new mapboxgl.Popup({
          closeButton:false,
          closeOnClick: true,
        }).setHTML(tacoshop[0]))
        .addTo(map); 
  };   


//creates center of map with a marker based on nearby brewery
const center = new mapboxgl.Marker({
  color: '#FFD700',
}) .setLngLat([center_long, center_lat])
.setPopup(new mapboxgl.Popup({
  closeButton: false,
  closeOnClick: true,
}).setHTML(center_brewery_name))
.addTo(map);


  //END OF MAP FEATURE//



//FAVORITE FEATURE//
//get tacoshop_id from button id on favorite button in html
const tacoshop_fav_buttons = document.querySelectorAll('#fav_tacoshop_btn');

// loops over all buttons on tacoshop results page so they behave the same
for (const tacoshop_fav_button of tacoshop_fav_buttons) {
  const tacoshop_id=tacoshop_fav_button.dataset.tacoshop_id
  const tacoshop_name=tacoshop_fav_button.dataset.tacoshop_name
  const tacoshop_address=tacoshop_fav_button.dataset.tacoshop_address
  const nearby_brewery=tacoshop_fav_button.dataset.nearby_brewery

  const tacoshop_data={
    tacoshop_id: tacoshop_id,
    tacoshop_name: tacoshop_name,
    tacoshop_address: tacoshop_address,
    nearby_brewery:nearby_brewery,
  }

  const request_tacoshop_data={
    method: 'POST',
    body: JSON.stringify(tacoshop_data),
    headers: {
      'Content-Type': 'application/json'
    }
  }

  //create event listener for favorite button in tachoshop_results.html
  tacoshop_fav_button.addEventListener('click', () =>{
    const url = `/fav_tacoshop`;


    fetch (url, request_tacoshop_data) //sending tacoshop_id plus other info to server to create tacoshop record
      .then((response) => response.text()) //returns Success from server.py route
      .then((status) => {
        if (status == "Success") {
          tacoshop_fav_button.innerHTML = "Liked"; //updates Favorite button once response received
          tacoshop_fav_button.disabled = true; //makes it so user can't favorite that brewery right then
        }
        else {
          alert("You've already favorited this tacoshop!")
        }
      })
  });
};