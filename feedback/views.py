# Create your views here.
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.core.mail import EmailMessage, BadHeaderError
from feedback.forms import FeedbackForm
from constants import *

def index(request):
	form = FeedbackForm()
	msg = None

	if request.method=='POST':	
		form = FeedbackForm(request.POST)		
		
		if form.is_valid():
			name = form.cleaned_data['name']
			email = form.cleaned_data['email']
			feedback = form.cleaned_data['feedback']
			#save to database and email to group
			new_obj = form.save(commit=False)
			new_obj.date_sub = datetime.now()	
			new_obj.save()
			form.save_m2m()	
			subject = '[Website Feedback] Feedback from %s'%(name)
			html_content = 'Hello Team.<br /> Following is a feedback on EDC website from <strong>%s</strong>. Concerned authority should reply to this feedback at <strong>%s</strong> as soon as possible. <br /><br /><span style="border:2px;border-style:solid;width:800px;display:block;"><p style="margin-left:20px;">%s</p></span><hr /><span style="color:grey;">You have received this message because the Website feedbacks have been programmed to be sent automatically to the EDC group. If you do not want to receive feedbacks on group, please hire another python programmer. </span><br /><br />Regards,<br/>Webmaster'%(name,email,feedback)
			from_email = 'feedback@edciitr.com'
			mail = EmailMessage(subject, html_content, "feedback@edciitr.com", ["edciitr@googlegroups.com"])
			mail.content_subtype = "html"  # Main content is now text/html
			mail.send()
			msg = 'Your feedback was recorded successfully. Thanks much! We shall get back to you soon.'

	return render_to_response('feedback/feedback.html',{'name':'Feedback','list':menu,'form':form,'msg':msg},context_instance=RequestContext(request)) 	


