from django.db import models
from django.forms import ModelForm, Textarea
from django import forms
from constants import *
from feedback.models import  Feedback
from ckeditor.widgets import CKEditorWidget
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

class FeedbackForm(forms.ModelForm):
	class Meta:
		model = Feedback
		exclude = ('date_sub',)

	def clean(self):
		cleaned_data = self.cleaned_data
		date_sub = cleaned_data.get('date_sub')
		email = cleaned_data.get('email')
		
		try:
			f = Feedback.objects.filter(email=email).order_by('-date_sub')[0]
			dif = datetime.now() - f.date_sub
			hours = dif.days*24 + dif.seconds/3600	
			
			if hours<24:
				raise forms.ValidationError('This email address submitted a feedback %s hours ago. You cannot submit a feedback twice in period of 24 hours.'%hours)
		except IndexError, ObjectDoesNotExist:
				pass

		return cleaned_data

