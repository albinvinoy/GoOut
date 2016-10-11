"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.EmailField(max_length=260,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Email address'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class RegistrationForm(forms.Form):
    reg_firstname = forms.CharField(max_length=100,
                                widget=forms.TextInput({
                                    'class':'form-control',
                                    'placeholder':'First name'}))
    reg_lastname = forms.CharField(max_length=100,
                                widget=forms.TextInput({
                                    'class':'form-control',
                                    'placeholder':'Last name'}))
    reg_email = forms.EmailField(max_length=260,
                                widget=forms.TextInput({
                                    'class':'form-control',
                                    'placeholder':'Email address'}))
    reg_password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class ProfileForm(forms.Form):
    firstname = forms.CharField(max_length=100,
                                widget=forms.TextInput({
                                    'class':'form-control',
                                    'placeholder':'First name'}))
    lastname = forms.CharField(max_length=100,
                                widget=forms.TextInput({
                                    'class':'form-control',
                                    'placeholder':'Last name'}))
    bio = forms.CharField(max_length=500,
                            widget=forms.Textarea({
                                'class':'form-control',
                                'placeholder':'500 Character Bio'}))

class ProfilePicForm(forms.Form):
    photo = forms.ImageField()