from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('evaluation.views',
    url(r'^projects/eval/AA/(?P<AAgraphtype>[a-z]{1})/$', 'evalAA', name="evalAA"),
    url(r'^projects/grapheval/AA/(?P<AAgraphtype>[a-z]{1})/$', 'graphevalAA', name="graphevalAA"),

)
