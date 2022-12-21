let breweryLocations=document.querySelectorAll(".coordinates");
console.log(breweryLocations)
for (location of breweryLocations) {
    location.addEventListener("click",(evt)=>{
        evt.preventDefault();
        const coords={
            lat:evt.target.dataset.lat,
            long:evt.target.dataset.long,
        };
        fetch("/taco",{
            method:"POST",
            body:JSON.stringify(coords),
    }).then((res)=>res.json()).then(
         (data)=>{
          console.log(data)  
         }   
        )
    })
}
