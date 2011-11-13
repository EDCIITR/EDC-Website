from django.contrib import admin
from users.models import User

class UserAdmin(admin.ModelAdmin):
	list_display = ('name','email','phone','organisation','date_registration','subscribe','blocked','category')
	ordering = ('-date_registration',)
	search_fields = ['name','email']
	list_filter = ('category','blocked','subscribe',)
	
admin.site.register(User,UserAdmin)

