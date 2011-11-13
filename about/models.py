from django.db import models
from constants import *

# Create your models here.
class Member(models.Model):
	name = models.CharField(max_length=50)
	email = models.EmailField(max_length=50,blank=True,null=True)
	phone = models.CharField(max_length=20,blank=True,null=True)
	pic = models.ImageField(upload_to='uploads/member_pics',blank=True,null=True,help_text='150x150')
	year = models.IntegerField(choices=YEAR_CHOICES)	
	branch = models.CharField(max_length=50,choices = BRANCH_CHOICES)
	rank = models.IntegerField(max_length=1,choices=RANK_CHOICES)
	intro = models.TextField(max_length=500,blank=True,null=True)
	
	def __unicode__(self):
		return self.name

	def get_absolute_url(self):
		return "/contact/#%s"%(self.name)

