function showPosition(position) {
    latitude = position.coords.latitude;
    longitude = position.coords.longitude;
    var center = { lat: latitude, lng: longitude };

    window.map.setCenter(center);
    window.map.setZoom(12);

    if (window.curr_loc_marker)
        window.curr_loc_marker.setMap(null);
    window.curr_loc_marker = new google.maps.Marker({
        position: center,
        map: window.map
    });

    window.geocoder.geocode({ 'location': center }, function (results, status) {
        if (status === 'OK') {
            if (results[2]) {
                $('#id_location').val(results[2].formatted_address);
            }
        }
    });
}

function showPositionError(error) {
    message = '';
    switch (error.code) {
        case error.PERMISSION_DENIED:
            message = "User denied the request for Geolocation."
            break;
        case error.POSITION_UNAVAILABLE:
            message = "Location information is unavailable."
            break;
        case error.TIMEOUT:
            message = "The request to get user location timed out."
            break;
        case error.UNKNOWN_ERROR:
            message = "An unknown error occurred."
            break;
    }
    $('#id_location').val(message);
}

function initMap() {
    var mapEl = document.getElementById('map');
    if (mapEl) {
        var center = { lat: 33.883, lng: -117.887 };
        if (typeof curr_loc !== 'undefined') {
            center['lat'] = curr_loc['lat'];
            center['lng'] = curr_loc['lng'];
        }
        window.map = new google.maps.Map(mapEl, {
            zoom: 8,
            center: center
        });
        if (typeof curr_loc !== 'undefined') {
            window.curr_loc_marker = new google.maps.Marker({
                position: center,
                map: window.map
            });
            window.map.setZoom(12);
        }
        window.geocoder = new google.maps.Geocoder();
        service = new google.maps.places.PlacesService(map);

        document.getElementById('btnGetCurrentLocation').addEventListener('click', function () {
            navigator.geolocation.getCurrentPosition(showPosition, showPositionError);
        });

        map.addListener('idle', function () { performSearch(); });
    }
}

function performSearch() {
    var request = {
        location: map.center,
        radius: 24000,
        keyword: 'bar'
    };

    service.radarSearch(request, callback);
}

function callback(results, status) {
    if (status !== google.maps.places.PlacesServiceStatus.OK) {
        console.error(status);
        return;
    }
    for (var i = 0, result; result = results[i]; i++) {
        addMarker(result);
    }
}

function addMarker(place) {
    var marker = new google.maps.Marker({
        map: window.map,
        position: place.geometry.location,
        icon: {
            url: 'https://developers.google.com/maps/documentation/javascript/images/circle.png',
            anchor: new google.maps.Point(10, 10),
            scaledSize: new google.maps.Size(10, 17)
        }
    });

    google.maps.event.addListener(marker, 'click', function () {
        service.getDetails(place, function (result, status) {
            if (status !== google.maps.places.PlacesServiceStatus.OK) {
                console.error(status);
                return;
            }
            infoWindow.setContent(result.name);
            infoWindow.open(map, marker);
        });
    });
}

$(function () {
    $('#userLocationLnk').popover({
        html: true,
        content: function () {
            return $('#locationPopoverContent').html();
        },
        placement: 'bottom',
        title: function () {
            return '<h3>Set Location</h3>';
        }
    }).click(initMap);
    $('#id_photo').change(function () {
        $('#profilePhotoForm  form').submit();
    });
});