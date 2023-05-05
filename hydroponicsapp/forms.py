from dataclasses import fields
from logging.config import valid_ident
from socket import fromshare
from tkinter.tix import Form
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.core.mail import send_mail


class UserRegistration(UserCreationForm):

    username = forms.CharField(
        widget = forms.EmailInput(
            attrs={
                "class": "form-control",
                "type": "email",
                "placeholder": "Enter your Email Address"
            }
        )
    )
   
    password1 = forms.CharField(
        widget = forms.PasswordInput(
            attrs={
                "class": "form-control",
                "type": "password",
                "placeholder": "Enter Password"
            }
        )
    )
    
    password2 = forms.CharField(
        widget = forms.PasswordInput(
            attrs={
                "class": "form-control",
                "type": "password",
                "placeholder": "Confirm Password"
            }
        )
    )

    class Meta:
        model = Registration
        fields = ('username', 'password1', 'password2')
    
    
class UserLoginForm(forms.Form):
    username = forms.CharField(
        
    )
   
    password = forms.CharField(
        widget = forms.PasswordInput(
        )
    )
