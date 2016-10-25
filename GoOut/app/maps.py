import googlemaps
from django.conf import settings

def getLocationFromString(locationString):
    """
    Given an input string, returns an object with
    keys city, state, country, lat, lng
    """
    gmaps = googlemaps.Client(key=settings.GS_SERVER_KEY)
    geocode_result = gmaps.geocode(locationString)
    location = {}

    for result in geocode_result:
        for component in result['address_components']:
            if ('locality' in component['types']):
                location['city'] = component['short_name']
            elif ('administrative_area_level_1' in component['types']):
                location['state'] = component['short_name']
            elif ('country' in component['types']):
                location['country'] = component['short_name']

        location['lat'] = result['geometry']['location']['lat']
        location['lng'] = result['geometry']['location']['lng']

    return location