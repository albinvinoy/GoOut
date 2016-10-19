from django.contrib.auth.models import User
from app.models import UserInfo, Interest
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

def getUserInterestsAsIdList(user):
    userInterests=getUserInfo(user).interests.values()
    interestIDs=[]
    for interest in userInterests:
        interestIDs.append(interest['id'])
    return interestIDs

def getSuggestedInterests(user):
    return Interest.objects.values()

def getSuggestedInterestsAsListOfTuples(user):
    interests = getSuggestedInterests(user)
    interestsList=[]
    for interest in interests:
        interestsList.append((interest['id'], interest['name']))
    return interestsList