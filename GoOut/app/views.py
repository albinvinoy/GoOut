"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as login_view
from datetime import datetime
from app.forms import RegistrationForm, BootstrapAuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login

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

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/about.html',
        {
            'title':'About',
            'message':'CPSC 462 App.',
            'year':datetime.now().year,
        })

def user_login(request):
    """Handles user login"""
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