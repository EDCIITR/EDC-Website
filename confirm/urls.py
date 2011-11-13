from django.conf.urls.defaults import *

urlpatterns = patterns('confirm.views',
    (r'registrations/(?P<pid>\d+)/(?P<hash_value>\w+)/$','registrations'),
    (r'^recruitments/(?P<pid>\d+)/(?P<hash_value>\w+)/$','recruitments'),
)
