from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'', include('agave.urls')),

#    (r'^doc/$', 'django.views.generic.simple.direct_to_template', {'template': 'docs/_build/html/index.html'}),


    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

#    (r'^site_media/static/(?P<path>.*)$', 'django.views.static.serve',
#    {'document_root': settings.STATIC_ROOT}),
    (r'^site_media/(.*)$', 'django.views.static.serve',
    {'document_root': settings.MEDIA_ROOT}),

#    (r'admin/initial$', graphs.views.generate_initial_graph, name="generate-initial-graph"),
    (r'^rest/', include('rest.urls')),

)
