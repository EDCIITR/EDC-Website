from django.db import models
from about.models import Member
from constants import *
from ckeditor.fields import RichTextField
# Create your models here.

def get_media_upload_to(instance,filename):
	return 'uploads/recruitments/pics/' + instance.setup.name + '/' + filename

class Setup(models.Model):
	name = models.CharField(max_length=50,help_text='Code name for the recruitment process')
	date_recruitment_starts = models.DateTimeField('date at which online recruitment starts')
	date_recruitment_ends = models.DateTimeField('date at which online recruitment ends')
	details = RichTextField(max_length=1000,config_name="admin",blank=True,null=True)
	test_email = models.EmailField(max_length=100,verbose_name="Test Email ID for Slot Mailer")
	mailer =  RichTextField(max_length=5000,config_name="admin",blank=True,null=True)
	year = models.IntegerField(choices = YEAR_CHOICES)
	coordinator = models.ManyToManyField(Member,blank=True,null=True)

	def __unicode__(self):
		return "%s"%self.name

	def get_name(self):
		return "%s"%self.name


class Candidate(models.Model):
	salutation = models.IntegerField(choices=SALUTATION_CHOICES,max_length=10)
	name = models.CharField(max_length=50)
	email = models.EmailField()
	branch = models.CharField(max_length=50,choices = BRANCH_CHOICES)
	phone = models.CharField(max_length=20)
	slot = models.IntegerField(blank=True,null=True)
	why_edc = models.TextField(max_length=500,verbose_name="Why do you want to join EDC")
	other_groups = models.TextField(max_length=100,verbose_name="Which other groups on campus are you involved in? (Please separate by commas): ")
	skills = models.TextField(max_length=500,blank=True,null=True,verbose_name="Do you possess any special skills like designing, web development, communication etc..")	
	hash_value = models.CharField(max_length=100)
	blocked = models.BooleanField()
	setup = models.ForeignKey(Setup)
	pic = models.ImageField(upload_to=get_media_upload_to,blank=True,null=True,verbose_name="Photograph (less than 2 MB in size)")

	def __unicode__(self):
		return "%s %s"%(self.salutation,self.name)

