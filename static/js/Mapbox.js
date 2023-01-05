
        mapboxgl.accessToken = 'pk.eyJ1IjoiY2hlc25leWJhbCIsImEiOiJjbGMwdXY3eWg0Z2liM3hsY2Uwcm5jcWpwIn0.B2XNvVgPluaaVx9aR3miqw';
        const map = new mapboxgl.Map({
          container: 'map', // container ID
          // Choose from Mapbox's core styles, or make your own style with Mapbox Studio
          style: 'mapbox://styles/mapbox/streets-v12', // style URL
          // center: [-117.1611, 32.7157], // starting position [lng, lat]
          center: center,
          zoom: 12 // starting zoom
        });
        

        const brewery_marker_coords=[];
       
        for (const brewery of mapbox_data) {
         let marker_lng=brewery['coordinates']['longitude']; 
         let marker_lat=brewery['coordinates']['latitude'];
         brewery_marker_coords.push [marker_lng, marker_lat];
        };
 
        console.log(brewery_marker_coords)
 
        for (const brewery_marker_coord of brewery_marker_coords) {
           brewery_marker_coord.push(
             new mapboxgl.Marker()
             .setLngLat(brewery_marker_coord)
             .addTo(map) 
           )
         };   


      //   const eppig_lng=-117.22766660410099
      //   const eppig_lat=32.72286208649556
      //   const marker_list=[eppig_lng, eppig_lat]

      //   for (const element of mapbox_data) 
      //   {
      //   const marker = new mapboxgl.Marker()
      //   .setLngLat(marker_list)
      //   // .setPopup(new mapboxgl.Popup().setHTML("<h4>BEER</h4>")) // add popup
      //   .addTo(map);
      // }
      
  
    



