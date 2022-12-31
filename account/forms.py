from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput
from .models import *
from django.contrib.auth.forms import UserCreationForm


class Userform(UserCreationForm):
    username=forms.CharField(max_length=30,help_text=None,label='Username')
    password1=forms.CharField(help_text=None,widget=PasswordInput,label='Password')
    password2=forms.CharField(help_text=None,widget=PasswordInput,label='Confirm Password')
    class Meta():
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')

        labels =(
            'password1','Password',
            'password2','Confirm Password'
        )

class UserProfileInfoform(forms.ModelForm):
    bio = forms.CharField(required=False)
    class Meta():
        model = User_Profile
        fields = ('bio',)




            