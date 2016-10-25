from django.conf import settings

def google_maps_key(request):
    return {'GOOGLE_API_KEY':settings.GS_MAPS_KEY}