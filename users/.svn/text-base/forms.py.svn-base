from django.db import models
from django.forms import ModelForm
from users.models import User
from django import forms
from constants import *

class RegistrationForm(forms.Form):
	name = forms.CharField(max_length=50,label='Your name(*)')
	email = forms.EmailField(max_length=50,label='Email(*)')
	password = forms.CharField(max_length=50,label='Password(*)',widget=forms.PasswordInput)
	password2 = forms.CharField(max_length=50,label='Confirm Password(*)',widget=forms.PasswordInput)
	phone = forms.IntegerField(required=False,label='Phone')
	organisation = forms.CharField(max_length=100,label='Organisation(*)')
	subscribe = forms.BooleanField(label='Subscribe to EDC newsletter and updates',required=False)

class LoginForm(forms.Form):
	email = forms.EmailField(max_length=50,label='Email')
	password = forms.CharField(max_length=50,label='Password',widget=forms.PasswordInput)

class EditForm(forms.Form):
	name = forms.CharField(max_length=50,label='Your name(*)')
	phone = forms.IntegerField(max_value=BIG_INT_MAX,min_value=BIG_INT_MIN,required=False,label='Phone')
	organisation = forms.CharField(max_length=100,label='Organisation(*)')
	subscribe = forms.BooleanField(label='Subscribe to EDC newsletters and updates', required=False)

class ChangePasswordForm(forms.Form):
	cur_password = forms.CharField(max_length=50,label='Current Password',widget=forms.PasswordInput)
	new_password = forms.CharField(max_length=50,label='New Password',widget=forms.PasswordInput)
	new_password2= forms.CharField(max_length=50,label='Confirm New Password', widget=forms.PasswordInput)

class ForgotPasswordForm(forms.Form):
	email = forms.EmailField(max_length=50,label='Email Address')

