from django.conf.urls.defaults import *

urlpatterns = patterns('users.views',
    (r'^register/$','register'),
    (r'^login/$','login'),
    (r'^logout/$','logout'),
    (r'^edit/$','edit'),
    (r'^change_password/$','change_password'),
    (r'^forgot_password/$','forgot_password'),
    (r'^judge/$','judge'),
    (r'^judge/(?P<domain>\w+)/(?P<num>\d+)/$','show_teams'),
    (r'^judge/(?P<domain>\w+)/(?P<num>\d+)/(?P<index>\d+)/$','show_entry'),
)
