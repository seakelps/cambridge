/* Plot map of cambridge for candidates
 * included into the page via django so that we can guarantee initMap is
 * defined before the maps API tries to call it without making this script a
 * seperate synchronous download.
 * Right now requires #map element and data stored in initialLocations
 */


function initMap() {
    /* google maps callback. waiting for document.ready so we don't ever load
     * it before the id=map exists */
    $(function() {
        var mapDiv = document.getElementById('map');

        center = {lat: 42.3767926, lng: -71.1064153};
        for (let location of initialLocations) {
            if (location.main) {
              center.lat = (center.lat + location.lat) / 2
              center.lng = (center.lng + location.lng) / 2
              break
            }
        }

        map = new google.maps.Map(mapDiv, {
            center,
            navigationControl: false,
            mapTypeControl: false,
            scaleControl: false,
            scrollwheel: false,
            zoom: 13
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


function addMarker(map, feature) {
    var marker = new google.maps.Marker({
        id : feature.id,
        position: new google.maps.LatLng(feature.lat, feature.lng),
        map: map,
        icon: {
          // https://developers.google.com/chart/image/docs/gallery/dynamic_icons?csw=1#pins
          // chld=size|rotation|color|fontsize|fontweight|text
          url: `https://chart.googleapis.com/chart?chst=d_map_spin&chld=0.75|0|${feature.color}|11|_|${feature.label}`
        },
        title: feature.name,
        zIndex: feature.main ? 2 : 1  // put primary focus on top of other candidate pins
    });

    var infowindow = new google.maps.InfoWindow({
        content: `<a href="${feature.link}">${feature.name}</a>`
    });

    google.maps.event.addListener(marker, 'click', function() {
        if (infowindow.getAnchor()) {
            infowindow.close(map, marker);
        } else {
            infowindow.open(map, marker);
        }
    });

    return marker;
};
