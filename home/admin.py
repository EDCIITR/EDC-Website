from django.contrib import admin
from home.models import *
from users.models import User
from django import forms
from datetime import datetime
from django.core.mail import EmailMessage, BadHeaderError

class NewsletterAdminForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
        	super(NewsletterAdminForm, self).__init__(*args, **kwargs)
		#self.fields['name'].help_text = '%d candidates have registered'%(len(  		
		#Init code here
		date_submitted = datetime.now()

class UpdateAdmin(admin.ModelAdmin):
	list_display = ('content','date_sub','contributor','link',)
	ordering = ('-date_sub',)

class NewsletterAdmin(admin.ModelAdmin):
	list_display = ('subject','date_submitted')
	ordering = ('-date_submitted',)
	actions = ['test_mailer','all_mailer']	

	#Test mailer function
	def test_mailer(self,request,queryset):
		#Test Mail
		if len(queryset)>1:
			self.message_user(request,"You cannot select more than one newsletters for any mailer operation including testing. Remember, sending mails to people is a very sensitive operation")	
		else:
			newsletter = list(queryset)[0]		
			sub = newsletter.subject
			content = newsletter.content
			subject = '[EDC IITR Newsletter] %s'%(sub)
			html_content = content + "<hr /><span style='color:grey; font-size:12px;'>This is an automatically generated e-mail message. Please do not reply to this email. You have received this e-mail because you have subscribed to EDC IITR newsletters. If you do not wish to receive our updates and information anymore, please <a href='http://www.edciitr.com/users/edit' target='_blank'>edit your profile</a></span>."
			from_email = 'newsletter@edciitr.com'
			html_content = html_content.replace('/media/','http://www.edciitr.com/media/')
			mail = EmailMessage(subject, html_content, from_email, [newsletter.test_email])
			mail.content_subtype = "html"  # Main content is now text/html
			mail.send()
			self.message_user(request,"Test Mail sent successfully. You may check the test inbox and proceed with mailing all subscribers if you are satisfied")	

	def all_mailer(self,request,queryset):
		#Test Mail
		if len(queryset)>1:
			self.message_user(request,"You cannot select more than one newsletters for any mailer operation including testing. Remember, sending mails to people is a very sensitive operation")	
		else:
			newsletter = list(queryset)[0]		
			sub = newsletter.subject
			content = newsletter.content
			subject = '[EDC IITR Newsletter] %s'%(sub)
			html_content = content + "<hr /><span style='color:grey; font-size:12px;'>This is an automatically generated e-mail message. Please do not reply to this email. You have received this e-mail because you have subscribed to EDC IITR newsletters. If you do not wish to receive our updates and information anymore, please <a href='http://www.edciitr.com/users/edit' target='_blank'>unsubscribe</a></span>."
			html_content = content + "<hr /><span style='color:grey; font-size:12px;'>This is an automatically generated e-mail message. Please do not reply to this email. You have received this e-mail because you have subscribed to EDC IITR newsletters. If you do not wish to receive our updates and information anymore, please <a href='http://www.edciitr.com/users/edit' target='_blank'>unsubscribe</a></span>."
			html_content = html_content.replace('/media/','http://www.edciitr.com/media/')

			for user in User.objects.filter(subscribe=True,blocked=False):
				from_email = 'newsletter@edciitr.com'
				mail = EmailMessage(subject, html_content, from_email, [user.email])
				mail.content_subtype = "html"  # Main content is now text/html
				mail.send()
				self.message_user(request,"All subscribers were mailed successfully")	

admin.site.register(Update,UpdateAdmin)
admin.site.register(Newsletter,NewsletterAdmin)

