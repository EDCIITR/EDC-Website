from django.db import models
from django.forms import ModelForm, Textarea
from users.models import User
from django import forms
from constants import *
from events.models import ArthData
from ckeditor.widgets import CKEditorWidget
from events.models import FieldCategory

class TeamForm(forms.Form):
	name = forms.CharField(max_length=50,required=True,label='Team Name')	
	member1 = forms.CharField(max_length=100,required=False,label='Name of Member 1')
	email1 = forms.EmailField(max_length=100,required=False,label='Email address of Member 1')
	organisation1 = forms.CharField(max_length=100,required=False,label='Organisation of Member 1')
	member2 = forms.CharField(max_length=100,required=False,label='Name of Member 2')
	email2 = forms.EmailField(max_length=100,required=False,label='Email address of Member 2')
	organisation2 = forms.CharField(max_length=100,required=False,label='Organisation of Member 2')

	#Custom validation
	def clean(self):
		cleaned_data = self.cleaned_data
		msg =  u'You cannot leave the other fields of a member blank if any one is filled.'
		m1 = cleaned_data.get('member1')
		e1 = cleaned_data.get('email1')
		o1 = cleaned_data.get('organisation1')	
		m2 = cleaned_data.get('member2')
		e2 = cleaned_data.get('email2')
		o2 = cleaned_data.get('organisation2')
				
		if (m1 and (not e1 or not o1)) or (e1 and (not m1 or not o1)) or (o1 and (not m1 or not e1)):
			raise forms.ValidationError(msg)
		
		if (m2 and (not e2 or not o2)) or (e2 and (not m2 or not o2)) or (o2 and (not m2 or not e2)):
			raise forms.ValidationError(msg)		
		
		if e1 and e2 and e1==e2:
			raise forms.ValidationError('Two members cannot have the same Email Address')
		
		return cleaned_data

class ArthForm(forms.ModelForm):
	class Meta:
		model = ArthData
		fields = ('category','intro','overview','product','market','management','financials','viability','offering',)
		#exclude = ('judge','mentor','comment','score_overview','score_product','score_market','score_management','score_financials', 'score_viability','score_offering')	
	
class ArthJudgeForm(forms.ModelForm):
	class Meta:
		model = ArthData
		fields = ('score_overview','score_product','score_market','score_management','score_financials', 'score_viability','score_offering','comment')

		widgets = {
            		'comment': Textarea(attrs={'cols': 100, 'rows': 5}),
	        }



