# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from constants import *
from about.models import Member


def index(request):
	return render_to_response('edc_media/index.html',{'name':'Media','list':menu,},context_instance=RequestContext(request))

