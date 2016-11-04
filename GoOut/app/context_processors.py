from django.conf import settings
from app.forms import LocationForm

def google_maps_key(request):
    return {'GOOGLE_API_KEY':settings.GS_MAPS_KEY}

def location_field(request):
    locationForm=LocationForm()
    return {'FORM_LOCATION':locationForm}