from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from constants import *
from home.models import Update
from events.models import Event
from associates.models import Sponsor
from about.models import Member
from django.core.exceptions import ObjectDoesNotExist

def index(request):
	updates = Update.objects.all().order_by('-date_sub')[0:updates_max]
	events = Event.objects.filter(parent=None).order_by('-date_event')[0:events_max]
	sponsors = Sponsor.objects.filter(main_homepage_display=True)
	return render_to_response('home/index.html',{'name':'Home','list':menu,'updates':updates,'events':events,'sponsors':sponsors},context_instance=RequestContext(request))

def contact(request):
	secy=None
	add_secy= None
	web_masters=None
	try:
		members = Member.objects.all().order_by('-year')
		secy = Member.objects.get(rank=ranks['secy'])
		add_secy = Member.objects.get(rank=ranks['add_secy'])
		web_masters = Member.objects.filter(rank = ranks['web_master'])
	except ObjectDoesNotExist:
		pass

	return render_to_response('contact.html',{'list':menu,'members':members,'secy':secy,'add_secy':add_secy,'web_masters':web_masters},context_instance=RequestContext(request))

def credits(request):
	return render_to_response('credits.html',{'list':menu,'name':'Credits'},context_instance=RequestContext(request))
