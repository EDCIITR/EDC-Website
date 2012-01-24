from django.conf.urls.defaults import *

urlpatterns = patterns('resources.views',
    url(r'^$','index'),
    url(r'^mentors/$','mentors'),
    url(r'^mentors/(?P<mentor_id>\d+)/$','mentors'),
    url(r'^jobs/register_startup/$','register_startup', name='register-startup'),
    url(r'^jobs/register_job/','register_jobs', name='register-job'),   
    url(r'^jobs/startups/$','jobs'),
    url(r'^jobs/startups/(?P<startup_id>\d+)/$','jobs'),
)
