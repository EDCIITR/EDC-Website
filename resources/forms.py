from django.db import models
from resources.models import Startup
from users.models import User
from django import forms
from constants import *

class MentorMailForm(forms.Form):
	subject = forms.CharField(max_length=100,label='Subject',initial='(Subject)')
	content = forms.CharField(max_length=100,label = 'Body', initial='(Write your message)',widget=forms.Textarea)

class StartupRegistrationForm(forms.ModelForm):
    class Meta:
        model = Startup
