from django.contrib import admin
from resources.models import Mentor, MentorMail
from users.models import User

class MentorAdmin(admin.ModelAdmin):
	list_display = ('name','organisation','email','phone','date_joining')
	ordering = ('-date_joining',)

class MentorMailAdmin(admin.ModelAdmin):
	list_display = ('user','mentor','subject','date_sending')
	ordering = ('-date_sending',)

admin.site.register(Mentor,MentorAdmin)
admin.site.register(MentorMail,MentorMailAdmin)


