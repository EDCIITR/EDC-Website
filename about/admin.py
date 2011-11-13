from django.contrib import admin
from about.models import Member

class MemberAdmin(admin.ModelAdmin):
	list_display = ('name','branch','year','phone','email','rank')
	ordering = ('-year',)
	search_fields = ['name','email']
	list_filter = ('year',)
	list_editable = ('email','phone','year','rank')
	actions = ['upgrade',]
	
	def upgrade(self,request,queryset):
		q = Member.objects.all()
		count=0

		for member in q:
			if member.year<4:
				member.year = member.year + 1
				member.save()
				count = count + 1
						
		msg_bit = "%d members were"%count
		self.message_user(request,"%s successfully upgraded" % msg_bit)	
	

admin.site.register(Member,MemberAdmin)

