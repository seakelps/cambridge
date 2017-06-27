/* Plot map of cambridge for candidates
 * Right now requires #map element and data stored in initialLocations
 */


function initMap() {
    var mapDiv = document.getElementById('map');
    map = new google.maps.Map(mapDiv, {
        center: {lat: 42.3767926, lng: -71.1064153},
        zoom: 13
    });

    for (let location of initialLocations) {
        addMarker(map, location);
    }
}

var Location = function(data) {
    this.id = data.id;
    this.name = data.name;
    this.lat = data.lat;
    this.lng = data.lng;
    this.color = data.color;
};


function addMarker(map, feature) {
    return new google.maps.Marker({
        id : feature.id,
        position: new google.maps.LatLng(feature.lat, feature.lng),
        map: map,
        icon: {
            url: 'http://maps.google.com/mapfiles/kml/paddle/' + feature.color + '-blank.png',
            scaledSize: new google.maps.Size(30, 30),
        },
        title: feature.name
    });
};
