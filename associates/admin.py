from django.contrib import admin
from associates.models import Sponsor

class SponsorAdmin(admin.ModelAdmin):
	list_display = ('name','title','main_homepage_display','event_homepage_display','event')
	list_editable = ('main_homepage_display','event_homepage_display',)
	search_fields = ['name']
	
admin.site.register(Sponsor,SponsorAdmin)

