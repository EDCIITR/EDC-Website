from django.conf.urls.defaults import *

urlpatterns = patterns('about.views',
    (r'^$','index'),
    (r'^team/$','team'),
)
