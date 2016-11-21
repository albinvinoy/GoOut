"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import BaseFormSet
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

class LocationForm(forms.Form):
    location = forms.CharField(max_length=500,
                                widget=forms.TextInput({
                                    'class':'form-control',
                                    'placeholder':'City, State'}))

class ProfileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        suggestedInterests = None
        if ('suggestedInterests' in kwargs):
            suggestedInterests=kwargs.pop('suggestedInterests')
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['interests'].choices=suggestedInterests if suggestedInterests is not None else []

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
    interests=forms.MultipleChoiceField(choices=(),
                            widget=forms.CheckboxSelectMultiple({
                                'class':'form-control'
                            }))

class ProfilePicForm(forms.Form):
    photo = forms.ImageField()

class SubinterestSelectionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        suggested_subinterests = None
        if ('subinterests' in kwargs):
            suggested_subinterests=kwargs.pop('subinterests')
        super(SubinterestSelectionForm, self).__init__(*args, **kwargs)
        self.fields['subinterests'].choices=suggested_subinterests if suggested_subinterests is not None else []

    subinterests=forms.MultipleChoiceField(choices=(),
                            widget=forms.CheckboxSelectMultiple({
                                'class':'form-control'
                            }))