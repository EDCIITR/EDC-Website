from django.db import models
from constants import *

# Create your models here.
class User(models.Model):
	name = models.CharField(max_length=50)
	email = models.EmailField(max_length=50,unique=True)
	password = models.CharField(max_length=50)
	phone = models.BigIntegerField(max_length=15,blank=True,null=True)
	organisation = models.CharField(max_length=100)
	subscribe = models.BooleanField()
	category = models.IntegerField(choices=USER_CATEGORY_CHOICES)
	date_registration = models.DateTimeField('date of registration')
	hash_value = models.CharField(max_length=100)
	blocked = models.BooleanField()


	def __unicode__(self):
		return self.email
