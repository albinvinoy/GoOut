from django.contrib.auth.models import User
from app.models import UserInfo
from django.core.exceptions import ObjectDoesNotExist

def getUserInfo(user):
    """Returns UserInfo associated with User
    Creates one, if it doesn't already exist."""
    try:
        return UserInfo.objects.get(user=user)
    except ObjectDoesNotExist:
        userInfo=UserInfo(user=user)
        userInfo.save()
        return userInfo