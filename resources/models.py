from django.db import models
from users.models import User

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
		return "From %s to %s, about %s"%(self.user.name,self.mentor.name,self.subject)

