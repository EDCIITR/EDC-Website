from django.conf.urls.defaults import *

# Next two lines are static files fix
from django.views.static import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^',include('home.urls')),
	(r'^about/',include('about.urls')),
	(r'^feedback/',include('feedback.urls')),
	(r'^edc_media/',include('edc_media.urls')),
	(r'^users/',include('users.urls')),
	(r'^resources/',include('resources.urls')),
	(r'^events/',include('events.urls')),
   	(r'^join/',include('recruitments.urls')),
   	(r'^confirm/',include('confirm.urls')),
	(r'^search/', include('haystack.urls')),
   	(r'^ckeditor/', include('ckeditor.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^admin/', include(admin.site.urls)),
    #Static files fix
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
