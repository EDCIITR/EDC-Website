from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class Update(models.Model):
	content = models.TextField(max_length=200)
	contributor = models.CharField(max_length=50)
	date_sub = models.DateTimeField('date submitted')
	link = models.URLField(max_length =200,blank=True,null=True)
		
	def __unicode__(self):
		return "Update: %s\nby %s on %s \n%s\n" % (self.content,self.contributor,self.date_sub,self.link)

class Newsletter(models.Model):
	subject = models.CharField(max_length=100)
	content = RichTextField(max_length=10000,config_name="default",blank=True,null=True)
	test_email = models.EmailField(max_length=100,verbose_name="Test Email ID for Newsletter")
	date_submitted = models.DateTimeField('Date of creation')
