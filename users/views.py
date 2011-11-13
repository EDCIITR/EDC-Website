# Create your views here.
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.mail import EmailMessage, BadHeaderError
from constants import *
from users.models import User
from events.models import Judge, Event,Team
from users.forms import RegistrationForm, LoginForm, EditForm, ChangePasswordForm, ForgotPasswordForm
from datetime import datetime
from events.views import get_event
from events.forms import ArthJudgeForm
import hashlib


def set_session(request,user):
	cat = None
	request.session['session_id'] = user.email
	request.session['name'] = user.name
	if user.category==USER_JUDGE:
		cat = 'JUDGE'
	elif user.category==USER_MEMBER:		
		cat = 'MEMBER'
	request.session['category']=cat
	request.session.set_expiry(108000) #Expiry time					


#Register user
def register(request):
	cust_errors = []
	if request.method=='POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			password = form.cleaned_data['password']
			password2 = form.cleaned_data['password2']
			mail = form.cleaned_data['email']
			check_list = User.objects.filter(email=mail)			

			if password==password2:
				if not check_list:		
					cat = None		
					name = form.cleaned_data['name']
					organisation = form.cleaned_data['organisation']
					phone = form.cleaned_data['phone']
					subscribe = form.cleaned_data['subscribe']	
					today = datetime.now()
					hash_value = str(hashlib.sha1(mail).hexdigest())[:20]
					u = User(name=name,email=mail,password=password,phone=phone,organisation=organisation,subscribe=subscribe,blocked=True,hash_value=hash_value,date_registration=today,category=USER_MEMBER)			
					u.save()
					link = "http://www.edciitr.com/confirm/registrations/%s/%s/"%(u.pk,u.hash_value)
					subject = '[EDC IITR] Confirm recruitment registration'
					html_content = 'Hi <strong>%s,</strong><br />. Please click <a href="%s">this link</a> to confirm your EDC IITR registration.  <br /><br />Regards,<br/>Team EDC'%(name,link)
					from_email = 'noreply@edciitr.com'
					email = EmailMessage(subject, html_content, from_email, [mail])
					email.content_subtype = "html"  # Main content is now text/html
					email.send()

					#set_session(request,u)
					return render_to_response('users/thanks.html',{'name':'Thanks','list':menu,'name':name,'email':mail,},context_instance=RequestContext(request)) 	
	
			if password!=password2:
				cust_errors.append('Passwords do not match')
			if check_list:
				cust_errors.append('This email has already been registered')

	else:
		form = RegistrationForm()

	return render_to_response('users/register.html',{'name':'Register','list':menu,'form':form,'cust_errors':cust_errors,},context_instance=RequestContext(request)) 	

#Login
def login(request):
	msg = None
	if request.method=='POST':	
		form = LoginForm(request.POST)
		if form.is_valid():
			mail = form.cleaned_data['email']
			password = form.cleaned_data['password']
			u = User.objects.filter(email=mail)
			
			if not u:
				msg = 'This email ID has not been registered'
			else:
				u = u[0]				
				if u.password!=password:
					msg = 'Password does not match'
				else:
					if u.blocked:
						msg = 'You have already registered but not confirmed yet'					
					else:					
						set_session(request,u)
						return HttpResponseRedirect(request.GET.get('next','/'))	
	else:
		form = LoginForm()
		
	return render_to_response('users/login.html',{'name':'Login','list':menu,'form':form,'msg':msg,},context_instance=RequestContext(request))


#Logout
def logout(request):
    try:
        del request.session['session_id']
	del request.session['name']
	request.session.flush()    	
    except KeyError:
        pass
    return HttpResponseRedirect(request.GET.get('next','/'))
	

#Edit Profile
def edit(request):
	msg = None
	success = None
	try:
		if request.method=='POST':
			form = EditForm(request.POST)
			u = User.objects.filter(email=request.session['session_id'])[0]

			if form.is_valid():
				u.name = form.cleaned_data['name']
				u.phone = form.cleaned_data['phone']
				u.organisation = form.cleaned_data['organisation']
				u.subscribe = form.cleaned_data['subscribe']
				u.save()
				request.session['name'] = u.name
				msg = 'Your changes were saved successfully'
				success=1
			else:
				msg = 'There are errors in the form'				
				success=0
		else:
			u = User.objects.filter(email=request.session['session_id'])[0]
			form = EditForm({'name':u.name,'phone':u.phone,'organisation':u.organisation,'subscribe':u.subscribe})

		return render_to_response('users/edit.html',{'name':'Edit','list':menu,'form':form,'msg':msg,'success':success},context_instance=RequestContext(request))
	except KeyError:
		form = LoginForm()
		next = '/users/edit'
		return HttpResponseRedirect('/users/login/?next=%s'%next)		



#Change password
def change_password(request):
	msg = None
	success=None
	try:
		if request.method=='POST':
			form = ChangePasswordForm(request.POST)	

			if form.is_valid():
				u = User.objects.filter(email=request.session['session_id'])[0]
				cur_password = form.cleaned_data['cur_password']

				if cur_password==u.password:
					password1 = form.cleaned_data['new_password']
					password2 = form.cleaned_data['new_password2']
				
					if password1==password2:
						u.password = password1
						u.save()
						msg = 'Your password was changed successfully'
						success=1		
					else:
						msg = 'The new passwords do not match'
						success=0
				else:
					msg = 'You entered a wrong password'
					success=0								
		else:
			form =  ChangePasswordForm()
			
		return render_to_response('users/change_password.html',{'name':'Edit','list':menu,'form':form,'msg':msg,'success':success},context_instance=RequestContext(request))
	except KeyError:
		form = LoginForm()
		next = '/users/change_password/'
		return HttpResponseRedirect('/users/login/?next=%s'%next)	

#Forgot password
def forgot_password(request):
	msg = None
	success=None

	if request.method=='POST':
		form = ForgotPasswordForm(request.POST)	
		
		if form.is_valid():
			mail = form.cleaned_data['email']
			u = User.objects.filter(email=mail)
				
			if u:
				u = u[0]
				subject = 'Forgot Password (EDC IITR)'
				html_content = 'Hi <strong>%s,</strong><br />. Your account password is %s <br />Regards,<br/>Team EDC'%(u.name,u.password)
				from_email = 'noreply@edciitr.com'
				email = EmailMessage(subject, html_content, from_email, [mail])
				email.content_subtype = "html"  # Main content is now text/html
				email.send()
				msg = 'Your password has been emailed to you'
				success=1
			else:
				msg = 'This Email ID has not been registered'		
				success=0	
	else:
		form =  ForgotPasswordForm()
			
	return render_to_response('users/forgot_password.html',{'name':'Edit','list':menu,'form':form,'msg':msg,'success':success},context_instance=RequestContext(request))
	

#judge
def judge(request):
	try:
		judge = Judge.objects.get(email=request.session['session_id']) 	
	except KeyError:
		return HttpResponseRedirect('/users/login/?next=%s'%request.path)
	except ObjectDoesNotExist:
		raise Http404

	events = judge.event_set.filter(date_result__gte=datetime.now())
	
	return render_to_response('users/judge/index.html',{'list':menu,'events':events,'judge':judge},context_instance=RequestContext(request))

def show_teams(request,domain,num):
	event = get_event(domain,num)
	
	try:
		judge = get_object_or_404(Judge,email=request.session['session_id'])
	except KeyError:
		return HttpResponseRedirect('/users/login/?next=%s'%request.path)		
	
	teams = Team.objects.filter(event=event,judge=judge)
	
	if event.category.domain=='arth':
		return render_to_response('users/judge/arth_teams.html',{'list':menu,'teams':teams,'judge':judge},context_instance=RequestContext(request))

	raise Http404

def show_entry(request,domain,num,index):
	event = get_event(domain,num)
	back = '/users/judge/' + event.get_link()
	msg = None
	success=None

	try:
		judge = get_object_or_404(Judge,email=request.session['session_id'])
	except KeyError:
		return HttpResponseRedirect('/users/login/?next=%s'%request.path)		
	
	team = get_object_or_404(Team,pk=index)
	
	if team.judge!=judge:
		raise Http404
	
	if event.category.domain=='arth':
		data = team.get_data()	
		form = ArthJudgeForm()
				
		if data:
			form = ArthJudgeForm(instance=data)
	
		if request.method=='POST':
			form = ArthJudgeForm(request.POST)
			
			if form.is_valid():		
				team.is_judged=True
				team.save()				
				form = ArthJudgeForm(request.POST,instance=data)
				form.save()	
				success=1
				msg = 'Changes were saved successfully'		
			else:
				success=0
				msg = 'Please ensure all scores are integers from 0 to 10'

		return render_to_response('users/judge/arth_entry.html',{'list':menu,'back':back,'team':team,'success':success,'msg':msg,'data':data,'form':form},context_instance=RequestContext(request))

	return HttpResponse()

