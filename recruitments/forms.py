from django.db import models
from django.forms import ModelForm, Textarea
from django import forms
from constants import *
from recruitments.models import Candidate, Setup
from ckeditor.widgets import CKEditorWidget
from django.core.exceptions import ObjectDoesNotExist


class CandidateForm(forms.ModelForm):
	class Meta:
		model = Candidate
		exclude = ('hash_value','blocked','setup','slot')
	
	def clean(self):
		cleaned_data = self.cleaned_data
		email = cleaned_data.get('email')
		
		try:
			s = Setup.objects.get(date_recruitment_ends__gt=datetime.now(),date_recruitment_starts__lt=datetime.now())
		
			Candidate.objects.get(email=email,setup=s) 
			raise forms.ValidationError('This Email ID has already applied for this recruitment process')
		except ObjectDoesNotExist:
			pass

		return cleaned_data

	'''
	salutation = forms.CharField(max_length=10,required=True,choices=SALUTATION_CHOICES)
	name = forms.CharField(max_length=50,required = True,label='Your name')
	email = forms.EmailField(max_length=50,required=True,label='Email Address')
	branch = forms.CharField(max_length=50,required=True,choices=BRANCH_CHOICES)
	phone = forms.CharField(max_length=15, required=True)	
	why_edc = forms.TextField(max_length=500,required=True)
	other_groups = forms.TextField(max_length=100)
	interests = forms.
	'''



