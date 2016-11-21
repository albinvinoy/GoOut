from django.contrib.auth.models import User
from app.models import UserInfo, Interest, Subinterest, UserInterest
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
    userInterests=UserInterest.objects.filter(user=getUserInfo(user))
    subinterestIDs=set()
    for interest in userInterests:
        subinterestIDs.update(interest.subinterests.values_list('id', flat=True))
    return list(subinterestIDs)

def getSuggestedInterests(user):
    return Interest.objects.values()

def getSubinterests(interest):
    selected_interest = Interest.objects.filter(id=interest['id'])
    subinterests = Subinterest.objects.filter(interest=selected_interest)
    return subinterests

def getSubinterestsFromInterestID(interestID):
    selected_interest = Interest.objects.filter(id=interestID)
    subinterests = Subinterest.objects.filter(interest=selected_interest)
    return subinterests

def getSuggestedInterestsAsListOfTuples(user):
    interests = getSuggestedInterests(user)
    interestsList = list(map((lambda interest: (interest['id'], interest['name'])), interests))
    return interestsList

def getSubinterestTuplesFromInterestID(interestID):
    subinterests = getSubinterestsFromInterestID(interestID)
    subinterestTuples = list(map((lambda subinterest: (subinterest.id, subinterest.name)), subinterests))
    return subinterestTuples

def getInterestsAndSubInterests(user):
    interests = getSuggestedInterests(user)
    interestsList = list(map((lambda interest: (interest['name'], (getSubinterestTuplesFromInterestID(interest['id'])))),interests))
    return interestsList

def generateNewsfeed(userInterests):
    for userInterest in userInterests:
        if (userInterest.interest.id==1): # Movies
            # subinterest = movie genres
            for subinterest in userInterest.interest.subinterests:
                x = 5 # filler, delete soon
        elif (userInterest.interest.id==2): # Music
            # subinterest = music genres
            for subinterest in userInterest.interest.subinterests:
                x=5
        elif (userInterest.interest.id==3): # Craft Beer
            # subinterest = beer type
            for subinterest in userInterest.interest.subinterest:
                x=5
        elif (userInterest.interest.id==4): # Cars
            # subinterest = car brand
            for subinterest in userInterest.interest.subinterest:
                x=5