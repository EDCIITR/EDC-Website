# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from constants import *
from about.models import Member
from home.views import contact

def index(request):
	return render_to_response('about/index.html',{'name':'About','list':menu,},context_instance=RequestContext(request))

def team(request):
	return contact(request)	
