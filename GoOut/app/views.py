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
from app.forms import BootstrapAuthenticationForm, ProfileForm, RegistrationForm

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
    if(request.method=='POST' and form.is_valid()):
        firstname=form.cleaned_data['firstname']
        lastname=form.cleaned_data['lastname']
        request.user.first_name=firstname
        request.user.last_name=lastname
        request.user.save()
    form = ProfileForm(initial={'firstname':request.user.first_name, 'lastname':request.user.last_name})
    return render(request,
        'app/profile.html',
        {
            'title':'Profile',
            'form':form,
            'message':'CPSC 462 App.',
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