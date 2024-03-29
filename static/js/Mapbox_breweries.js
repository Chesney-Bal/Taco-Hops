'use strict';
//MAP FEATURE//
//information to center the map based on original search term location
const center_coordinates=document.querySelector("#map_center")
const center_lat=center_coordinates.dataset.lat; 
const center_long=center_coordinates.dataset.long; 


//establishes map on page
mapboxgl.accessToken = 'pk.eyJ1IjoiY2hlc25leWJhbCIsImEiOiJjbGMwdXY3eWg0Z2liM3hsY2Uwcm5jcWpwIn0.B2XNvVgPluaaVx9aR3miqw';
const map = new mapboxgl.Map({
  container: 'map', // container ID
  style: 'mapbox://styles/mapbox/streets-v12', // style URL
  center: [center_long, center_lat],
  zoom: 12 // starting zoom
});

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
        .setPopup(new mapboxgl.Popup({
          closeButton:false,
          closeOnClick: true,
        }).setHTML(brewery[0]))
        .addTo(map); 
  };   
//END OF MAP FEATURE//



//FAVORITE FEATURE//
//get brewery_id from button id on favorite button in html
const brewery_fav_buttons = document.querySelectorAll('#fav_brewery_btn');

// loops over all buttons on brewery results page so they behave the same
for (const brewery_fav_button of brewery_fav_buttons) {
  const brewery_id = brewery_fav_button.dataset.brewery_id
  const brewery_name=brewery_fav_button.dataset.brewery_name
  const brewery_address=brewery_fav_button.dataset.brewery_address
  const brewery_long=brewery_fav_button.dataset.brewery_long
  const brewery_lat=brewery_fav_button.dataset.brewery_lat
  const brewery_image_url=brewery_fav_button.dataset.brewery_image_url
  const brewery_url=brewery_fav_button.dataset.brewery_url


  const brewery_data={
    brewery_id: brewery_id,
    brewery_name: brewery_name,
    brewery_address: brewery_address,  
    brewery_long: brewery_long,
    brewery_lat: brewery_lat,
    brewery_image_url:brewery_image_url,
    brewery_url:brewery_url,
  }
  
  const request_data={
    method: 'POST',
    body: JSON.stringify(brewery_data),
    headers: {
      'Content-Type': 'application/json'
    }
  }
  
  //create event listener for favorite button in brewery_search_retults.html
  brewery_fav_button.addEventListener('click', () =>{
    const url = `/fav_brewery`;

  
    fetch (url, request_data ) //sending brewery_id plus other info to server to create brewery record
      .then ((response) => response.text()) //returns Success from server.py route
      .then((status) => {
        if (status == "Success"){ 
          brewery_fav_button.innerHTML = "Liked"; //updating Favorite button once response received
          brewery_fav_button.disabled = true; //makes it so user can't favorite that brewery again-should gray out button
        }
        else {
          alert("You've already favorited this brewery!")
        }
      }) 
  });
};