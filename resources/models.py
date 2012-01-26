from django.db import models
from users.models import User
from datetime import datetime


# Create your models here.
class Mentor(models.Model):
	name = models.CharField(max_length=100)
	organisation = models.CharField(max_length=50)
	about = models.TextField(max_length=500,blank=True,null=True)
	interests = models.TextField(max_length=500,blank=True,null=True)
	pic = models.ImageField(upload_to='mentor_pics',blank=True,null=True)
	email = models.EmailField(max_length=50,unique=True)
	email_public = models.BooleanField()
	phone = models.BigIntegerField(max_length=15,blank=True,null=True)
	phone_public = models.BooleanField()
	linked_in = models.URLField(blank=True,null=True)
	linked_in_public = models.BooleanField()
	date_joining = models.DateTimeField('date of joining')
	
	def __unicode__(self):
		return "%s"%self.name

class MentorMail(models.Model):
	user = models.ForeignKey('users.User')
	mentor = models.ForeignKey('resources.Mentor')
	subject = models.CharField(max_length=50)
	content = models.TextField(max_length=1000)
	date_sending = models.DateTimeField('date of sending')
		
	def __unicode__(self):
		return "From %s to %s, about %s" % (self.user.name,self.mentor.name,self.subject)

class Startup(models.Model):
    user = models.ForeignKey('users.User')
    startup_name = models.CharField('Startup Name*', max_length=100)
    description  = models.TextField('Startup Description*', max_length=500)
    region = models.CharField('Geographical Region*', max_length=100)
    logo = models.ImageField('Startup Logo',
          upload_to='uploads/startup_pics',blank=True,null=True)
    website = models.URLField('Website', blank=True,null=True)
    iitr_startup = models.BooleanField('Is your startup in IITR ?')
    
    def __unicode__(self):
        return "%s" % self.startup_name
class Job(models.Model):
    startup = models.ForeignKey('resources.Startup')
    position = models.CharField('Position*', max_length=100)
    requirements = models.TextField('Requirements', max_length=1000,blank=True,null=True)
    duration = models.CharField('Duration of Work', max_length=100,blank=True,null=True)
    salary = models.CharField('Approximate Salary', max_length=100,
            blank=True, null=True)
    details = models.TextField('More details', max_length=1000,
            blank=True, null=True)
    applicants = models.ManyToManyField(User, through='Application')

    def __unicode__(self):
        return "%s : Position %s" % (self.startup, self.position)

class Application(models.Model):
    user = models.ForeignKey('users.User')
    skills = models.CharField('Skills', max_length=200)
    job = models.ForeignKey('resources.Job')
    status = models.CharField('Status', max_length=100) #define categories
    message = models.TextField('Cover Letter')
    linked_in = models.URLField()
    date_applied = models.DateTimeField('Date Applied', default=datetime.now())

    def __unicode__(self):
        return '%s applied at %s' % (self.user, self.job)
