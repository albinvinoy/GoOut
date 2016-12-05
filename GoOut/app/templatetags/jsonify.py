from django.core.serializers import serialize
from django.utils.safestring import mark_safe
from django.template import Library

import json

register = Library()

def jsonify(object):

    return mark_safe(json.dumps(object))

register.filter('jsonify', jsonify)
jsonify.is_safe = True  
