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



function favoriteBrewery(){ 
  console.log('testing testing')
//get brewery_id from datset on favorite button
const brewery_fav_button = document.querySelector(dataset.brewery_id);
console.log('Can you hear me now?')
//create event listener for favorite button in brewery_search_retults.html
brewery_fav_button.addEventListener('click', () =>{
  const url = `/fav_brewery?${dataset.brewery_id, dataset.name, dataset.address}`;
  console.log('button click heard')
  fetch (url) //sending brewery_id plus other info to server to create brewery record
    .then ((response) => response.text())
    .then((status) =>{

      brewery_fav_button.innerHTML = "My Fave"; //updating Favorite button once response received
      brewery_fav_button.disabled= true; //makes it so user can't favorite that brewery again
    })
});
};  



// //on CLICK target, make request to ??? API or DB
//   if (favBtn) {
//     const url = 

//     fetch(url)
//     .then((response) => response.json()) //how does this need to be updated to get brewery info
//     .then((resp) => {
//       if (resp.status=="Success") {
//         console.log(`${resp.status}- ${resp.msg}`);
//         favBtn.innerHTML = "My Fave"; //updating Favorite button once response received
//         favBtn.disabled= true; //makes it so user can't favorite that brewery again
//       } else {
//         console.log(`${resp.status} -${resp.msg}`);
//         favBtn.innerHTML = "Already been favorited.";
//         favBtn.disabled = true;
//       }
//     });
//   };




