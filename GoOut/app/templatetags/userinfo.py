from django import template
from django.contrib.auth.models import User
from app.utilities import getUserInfo
from app.models import Interest

register=template.Library()

@register.simple_tag
def user_icon_url(user):
    userInfo=getUserInfo(user)
    return userInfo.profilepic.url if bool(userInfo.profilepic) else ''

@register.assignment_tag
def get_user_interests(user):
    userInfo=getUserInfo(user)
    return userInfo.interests.values()

@register.assignment_tag
def get_suggested_interests(user):
    return Interest.objects.values()