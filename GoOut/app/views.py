"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as login_view
from django.forms import formset_factory
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import login
from app.forms import BootstrapAuthenticationForm, ProfileForm, RegistrationForm, ProfilePicForm, LocationForm, SubinterestSelectionForm
from app.models import Interest, UserInfo, UserInterest, Subinterest
from app.utilities import getUserInfo, getUserInterestsAsIdList, getInterestsAndSubInterests
from app.maps import getLocationFromString
from app.newsfeed import Newsfeed

@login_required
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    form = LocationForm(request.POST or None)
    userInfo = getUserInfo(user=request.user)
    newsfeed = Newsfeed(userInfo)
    if(request.method=='POST' and form.is_valid()):
        location = getLocationFromString(form.cleaned_data['location'])
        request.session['location'] = location
        form.fields['location'].initial = '{0}, {1}, {2}'.format(location['city'], location['state'], location['country'])
        newsfeed.nextPage()
    elif ('location' in request.session):
        location = request.session['location']
        form.fields['location'].initial = '{0}, {1}, {2}'.format(location['city'], location['state'], location['country'])
        newsfeed.nextPage()
    return render(request,
        'app/index.html',
        {
            'title':'Go Out',
            'year':datetime.now().year,
            'form':form,
            'newsfeed':newsfeed.articles
        })

@login_required
def profile(request):
    """Renders the profile page."""
    assert isinstance(request, HttpRequest)
    interests = getInterestsAndSubInterests(request.user)
    form = ProfileForm(request.POST or None, suggestedInterests=interests)
    photoform = ProfilePicForm()
    userInfo=getUserInfo(request.user)
    photoUrl = userInfo.profilepic.url if bool(userInfo.profilepic) else ''
    if(request.method=='POST' and form.is_valid()):
        firstname=form.cleaned_data['firstname']
        lastname=form.cleaned_data['lastname']
        bio=form.cleaned_data['bio']
        request.user.first_name=firstname
        request.user.last_name=lastname
        request.user.save()
        userInfo.bio=bio
        userInfo.save()
        subinterestIDs=form.cleaned_data['interests']
        subinterests=list(map(lambda subinterestID:Subinterest.objects.get(id=subinterestID), subinterestIDs))
        uniqueInterests = {subinterest.interest for subinterest in subinterests}
        UserInterest.objects.filter(user=userInfo).delete()
        for interest in uniqueInterests:
            userInterest=UserInterest(user=userInfo, interest=interest, priority=1)
            userInterest.save()
            userSubInterests =[subinterest for subinterest in subinterests if subinterest.interest == interest]
            userInterest.subinterests=userSubInterests
            userInterest.save()
    userInterests = getUserInterestsAsIdList(request.user)
    form = ProfileForm(suggestedInterests=interests,
    initial={
        'firstname':request.user.first_name, 
        'lastname':request.user.last_name,
        'bio':userInfo.bio,
        'interests':userInterests
    })
    return render(request,
        'app/profile.html',
        {
            'title':'Profile',
            'form':form,
            'photoform':photoform,
            'photoUrl':photoUrl,
        })

def user_login(request):
    """Handles user login"""
    assert isinstance(request, HttpRequest)
    form = BootstrapAuthenticationForm()
    signup_form = RegistrationForm()
    if(request.method == 'POST'):
        return login_view(request, 'app/login.html',
            authentication_form = BootstrapAuthenticationForm,
            extra_context={
                'signin_title':'Login',
                'signup_title':'Sign Up',
                'signup_form':RegistrationForm
            })
    else:
        return render(request,
            'app/login.html',
            {
                'signin_title':'Login',
                'signup_title':'Sign Up',
                'form':BootstrapAuthenticationForm,
                'signup_form':RegistrationForm
            })

def register(request):
    """Handles user registration."""
    assert isinstance(request, HttpRequest)
    form = RegistrationForm(request.POST or None)
    if(request.method == 'POST' and form.is_valid()):
        user = User.objects.create_user(form.cleaned_data['reg_email'],form.cleaned_data['reg_email'],form.cleaned_data['reg_password'],first_name=form.cleaned_data['reg_firstname'],last_name=form.cleaned_data['reg_lastname'])
        login(request, user)
        return HttpResponseRedirect('/')
    else:
        return render(request,
            'app/login.html',
            {
                'signin_title':'Login',
                'signup_title':'Sign Up',
                'form':BootstrapAuthenticationForm,
                'signup_form':form
            })

@login_required
def profilepic(request):
    """Handles profile photo update"""
    assert isinstance(request, HttpRequest)
    userInfo = getUserInfo(request.user)
    form = ProfilePicForm(request.POST, request.FILES)
    if (request.method=='POST' and form.is_valid()):
        if(userInfo.profilepic):
            userInfo.profilepic.storage.delete(userInfo.profilepic.name)
        userInfo.profilepic=request.FILES['photo']
        userInfo.save()
    form = ProfileForm(suggestedInterests=getSuggestedInterestsAsListOfTuples(request.user),
    initial={
        'firstname':request.user.first_name, 
        'lastname':request.user.last_name,
        'bio':userInfo.bio,
        'interests':getUserInterestsAsIdList(request.user)
    })
    photoUrl = userInfo.profilepic.url if bool(userInfo.profilepic) else ''
    return render(request,
        'app/profile.html',
        {
            'title':'Profile',
            'form':form,
            'photoform':ProfilePicForm,
            'photoUrl':photoUrl,
            'year':datetime.now().year,
        })

@login_required
def location(request):
    """Handles location update"""
    assert isinstance(request, HttpRequest)
    form = LocationForm(request.POST or None)
    if (request.method == 'POST' and form.is_valid()):
        location = getLocationFromString(form.cleaned_data['location'])
        request.session['location'] = location
    next = request.POST.get('next','/')
    return HttpResponseRedirect(next)
