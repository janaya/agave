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

from agave.models import ActorConcept, AAp, AAc
from django.conf import settings
from django.db import connections
from django.db.models import Count
from agave.models import Actor, Concept

def get_Aweight_list_from_C(c, db='default', number_nodes=40):
    """
    [(a_concepts.actor, a_concepts.weight) for a_concepts in ActorConcept.objects.filter(concept__name="Neurons").order_by('-weight','actor__name')]
    """
    return [(a_concepts.actor.name, a_concepts.weight)
            for a_concepts in ActorConcept.objects.using(db).filter(concept=c)\
                        .order_by('-weight', 'actor__name')[:number_nodes]]

def get_A_ids_from_AAp_from_A(a, db='default', number_nodes=40):
    actors_from_instances = [afromp['actor_to']
        for afromp in AAp.objects.using(db).filter(actor_from__id=a.id)\
            .values('actor_to').distinct()]
    actors_to_instances = [atop['actor_from']
        for atop in AAp.objects.filter(actor_to__id=a.id)\
            .values('actor_from').distinct()]
    return set(actors_from_instances + actors_to_instances)

def get_Aweight_dict_from_AAp_from_A(a, db='default', number_nodes=40):
    actors_from_instances = AAp.objects.using(db).filter(actor_from=a)\
                    .values('actor_to__name').annotate(weight=Count('id'))
    actors_to_instances = AAp.objects.using(db).filter(actor_to=a)\
                    .values('actor_from__name').annotate(weight=Count('id'))
    w_asfrom = dict([(y["actor_to__name"], y['weight'])
                     for y in actors_from_instances])
    w_asto = dict([(y["actor_from__name"], y['weight'])
                   for y in actors_to_instances])
    w_anodes = dict()
    map(lambda x: w_anodes.__setitem__(x[0], w_asfrom.get(x[0], 0) \
                + w_asto.get(x[0], 0)), w_asfrom.items() + w_asto.items())
    return w_anodes

def get_Aweight_dict_from_AAc_from_A(a, db='default', number_nodes=40):
    actors_from_concepts = AAc.objects.using(db).filter(actor_from=a)\
                    .values('actor_to__name').annotate(weight=Count('id'))
    actors_to_concepts = AAc.objects.using(db).filter(actor_to=a)\
                    .values('actor_from__name').annotate(weight=Count('id'))
    w_asfrom = dict([(y["actor_to__name"], y['weight']) for y in actors_from_concepts])
    w_asto = dict([(y["actor_from__name"], y['weight']) for y in actors_to_concepts])
    w_anodes = dict()
    map(lambda x: w_anodes.__setitem__(x[0], w_asfrom.get(x[0], 0) \
                + w_asto.get(x[0], 0)), w_asfrom.items() + w_asto.items())
    return w_anodes

def getAweight_dict_from_AAb_from_A(a, db='default', number_nodes=40):
    dbname = settings.DATABASES[db]['NAME']
    appname = 'agave'
    print dbname
    print appname
    query = """
    SELECT a2.name, count(*) as weight
        FROM
            %(dbname)s.%(appname)s_actor as a1,
            %(dbname)s.%(appname)s_actor as a2,
            %(dbname)s.%(appname)s_actorconcept as ac1,
            %(dbname)s.%(appname)s_actorconcept as ac2,
            %(dbname)s.%(appname)s_ccb as br1
        """ % {'appname': appname, 'dbname': dbname} + \
        """
        WHERE
            a1.name = %s AND
            ac1.actor_id = a1.id AND
            ac1.concept_id = br1.concept_from_id AND
            ac2.concept_id = br1.concept_to_id AND
            ac2.actor_id = a2.id AND
            a1.id != a2.id
        GROUP BY a2.name
        ORDER BY weight DESC
        """ + \
        """
        LIMIT %s;
        """ % number_nodes
    cursor = connections[db].cursor()
#    cursor.execute(query, [appname, dbname, appname, dbname, appname, dbname, appname, dbname, appname, dbname, a.name])
    cursor.execute(query, [a.name])

    row = cursor.fetchall()
    """
    ((33L, u' Pouillart  P  P  '),
     (33L, u' Asselain  B  B  '),
    """
    w_anodes = dict(row)
    return w_anodes

def get_Aidsweight_from_AAb_from_A(a, db='default', number_nodes=40):
    dbname = settings.DATABASES[db]['NAME']
    appname = 'agave'
    print dbname
    print appname
    query = """
    SELECT a1.name, a1.id, a2.name, a2.id, count(*) AS weight 
    FROM  %(dbname)s.%(appname)s_actor AS a1 INNER JOIN %(dbname)s.%(appname)s_actorconcept AS ac1 ON a1.id = ac1.actor_id 
    INNER JOIN  %(dbname)s.%(appname)s_ccb AS br1 ON br1.concept_from_id = ac1.concept_id 
    INNER JOIN  %(dbname)s.%(appname)s_actorconcept AS ac2 ON br1.concept_to_id = ac2.concept_id 
    INNER JOIN  %(dbname)s.%(appname)s_actor AS a2 ON ac2.actor_id = a2.id 
    """ % {'appname': appname, 'dbname': dbname} + \
    """
    WHERE  a1.id != a2.id AND a1.id=%s
    GROUP BY a1.name,a2.name 
    ORDER BY weight DESC, a1.name, a2.name
    """ % a.id + \
    """
    LIMIT %s;
    """ % number_nodes
    cursor = connections[db].cursor()
#    cursor.execute(query, [appname, dbname, appname, dbname, appname, dbname, appname, dbname, appname, dbname, a.name])
#    cursor.execute(query, [a.name])
    cursor.execute(query)
    row = cursor.fetchall()
    return row

def get_Aweight_dict_from_AAn_from_A(a, db='default', number_nodes=40):
    dbname = settings.DATABASES[db]['NAME']
    appname = 'agave'
    query = """
    SELECT a2.name, count(*) as weight
        FROM
            %(dbname)s.%(appname)s_actor as a1,
            %(dbname)s.%(appname)s_actor as a2,
            %(dbname)s.%(appname)s_actorconcept as ac1,
            %(dbname)s.%(appname)s_actorconcept as ac2,
            %(dbname)s.%(appname)s_ccb as br1
        """ % {'appname': appname, 'dbname': dbname} + \
        """
        WHERE
            a1.name = %s AND
            ac1.actor_id = a1.id AND
            ac1.concept_id = br1.concept_to_id AND
            ac2.concept_id = br1.concept_from_id AND
            ac2.actor_id = a2.id AND
            a1.id != a2.id
        GROUP BY a2.name
        ORDER BY weight DESC
        """ + \
        """
        LIMIT %s;
        """ % number_nodes
    cursor = connections[db].cursor()
    cursor.execute(query, [a.name])

    row = cursor.fetchall()
    w_anodes = dict(row)
    return w_anodes

def get_Aweight_dict_from_AAbb_from_A(a, db='default', number_nodes=40):
    dbname = settings.DATABASES[db]['NAME']
    appname = 'agave'
    query = """
    SELECT a2.name, count(*) as weight
        FROM
           %(dbname)s.%(appname)s_actor as a1,
           %(dbname)s.%(appname)s_actor as a2,
           %(dbname)s.%(appname)s_actorconcept as ac1,
           %(dbname)s.%(appname)s_actorconcept as ac2,
           %(dbname)s.%(appname)s_ccb as br1,
           %(dbname)s.%(appname)s_ccb as br2
        """ % {'appname': appname, 'dbname': dbname} + \
        """
        WHERE
            a1.name =%s AND
            ac1.actor_id = a1.id AND
            ac1.concept_id = br1.concept_from_id AND
            br2.concept_to_id = br1.concept_to_id AND
            br1.concept_from_id != br2.concept_from_id AND
            ac2.concept_id = br2.concept_from_id AND
            ac2.actor_id = a2.id AND
            a1.id != a2.id
        GROUP BY a2.name
        ORDER BY weight DESC
        """ + \
        """
        LIMIT %s;
        """ % number_nodes
    cursor = connections[db].cursor()
    cursor.execute(query, [a.name])

    row = cursor.fetchall()
    w_anodes = dict(row)
    return w_anodes

def get_Aweight_dict_from_AAbc_from_A(a, db='default', number_nodes=40):
    dbname = settings.DATABASES[db]['NAME']
    appname = 'agave'
    query = """
    SELECT a2.name, count(*) as weight
        FROM
           %(dbname)s.%(appname)s_actor as a1,
           %(dbname)s.%(appname)s_actor as a2,
           %(dbname)s.%(appname)s_actorconcept as ac1,
           %(dbname)s.%(appname)s_actorconcept as ac2,
           %(dbname)s.%(appname)s_ccb as br1,
           %(dbname)s.%(appname)s_ccb as br2
        """ % {'appname': appname, 'dbname': dbname} + \
        """
        WHERE
            a1.name =%s AND
            ac1.actor_id = a1.id AND
            ac1.concept_id = br1.concept_to_id AND
            br2.concept_from_id = br1.concept_from_id AND
            br1.concept_to_id != br2.concept_to_id AND
            ac2.concept_id = br2.concept_to_id AND
            ac2.actor_id = a2.id AND
            a1.id != a2.id
        GROUP BY a2.name
        ORDER BY weight DESC
        """ + \
        """
        LIMIT %s;
        """ % number_nodes
    print query
    cursor = connections[db].cursor()
    cursor.execute(query, [a.name])

    row = cursor.fetchall()
    w_anodes = dict(row)
    return w_anodes

def get_Aweight_dict_from_AAbnbc_from_A(a, db='default', number_nodes=40):
    w_asb = getAweight_dict_from_AAb_from_A(a, db)
    w_asn = get_Aweight_dict_from_AAn_from_A(a, db)
    w_asbb = get_Aweight_dict_from_AAbb_from_A(a, db)
    w_asbc = get_Aweight_dict_from_AAbc_from_A(a, db)
    w_anodes = dict()
    map(lambda x: w_anodes.__setitem__(x[0], w_asb.get(x[0], 0)\
                                           + w_asn.get(x[0], 0)\
                                           + w_asbb.get(x[0], 0)\
                                           + w_asbc.get(x[0], 0)),
                                       w_asb.items()\
                                       + w_asn.items()\
                                       + w_asbb.items()
                                       + w_asbc.items())

    return w_anodes

# does not work
#def get_Aweight_dict_from_AAbnbc_from_A(a, db='default', number_nodes=40):
#    """
#    too many time! 
#    """
#    """
#    SELECT a2.name, count(*) as weight
#        FROM
#            agave.actor as a1,
#            agave.actor as a2,
#            agave.actorconcept as ac1,
#            agave.actorconcept as ac2,
#            agave.ccb as br1,
#            agave.ccb as br2
#        WHERE
#            a1.name = ' Pierga  J-Y  JY  ' AND
#            ac1.actor_id = a1.id AND
#            (
#            (ac1.concept_id = br1.concept_from_id AND
#            ac2.concept_id = br1.concept_to_id)
#            
#            OR
#            (ac1.concept_id = br1.concept_to_id AND
#            ac2.concept_id = br1.concept_from_id)
#            
#            OR
#            (ac1.concept_id = br1.concept_from_id AND
#            br2.concept_to_id=br1.concept_to_id AND
#            br1.concept_from_id != br2.concept_from_id AND
#            ac2.concept_id = br2.concept_from_id)
#            
#            OR
#            (ac1.concept_id = br1.concept_to_id AND
#            br2.concept_from_id=br1.concept_from_id AND
#            br1.concept_to_id != br2.concept_to_id AND
#            ac2.concept_id = br2.concept_to_id)
#            ) AND
#            ac2.actor_id = a2.id AND
#            a1.id != a2.id
#        GROUP BY a2.name
#        ORDER BY weight DESC
#        LIMIT 100;
#    """
#    dbname = settings.DATABASES[db]['NAME']
#    appname = 'agave'
#    print dbname
#    print appname
#    query = """
#    SELECT a2.name, count(*) as weight
#        FROM
#            %(dbname)s.%(appname)s_actor as a1,
#            %(dbname)s.%(appname)s_actor as a2,
#            %(dbname)s.%(appname)s_actorconcept as ac1,
#            %(dbname)s.%(appname)s_actorconcept as ac2,
#            %(dbname)s.%(appname)s_ccb as br1,
#            %(dbname)s.%(appname)s_ccb as br2
#        """%{'appname': appname, 'dbname': dbname} + \
#        """
#        WHERE
#            a1.name = %s AND
#            ac1.actor_id = a1.id AND
#
#            ac1.concept_id = br1.concept_from_id AND
#            ac2.concept_id = br1.concept_to_id AND
#
#            ac1.concept_id = br1.concept_to_id AND
#            ac2.concept_id = br1.concept_from_id AND
#                
#            ac1.concept_id = br1.concept_from_id AND
#            br2.concept_to_id=br1.concept_to_id AND
#            br1.concept_from_id != br2.concept_from_id AND
#            ac2.concept_id = br2.concept_from_id AND
#
#            ac1.concept_id = br1.concept_to_id AND
#            br2.concept_from_id=br1.concept_from_id AND
#            br1.concept_to_id != br2.concept_to_id AND
#            ac2.concept_id = br2.concept_to_id AND
#
#
#            ac2.actor_id = a2.id AND
#            a1.id != a2.id
#        GROUP BY a2.name
#        ORDER BY weight DESC
#        LIMIT 100;
#        """
#    print query
#    cursor = connections[db].cursor()
#    cursor.execute(query, [a.name])
#
#    row = cursor.fetchall()
#    w_anodes = dict(row)
#    return w_anodes
##############################################################################

def concept(c):
    if isinstance(c, Concept):
        return c
    else:
        return Concept.objects.get(name=c)

def actor(a):
    if isinstance(a, Actor):
        return a
    else:
        return Actor.objects.get(name=a)

def actors_weight_from_broaders_from_concept(c):
    """
    >>>d = dict([(br,[(aconcepts.actor, aconcepts.weight) for aconcepts in ActorConcept.objects.filter(concept=br)]) for br in concept(c).broaders.all()])
    {<Concept: Microscopy>: [(<Author: Kremer Y Y>, 1L),
                    (<Author: Léger J-F JF>, 1L),
    >>> rev_dict_of_lists(d)
    <Author: Amigorena Sebastian S>: [<Concept: Cell Surface Extensions>]}
    >>>[dict(zip(("broader","actors"), x)) for x in d.items()]
    'broader': <Concept: Cell Surface Extensions>},
 {'actors': [<Author: Salomé R R>,
              <Author: Kremer Y Y>,

    """
    #d = dict([
    #        (br.name,[(aconcepts.actor.name, aconcepts.weight) 
    #        for aconcepts in ActorConcept.objects.filter(concept=br)]) 
    #                for br in concept.broaders.all()])
    concept = concept(c)
    print concept
    print isinstance(concept, Concept)
    d = dict([
            (br.name, [(aconcepts.actor.name, aconcepts.weight)
            for aconcepts in ActorConcept.objects.filter(concept=br).order_by('-weight', 'actor__name')])
                    for br in concept.broaders.filter(not_in_dataset=False)])
    return [dict(zip(("broader", "actors"), x)) for x in d.items()]


def actors_weight_from_narrowers_from_concept(c):
    """
    c<-c-a, CCba U ACp
      <    \a    
         \c-a
        
    >>> dict([(br,[(aconcepts.actor, aconcepts.weight) for aconcepts in ActorConcept.objects.filter(concept=br.concept_from)]) for  br in Concept.objects.get(name="Microscopy, Electron").is_broader_of.all()])
     <Concept: Microscopy, Electron, Transmission>: [(<Author: Lizárraga Floria F>, 1L),
    ...
    """
    """
    return [(br, br.actors.all()) for br in concept.is_broader_of.all()]    
    """
    """
    d = dict([
        (br.concept_from.name,[(aconcepts.actor, aconcepts.weight) 
        for aconcepts in ActorConcept.objects.filter(concept=br.concept_from).order_by('-weight')]) 
        for  br in CCb.objects.filter(concept_to = concept).filter(concept_from__not_in_dataset=False)])
    """
    concept = concept(c)
    d = dict([
        (br.concept_from.name, [(aconcepts.actor.name, aconcepts.weight)
        for aconcepts in ActorConcept.objects.filter(concept=br.concept_from).order_by('-weight', 'actor__name')])
        for  br in concept.is_broader_of.filter(concept_from__not_in_dataset=False)])
    return d

def aalljsonweights(a):
    pass
