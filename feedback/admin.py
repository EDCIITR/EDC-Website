from django.contrib import admin
from home.models import *
from feedback.models import Feedback
from django import forms
from datetime import datetime
from django.core.mail import EmailMessage, BadHeaderError


class FeedbackAdmin(admin.ModelAdmin):
	list_display = ('name','email','feedback','date_sub')
	ordering = ('-date_sub',)

admin.site.register(Feedback,FeedbackAdmin)
