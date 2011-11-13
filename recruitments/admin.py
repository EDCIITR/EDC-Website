from django.contrib import admin
from recruitments.models import *
from django import forms
import os
import settings
from django.core.mail import EmailMessage, BadHeaderError
import cStringIO as StringIO
from sx.pisa3 import pisaDocument
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import get_template
from django.template import Context
import tarfile

def render_to_pdf(template_src, context_dict):
    
    print result.getvalue()	 
    #print result.getvalue()   


class SetupAdminForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
        	super(SetupAdminForm, self).__init__(*args, **kwargs)
		#self.fields['name'].help_text = '%d candidates have registered'%(len(  		
		#Init code here
	
	def clean(self):
		super(SetupAdminForm, self)
		try:
			cleaned_data = self.cleaned_data
			s = Setup.objects.get(date_recruitment_starts__lt=datetime.now(),date_recruitment_ends__gt=datetime.now())	
			#print cleaned_data	
			if not cleaned_data['name']==s.name and is_overlap(s.date_recruitment_starts,s.date_recruitment_ends,cleaned_data['date_recruitment_starts'],cleaned_data['date_recruitment_ends']):
				raise forms.ValidationError('Recruitments are already happening in this date range called %s'%s.name)				
		except ObjectDoesNotExist:	
			pass
		except KeyError:
			raise forms.ValidationError('You missed some mandatory parameter')

		return cleaned_data
	
	

class CandidateAdmin(admin.ModelAdmin):
	list_display = ('name','salutation','branch','email','slot','blocked','setup',)
	search_fields = ['salutation',]
	list_filter = ('salutation','setup','blocked')
	list_editable = ('slot',)	
	#date_hierarchy = 'setup.date_recruitment_starts'
		
class SetupAdmin(admin.ModelAdmin):
	form = SetupAdminForm	
	list_display = ('name','year','date_recruitment_starts','date_recruitment_ends')
	ordering = ('-date_recruitment_starts',)
	actions = ['test_mailer','all_mailer','generate_slot_pdf','generate_candidate_zip']	
	def save_model(self, request, obj, form, change):
		try:		
			os.mkdir(settings.MEDIA_ROOT + '/uploads/recruitments/pdf/' + obj.name)
			#please write the code for recursively copying directory structure to new folder		
			#or prevent change of codename		
		except OSError:
			pass		
		obj.save()

	#Test mailer function
	def test_mailer(self,request,queryset):
		#Test Mail
		if len(queryset)>1:
			self.message_user(request,"You cannot select more than one setup for any mailer operation including testing. Remember, sending mails to people is a very sensitive operation")	
		else:
			setup = list(queryset)[0]		
			subject = '[EDC IITR] Recruitment(%s) Test Mailer'%(setup.name)
			html_content = 'Dear Candidate,<br/>Thanks for your interest in EDC Recruitments. Your slot number is x <br /><hr />%s'%setup.mailer			
			from_email = 'noreply@edciitr.com'
			mail = EmailMessage(subject, html_content, from_email, [setup.test_email])
			mail.content_subtype = "html"  # Main content is now text/html
			mail.send()
			self.message_user(request,"Test Mail sent successfully. You may check the test inbox and proceed with mailing all candidates if you are satisfied")	
	
	#All mailer function	
	def all_mailer(self,request,queryset):
		#Main Mail
		if len(queryset)>1:
			self.message_user(request,"Dude, weak! You cannot select more than one setup for mailer operations")	
		else:
			setup = list(queryset)[0]		
			c = Candidate.objects.filter(setup=setup,slot=None)
			if c: #Candidates with no slot exist
				self.message_user(request,"Dude, weak! You cannot mail the candidates since there are still candidates who have not been assigned any slot. Please check the candidates table")
			else: #All set. Ready to mail
				subject = '[EDC IITR] Recruitment Details'
				content = setup.mailer
				candidates = Candidate.objects.filter(setup=setup)		
				html_content = None
				mail=None
				from_email='noreply@edciitr.com'
	
				for candidate in candidates:
					html_content = 'Dear %s,<br/>Thanks for your interest in EDC Recruitments. Your slot number is  %d.,<br /><hr />%s'%(candidate.name,candidate.slot,content)			
					mail = EmailMessage(subject, html_content, from_email, [candidate.email])
					mail.content_subtype = "html"  # Main content is now text/html
					mail.send()
			
			#Test mail			
				mail = EmailMessage(subject, html_content, from_email, [setup.test_email])
				mail.content_subtype = "html"  # Main content is now text/html
				mail.send()
						
				self.message_user(request,"%d mails were sent successfully. A mail has also been sent to the test address"%len(candidates))

	#Generate PDF function
	def generate_slot_pdf(self,request,queryset):
		if len(queryset)>1:
			self.message_user(request,"Dude, weak! You cannot select more than one setup for generating PDFs")	
		else:
			setup = list(queryset)[0]		
			c = Candidate.objects.filter(setup=setup,slot=None)
			if c: #Candidates with no slot exist
				self.message_user(request,"Dude, weak! You cannot generate the PDF until all candidates are given slots. Please check the candidate table again. ")
			else: #All set. Ready to generate PDF
				num_slots=0			
				for candidate in Candidate.objects.filter(setup=setup):
					if candidate.slot>num_slots:
						num_slots=candidate.slot
				
				slots = [[] for x in range(0,num_slots)]	
				
				for candidate in Candidate.objects.filter(setup=setup):
					slots[int(candidate.slot)-1].append(candidate)					
	
				template = get_template("recruitments/slots_pdf_base.html")
				context = Context({'setup':setup,'slots':slots,'pagesize':'A4'})
				html = template.render(context)
				result = StringIO.StringIO()
				pdf = pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")),dest=result)
				
				#if not pdf.error:
				link = settings.MEDIA_ROOT + '/uploads/recruitments/slots.pdf'
				f = open(link ,"wb")
				f.write(result.getvalue())  
     				#return HttpResponse(result.getvalue(),mimetype='application/pdf')
   				
				self.message_user(request,"The PDF was generated successfully")	
	
		
	def generate_candidate_zip(self,request,queryset):
		#Generate tar file for all files in the folder
		if len(queryset)>1:
			self.message_user(request,"You cannot select more than one setup for generating candidate PDFs")	
		else:
			setup = list(queryset)[0]		
			t = tarfile.open(settings.MEDIA_ROOT + '/uploads/recruitments/pdf.tar.gz','w:gz')
			t.add(settings.MEDIA_ROOT + '/uploads/recruitments/pdf/'+setup.name + '/',recursive=True)
			t.close()			
			self.message_user(request,"The Candidate PDF Zip  was generated successfully")	
	
	test_mailer.short_description = "Test  Mailer"
	all_mailer.short_description="Send mailer to all candidates"	
	generate_slot_pdf.short_description = "Generate Slot PDFs"
	generate_candidate_zip.short_description = "Generate Candidate PDFs"
	
admin.site.register(Setup,SetupAdmin)
admin.site.register(Candidate,CandidateAdmin)


