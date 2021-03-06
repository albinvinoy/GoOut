﻿function showPosition(position) {
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

        //map.addListener('idle', function () { performSearch(); });
    }
}

function performSearch() {
    var request = {
        location: map.center,
        radius: 24000,
        keyword: ['bar', 'theater', 'brewery', 'winery', 'concert', 'park']
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
        clickable: true,
        place: {
            placeId: place.place_id,
            location: place.geometry.location
        },
        icon: {
            url: 'https://developers.google.com/maps/documentation/javascript/images/circle.png',
            anchor: new google.maps.Point(10, 10),
            scaledSize: new google.maps.Size(10, 17)
        },
    });

    //addInfoWindow(marker, place.name);
}

function addInfoWindow(marker, message) {

    var infoWindow = new google.maps.InfoWindow({
        map: marker.map,
        content: message,
        position: marker.location
    });

    marker.addListener(marker, 'click', function () {
        infoWindow.open(map, marker);
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

    $('.btn-showtimes').click(function () {
        var $moreInfo = $('#moreInfo');
        var $article = $(this).closest('.article');
        // Load article info
        var articleInfo = $.parseJSON($article.find('script').text());
        $moreInfo.find('.modal-title').text('Theatres playing ' + articleInfo['title']);
        // Show modal
        $moreInfo.modal('show');
        $moreInfo.one('shown.bs.modal', function () {
            if (typeof window.articleInfoMap !== 'undefined') {
                // If initialized, remove markers
                window.articleInfoMap.markers.forEach(function (marker) {
                    marker.setMap(null);
                    marker = null;
                });
            }
            else {
                // If not initialized, initialize articleInfoMap
                var mapEl = document.getElementById('infoMap');
                var center = { lat: 33.883, lng: -117.887 };
                if (typeof curr_loc !== 'undefined') {
                    center['lat'] = curr_loc['lat'];
                    center['lng'] = curr_loc['lng'];
                }
                window.articleInfoMap = new google.maps.Map(mapEl, {
                    zoom: 10,
                    center: center
                });
                window.articleInfoMap.markers = [];
            }
            // Attach markers, marker info
            var theatres = new Set();
            articleInfo.showtimes.forEach(function (showtime) {
                theatres.add(showtime.theatre.name);
            });
            window.infowindow = new google.maps.InfoWindow();
            window.placeService = new google.maps.places.PlacesService(window.articleInfoMap);
            for (let theatre of theatres) {
                var name = theatre;
                window.placeService.radarSearch({
                    location: window.articleInfoMap.center,
                    radius: 50000,
                    name: name
                }, theatreSearchCallback);
            }
        });
    });
});

function theatreSearchCallback(results, status) {
    if (status !== google.maps.places.PlacesServiceStatus.OK) {
        return;
    }
    for (var i = 0, result; result = results[i]; i++) {
        var request = {
            placeId:result.place_id
        };
        window.placeService.getDetails(request, function (place, status) {
            var marker = new google.maps.Marker({
                map: window.articleInfoMap,
                position: place.geometry.location,
                clickable: true,
                place: {
                    placeId: place.place_id,
                    location: place.geometry.location
                },
            });
            window.articleInfoMap.markers.push(marker);
            window.infowindow.setContent('<div><strong>' + place.name + '</strong>');
            window.infowindow.open(window.articleInfoMap, marker);
        });
    }
}
