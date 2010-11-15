# -*- coding: utf-8 -*-
#!/usr/bin/python
# vim: set expandtab tabstop=4 shiftwidth=4:
# -*- coding: utf-8 -*-
#
# This file is part of AGAVE
#
# AGAVE is distributed under the terms of the BSD License. The full license is in
# the file LICENSE, distributed as part of this software.
#
# Copyright (c) 2010, Digital Enterprise Research Institute (DERI),NUI Galway.
# All rights reserved.
#
# Author: Julia Anaya
# Email: julia dot anaya at gmail dot com
#
# FILE:
# file-name
#
# DESCRIPTION:
# Description
#
# TODO:

#__all__ = ['']

from collections import defaultdict
from django.conf import settings
from django.db import connection, connections, transaction
from django.db.models import Avg, Max, Min, Count, F
from django.utils import simplejson
from agave.models import *
from agave.controller_graphs_queries import *
import string

TYPE_ACTOR = 1
TYPE_CONCEPT = 0
TYPE_INITIAL = 2

def nodes_list_to_json_edges(nodes):
    """
    >>> nodes = [
     {'nodeName': u'Michael AA MIGLIOR', 'type': 2},
     {'nodeName': u'Sebastien COURTY', 'type': 1},]
    >>> nodes_list_to_json_edges(nodes)
    [{'source': 0, 'target': 1, 'value': 1},
     {'source': 0, 'target': 2, 'value': 1}]
    """
    edges = [{'source':0, 'target':list(nodes).index(node) + 1, 'value':1}\
              for node in nodes]
    return edges

def nodesweight_dict_to_json_nodes_edges(node_origin, nodes_dict, node_type=TYPE_ACTOR):
    """
    >>> node_origin = Actor.objects.get(id=2)
    >>> nodes = { 
     u'Vincent Croquette': 4,
     u'Yohanns BELLAICHE': 3}
    >>> nodes_dict_to_edges(nodes)
    {'links': [{'source': 0, 'target': 1, 'value': 3},
           {'source': 0, 'target': 2, 'value': 4}],
     'nodes': [{'nodeName': u'Michael AA MIGLIOR', 'type': 2},
           {'nodeName': u'Yohanns BELLAICHE', 'type': 1},
           {'nodeName': u'Vincent Croquette', 'type': 1}]}
    """
    nodes = node_origin + \
            [{'nodeName':node, 'type':node_type} for node in nodes_dict.keys()]
    pos_nodes = dict([(node["nodeName"], pos) for pos, node in enumerate(nodes)])
    edges = [{'source':0, 'target':pos_nodes[node], 'value':weight}
             for node, weight in nodes_dict.items()]
    return {'nodes':nodes, 'links':edges}

def rows_to_json_nodes_edges(row, node_type=TYPE_ACTOR):
    nodes_set = set()
#    for node in row:
#        nodes_set.add((node[0], node[1]))
#        nodes_set.add((node[2], node[3]))
#    nodes = [{'nodeName':node_name, 'type':TYPE_ACTOR, 'id':node_id} for node_name, node_id in nodes_set]
#    edges = [{'sourceId':node[1], 'targetId':node[3], 'value':node[4]} for node in row]
    nodes_set = set()
    edges = []
    for node_name_from, node_id_from, node_name_to, node_id_to, weight in row:
        nodes_set.add((node_name_from, node_id_from))
        nodes_set.add((node_name_to, node_id_to))
        edges.append({'sourceId':node_id_from, 'targetId':node_id_to, 'value':weight})
    nodes = [{'nodeName':node_name, 'type':node_type, 'id':node_id}
             for node_name, node_id in nodes_set]
    data = {'nodes':nodes, 'links':edges}
    return data

def get_AAp_json_from_A(a, db='default', number_nodes=40):
    aids = get_A_ids_from_AAp_from_A(a, db)
    if aids:
        anodes = [{'nodeName':a.name, 'type':TYPE_INITIAL}] + \
        [{'nodeName':Actor.objects.using(db).get(id=aid).name, 'type':TYPE_ACTOR}
         for aid in aids]
    
    #    aedges = [{'source':a.id,'target':aid, 'value':1} for aid in aids]
        aedges = nodes_list_to_json_edges(anodes)
    else:
        anodes = [{'nodeName':a.name, 'type':TYPE_INITIAL}]
        aedges = []
    data = {'nodes':anodes, 'links':aedges}
    content = "var jsondata = " + simplejson.dumps(data, ensure_ascii=False)
    logging.debug("Generated AAp JSON from %s" % a.name)
    return content

def get_AAp_weight_json_from_As(a, db='default', number_nodes=40):
    node_origin = [{'nodeName':a.name, 'type':TYPE_INITIAL}]
    nodes_dict = get_Aweight_dict_from_AAp_from_A(a, db)
    data = nodesweight_dict_to_json_nodes_edges(node_origin, nodes_dict, TYPE_ACTOR)(node_origin, nodes_dict)
    content = "var jsondata = " + simplejson.dumps(data, ensure_ascii=False)
    logging.debug("Generated AAp JSON from %s" % a.name)
    return content

def get_AAc_json_from_A(a, db='default', number_nodes=40):
    """
    weight by the number of concepts they share (lost a-c initial weight)
    """

    aids = set([afromp['actor_to']
                for afromp in AAc.objects.filter(actor_from__id=a.id)\
                                                        .values('actor_to').distinct()]\
                 + [atop['actor_from']
                    for atop in AAc.objects.filter(actor_to__id=a.id).values('actor_from').distinct()])
    anodes = [{'nodeName':a.name, 'type':TYPE_INITIAL}]\
                 + [{'nodeName':Actor.objects.get(id=aid).name, 'type':TYPE_ACTOR} for aid in aids]
    aedges = nodes_list_to_json_edges(anodes)
    data = {'nodes':anodes, 'links':aedges}
    content = "var jsondata = " + simplejson.dumps(data, ensure_ascii=False)
    logging.debug("Generated AAp JSON from %s" % a.name)
    return content

    query = """
select ma.name, mc.name
    from agave.actorconcept as ama,
        agave.actor as ma,
        agave.actor as mb,
        agave.concept as mc,
        agave.actorconcept as amc
    where
        mb.name="Chavrier Philippe P" AND 
        mb.id=ama.actor_id AND
        ama.concept_id=mc.id AND
        ama.concept_id=amc.concept_id AND
        amc.actor_id != mb.id AND
        amc.actor_id = ma.id
    groub by ma.name;
    """

def get_AAc_weight_json_from_A(a, db='default', number_nodes=40):
    node_origin = [{'nodeName':a.name, 'type':TYPE_INITIAL}]
    nodes_dict = get_Aweight_dict_from_AAc_from_A(a, db)
    data = nodesweight_dict_to_json_nodes_edges(node_origin, nodes_dict, TYPE_ACTOR)
    content = "var jsondata = " + simplejson.dumps(data, ensure_ascii=False)
    logging.debug("Generated AAc JSON from %s" % a.name)
    return content

def get_AAb_json_from_A(a, db='default', number_nodes=40):
    aids = set([])
    [[[aids.add(a) for a in br.actors.all()] for br in concept.broaders.all()]
                                                    for concept in a.concepts.all()]
    anodes = [{'nodeName':a.name, 'group':2}] + [{'nodeName':aid.name, 'group':2}
                                                 for aid in aids]
    aedges = nodes_list_to_json_edges(anodes)
    data = {'nodes':anodes, 'links':aedges}
    content = "var jsondata = " + simplejson.dumps(data, ensure_ascii=False)
    return content

def get_AAb_weight_json_from_A(a, db='default', number_nodes=40):
    node_origin = [{'nodeName':a.name, 'type':TYPE_INITIAL}]
    nodes_dict = getAweight_dict_from_AAb_from_A(a, db)
    data = nodesweight_dict_to_json_nodes_edges(node_origin, nodes_dict, TYPE_ACTOR)
    content = "var jsondata = " + simplejson.dumps(data, ensure_ascii=False)
    logging.debug("Generated AAb JSON from %s" % a.name)
    return content

def get_AAn_weight_json_from_A(a, db='default', number_nodes=40):
    node_origin = [{'nodeName':a.name, 'type':TYPE_INITIAL}]
    nodes_dict = get_Aweight_dict_from_AAn_from_A(a, db)
    data = nodesweight_dict_to_json_nodes_edges(node_origin, nodes_dict, TYPE_ACTOR)
    content = "var jsondata = " + simplejson.dumps(data, ensure_ascii=False)
    logging.debug("Generated AAn JSON from %s" % a.name)
    return content

def get_AAbb_weight_json_from_A(a, db='default', number_nodes=40):
    node_origin = [{'nodeName':a.name, 'type':TYPE_INITIAL}]
    nodes_dict = get_Aweight_dict_from_AAbb_from_A(a, db)
    data = nodesweight_dict_to_json_nodes_edges(node_origin, nodes_dict, TYPE_ACTOR)
    content = "var jsondata = " + simplejson.dumps(data, ensure_ascii=False)
    logging.debug("Generated AAbb JSON from %s" % a.name)
    return content

def get_AAbc_weight_json_from_A(a, db='default', number_nodes=40):
    node_origin = [{'nodeName':a.name, 'type':TYPE_INITIAL}]
    nodes_dict = get_Aweight_dict_from_AAbc_from_A(a, db)
    data = nodesweight_dict_to_json_nodes_edges(node_origin, nodes_dict, TYPE_ACTOR)
    content = "var jsondata = " + simplejson.dumps(data, ensure_ascii=False)
    logging.debug("Generated AAbc JSON from %s" % a.name)
    return content

def get_AAbnbc_weight_json_from_A(a, db='default', number_nodes=40):
    node_origin = [{'nodeName':a.name, 'type':TYPE_INITIAL}]
    nodes_dict = get_Aweight_dict_from_AAbnbc_from_A(a, db)
    data = nodesweight_dict_to_json_nodes_edges(node_origin, nodes_dict, TYPE_ACTOR)
    content = "var jsondata = " + simplejson.dumps(data, ensure_ascii=False)
    logging.debug("Generated AAbnbc JSON from %s" % a.name)
    return content

def get_CCb_weight_json_from_A(a, db='default', number_nodes=40):
#    concepts = a.concepts.all()
#    cnodes = [{'nodeName':c.name,'type':TYPE_CONCEPT} for c in concepts]
    if db == 'projects': db = 'default'
    cq = ActorConcept.objects.using(db).filter(actor=a).order_by('-weight')[:number_nodes]
    cnames = cq.values('concept__name', 'weight')
    cnodes = [{'nodeName':c['concept__name'], 'type':TYPE_CONCEPT} for c in cnames]
    pos_nodes = dict([(y["nodeName"], x) for x, y in enumerate(cnodes)])

    concepts = [c.concept for c in cq]
    brs = CCb.objects.using(db).filter(concept_from__in=concepts,
                                               concept_to__in=concepts)
    cedges = [{'source':pos_nodes[concept.concept_from.name],
               'target':pos_nodes[concept.concept_to.name]} for concept in brs]
    data = {'nodes':cnodes, 'links':cedges}
    content = "var jsondata = " + simplejson.dumps(data, ensure_ascii=False)
    return content

def get_CCn_weight_json_from_A(a, db='default', number_nodes=40):
#    concepts = a.concepts.all()
#    cnodes = [{'nodeName':c.name,'type':TYPE_CONCEPT} for c in concepts]
    if db == 'projects': db = 'default'
    cq = ActorConcept.objects.using(db).filter(actor=a).order_by('-weight')[:number_nodes]
    cnames = cq.values('concept__name', 'weight')
    cnodes = [{'nodeName':c['concept__name'], 'type':TYPE_CONCEPT} for c in cnames]
    pos_nodes = dict([(y["nodeName"], x) for x, y in enumerate(cnodes)])

    concepts = [c.concept for c in cq]
    brs = CCb.objects.using(db).filter(concept_from__in=concepts,
                                               concept_to__in=concepts)
    cedges = [{'source':pos_nodes[concept.concept_from.name],
               'target':pos_nodes[concept.concept_to.name]} for concept in brs]
    data = {'nodes':cnodes, 'links':cedges}
    content = "var jsondata = " + simplejson.dumps(data, ensure_ascii=False)
    return content

def get_AC_weight_json_from_A(a, db='default', number_nodes=40):
    nodes = [{'nodeName':a.name, 'type':TYPE_INITIAL}]
    #    q1=a.concepts.all().extra(select={'weight':})
    cq = ActorConcept.objects.using(db).filter(actor=a).order_by('-weight')[:number_nodes]
    cnames = cq.values('concept__name', 'weight')
    cnodes = [{'nodeName':c['concept__name'], 'type':TYPE_CONCEPT} for c in cnames]
    nodes = nodes + cnodes
    pos_nodes = dict([(y["nodeName"], x) for x, y in enumerate(nodes)])

    cedges = [{'source':0, 'target':pos_nodes[c['concept__name']], 'value':c['weight']} for c in cnames]
    data = {'nodes':nodes, 'links':cedges}
    content = "var jsondata = " + simplejson.dumps(data, ensure_ascii=False)
    return content

def get_AC_weight_2l_json_from_A(a, db='default', number_nodes=40):
    nodes = [{'nodeName':a.name, 'type':TYPE_INITIAL}]
    #    q1=a.concepts.all().extra(select={'weight':})
    cq = ActorConcept.objects.using(db).filter(actor=a).order_by('-weight')[:10]
    cnames = cq.values('concept__name', 'weight')
    cnodes = [{'nodeName':c['concept__name'], 'type':TYPE_CONCEPT} for c in cnames]
    pos_cnodes = dict([(y["nodeName"], x) for x, y in enumerate(cnodes)])
    aq = ActorConcept.objects.using(db).filter(concept__name__in=pos_cnodes.keys()).exclude(actor=a).order_by('-weight')[:70]
#    aq = ActorConcept.objects.filter(concept__name__in=pos_cnodes.keys()).order_by('-weight')
#    anames = aq.values('actor__name','weight')
#    anames = list(set([a['actor__name'] for a in aq.values('actor__name')]))
    anames = list(set([c.actor.name for c in aq]))
#    anodes = [{'nodeName':c['actor__name'],'type':TYPE_ACTOR} for c in anames]
    anodes = [{'nodeName':c, 'type':TYPE_ACTOR} for c in anames]

    nodes = nodes + cnodes + anodes
    pos_nodes = dict([(y["nodeName"], x) for x, y in enumerate(nodes)])

    cedges = [{'source':0, 'target':pos_nodes[c['concept__name']], 'value':c['weight']} for c in cnames]
    aedges = [{'source':pos_nodes[c.concept.name], 'target':pos_nodes[c.actor.name], 'value':c.weight} for c in aq]

    data = {'nodes':nodes, 'links':cedges + aedges}
    content = "var jsondata = " + simplejson.dumps(data, ensure_ascii=False)
    return content

def get_AC_weight_json_from_C(c, db='default', number_nodes=40):
    node_origin = [{'nodeName':c.name, 'type':TYPE_INITIAL}]
    nodes_list = get_Aweight_list_from_C(c)
    nodes_dict = dict(nodes_list)
    data = nodesweight_dict_to_json_nodes_edges(node_origin, nodes_dict, TYPE_ACTOR)
    content = "var jsondata = " + simplejson.dumps(data, ensure_ascii=False)
    logging.debug("Generated AC JSON from %s" % c.name)
    return content

# the same
#def get_AC_weight_json_from_C(c, number_nodes=40):
#    aq = ActorConcept.objects.using(db).filter(concept=c).order_by('-weight', 'actor__name')[:number_nodes]
#    anames = aq.values('actor__name', 'weight')
#    anodes = [{'nodeName':c['actor__name'], 'type':TYPE_ACTOR} for c in cnames]
#    nodes = nodes + cnodes
#    pos_nodes = dict([(y["nodeName"], x) for x, y in enumerate(nodes)])
#
#    cedges = [{'source':0, 'target':pos_nodes[c['concept__name']], 'value':c['weight']} for c in cnames]
#    data = {'nodes':nodes, 'links':cedges}
#    content = "var jsondata = " + simplejson.dumps(data, ensure_ascii=False)
#    return content


def get_AAb_weight_jsoncustomids_from_A(a, db='default', number_nodes=40):
    row = get_Aidsweight_from_AAb_from_A(a, db, number_nodes)
    data = rows_to_json_nodes_edges(row)
    content = "var jsondata = " + simplejson.dumps(data, ensure_ascii=False)
    logging.debug("Generated AAb JSON from %s" % a.name)
    return content
