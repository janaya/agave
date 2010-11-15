from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication
#from piston.authentication import  HttpBasicSimple
#from piston.doc import documentation_view

from rest.handlers import *


auth = HttpBasicAuthentication(realm='TestApplication')

#SIMPLE_USERS = (('duy', 'duy'),)
#AUTHENTICATORS = [auth,]
#[AUTHENTICATORS.append(HttpBasicSimple(realm='Test', 
#                            username=username, password=password)) 
#                            for username, password in SIMPLE_USERS]
#actor_handler = Resource(handler=ActorHandler, authentication=AUTHENTICATORS)

actor_handler = Resource(handler=ActorHandler, authentication=auth)
#actor_handler = Resource(handler=AnonymousActorHandler)
concept_handler = Resource(handler=ConceptHandler, authentication=auth)
instance_handler = Resource(handler=InstanceHandler, authentication=auth)
instance_actor_handler = Resource(handler=InstanceActorHandler, authentication=auth)
instance_concept_handler = Resource(handler=InstanceConceptHandler, authentication=auth)

graphs_json_handler = Resource(handler=GraphsJsonHandler, authentication=auth)
#graphs_handler = Resource(handler=GraphsHandler, authentication=auth)
graphs_json_C_handler = Resource(handler=GraphsJsonCHandler, authentication=auth)

#
#graphs_js_handler = Resource(handler=GraphsJsHandler, authentication=auth)
##graphs_handler = Resource(handler=GraphsHandler, authentication=auth)
#graphs_js_C_handler = Resource(handler=GraphsJsCHandler, authentication=auth)

urlpatterns = patterns('',
#    url(r'^actor/$', actor_handler),
#    url(r'^actor/(?P<actor_id>\d+)/$', actor_handler, name='actors'),
#    url(r'^concept/$', concept_handler),
#    url(r'^concept/(?P<concept_id>\d+)/$', concept_handler, name='concepts'),
#    url(r'^instance/$', instance_handler),
#    url(r'^instance/(?P<instance_id>\d+)/$', instance_handler, name="instances"),
#    url(r'^instance/(?P<instance_id>\d+)/concept/$', instance_concept_handler),
#    url(r'^instance/(?P<instance_id>\d+)/concept/(?P<concept_id>\d+)/$', instance_concept_handler, name="instance_concepts"),
#    url(r'^instance/(?P<instance_id>\d+)/actor/$', instance_actor_handler),
#    url(r'^instance/(?P<instance_id>\d+)/actor/(?P<actor_id>\d+)/$', instance_actor_handler, name="instance_actors"),

    url(r'^(?P<db>\w+)/actor/$', actor_handler),
    url(r'^(?P<db>\w+)/actor/(?P<actor_id>\d+)/$', actor_handler,
                                                    name='actors'),
    url(r'^(?P<db>\w+)/concept/$', concept_handler),
    url(r'^(?P<db>\w+)/concept/(?P<concept_id>\d+)/$', concept_handler, name='concepts'),
    url(r'^(?P<db>\w+)/instance/$', instance_handler),
    url(r'^(?P<db>\w+)/instance/(?P<instance_id>\d+)/$', instance_handler
                                                            , name="instances"),
    url(r'^(?P<db>\w+)/instance/(?P<instance_id>\d+)/concept/$',
                            instance_concept_handler, name="instance_concepts"),
    url(r'^(?P<db>\w+)/instance/(?P<instance_id>\d+)/concept/(?P<concept_id>\d+)/$',
                            instance_concept_handler, name="instance_concepts"),
    url(r'^(?P<db>\w+)/instance/(?P<instance_id>\d+)/actor/$',
                            instance_actor_handler, name="instance_actors"),
    url(r'^(?P<db>\w+)/instance/(?P<instance_id>\d+)/actor/(?P<actor_id>\d+)/$',
                            instance_actor_handler, name="instance_actors"),
#    url(r'^json/(?P<db>\w+)/(?P<graphtype>[A,C]{2})/(?P<graphsubtype>[a-z,1,2]{1})/$',
#                            graphs_json_handler, name="graphs_json_handler"),
    url(r'^(?P<db>\w+)/(?P<graphtype>[A,C]{2})/(?P<graphsubtype>[a-z,1,2]{1})/actor/(?P<actor_id>\d+)/$',
                            graphs_json_handler, name="graphs_json_handler"),
#    url(r'^graph/(?P<db>\w+)/(?P<graphtype>[A,C]{2})/(?P<graphsubtype>[a-z,1,2]{1})/$',
#                            graphs_handler, name="graphs_handler_graph"),
    url(r'^(?P<db>\w+)/(?P<graphtype>[A,C]{2})/(?P<graphsubtype>[a-z,1,2]{1})/concept/(?P<concept_id>\d+)/$',
                            graphs_json_C_handler, name="graphs_json_C_handler"),
 
#    
#    url(r'^(?P<db>\w+)/js/(?P<graphtype>[A,C]{2})/(?P<graphsubtype>[a-z,1,2]{1})/actor/(?P<actor_id>\d+)/$',
#                            graphs_js_handler, name="graphs_js_handler"),
#
#    url(r'^(?P<db>\w+)/js/(?P<graphtype>[A,C]{2})/(?P<graphsubtype>[a-z,1,2]{1})/concept/(?P<concept_id>\d+)/$',
#                            graphs_js_C_handler, name="graphs_js_C_handler"),

#    # automated documentation
#    url(r'^$', documentation_view),
)
