from django.conf.urls.defaults import *

urlpatterns = patterns('resources.views',
    (r'^$','index'),
    (r'^mentors/$','mentors'),
    (r'^mentors/(?P<mentor_id>\d+)/$','mentors'),
    (r'^careers/register/$','register'),
)
