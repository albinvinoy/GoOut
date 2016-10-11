$('#btnGetLocation').click(function () {
    navigator.geolocation.getCurrentPosition(showPosition, showPositionError);
});

function showPosition(position) {
    latitude = position.coords.latitude;
    longitude = position.coords.longitude;
    coords = latitude + ', ' + longitude;
    $('#txtLocation').val(coords);
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
    $('#txtLocation').val(message);
}