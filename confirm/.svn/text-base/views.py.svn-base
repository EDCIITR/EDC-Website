# Create your views here.
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from constants import *
from datetime import datetime
from recruitments.models import Candidate
from users.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import get_template
from django.template import Context
import cStringIO as StringIO
from sx.pisa3 import pisaDocument
import cgi
import hashlib
import os
import settings
import sys

def fetch_resources(uri, rel):
 """
 Callback to allow pisa/reportlab to retrieve Images,Stylesheets, etc.
 `uri` is the href attribute from the html link element.
 `rel` gives a relative path, but it's not used here.

 """
 #path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
 #path = os.path.join(settings.MEDIA_ROOT,uri)
 path = settings.MEDIA_ROOT + uri.replace(settings.MEDIA_URL,"")
 #print uri
 #print path
 return path


def render_to_pdf(template_src, context_dict,link):
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    #return HttpResponse(html)
    result = StringIO.StringIO()
    pdf = pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")),dest=result,link_callback=fetch_resources)
    #print result.getvalue()   
  
    if not pdf.err:
	c = context_dict['candidate']
	f = open(link ,"wb")
	f.write(result.getvalue())  
     
	    
    #return HttpResponse('We had some errors<pre>%s</pre>' % cgi.escape(html))


def registrations(request,pid,hash_value):
	#raise Http404
	'''
		state=0 -> fail
		state=1 -> success
	'''
	try:
		u = User.objects.get(pk=pid,hash_value=hash_value)
		state=1	
		msg = "Congratulations %s! Confirmation successful."%(u.name)	
		u.blocked = False
		u.hash_value = '0'
		u.save()
	except ObjectDoesNotExist:
		state = 0
		msg= "This confirmation link is invalid"	
	
	return render_to_response('confirm/index.html',{'list':menu,'msg':msg,'state':state},context_instance=RequestContext(request))


def recruitments(request,pid,hash_value):
	try:
		c = Candidate.objects.get(pk=pid,hash_value=hash_value)
		state=1	
		link = '/uploads/recruitments/pdf/' + c.setup.name + '/' + str(c.name).replace(' ','_') + '_' + str(c.pk) + '.pdf'
		link2 = settings.MEDIA_URL+link
		if c.blocked:		
			c.blocked = False
			render_to_pdf('recruitments/pdf_base.html',{'pagesize':'A4','candidate':c,'MEDIA_URL':settings.MEDIA_URL},settings.MEDIA_ROOT + link)
			msg = "Congratulations %s! Confirmation successful. We have received the following <a href='%s'>recruitment application</a>. This application is for official use, though you may download it for reference. If there is any discrepancy in the pdf, please contact the coordinators. "%(c.name,link2)	
			c.save()

		else:
			msg = 'You have already confirmed your interest in EDC recruitment. We have receieved your <a href="%s">application</a>.'%link2
		#return render_to_response('recruitments/pdf_base.html',{'list':menu,'candidate':u},context_instance=RequestContext(request))		
		#create PDF
	except ObjectDoesNotExist:
		state = 0
		msg= "This confirmation link is invalid"	

	return render_to_response('confirm/index.html',{'list':menu,'msg':msg,'state':state},context_instance=RequestContext(request))
