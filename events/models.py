from django.db import models
from about.models import Member
from users.models import User
from constants import *
from settings import *
from ckeditor.fields import RichTextField
from datetime import datetime
from associates.models import Sponsor

# Create your models here.
#Upload folder
def get_media_upload_to(instance,filename):
	cat = EventCategory.objects.filter(id=instance.category_id)[0]
	return 'events/' + cat.name + '/' + filename

class Menu(models.Model):
	name = models.CharField(max_length=20)
	url = models.CharField(max_length=20,blank=True,null=True,unique=True)

	def __unicode__(self):
		return self.name

class Event(models.Model):
	name = models.CharField(max_length=100,blank=True,null=True)
	date_event = models.DateTimeField('date of event')
	venue = models.CharField(max_length=100,blank=True,null=True)
	banner = models.ImageField(upload_to=get_media_upload_to,blank=True,null=True,help_text='1024 x 260')
	intro = RichTextField(max_length=5000,config_name="admin")
	overview = RichTextField(max_length=2500,config_name="admin",blank=True,null=True)
	rules = RichTextField(max_length=5000,config_name="admin",blank=True,null=True)
	fb_link = models.CharField(max_length=100,blank=True,null=True) #Url
	participation = RichTextField(max_length=5000,config_name="admin",blank=True,null=True)
	result = RichTextField(max_length=5000,config_name="admin",blank=True,null=True)
	schedule = RichTextField(max_length=1000,config_name="admin",blank=True,null=True)	
	date_participation_starts = models.DateTimeField('date at which online participation starts',blank=True,null=True)
 	date_participation_ends = models.DateTimeField('date at which online participation ends',blank=True,null=True)
	date_result = models.DateTimeField('Date to declare results',blank=True,null=True)	
	separate = models.BooleanField(help_text='Do you want a separate website for this event? No need to set this for Flagship Events') 
	topic = models.CharField(max_length=100,blank=True,null=True)
	category = models.ForeignKey('events.EventCategory')
	parent = models.ForeignKey('events.Event',blank=True,null=True)
	menu_items = models.ManyToManyField(Menu,blank=True,null=True)
	judges = models.ManyToManyField('events.Judge',blank=True,null=True)
	coordinator = models.ManyToManyField(Member,blank=True,null=True)

	def __unicode__(self):
		return self.name

	def get_date(self):
		return self.date_event

	def is_valid(self):
		if self.date_event < datetime.now():
			return False
		else:
			return True

	def has_participation_started(self):
		if self.date_participation_starts and self.date_participation_starts < datetime.now():
			return True
		else: 
			return False

	def has_participation_ended(self):
		if self.date_participation_ends and self.date_participation_ends < datetime.now():
			return False
		else: 
			return False

	def is_participation_valid(self):
		if self.date_participation_starts > datetime.now() or self.date_participation_ends < datetime.now():	
			return False
		else:
			return True	
			
		
	def is_result_declared(self):
		if self.date_result and self.date_result<datetime.now():
			return True
		else:
			return False

	
	def is_flagship(self):
		return self.category.is_flagship()

	def get_link(self):
		if self.is_flagship():
			return ('%s/%s')%(self.category.get_domain(),self.date_event.year)
		else:
			return ('%s/%s')%(self.category.get_domain(),self.pk)

	def get_inside_link(self):
		if self.is_flagship():
			return ('inside/%s/%s')%(self.category.get_domain(),self.date_event.year)
		else:
			return ('inside/%s/%s')%(self.category.get_domain(),self.pk)

	def get_fb_link(self):
		if self.fb_link:	
			link = self.fb_link.replace(':','%3A')
			link = link.replace('/','%2F')
			return FB_PREFIX + link
		else: 
			return None

	def has_partners(self):
		try:
			p = Sponsor.objects.filter(event=self,event_homepage_display=True)
			print "Hello"			
			if p:
				return True		
		except ObjectDoesNotExist:
			pass
		return False

	def has_contacts(self):
		contacts = self.coordinator.all()
		if contacts: 
			return True
		else:
			return False

	def get_title(self):
		if self.is_flagship():
			return ('%s %s')%(self.category,str(self.date_event.year))
		else:
			return self.name
	def has_stages(self):
		stages = Stage.objects.filter(event=self)
		if stages:
			return True
		else:
			return False

	def get_num_teams(self):
		return Team.objects.filter(event=self).count()
	
	def get_num_judged_teams(self):
		return Team.objects.filter(event=self,is_judged=True).count()

	def get_absolute_url(self):
		return ("/events/%s")%(self.get_link())

#EventCategory
class EventCategory(models.Model):
	name = models.CharField(max_length=100)
	domain = models.CharField(max_length=50,blank=True,null=True)
	intro = models.TextField(max_length=100,blank=True,null=True)
	flagship = models.BooleanField()	
	fest = models.BooleanField()

	def __unicode__(self):
		return self.name

	def is_flagship(self):
		return self.flagship
	
	def get_domain(self):
		return self.domain


class Stage(models.Model):
	name = models.CharField(max_length=100)
	details = RichTextField(config_name="admin",max_length=1000)
	date_start = models.DateTimeField('date of starting')
	date_end = models.DateTimeField('date of ending')
	venue = models.CharField(max_length=100,blank=True,null=True)
	event = models.ForeignKey('events.Event')
		
	def __unicode__(self):	
		return self.name

	def is_valid(self):
		if self.date_end > datetime.now():
			return True
		else:
			return False


class Guest(models.Model):
	name = models.CharField(max_length=100)
	organisation = models.CharField(max_length=100,blank=True,null=True)
	designation = models.CharField(max_length=100,blank=True,null=True)
	details = models.TextField(max_length=1000)
	category = models.IntegerField(choices = GUEST_CATEGORY_CHOICES)	
	finalised = models.BooleanField()
	event = models.ForeignKey('events.Event')
	email = models.EmailField(blank=True,null=True)
	pic = models.ImageField(upload_to='uploads/guest_pics/' + str(datetime.now().year),blank=True,null=True)
	specialisation = models.ForeignKey('events.FieldCategory',blank=True,null=True)

	def __unicode__(self):
		return self.name

	def get_event(self):
		return self.event

	def get_absolute_url(self):
		return ("%s/#%s")%(self.event.get_absolute_url(),self.name)


class Judge(models.Model):
	name = models.CharField(max_length=100)
	organisation = models.CharField(max_length=100)
	designation = models.CharField(max_length=100,blank=True,null=True)
	details = models.TextField(max_length=1000,blank=True,null=True)
	email = models.EmailField(unique=True)
	pic = models.ImageField(upload_to='uploads/judge_pics/' + str(datetime.now().year),blank=True,null=True)
	specialisation = models.ForeignKey('events.FieldCategory',blank=True,null=True)

	def __unicode__(self):
		return self.name

class Mentor(models.Model):
	name = models.CharField(max_length=100)
	organisation = models.CharField(max_length=100)
	designation = models.CharField(max_length=100,blank=True,null=True)
	details = models.TextField(max_length=1000,blank=True,null=True)
	email = models.EmailField(blank=True,null=True)
	pic = models.ImageField(upload_to='uploads/mentor_pics/' + str(datetime.now().year),blank=True,null=True)
	specialisation = models.ForeignKey('events.FieldCategory',blank=True,null=True)



class FAQ(models.Model):
	question = models.CharField(max_length=200)
	answer = models.TextField(max_length=1000)
	#answer = RichTextField(config_name="admin",max_length=1000)
	event = models.ForeignKey('events.Event')

	def __unicode__(self):
		return self.question

class Incentive(models.Model):
	#details = RichTextField(config_name="admin",max_length=1000)
	details = models.TextField(max_length=1000)	
	finalised = models.BooleanField()
	event = models.ForeignKey('events.Event')

class FieldCategory(models.Model):
	name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name	
	

class ArthData(models.Model):
	intro = RichTextField(config_name="arth",max_length=10,blank=True,null=True,verbose_name='Brief Introduction')
	overview = RichTextField(config_name="arth",max_length=1000,blank=True,null=True,verbose_name='Company Overview')
	product = RichTextField(config_name="arth",max_length=1000,blank=True,null=True,verbose_name='Products/Services')
	market = RichTextField(config_name="arth",max_length=1000,blank=True,null=True,verbose_name='Market and Marketing Strategy')
	management = RichTextField(config_name="arth",max_length=1000,blank=True,null=True,verbose_name='Management')
	financials = RichTextField(config_name="arth",max_length=1000,blank=True,null=True,verbose_name='Financials')
	viability = RichTextField(config_name="arth",max_length=1000,blank=True,null=True,verbose_name='Viability')
	offering = RichTextField(config_name="arth",max_length=1000,blank=True,null=True,verbose_name='Offering')
	team = models.ForeignKey('events.Team')
	event = models.ForeignKey('events.Event')
	category = models.ForeignKey('events.FieldCategory',blank=True,null=True)	
	comment = models.TextField(max_length=500,blank=True,null=True)
	score_overview = models.IntegerField(default=0)
	score_product = models.IntegerField(default=0)
	score_market = models.IntegerField(default=0)
	score_management = models.IntegerField(default=0)
	score_financials = models.IntegerField(default=0)
	score_viability = models.IntegerField(default=0)
	score_offering = models.IntegerField(default=0)

class Team(models.Model):
	name = models.CharField(max_length=50)
	leader = models.ForeignKey('users.User')
	member1 = models.CharField(max_length=100,blank=True,null=True)
	email1 = models.EmailField(max_length=100,blank=True,null=True)
	organisation1 = models.CharField(max_length=100,blank=True,null=True)
	member2 = models.CharField(max_length=100,blank=True,null=True)
	email2 = models.EmailField(max_length=100,blank=True,null=True)
	event = models.ForeignKey('events.Event')	
	judge = models.ForeignKey('events.Judge',related_name='judges',blank=True,null=True)
	mentor = models.ForeignKey('events.Mentor',related_name='mentors',blank=True,null=True)	
	organisation2 = models.CharField(max_length=100,blank=True,null=True)
	confirmed = models.BooleanField()
	selected = models.BooleanField(help_text='Set this if the team has been selected for the next rounds')
	is_judged = models.BooleanField(verbose_name='Has the team been judged?')
	seen = models.BooleanField(help_text='Set this if you have read this team\'s content')
	
	
	def __unicode__(self):
		return self.name

	def get_leader(self):
		return self.leader.name		

	def organisation(self):
		return "%s, %s, %s"%(self.leader.organisation,self.organisation1,self.organisation2) 

	def get_data(self):
		if self.event.category.domain=='arth':
			return ArthData.objects.get(team=self)

	def get_score(self):
		data = self.get_data()

		if self.event.category.domain=='arth':
			return data.score_overview + data.score_product + data.score_management + data.score_market + data.score_financials + data.score_viability + data.score_offering		

class Announcement(models.Model):
	announcement = models.TextField(max_length=200)
	date_added = models.DateTimeField('date of adding')
	event = models.ForeignKey('events.Event')


	

