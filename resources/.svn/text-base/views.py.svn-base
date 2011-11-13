# Create your views here.
# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from constants import *
from datetime import datetime
from resources.models import Mentor,MentorMail
from resources.forms import MentorMailForm
from users.models import User
from datetime import datetime, timedelta
from django.core.mail import send_mail, EmailMessage


def index(request):
	return render_to_response('resources/index.html',{'name':'Resources','list':menu},context_instance=RequestContext(request))
 
def mentors(request,mentor_id=None):
	form = None
	date_last_sent = None
	hours = 50
	msg = None

	if not mentor_id:
		mentors = Mentor.objects.all()	
		return render_to_response('resources/mentors/index.html',{'list':menu,'mentors':mentors},context_instance=RequestContext(request))
	else:
		try:
			if request.session['session_id']:			
				user = get_object_or_404(User,email=request.session['session_id'])
				mentor = get_object_or_404(Mentor,pk=mentor_id)
				sent_mail = MentorMail.objects.filter(user=user,mentor=mentor).order_by('-date_sending')

				if sent_mail:				
					date_last_sent =sent_mail[0].date_sending
					dif = datetime.now() - date_last_sent
					hours = dif.days*24 + dif.seconds/3600						
									#return HttpResponse(hours)

				if request.method=='POST':
					if hours>48:
						form = MentorMailForm(request.POST)
						if form.is_valid():
							obj = MentorMail(user_id=user.id,mentor_id=mentor.id,subject=form.cleaned_data['subject'],content=form.cleaned_data['content'],date_sending=datetime.now())
							html_content = 'Hello <strong>%s</strong>. Hope this mail finds you in great health. Following is a message sent by %s,<p>%s</p> <br />You have recieved this mail from the EDC portal because you have associated with EDC IITR as a mentor. If you do not wish to receive any such mails from EDC IITR, please click here.'%(mentor.name,user.name,obj.content)
							from_email = request.session['session_id']
							email = EmailMessage(obj.subject, html_content, from_email, [mentor.email])
							email.content_subtype = 'html'  # Main content is now text/html
							email.send()
							obj.save()
							hours = 0
							date_last_sent = datetime.now()
							msg = 'Your message was sent successfully'
				else:
					mentor = get_object_or_404(Mentor, pk=mentor_id)
				
					if not mentor.email_public:
						form = MentorMailForm()							
					
				return render_to_response('resources/mentors/profile.html',{'list':menu,'mentor':mentor,'form':form,'hours':hours,'date_last_sent':date_last_sent,'time_left':48-hours,'msg':msg}, context_instance=RequestContext(request))

		except KeyError:
			pass
		
	return HttpResponseRedirect('/users/login?next=%s'%request.path)	


