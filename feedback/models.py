from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class Feedback(models.Model):
	name = models.CharField(max_length=50)
	email = models.EmailField(max_length=50)
	feedback = models.TextField(max_length=1000)
	date_sub = models.DateTimeField('date submitted')
	
