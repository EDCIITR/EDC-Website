from django.contrib import admin
from resources.models import Mentor, MentorMail, Startup, Job, Application
from users.models import User

class MentorAdmin(admin.ModelAdmin):
	list_display = ('name','organisation','email','phone','date_joining')
	ordering = ('-date_joining',)

class MentorMailAdmin(admin.ModelAdmin):
	list_display = ('user','mentor','subject','date_sending')
	ordering = ('-date_sending',)

class StartupAdmin(admin.ModelAdmin):
    list_display = ('startup_name','user')

class JobAdmin(admin.ModelAdmin):
    list_display = ('position', 'startup')

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'job')

admin.site.register(Mentor, MentorAdmin)
admin.site.register(MentorMail, MentorMailAdmin)
admin.site.register(Startup, StartupAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Application, ApplicationAdmin)
