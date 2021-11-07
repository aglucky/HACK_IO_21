mapboxgl.accessToken = 'pk.eyJ1IjoibXJhbHBhY2EiLCJhIjoiY2pyYmV5dWg4MTJheDQzcGNxeGtleWx0bCJ9.SwBpLsVT9FGuA9JoEHg60w';
const map = new mapboxgl.Map({
container: 'map',
style: 'mapbox://styles/mapbox/streets-v11',
center: [-77.04, 38.907],
zoom: 11.15
});
 
/*
const getData = async () => {
    const data = await 
}
*/

var JSON_OBJECT = fetch('https://owsz3kcw32.execute-api.us-east-1.amazonaws.com/staging/api2/getMapData')
.then(data => {
return data.json();
})
.then(post => {
console.log(post.title);
});
// TODO : Request from API, add it to addSource() object
map.on('load', () => {
map.addSource('places', JSON_OBJECT); // INSERT THE MAPBOX OBJECT HERE
// Add a layer showing the places.
map.addLayer({
'id': 'places',
'type': 'symbol',
'source': 'places',
'layout': {
'icon-image': '{icon}',
'icon-allow-overlap': true
}
});
 

map.on('click', 'places', (e) => {

const coordinates = e.features[0].geometry.coordinates.slice();
const description = e.features[0].properties.description;
 

while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
}
 
new mapboxgl.Popup()
.setLngLat(coordinates)
.setHTML(description)
.addTo(map);
});
 
map.on('mouseenter', 'places', () => {
map.getCanvas().style.cursor = 'pointer';
});

map.on('mouseleave', 'places', () => {
map.getCanvas().style.cursor = '';
});
});