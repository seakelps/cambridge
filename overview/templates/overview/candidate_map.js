/* Plot map of cambridge for candidates
 * included into the page via django so that we can guarantee initMap is
 * defined before the maps API tries to call it without making this script a
 * seperate synchronous download.
 * Right now requires #map element and data stored in initialLocations
 */


async function initMap() {
    /* google maps callback. waiting for document.ready so we don't ever load
     * it before the id=map exists */
    $(async function() {
        const { Map } = await google.maps.importLibrary("maps");

        var mapDiv = document.getElementById('map');

        center = {lat: 42.3767926, lng: -71.1064153};
        for (let location of initialLocations) {
            if (location.main) {
              center.lat = (center.lat + location.lat) / 2
              center.lng = (center.lng + location.lng) / 2
              break
            }
        }

        map = new Map(mapDiv, {
            center,
            navigationControl: false,
            mapTypeControl: false,
            scaleControl: false,
            scrollwheel: false,
            zoom: 13,
	    mapId: "CAMB"
        });

        for (let location of initialLocations) {
            addMarker(map, new Location(location));
        }
    });
}

var Location = function(data) {
    this.id = data.id;
    this.name = data.name;

    var names = data.name.split(' ')
    this.label = names[0][0] + names[names.length - 1][0]; // two letter abbreviation
    this.lat = data.lat;
    this.lng = data.lng;
    this.color = data.color;
    this.main = data.main;
    this.link = data.link;
};


async function addMarker(map, feature) {
    const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary("marker");


    const pinGlyph = new PinElement({
	scale: 0.75,
        glyphColor: feature.color,
    })

    var marker = new AdvancedMarkerElement({
        id : feature.id,
        position: new google.maps.LatLng(feature.lat, feature.lng),
        map: map,
        title: feature.name,
        zIndex: feature.main ? 2 : 1,  // put primary focus on top of other candidate pins
        content: pinGlyph.element,
        gmpClickable: true,
    });

    var infoWindow = new google.maps.InfoWindow({
        content: `<a href="${feature.link}">${feature.name}</a>`
    });

    marker.addListener('click', ({ domEvent, latLng }) => {
	const { target } = domEvent;
        if (infoWindow.getAnchor()) {
            infoWindow.close(map, marker);
        } else {
            infoWindow.open(map, marker);
        }
    });

    return marker;
};
