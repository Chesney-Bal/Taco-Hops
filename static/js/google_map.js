'use strict';

function initMap() {
    // Code that works with Google Maps here
    const searchCoords = {
        lat: 32.0,
        lng: -117.0,
    };
    console.log("1-Where's my map?")

    const basicMap = new google.maps.Map(document.querySelector('#map'), {
        center: searchCoords,
        zoom: 11,
    });

    // console.log("2-Now Where's my map?")

    // const mapMarker = new google.maps.Marker({
    //     postion: searchCoords,
    //     title:'Search Location',
    //     map: basicMap,
    // });
    
    // console.log("3-Wait-really? No Map?!")

    // mapMarker.addListener('click',()=> {
    //     alert('Im listening to this!!');
    // });

    // const mapInfo= new google.maps.InfoWindow({
    //     content: '<h1> Brewery Heaven</h1>',
    // });

    // mapInfo.open(basicMap, mapMarker);

    // console.log("4-You gotta be kidding me!")

    // const locations =[
    //     {
    //         name: 'Eppig Brewing',
    //         coords: {
    //             lat: 32.76634,
    //             lng: -117.12873,
    //         },
    //     },
    //     // {
    //     //     // next brewery
    //     // }
    // ];

    // console.log("5-Is it me?!")

    // const markers = [];
    // for (const location of locations) {
    //     markers.push(
    //         new google.maps.Marker({
    //             position: location.coords,
    //             title:location.name,
    //             map: basicMap,
    //             icons:{
    //                 //custom icon
    //                 url: 'static/img/marker.svg',
    //                 scaledSize: {
    //                     width: 30,
    //                     height: 30,
    //                 },
    //             },
    //         }),
    //     );
    // }

    // console.log("6-This is wack!")

    // // for (const marker of markers) {
    // //     const markerInfo= `
    // //       <h1>${marker.title}</h1>
    // //     <p>
    // //         Located at: <code>${marker.position.lat()}</code>,
    // //         <code>${marker.position.lng()}</code>
    // //     </p>
    // //     `;

    // //     const inforWindow= new google.maps.InfoWindow({
    // //         content: markerInfo,
    // //         maxwidth:200,
    // //     });

    // //     marker.addListener('click', () => {
    // //         inforWindow.open(basicMap, marker);
    // //     });
    // // }

    // console.log("7-I feel used.")

  }