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

        document.getElementById('btnGetCurrentLocation').addEventListener('click', function () {
            navigator.geolocation.getCurrentPosition(showPosition, showPositionError);
        });
    }
}