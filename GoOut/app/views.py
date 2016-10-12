"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as login_view
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import login
from app.forms import BootstrapAuthenticationForm, ProfileForm, RegistrationForm, ProfilePicForm
from app.models import UserInfo
from app.utilities import getUserInfo

@login_required
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/index.html',
        {
            'title':'CPSC462 App',
            'year':datetime.now().year,
        })

@login_required
def profile(request):
    """Renders the profile page."""
    assert isinstance(request, HttpRequest)
    form = ProfileForm(request.POST or None)
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
    form = ProfileForm(initial={
        'firstname':request.user.first_name, 
        'lastname':request.user.last_name,
        'bio':userInfo.bio
    })
    return render(request,
        'app/profile.html',
        {
            'title':'Profile',
            'form':form,
            'photoform':photoform,
            'photoUrl':photoUrl,
            'year':datetime.now().year,
        })

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Contact us to get an ad-free application for 30 days!!',
            'year':datetime.now().year,
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
    form = ProfileForm(initial={
        'firstname':request.user.first_name, 
        'lastname':request.user.last_name,
        'bio':userInfo.bio
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