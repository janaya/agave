from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
#    url(r'^doc/$', 'django.views.generic.simple.direct_to_template', {'template': 'api_graphs.html'}),
#    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),

)

urlpatterns += patterns('agave.views',
#    url(r'^json/(?P<db>\w+)/(?P<graphtype>[A,C]{2})/(?P<graphsubtype>[a-z,1,2]{1})/$', 
#                                                    'graph_json', name="graph_json"),
#    url(r'^graph/(?P<db>\w+)/(?P<graphtype>[A,C]{2})/(?P<graphsubtype>[a-z,1,2]{1})/$', 
#                                                    'graph_graph', name="graph_graph"),
#    url(r'^graph/(?P<db>\w+)/(?P<graphtype>[A,C]{2})/(?P<graphsubtype>[a-z,1,2]{1})/actor/(?P<actor_id>\w+)/$',
#                                            'graph_graph', name="graph_graph"),
#    url(r'^graph/(?P<db>\w+)/(?P<graphtype>[A,C]{2})/(?P<graphsubtype>[a-z,1,2]{1})/concept/(?P<actor_id>\w+)/$',
#                                            'graph_graph', name="graph_graph"),


    url(r'^graph/(?P<db>\w+)/(?P<graphtype>[A,C]{2})/(?P<graphsubtype>[a-z,1,2]{1})/actor/(?P<actor_id>\w+)/$',
                                            'graph_visualization', name="graph_visualization"),
    url(r'^graphv/(?P<db>\w+)/(?P<graphtype>[A,C]{2})/(?P<graphsubtype>[a-z,1,2]{1})/concept/(?P<actor_id>\w+)/$',
                                            'graph_visualization', name="graph_visualization"),
                                            
    url(r'^projects/search/$', 'search', name="search"),
    url(r'^projects/concepts/$', 'autocomplete_concepts', name='autocomplete_concepts'),
    url(r'^projects/names/$', 'autocomplete_names', name='autocomplete_names'),
    url(r'^projects/ac_concept/$', 'ac_concept', name="ac_concept"),
    url(r'^projects/aab_concept/$', 'aab_concept', name="aab_concept"),
    url(r'^projects/aan_concept/$', 'aan_concept', name="aan_concept"),
    url(r'^projects/actors_broaders_concept_image/$',
        'actors_broaders_concept_image', name="actors_broaders_concept_image"),

#    url(r'^projects/eval/AA/(?P<AAgraphtype>[a-z]{1})/$', 'evalAA', name="evalAA"),
#    url(r'^projects/grapheval/AA/(?P<AAgraphtype>[a-z]{1})/$', 'graphevalAA', name="graphevalAA"),

)

"""
    Other possible url regex
    
    url(r'^concepts/$', ),
    url(r'^concepts/<?concept>/$', ),
    
    url(r'^concepts/<?concept>/actors/$', ),
    
    url(r'^concepts/<?concept>/broaders/$', ),
    url(r'^concepts/<?concept>/broaders/<?concept>/actors/$', ),
    
    url(r'^concepts/<?concept>/narrowers/$', ),
    url(r'^concepts/<?concept>/narrowers/<?concept>/actors/$', ),
    
    url(r'^concepts/<?concept>/broaders/<?concept>/narrowers/$', ),
    url(r'^concepts/<?concept>/broaders/<?concept>/narrowers/<?concept>/actors/$', ),
    
    url(r'^concepts/<?concept>/narrowers/<?concept>/broaders/$', ),
    url(r'^concepts/<?concept>/narrowers/<?concept>/broaders/<?concept>/actors/$', ),
    
    url(r'^actors/$', ),
    url(r'^actors/<?actor>/$', ),
    
    url(r'^actors/<?actor>/concepts/$', ),
    url(r'^actors/<?actor>/concepts/<?concept>/$', ),
    
    url(r'^actors/<?actor>/concepts/<?concept>/broaders/$', ),
    url(r'^actors/<?actor>/concepts/<?concept>/broaders/<?concept>/actors/$', ),
    
    url(r'^actors/<?actor>/concepts/<?concept>/narrowers/$', ),
    url(r'^actors/<?actor>/concepts/<?concept>/narrowers/<?concept>/actors/$', ),
    
    url(r'^actors/<?actor>/concepts/<?concept>/broaders/<?concept>/narrowers/$', ),
    url(r'^actors/<?actor>/concepts/<?concept>/broaders/<?concept>/narrowers/<?concept>/actors/$', ),
    
    url(r'^actors/<?actor>/concepts/<?concept>/narrowers/<?concept>/broaders/$', ),
    url(r'^actors/<?actor>/concepts/<?concept>/narrowers/<?concept>/broaders/<?concept>/actors/$', ),
"""
