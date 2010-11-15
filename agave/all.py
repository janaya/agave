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

from django.db import connection, transaction
from agave.models import *
#from agave.models import *
from collections import defaultdict
from django.db.models import Avg, Max, Min, Count, F
from django.utils import simplejson

def concept(c):
    if isinstance(c, Concept):
        return c
    else:
        return Concept.objects.get(name=c)

def actor(a):
    if isinstance(a, Actor):
        return a
    else:
        return Actor.objects.get(name=c)

def reverse_dict(orig):
    rev = defaultdict(list)
    [rev[v].append(k) for k, v in orig.items()]
    return rev

def rev_dict_of_lists(d):
    newd = defaultdict(list)
    [[newd[i].append(k) for i in v] for k, v in d.items()]
    return newd

def is_actor_or_concept(name, db):
    if not name:
        return (None, None)
    elif Concept.objects.using(db).filter(name=name):
        return ('Concept', Concept.objects.using(db).get(name=name))

    elif Actor.objects.using(db).filter(name=name):
        return ('Actor', Actor.objects.using(db).get(name=name))
    else:
        return(None, None)

def actors_from_concept(c):
    """
    c-a, ACp
      \a
    
    other method:
    concept(c).actorconcept_set.all()
    """
    return concept(c).actors.all()

def actors_from_concept_ds(c, pxds):
    return ActorConcept.objects.filter(dataset=pxds, concept=concept(c))

def actors_weight_from_concept_ds(c, pxds):
    return  [(a_concepts.actor, a_concepts.weight) for a_concepts in ActorConcept.objects.filter(concept=concept(c), dataset=pxds)]


def coactors(a):
    # o from AAp
#    return [p.actors.all() for p in a.instances.all()]
    # ?
    return Actor.objects.filter(instances__in=a.instances.all()).exclude(id=a.id)

def nonejson():
    data = {'nodes':[{'nodeName':"Error: give me a valid argument!!", 'type':2}], 'links':[]}
    content = "var jsondata = " + simplejson.dumps(data, ensure_ascii=False)
    return content



def allccb():
    broaders = CCb.objects.filter(concept_to__not_in_dataset=False).filter(concept_from__not_in_dataset=False).values('concept_to__name').annotate(weight=Count('id')).order_by('-weight')
#    cnames_set = set()
#    [cnames_set.add(c.concept_from.name) for c in broaders]
#    [cnames_set.add(c.concept_to.name)  for c in broaders]
    broaders_list = [c['concept_to__name'] for c in broaders]
#    cq = CCb.objects.filter(concept_from__name__in = cnames_set,concept_to__name__in = cnames_set)
#    cq = CCb.objects.filter(concept_from__name__in = broaders_list,concept_to__name__in = broaders_list)
#    cq = CCb.objects.filter(concept_from__not_in_dataset=False,concept_to__name__in = broaders_list)
    cq = CCb.objects.filter(concept_to__name__in=broaders_list)
    cnames_set = set()
    [cnames_set.add(c.concept_from.name) for c in cq]
    [cnames_set.add(c.concept_to.name)  for c in cq]
    cnodes = [{'nodeName':c, 'type':0} for c in cnames_set]
    pos_nodes = dict([(y["nodeName"], x) for x, y in enumerate(cnodes)])
    cedges = [{'source':pos_nodes[br.concept_from.name], 'target':pos_nodes[br.concept_to.name]} for br in cq]
    data = {'nodes':cnodes, 'links':cedges}
    content = "var jsondata = " + simplejson.dumps(data, ensure_ascii=False)
    return content

def aalljsonweights(a):
    pass


def get_root(concept):
    return concept, [get_root(br.concept_to) for br in CCb.objects.filter(concept_from=concept)]

def get_leaf(concept):
    return concept, [get_leaf(br.concept_from) for br in CCb.objects.filter(concept_to=concept)]

# operations

def detect_transitive_rel():
    count = 0
    for concept in Concept.objects.all():
        broaders = concept.broaders.all()
        for broader in broaders:
            for broader2 in broader.broaders.all():
                if broader2 in broaders:
                    print "transitive: %s, %s, %s" % (concept, broader, broader2)
                    count += 1
    return count

def eliminate_transitive_rel():
    count = 0
    for concept in Concept.objects.all():
        broaders = concept.broaders.all()
        for broader in broaders:
            for broader2 in broader.broaders.all():
                if broader2 in broaders:
                    print "transitive: %s, %s, %s" % (concept, broader, broader2)
                    count += 1
                    CCb.objects.filter(concept_from=concept, concept_to=broader2).delete()
    return count

def detect_transitive_rel():
    for concept in Concept.objects.all():
    #    concept = Concept.objects.get(name="Symporters")
        #not_broaders = broaders_from(1, concept, {}, pxds)
        #not_broaders = concept.broaders.all()
        not_broaders = set(concept.broaders.all())
        #broaders = not_broaders[1]
        broaders = not_broaders
        for broader in broaders:
            broaders = list(set(broaders).difference(set(broaders).difference([broader]).intersection(set(broader.broaders.all()))))
        #    broaders.difference_update(broaders.difference([broader]).intersection(set(broader.broaders.all()))
        #[broaders.difference_update(broaders.difference([broader]).intersection(set(broader.broaders.all()))) for broader in broaders]
        not_broaders.difference_update(broaders)
        not_ccb = []
        for not_broader in not_broaders:
            [not_ccb.append() for br_rel in CCb.objects.filter(concept_from=concept, concept_to=not_broader)]
        return not_ccb

def eliminate_transitive_rel_ds(pxds):
    for concept in Concept.objects.all():
    #    concept = Concept.objects.get(name="Symporters")
        #not_broaders = broaders_from(1, concept, {}, pxds)
        #not_broaders = concept.broaders.all()
        not_broaders = set(concept.broaders.all())
        #broaders = not_broaders[1]
        broaders = not_broaders
        for broader in broaders:
            broaders = list(set(broaders).difference(set(broaders).difference([broader]).intersection(set(broader.broaders.all()))))
        #    broaders.difference_update(broaders.difference([broader]).intersection(set(broader.broaders.all()))
        #[broaders.difference_update(broaders.difference([broader]).intersection(set(broader.broaders.all()))) for broader in broaders]
        not_broaders.difference_update(broaders)
        for not_broader in not_broaders:
            [br_rel.delete() for br_rel in CCb.objects.filter(concept_from=concept, concept_to=not_broader)]

def diadic_cycles(pxds):
    count = 0
    for ccb in  CCb.objects.filter(datasets=pxds):
        if  CCb.objects.filter(datasets=pxds, concept_from=ccb.concept_to, concept_to=ccb.concept_from):
            count += 1
            print "cycle!!"
            print ccb
    print count
#    CCb.objects.get(concept_from__name="Immunoglobulin Constant Regions", concept_to__name="Immunoglobulin Fc Fragments").delete()
#     CCb.objects.filter(concept_from__name="Immunoglobulin Fab Fragments",concept_to__name="Immunoglobulin Variable Region").delete()

def triadic_cycles(pxds):
    count = 0
    for ccb in  CCb.objects.filter(datasets=pxds):
#        for grandparent in ccb.concept_to.broaders.filter(datasets=pxds):
        for grandparent in CCb.objects.filter(datasets=pxds, concept_from=ccb.concept_to):
#            if ccb.concept_from in grandparent.broaders.filter(datasets = pxds):
            if CCb.objects.filter(concept_from=grandparent.concept_to, concept_to=ccb.concept_from, datasets=pxds):
                print "cycle!!"
                print ccb
                print grandparent
                print CCb.objects.filter(concept_from=grandparent.concept_to, concept_to=ccb.concept_from, datasets=pxds)
                print "\n"
                count += 1

    print count


def cycles():
#    count = 0
#    for concept in Concept.objects.all():
#        if CCb.objects.filter(concept_from = concept, concept_to = concept):
#            count +=1
#            print "cycle!!"
#            print CCb.objects.filter(concept_from = concept, concept_to = concept)
#    print count
    print len(CCb.objects.filter(concept_from__name=F('concept_to__name')))


def diadic_cycles():
    count = 0
    for ccb in  CCb.objects.filter():
        if  CCb.objects.filter(concept_from=ccb.concept_to, concept_to=ccb.concept_from):
            count += 1
            print "cycle!!"
            print ccb
    print count

def triadic_cycles():
    count = 0
    for ccb in  CCb.objects.filter():
#        for grandparent in ccb.concept_to.broaders.filter(datasets=pxds):
        for grandparent in CCb.objects.filter(concept_from=ccb.concept_to):
#            if ccb.concept_from in grandparent.broaders.filter(datasets = pxds):
            if CCb.objects.filter(concept_from=grandparent.concept_to, concept_to=ccb.concept_from):
                print "cycle!!"
                print ccb
                print grandparent
                print CCb.objects.filter(concept_from=grandparent.concept_to, concept_to=ccb.concept_from)
                print "\n"
                count += 1

    print count

def narrowers_from(count, concept, dict, dataset):
    narrowers_list = [na.concept_from for na in CCb.objects.filter(concept_to=concept, datasets=dataset)]
    if narrowers_list:
        if not dict.get(count, False):
    #        print "dict[%s] did not exists" % count
            dict[count] = narrowers_list
        else:
            dict[count] += narrowers_list
    #    print "dict[%s] before applying set: " % count
    #    print dict[count]
        dict[count] = list(set(dict[count]))
    #    print "after"
    #    print dict[count]
        for na in dict[count]:
    #        print "calling again with na" + na.__unicode__()
            narrowers_from(count + 1, na, dict, dataset)
    #    print "e
    return dict

def broaders_from(count, concept, dict, dataset):
    broaders_list = [br.concept_to for br in CCb.objects.filter(concept_from=concept, datasets=dataset)]
    if broaders_list:
        if not dict.get(count, False):
    #        print "dict[%s] did not exists" % count
            dict[count] = broaders_list
        else:
            dict[count] += broaders_list
    #    print "dict[%s] before applying set: " % count
    #    print dict[count]
        dict[count] = list(set(dict[count]))
    #    print "after"
    #    print dict[count]
        for br in dict[count]:
    #        print "calling again with na" + na.__unicode__()
            broaders_from(count + 1, br, dict, dataset)
    #    print "end: returning"
    return dict


def broadersjson():
    nodes = [{'nodeName':c['name'], 'new':c['not_in_dataset']} for c in Concept.objects.values('name', 'not_in_dataset').order_by('id')]
    # if all database ids are consecutive!!
    edges = [{'source':br['concept_from'] - 1, 'target':br['concept_to'] - 1} for br in CCb.objects.values('concept_from', 'concept_to')]
    data = {'nodes':nodes, 'links':edges}
    content = "var jsondata = " + simplejson.dumps(data, ensure_ascii=False)
    return content


def broaders_hierarchy_first_3levels_json():
    pass

def broaders_from_concept(c):
    """
    c->c, CCba
      \>c
    """
    return  concept(c).broaders.filter(not_in_dataset=False)

def broaders_from_concept_ds(c, pxds):
    CCb.objects.filter(concept_from=concept(c), datasets=pxds)

def broaders_from_concept_not_transitive(c):
    """
    c->!c->c, CCba
      \----/
    """
    pass

def broaders_from_concept_not_transitive_sql(c):
    #wrong
    query = """
    SELECT cb.name
    FROM 
        agave.ccb as bra,
        agave.concept as ca,
        agave.concept as cb
        
    WHERE 
        ca.name="Axons" AND 
        ca.id=bra.concept_from_id AND
        
        bra.concept_to_id=cb.id AND
        
        cb.id NOT IN 
        
        (SELECT *
            FROM
                agave.ccb as brb,
                agave.ccb as brc
            WHERE
                cb.id=brb.concept_from_id AND
                brb.concept_to_id=brc.concept_to_id AND
                brc.concept_from_id=ca.id
            )
        ;
    """
def transitive_from_concept_sql(c):
    query = """SELECT cb.name
    FROM 
        agave.ccb as bra,
        agave.ccb as brb,
        agave.ccb as brc,
        agave.concept as ca,
        agave.concept as cb
        
    WHERE 
        ca.name="Axons" AND 
        ca.id=bra.concept_from_id AND
        bra.concept_to_id=brb.concept_from_id AND
        brb.concept_to_id=brc.concept_to_id AND
        
        brc.concept_to_id=cb.id AND
        
        brc.concept_from_id=ca.id;
    """
    query_c = """
SELECT ca.name, cc.name, cb.name
    FROM 
        agave.ccb as bra,
        agave.ccb as brb,
        agave.ccb as brc,
        agave.concept as ca,
        agave.concept as cb,
        agave.concept as cc
        
    WHERE 
        ca.name="Axons" AND 
        ca.id=bra.concept_from_id AND
        bra.concept_to_id=brb.concept_from_id AND
        
        brb.concept_from_id=cc.id AND
        
        brb.concept_to_id=brc.concept_to_id AND
        
        brc.concept_to_id=cb.id AND
        
        brc.concept_from_id=ca.id;
    """

def actors_from_broaders_from_concept(c):
    """
    c->c-a, CCba U ACp
     \      \a    
      \>c-a

    >>> d= dict([(br,[a for a in br.actors.all()]) for br in Concept.objects.get(name="Axons").broaders.all()])
    >>> d
    {<Concept: Nerve Fibers>: [<Author: Dieudonné S S>],
     <Concept: Neurons>: [<Author: Salomé R R>,
                     <Author: Kremer Y Y>, 
                    ...
    >>> rev_dict_of_lists(d)
    <Author: Gasnier B B>: [<Concept: Neurons>], <Author: Amigorena Sebastian S>: [<Concept: Cell Surface Extensions>]}
    ...
    """
    #return dict([(br,[a for a in br.actors.all()]) for br in concept(c).broaders.all()])
    return dict([(br, br.actors.all()) for br in concept(c).broaders.all()])

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

def actors_weight_broaders_from_concept_ds(c, pxds):
    return dict([(br, [(aconcepts.actor, aconcepts.weight) for aconcepts in ActorConcept.objects.filter(concept=br.concept_to, dataset=pxds)]) for  br in CCb.objects.filter(concept_from=concept(c), datasets=pxds)])

def actors_from_broaders_from_concept_sql():
    query = """
SELECT ma.name, mc.name
    FROM agave.ccb, 
        agave.actorconcept,
        agave.concept as ma,
        agave.concept as mb,
        agave.actor as mc
    WHERE 
        mb.name="Axons" AND 
        mb.id=agave.ccb.concept_from_id AND
        agave.ccb.concept_to_id=agave.actorconcept.concept_id AND
        agave.ccb.concept_to_id=ma.id AND
        agave.actorconcept.actor_id=mc.id
    group by mc.name;
    """
    """
    | Neurons                 | Aebischer Patrick P       |
    | Neurons                 | Amarir S S                |
    | Cell Surface Extensions | Amigorena Sebastian S     |
    """
    query_count = """
SELECT count(ma.name), mc.name, ma.name
    FROM agave.ccb, 
        agave.actorconcept,
        agave.concept as ma,
        agave.concept as mb,
        agave.actor as mc
    WHERE 
        mb.name="Axons" AND 
        mb.id=agave.ccb.concept_from_id AND
        agave.ccb.concept_to_id=agave.actorconcept.concept_id AND
        agave.ccb.concept_to_id=ma.id AND
        agave.actorconcept.actor_id=mc.id
    group by mc.name order by count(ma.name), mc.name asc;
    """


def actors_from_broaders_from_concepts_from_actor(a):
    "AAb"
    """
    a-c->c-a, CCba U ACp or AAba
      \  \>c-a
       \c     \a
    
    aset=set()
    [[[aset.add(a) for a in br.actors.all()] for br in concept.broaders.all()] for concept in Actor.objects.get(name="Chavrier Philippe P").concepts.all()]
    
    >>>[(concept,[(br,[a for a in br.actors.all()]) for br in concept.broaders.filter(not_in_dataset=False)]) for concept in Actor.objects.get(name="Chavrier Philippe P").concepts.all()]
    ...
(<Concept: Cytoskeleton>, [(<Concept: Cytoplasmic Structures>, [])]),
 (<Concept: Antigen Presentation>,
  [(<Concept: Immunity, Cellular>,
    [<Author: Møller A P AP>,
    ...
     <Author: Pasqual Nicolas N>,
     <Author: Klatzmann David D>])]),
 (<Concept: Mutation>, [(<Concept: Variation (Genetics)>, [])]),
    
    >>> dict([(concept,dict([(br,[a for a in br.actors.all()]) for br in concept.broaders.filter(not_in_dataset=False)])) for concept in Actor.objects.get(name="Chavrier Philippe P").concepts.all()])
<Concept: Mutation>: {},
 <Concept: Microscopy, Electron>: {<Concept: Microscopy>: [<Author: Kremer Y Y>,
                                                 <Author: Léger J-F JF>,
    """
    pass

def edges_actors_from_broaders_from_concepts_from_actors_ds(pxds):
#    for aa in combinations(Actor.objects.filter(datasets = pxds), 2):
#        if set(aa[0].concepts.filter(datasets=pxds)).intersection(set(aa[1].concepts.filter(datasets=pxds))) != set([]):
#        for a_from in br.concept_from.actors.filter(datasets = pxds):
#            for a_to in br.concept_to.actors.filter(datasets = pxds):
#                if a_from != a_to and not (a_from, a_to) in AAbB:
#                AAbA.append((a_from, a_to))
    AAbA = {}
    for br in [CCb.objects.filter(datasets=pxds).filter(concept_from__not_in_dataset=False).filter(concept_to__not_in_dataset=False)[0]]:
        for a_from in br.concept_from.actors.filter(datasets=pxds):
            for a_to in br.concept_to.actors.filter(datasets=pxds):
#                if a_from != a_to and  not (a_from, a_to) in AAbA:
#                if a_from != a_to and AAbA.get(a_from.id+'-'+a_to.id, False):
                if a_from != a_to and not AAbA.get((a_from.id, a_to.id), False):
#                    AAbA[a_from.id+'-'+a_to.id] =True
                    AAbA[(a_from.id, a_to.id)] = True
#                    AAbA.append((a_from, a_to))
    return AAbA

def actors_from_broaders_from_concepts_from_actor_sql(a):
    "AAb"
    query = """
SELECT mc.name
    FROM agave.ccb, 
        agave.actorconcept as ama, 
        agave.actorconcept as amb,
        agave.actor as mb,
        agave.actor as mc
    WHERE 
        mb.name="Chavrier Philippe P" AND 
        mb.id=ama.actor_id AND
        ama.concept_id=agave.ccb.concept_from_id AND
        agave.ccb.concept_to_id=amb.concept_id AND
        amb.actor_id != mb.id AND
        amb.actor_id=mc.id;
    """
    query_count = """
SELECT count(mc.name),ma.name, mc.name 
    FROM agave.ccb, 
        agave.actorconcept as ama, 
        agave.actorconcept as amb,
        agave.concept as ma,
        agave.actor as mb,
        agave.actor as mc
    WHERE 
        mb.name="Chavrier Philippe P" AND 
        mb.id=ama.actor_id AND
        ama.concept_id=agave.ccb.concept_from_id AND
        agave.ccb.concept_to_id=amb.concept_id AND
        amb.concept_id = ma.id AND
        amb.actor_id != mb.id AND
        amb.actor_id=mc.id 
    group by mc.name order by count(mc.name) desc, mc.name asc;
    """
    """
|              1 | Membrane Proteins                             | Zatsepina O V OV                          |
|              1 | Animals                                       | Zirpe Milind M        
    """
    #wrong
    query_without_CCa = """
SELECT count(mc.name),ma.name, mc.name 
    FROM agave.ccb, 
        agave.actorconcept as ama, 
        agave.actorconcept as amb,
        agave.concept as ma,
        agave.actor as mb,
        agave.actor as mc
    WHERE 
        mb.name="Chavrier Philippe P" AND 
        mb.id=ama.actor_id AND
        ama.concept_id=agave.ccb.concept_from_id AND
        agave.ccb.concept_to_id=amb.concept_id AND
        amb.concept_id = ma.id AND
        amb.actor_id=mc.id AND
        amb.auhor_id NOT IN
            (select distinct ma.id
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
        amc.actor_id = ma.id)
    group by mc.name order by count(mc.name) desc, mc.name asc;
    """

def narrowers_from_concept(c):
    """
    c<-c, CCba
      <\c
    
    [na.concept_from for na in Concept.objects.get(name="Cells").is_broader_of.all()]
    
    other way:
    [Concept.objects.get(id=br.concept_from.id) for br in CCb.objects.filter(concept_to__name="Cells")]
    
    other way:
    [(br.concept_from.id, br.concept_from.name) for br in CCb.objects.filter(concept_to__name="Cells")]
    
    other way:
    concept(c).concept_set.all()
    """
    return  [na.concept_from for na in concept(c).is_broader_of.filter(concept_from__not_in_dataset=False)]

def narrowers_from_concept_sql(c):
    query = """
SELECT agave.ccb.concept_from_id, 
        b.name 
        FROM agave.ccb, 
            agave.concept as a,
            agave.concept as b 
        WHERE 
            a.name="%s" AND 
            a.id=agave.ccb.concept_to_id AND
            b.id=agave.ccb.concept_from_id;
    """
    cursor = connection.cursor()
    cursor.execute(query, [c])
    rows = cursor.fetchall()
    return rows

def narrowers_from_concept_not_transitive():
    """
    c<-!c<-c, CCba
      \------/
    """



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

def actors_weight_from_narrowers_from_concept_ds(c, pxds):
    return dict([(br, [(aconcepts.actor, aconcepts.weight) for aconcepts in ActorConcept.objects.filter(concept=br.concept_from, dataset=pxds)]) for  br in CCb.objects.filter(concept_to=concept(c), datasets=pxds)])

def actors_from_narrowers_from_concepts_from_actor():
    """
    a-c<-c-a, CCba U ACp or AAba
      \  <\c-a
       \c     \a
    """

def is_narrower_from_broaders_from_concept(c1, c2):
    """
    def concepts_with_broaders_in_common(c1,c1):
    """
    pass

def is_narrower_from_broaders_from_concept_ds(c1, c2, pxds):
    if set(c1.broaders.filter(datasets=pxds)).intersection(set(c2.broaders.filter(datasets=pxds))):
        return True
    else: return False


def is_actor_from_narrowers_from_broaders_from_concepts_from_actor_ds(a, b, pxds):
#    if CCb.objects.filter(datasets = pxds).filter(concept_from = a)
    for concepta in a.concepts.filter(datasets=pxds):
        for conceptb in a.concepts.filter(datasets=pxds):
            if is_narrower_from_broaders_from_concept_ds(concepta, conceptb, pxds):
                return True
    return False

def broaders_from_narrowers_from_concept():
    """
    c<-c->c, CCba U ACp or CCbc
      <\c->c
            \>c
    """
    pass

def broaders_from_narrowers_from_concepts_from_actor():
    """
    a-c<-c->c, CCba U ACp or CCbc U ACp
      \  <\c->c
       \c<-c->c     
    """
    pass

def actors_from_broaders_from_narrowers_from_concepts_from_actor():
    """
    a-c<-c->c-a, CCba U ACp or AAbc
      \  <\c->c-a
       \c<-c     \a
    """
    pass

def actors_from_broaders_from_narrowers_from_concepts_from_actor_sql(a):
    query = """
SELECT ab.name
    FROM agave.ccb, 
        agave.actorconcept as ama, 
        agave.actorconcept as amb,
        agave.actor as aa,
        agave.actor as ab,
        agave.ccb as bra,
        agave.ccb as brb
    WHERE 
        aa.name="Chavrier Philippe P" AND 
        aa.id=ama.actor_id AND
        ama.concept_id=bra.concept_to_id AND
        bra.concept_from_id=brb.concept_from_id AND
        brb.concept_to_id=amb.concept_id AND
        amb.actor_id != aa.id AND
        amb.actor_id=ab.id;
    """
    """
# 1216995 rows in set (6.50 sec)
    """

def narrowers_from_broaders_from_concept(c):
    """
    c->c<-c, CCba U ACp or CCbb
      \>c<-c
            <\c
    
    [[(<CCb: Microscopy, Fluorescence, Microscopy>,
   [<Author: Bouloussa Othman O>, ...
    """
    concept = concept(c)
    l = [[(child, child.concept_from.actors.all())
            for child in parent.is_broader_of.filter(concept_from__not_in_dataset=False).exclude(concept_from=concept)]
            for parent in concept.broaders.all()]
    return

def actors_weight_from_narrowers_from_broaders_from_concept(c):
    """
    l =  [[(child.concept_from.name, 
            [(a.name,a.actorconcept_set.filter(concept=child.concept_from)[0].weight) for a in child.concept_from.actors.order_by('-actorconcept__weight','name')]) 
            for child in parent.is_broader_of.filter(concept_from__not_in_dataset=False).exclude(concept_from = concept)] 
            for parent in concept.broaders.all()]

l =  [(parent.name,
        [(child.concept_from.name, 
            [(aconcepts.actor.name, aconcepts.weight) for aconcepts in ActorConcept.objects.filter(concept=child.concept_from).order_by('-weight','actor__name')])
            for child in parent.is_broader_of.filter(concept_from__not_in_dataset=False).exclude(concept_from = concept)]) 
            for parent in concept.broaders.all()]
    """
    d = dict([(parent.name,
        dict([(child.concept_from.name,
            [(aconcepts.actor.name, aconcepts.weight) for aconcepts in ActorConcept.objects.filter(concept=child.concept_from).order_by('-weight', 'actor__name')])
            for child in parent.is_broader_of.filter(concept_from__not_in_dataset=False).exclude(concept_from=concept)]))
            for parent in concept.broaders.all()])
    return d

def narrowers_from_broaders_from_concepts_from_actor():
    """
    a-c->c<-c, CCba U ACp or CCbb U ACp
      \  \>c<-c
       \c->c<-c     
    """
    pass

def actors_from_narrowers_from_broaders_from_concepts_from_actor():
    """
    a-c->c<-c-a, CCba U ACp or AAbb
      \  \>c<-c-a
       \c->c     \a
    """
    pass

def actors_from_narrowers_from_broaders_from_concepts_from_actor(a):
    query = """
SELECT ab.name
    FROM agave.ccb, 
        agave.actorconcept as ama, 
        agave.actorconcept as amb,
        agave.actor as aa,
        agave.actor as ab,
        agave.ccb as bra,
        agave.ccb as brb
    WHERE 
        aa.name="Chavrier Philippe P" AND 
        aa.id=ama.actor_id AND
        ama.concept_id=bra.concept_from_id AND
        bra.concept_to_id=brb.concept_to_id AND
        brb.concept_from_id=amb.concept_id AND
        amb.actor_id != aa.id AND
        amb.actor_id=ab.id;
    """
    """
# 2048865 rows in set (11.45 sec)
    """
    query_count = """
SELECT count(ab.name),ab.name
    FROM agave.ccb, 
        agave.actorconcept as ama, 
        agave.actorconcept as amb,
        agave.actor as aa,
        agave.actor as ab,
        agave.ccb as bra,
        agave.ccb as brb
    WHERE 
        aa.name="Chavrier Philippe P" AND 
        aa.id=ama.actor_id AND
        ama.concept_id=bra.concept_from_id AND
        bra.concept_to_id=brb.concept_to_id AND
        brb.concept_from_id=amb.concept_id AND
        amb.actor_id != aa.id AND
        amb.actor_id=ab.id
    group by ab.name order by ab.name asc;
    """
    """
# 177 rows in set (12.96 sec)
    """
    query_c = """
SELECT ca.name, cb.name,ab.name
    FROM agave.ccb, 
        agave.actorconcept as ama, 
        agave.actorconcept as amb,
        agave.actor as aa,
        agave.actor as ab,
        agave.ccb as bra,
        agave.ccb as brb,
        agave.concept as ca,
        agave.concept as cb
    WHERE 
        aa.name="Chavrier Philippe P" AND 
        aa.id=ama.actor_id AND
        ama.concept_id=bra.concept_from_id AND
        
        bra.concept_from_id=ca.id AND
        
        bra.concept_to_id=brb.concept_to_id AND
        brb.concept_from_id=amb.concept_id AND
        
        brb.concept_from_id=cb.id AND
        
        amb.actor_id != aa.id AND
        amb.actor_id=ab.id
    group by ca.name, cb.name, ab.name;
    """
    query_c_count = """
SELECT count(ab.name),ab.name, cb.name, ca.name
    FROM agave.ccb, 
        agave.actorconcept as ama, 
        agave.actorconcept as amb,
        agave.actor as aa,
        agave.actor as ab,
        agave.ccb as bra,
        agave.ccb as brb,
        agave.concept as ca,
        agave.concept as cb
    WHERE 
        aa.name="Chavrier Philippe P" AND 
        aa.id=ama.actor_id AND
        ama.concept_id=bra.concept_from_id AND
        
        bra.concept_from_id=ca.id AND
        
        bra.concept_to_id=brb.concept_to_id AND
        brb.concept_from_id=amb.concept_id AND
        
        brb.concept_from_id=cb.id AND
        
        amb.actor_id != aa.id AND
        amb.actor_id=ab.id
    group by ab.name;
    """

#statistics with agave.model
def aac_weighted():

    query = """
SELECT count(aac.concept_id), aac.actor_from_id, aac.concept_id, aac.actor_to_id
     FROM
         agave.aac as aac
     GROUP BY aac.actor_from_id, aac.actor_to_id
     LIMIT 10;
    """
    query = """
SELECT count(aac.concept_id), a1.name, a2.name
     FROM
         agave.aac as aac,
         agave.actor as a1,
         agave.actor as a2
     WHERE
        aac.actor_from_id = a1.id AND
        aac.actor_to_id = a2.id
     GROUP BY aac.actor_from_id, aac.actor_to_id
     LIMIT 10;
    """

def edges_actors_from_sibling():

    query = """
    SELECT c1.name, parent.name, c2.name
        FROM
            agave.concept as c1,
            agave.concept as c2,
            agave.concept as parent,
            agave.ccb as br1,
            agave.ccb as br2
        WHERE
            br1.concept_to_id=parent.id AND
            br2.concept_to_id=parent.id AND
            br2.concept_from_id= c2.id AND
            br1.concept_from_id= c1.id AND
            c2.id != c1.id
        LIMIT 40;
        """

    query = """
    SELECT a1.name, c1.name, parent.name, c2.name, a2.name
        FROM
            agave.actor as a1,
            agave.actor as a2,
            agave.actorconcept as am1,
            agave.actorconcept as am2,
            agave.concept as c1,
            agave.concept as c2,
            agave.concept as parent,
            agave.ccb as br1,
            agave.ccb as br2
        WHERE
            a1.id=am1.actor_id AND
            am1.concept_id=br1.concept_from_id AND
            br1.concept_from_id= c1.id AND
            br1.concept_to_id=parent.id AND
            br2.concept_to_id=parent.id AND
            br2.concept_from_id= c2.id AND
            c2.id != c1.id AND
            br2.concept_from_id=am2.concept_id AND
            am2.actor_id !=am1.actor_id AND
            am2.actor_id=a2.id
        GROUP BY a1.name, a2.name
        LIMIT 40;
        """

    query = """
    select count(*) 
        from 
            (SELECT distinct a1.name as A1, a2.name as A2
                FROM
                    agave.actor as a1,
                    agave.actor as a2,
                    agave.actorconcept as am1,
                    agave.actorconcept as am2,
                    agave.ccb as br1,
                    agave.ccb as br2
                WHERE
                    a1.id=am1.actor_id AND
                    am1.concept_id=br1.concept_from_id AND
                    br1.concept_to_id = br2.concept_to_id AND
                    br1.concept_from_id != br2.concept_from_id AND
                    br2.concept_from_id=am2.concept_id AND
                    am2.actor_id !=am1.actor_id AND
                    am2.actor_id=a2.id
                GROUP BY a1.name, a2.name) as AAbb
                INTO OUTFILE 'all-AAbb-2010-08-24.csv'
                FIELDS TERMINATED BY ','
                ENCLOSED BY '"'
                LINES TERMINATED BY '\n';
        """

    query = """
    select count(*) 
        from 
            (SELECT distinct am1.actor_id as A1, am2.actor_id as A2
                FROM
                    agave.actor as a1,
                    agave.actor as a2,
                    agave.actorconcept as am1,
                    agave.actorconcept as am2,
                    agave.ccb as br1,
                    agave.ccb as br2
                WHERE
                    am1.concept_id=br1.concept_from_id AND
                    br1.concept_to_id = br2.concept_to_id AND
                    br1.concept_from_id != br2.concept_from_id AND
                    br2.concept_from_id=am2.concept_id AND
                    am2.actor_id !=am1.actor_id
                GROUP BY a1.name, a2.name) as AAbb
                INTO OUTFILE '/home/janaya/agave_prj/site_media/static/all-AAbb-2010-08-24.csv'
                FIELDS TERMINATED BY ','
                LINES TERMINATED BY '\n';
        """

    """
SELECT
    FROM 
        `agave.concept` INNER JOIN `agave.ccb` ON (`agave.concept`.`id` = `agave.ccb`.`concept_to_id`) 
    WHERE 
        `agave.ccb`.`concept_from_id` =
    """

def edges_AAbc():
    query = """
    select count(*) 
        from 
            (SELECT distinct am1.actor_id as A1, am2.actor_id as A2
                FROM
                    agave.actor as a1,
                    agave.actor as a2,
                    agave.actorconcept as am1,
                    agave.actorconcept as am2,
                    agave.ccb as br1,
                    agave.ccb as br2
                WHERE
                    am1.concept_id=br1.concept_to_id AND
                    br1.concept_from_id = br2.concept_from_id AND
                    br1.concept_to_id != br2.concept_to_id AND
                    br2.concept_to_id=am2.concept_id AND
                    am2.actor_id !=am1.actor_id
                GROUP BY a1.name, a2.name) as AAbc
                INTO OUTFILE '/home/janaya/agave_prj/site_media/static/all-AAbc-2010-08-24.csv'
                FIELDS TERMINATED BY ','
                LINES TERMINATED BY '\n';
        """
def edges_AAbc():
    query = """
    select count(*) 
        from 
            (SELECT distinct am1.actor_id as A1, am2.actor_id as A2
                FROM
                    agave.actor as a1,
                    agave.actor as a2,
                    agave.actorconcept as am1,
                    agave.actorconcept as am2,
                    agave.ccb as br1,
                    agave.ccb as br2
                WHERE
                    am1.concept_id=br1.concept_to_id AND
                    br1.concept_from_id = br2.concept_from_id AND
                    br1.concept_to_id != br2.concept_to_id AND
                    br2.concept_to_id=am2.concept_id AND
                    am2.actor_id !=am1.actor_id
                GROUP BY a1.name, a2.name) as AAbc
                INTO OUTFILE '/home/janaya/agave_prj/site_media/static/all-AAbc-2010-08-24.csv'
                FIELDS TERMINATED BY ','
                LINES TERMINATED BY '\n';
        """
def edges_AAbbc():
    query = """
    select count(*) 
        from 
            (SELECT distinct am1.actor_id as A1, am2.actor_id as A2
                FROM
                    agave.actor as a1,
                    agave.actor as a2,
                    agave.actorconcept as am1,
                    agave.actorconcept as am2,
                    agave.ccb as br1,
                    agave.ccb as br2
                WHERE
                    (am1.concept_id=br1.concept_to_id AND
                    br1.concept_from_id = br2.concept_from_id AND
                    br1.concept_to_id != br2.concept_to_id AND
                    br2.concept_to_id=am2.concept_id AND
                    am2.actor_id !=am1.actor_id) OR
                    (am1.concept_id=br1.concept_to_id AND
                    br1.concept_from_id = br2.concept_from_id AND
                    br1.concept_to_id != br2.concept_to_id AND
                    br2.concept_to_id=am2.concept_id AND
                    am2.actor_id !=am1.actor_id) OR
                    (am1.concept_id=br1.concept_from_id AND
                    br1.concept_to_id=am2.concept_id AND
                    am2.actor_id !=am1.actor_id)
                    
                GROUP BY a1.name, a2.name) as AAbabc
                INTO OUTFILE '/home/janaya/agave_prj/site_media/static/all-AAbabc-2010-08-24.csv'
                FIELDS TERMINATED BY ','
                LINES TERMINATED BY '\n';
        """

def edges_AAp():
    query = """
select count(*) 
    from 
        (SELECT distinct agave.aap .actor_from_id as A1, agave.aap .actor_to_id as A2
            FROM
                agave.aap
            GROUP BY A1,A2) as AAp;
"""
"""
SELECT count(distinct agave.aap .actor_from_id,agave.aap .actor_to_id) as w, agave.aap .actor_from_id as A1, agave.aap .actor_to_id as A2
             FROM
                 agave.aap
             GROUP BY A1,A2;
"""
"""
SELECT count(agave.aap.actor_from_id,agave.aap.actor_to_id) as w, agave.aap.actor_from_id as A1, agave.aap.actor_to_id as A2
             FROM
                 agave.aap
             GROUP BY A1,A2;
"""
"""
SELECT actor_from_id as A1, actor_to_id as A2
             FROM
                 agave.aap
             GROUP BY A1,A2;
"""

#################################
#Instance.objects.filter(instance__in=Instance.objects.filter(year='2009')).count()
#Out[45]: 4389

#Actor.objects.filter(instances__in=Instance.objects.filter(year='2009')).count()
#Out[44]: 2853


################################

import codecs

def generate_C_names_csv():
    f = codecs.open(settings.MEDIA_ROOT + '/static/' + "all-C-names-20100813.csv", "w", encoding="utf-8")
    f.write("index;name\n")
    for m in Concept.objects.filter(not_in_dataset=False):
        f.write(str(m.id) + ";" + m.__unicode__() + "\n")
    f.close()

def generate_K_names_csv():
    f = codecs.open(settings.MEDIA_ROOT + '/static/' + "all-K-names-20100813.csv", "w", encoding="utf-8")
    f.write("index;name\n")
    for m in Concept.objects.all():
        f.write(str(m.id) + ";" + m.__unicode__() + "\n")
    f.close()

def generate_K_C_names_csv():
    f = codecs.open(settings.MEDIA_ROOT + '/static/' + "all-K-c-names-20100813.csv", "w", encoding="utf-8")
    for m in Concept.objects.filter(not_in_dataset=True):
        f.write(str(m.id) + ";" + m.__unicode__() + "\n")
    f.close()

def generate_A_names_csv():
    f = codecs.open(settings.MEDIA_ROOT + '/static/' + "all-A-names-20100813.csv", "w", encoding="utf-8")
    f.write("index;name\n")
    for a in Actor.objects.all():
#        f.write(str(a.id)+","+a.__unicode__()+"\n")
        f.write(str(a.id) + ";" + a.__unicode__() + "\n")
    f.close()

def generate_CCb_csv():
    f = codecs.open(settings.MEDIA_ROOT + '/static/' + "all-CCb-20100813.csv", "w", encoding="utf-8")
    for ccb in  CCb.objects.filter(not_in_dataset=True):
        f.write("C" + str(ccb.concept_from.id) + ",C" + str(ccb.concept_to.id) + "\n")
    f.close()

def generate_KKb_csv():
    f = codecs.open(settings.MEDIA_ROOT + '/static/' + "all-KKb-20100813.csv", "w", encoding="utf-8")
    for ccb in  CCb.objects.all():
        f.write('"C' + str(ccb.concept_from.id) + '","C' + str(ccb.concept_to.id) + '"\n')
    f.close()

def generate_AC_csv():
#    f = codecs.open(settings.MEDIA_ROOT + '/static/' + "all-AAcw-20100813.csv","w",encoding="utf-8")
    f = open(settings.MEDIA_ROOT + '/static/' + "all-AC-20100813.csv", "w")
    f.write("A,C,w\n")
    ac = "\n".join(['"A%(actor__id)s", "C%(concept__id)s", %(weight)s' % a for a in ActorConcept.objects.values('actor__id', 'concept__id', 'weight').order_by('actor__id', 'concept__id')])
#    for aconcepts in ActorConcept.objects.all():
#        f.write('"A'+str(aconcepts.actor.id)+'","C'+str(aconcepts.concept.id)+'",'+str(aconcepts.weight)+'\n')
    f.write(ac)
    f.close()

def generate_AP_csv():
    f = open(settings.MEDIA_ROOT + '/static/' + "all-AP-20100825.csv", "w")
    f.write("A,P,w\n")
    ac = "\n".join(['"A%(actor__id)s", "C%(instance__id)s", %(weight)s' % a for a in InstanceActor.objects.values('actor__id', 'instance__id', 'weight').order_by('actor__id', 'instance__id')])
    f.write(ac)
    f.close()

def generate_AAcw_csv():
#    f = codecs.open(settings.MEDIA_ROOT + '/static/' + "all-AAcw-20100813.csv","w",encoding="utf-8")
    f = open(settings.MEDIA_ROOT + '/static/' + "all-AAcw-20100813.csv", "w")
    f.write("A1,A2,w\n")
    for aacw in AAcw.objects.all():
        f.write('"A' + str(aacw.actor_from.id) + '","A' + str(aacw.actor_to.id) + '",' + str(aacw.weight) + '\n')
    f.close()

def generate_AAp_csv():
    pass
# In [35]: ActorConcept.objects.aggregate(Max('weight'))
#Out[35]: {'weight__max': 482}

################3

def n_p():
    return Instance.objects.count()

def n_a():
    return Actor.objects.count()

def n_c():
    return Concept.objects.exclude(not_in_dataset=True).count()

def n_c_notinds():
    return Concept.objects.count()

def avg_a_p():
    return n_a() / n_p()

def avg_a_p(na, np):
    return float(na) / np

def avg_c_p():
    return n_c() / n_p()

def avg_c_p(nc, np):
    return float(nc) / np

def avg_c_a():
    return n_c() / n_a()

def avg_c_a(nc, na):
    return float(nc) / na

def avg_a_c():
    return n_a() / n_c()

def avg_a_c(na, nc):
    return float(na) / nc

def n_ac():
    ActorConcept.objects.count()

def n_aap():
    AAp = set()
    for p in Instance.objects.all():
        for a_from, a_to in combinations([a for a in p.actors.all()], 2):
            if (a_to, a_from) not in AAp and a_to != a_from:
                AAp.add((a_from, a_to))
    return len(AAp)

def n_ccp():
    CCp = set()
    for p in Instance.objects.all():
        for c_from, c_to in combinations([c for c in p.concepts.all()], 2):
            if (c_to, c_from) not in AAp and c_to != c_from:
                CCp.add((c_from, c_to))
    return len(CCp)

def perc_a_b(a, b):
    return float(a) / b * 100

def cca():
#    return CCa.objects.values('concept_from','concept_to').distinct().count()
    cca = list(CCa.objects.values('concept_from', 'concept_to').distinct())
#    new_cca = [ccae for ccae in cca if not {'concept_to':ccae['concept_from'], 'concept_from': ccae['concept_to']} in cca]
#    return new_cca
    [cca.remove({'concept_to':ccae['concept_from'], 'concept_from': ccae['concept_to']}) for ccae in cca  if {'concept_to':ccae['concept_from'], 'concept_from': ccae['concept_to']} in cca]
    return cca

def n_cca():
#    return CCa.objects.values('concept_from','concept_to').distinct().count()
    cca = CCa.objects.values('concept_from', 'concept_to').distinct()
    new_cca = [ccae for ccae in cca if not {'concept_to':ccae['concept_from'], 'concept_from': ccae['concept_to']} in cca]
    return new_cca

def n_cca(cca):
    return len(cca)

def aac():
#    return AAc.objects.values('actor_from','actor_to').distinct().count()
    aac = list(AAc.objects.values('actor_from', 'actor_to').distinct())
#    new_aac = [aace for aace in aac if not {'actor_to':aace['actor_from'], 'actor_from': aace['actor_to']} in aac]
#    return new_aac
    [aac.remove({'actor_to':aace['actor_from'], 'actor_from': aace['actor_to']}) for aace in aac if {'actor_to':aace['actor_from'], 'actor_from': aace['actor_to']} in aac]
    return aac

def n_aac():
#    return AAc.objects.values('actor_from','actor_to').distinct().count()
    aac = AAc.objects.values('actor_from', 'actor_to').distinct()
    new_aac = [aace for aace in aac if not {'actor_to':aace['actor_from'], 'actor_from': aace['actor_to']} in aac]
    return len(new_aac)

def n_aac(aac):
    return len(aac)

def max_AC():
    return n_a()*n_c()

def max_AC(na, nc):
    return na * nc

def max_AA():
    return n_a()*(n_a() - 1) / 2

def max_AA(na):
    return na * (na - 1) / 2

def max_CC():
    return n_c()*(n_c() - 1) / 2

def max_CC(nc):
    return nc * (nc - 1) / 2

def max_CC_notinds():
    return n_c_notinds()*(n_c_notinds() - 1) / 2

def max_CC_notinds(nc_notinds):
    return nc_notinds * (nc_notinds - 1) / 2


def ccba():
    return CCb.objects.exclude(concept_from__not_in_dataset=True).exclude(concept_to__not_in_dataset=True)

def n_ccba():
#    return CCb.objects.exclude(concept_from__not_in_dataset=True).exclude(concept_to__not_in_dataset=True).count()
    ccba = CCb.objects.exclude(concept_from__not_in_dataset=True).exclude(concept_to__not_in_dataset=True)
    return len(ccba)

def n_ccba(ccba):
    return len(ccba)

def ccbb():
#    return CCbb.objects.values('concept_from', 'concept_to').distinct()
    ccbb = list(CCbb.objects.values('concept_from', 'concept_to').distinct())
    [ccbb.remove({'concept_to':ccbbe['concept_from'], 'concept_from': ccbbe['concept_to']}) for ccbbe in ccbb if {'concept_to':ccbbe['concept_from'], 'concept_from': ccbbe['concept_to']} in ccbb]
    return ccbb

def n_ccbb(ccbb):
    return len(ccbb)

def ccbc():
#    return CCbc.objects.values('concept_from', 'concept_to').distinct()
    ccbc = list(CCbc.objects.values('concept_from', 'concept_to').distinct())
    [ccbc.remove({'concept_to':ccbbe['concept_from'], 'concept_from': ccbbe['concept_to']}) for ccbbe in ccbc if {'concept_to':ccbbe['concept_from'], 'concept_from': ccbbe['concept_to']} in ccbc]
    return ccbc

def n_ccbc(ccbc):
    return len(ccbc)

def n_aaba():
    return AAba.objects.values('actor_from', 'actor_to').distinct().count()

def aaba():
    aaba = list(AAba.objects.values('actor_from', 'actor_to').distinct())
#    new_aaba = [aabae for aabae in aaba if not {'actor_to':aabae['actor_from'], 'actor_from': aabae['actor_to']} in aaba]
#    return new_aaba
    [aaba.remove({'actor_to':aabae['actor_from'], 'actor_from': aabae['actor_to']}) for aabae in aaba if {'actor_to':aabae['actor_from'], 'actor_from': aabae['actor_to']} in aaba]
    return aaba

def n_aaba(aaba):
    return len(aaba)

def n_aabb():
    return AAbb.objects.values('actor_from', 'actor_to').distinct().count()

def aabb():
    aabb = list(AAbb.objects.values('actor_from', 'actor_to').distinct())
#    new_aabb = [aabbe for aabbe in aabb if not {'actor_to':aabbe['actor_from'], 'actor_from': aabbe['actor_to']} in aabb]
#    return new_aabb
    [aabb.remove({'actor_to':aabbe['actor_from'], 'actor_from': aabbe['actor_to']}) for aabbe in aabb if {'actor_to':aabbe['actor_from'], 'actor_from': aabbe['actor_to']} in aabb]
    return aabb

def n_aabb(aabb):
    return len(aabb)

def n_aabc():
    return AAbc.objects.values('actor_from', 'actor_to').distinct().count()

def aabc():
#    aabc = AAbc.objects.values('actor_from', 'actor_to').distinct()
#    new_aabc = [aabce for aabce in aabc if not {'actor_to':aabce['actor_from'], 'actor_from': aabce['actor_to']} in aabc]
    aabc = list(AAbc.objects.values('actor_from', 'actor_to').distinct())
    new_aabc = [aabc.remove({'actor_to':aabce['actor_from'], 'actor_from': aabce['actor_to']}) for aabce in aabc if {'actor_to':aabce['actor_from'], 'actor_from': aabce['actor_to']} in aabc]
    return aabc

def n_aabc(aabc):
    return len(aabc)


def new_ccba_cca():
#    a = [(,),(,)]
#    b = [(,),(,)]
#    [(x,y) fro x,y in a if not (((x,y) in b) or ((y,x) in b))]

    cca = CCa.objects.values('concept_from', 'concept_to').distinct()
#    new_cca = [ccae for ccae in cca if not {'concept_to':ccae['concept_from'], 'concept_from': ccae['concept_to']} in cca]
    ccba = CCb.objects.exclude(concept_from__not_in_dataset=True).exclude(concept_to__not_in_dataset=True).values('concept_from', 'concept_to')
    new_ccba = [ccbae for ccbae in ccba if {'concept_from':ccbae['concept_to'], 'concept_to':ccbae['concept_from']} not in cca and {'concept_from':ccbae['concept_from'], 'concept_to':ccbae['concept_to']} not in cca]
    return len(new_ccba)

def new_ccba_cca(ccba, cca):
    ccba = ccba.values('concept_from', 'concept_to')
    new_ccba = [ccbae for ccbae in ccba if {'concept_from':ccbae['concept_to'], 'concept_to':ccbae['concept_from']} not in cca and ccbae not in cca]
    return new_ccba

def n_new_ccba_cca(new_ccba):
    return len(new_ccba)

def new_ccbb_cca():
    cca = CCa.objects.values('concept_from', 'concept_to').distinct()
#    new_cca = [ccae for ccae in cca if not {'concept_to':ccae['concept_from'], 'concept_from': ccae['concept_to']} in cca]
    ccbb = CCbb.objects.values('concept_from', 'concept_to').distinct()
    new_ccba = [ccbae for ccbae in ccbb if {'concept_from':ccbae['concept_to'], 'concept_to':ccbae['concept_from']} not in cca and {'concept_from':ccbae['concept_from'], 'concept_to':ccbae['concept_to']} not in cca]
    return len(new_ccba)

def new_ccbb_cca(ccbb, cca):
    new_ccbb = [ccbae for ccbae in ccbb if {'concept_from':ccbae['concept_to'], 'concept_to':ccbae['concept_from']} not in cca and ccbae not in cca]
    return new_ccbb

def n_new_ccbb_cca(new_ccbb):
    return len(new_ccbb)

def new_ccbc_cca():
    cca = CCa.objects.values('concept_from', 'concept_to').distinct()
#    new_cca = [ccae for ccae in cca if not {'concept_to':ccae['concept_from'], 'concept_from': ccae['concept_to']} in cca]
    ccbc = CCbc.objects.values('concept_from', 'concept_to').distinct()
    CCb.objects.exclude(concept_from__not_in_dataset=True).exclude(concept_to__not_in_dataset=True).values('concept_from', 'concept_to')
    new_ccba = [ccbae for ccbae in ccba if {'concept_from':ccbae['concept_to'], 'concept_to':ccbae['concept_from']} not in cca and {'concept_from':ccbae['concept_from'], 'concept_to':ccbae['concept_to']} not in cca]
    return len(new_ccba)

def new_ccbc_cca(ccbc, cca):
    new_ccbc = [ccbae for ccbae in ccbc if {'concept_from':ccbae['concept_to'], 'concept_to':ccbae['concept_from']} not in cca and ccbae not in cca]
    return new_ccbc

def n_new_ccbc_cca(new_ccbc):
    return len(new_ccbc)

def new_aaba_aac(aaba, aac):
    new_aaba = [ccbae for ccbae in aaba if {'actor_from':ccbae['actor_to'], 'actor_to':ccbae['actor_from']} not in aac and ccbae not in aac]
    return new_aaba

def n_new_aaba_aac(new_aaba):
    return len(new_aaba)

def new_aabb_aac(aabb, aac):
    new_aabb = [ccbae for ccbae in aabb if {'actor_from':ccbae['actor_to'], 'actor_to':ccbae['actor_from']} not in aac and ccbae not in aac]
    return new_aabb

def n_new_aabb_aac(new_aabb):
    return len(new_aabb)

def new_aabc_aac(aabc, aac):
    new_aabc = [ccbae for ccbae in aabc if {'actor_from':ccbae['actor_to'], 'actor_to':ccbae['actor_from']} not in aac and ccbae not in aac]
    return new_aabc

def n_new_aabc_aac(new_aabc):
    return len(new_aabc)


def n_ccba_wotrans():
    return CCb.objects.exclude(concept_from__not_in_dataset=True).exclude(concept_to__not_in_dataset=True).count()

def n_ccbb_wotrans():
    return CCbb.objects.values('concept_from', 'concept_to').distinct().count()

def n_ccbc_wotrans():
    return CCbc.objects.values('concept_from', 'concept_to').distinct().count()

def n_aaba_wotrans():
    return AAba.objects.values('actor_from', 'actor_to').distinct().count()

def n_aabb_wotrans():
    return AAba.objects.values('actor_from', 'actor_to').distinct().count()

def n_aabc_wotrans():
    return AAba.objects.values('actor_from', 'actor_to').distinct().count()


"""
import csv
from collections import defaultdict
f = open('../rdhi2/AAb_comm.csv','rb')
d = csv.reader(f, delimiter=';')
l = [(com,name) for _,com,name  in d]
l.remove(('cluster', 'name'))
f.close()
dict_com = defaultdict(list)
[dict_com[com].append(name) for com,name  in l]
inter_set = set([])

#[Actor.objects.get(name=unicode(a,'utf-8')).concepts.all() for a in dict_com['0']]
#[inter_set.intersection_update(Actor.objects.get(name=unicode(a,'utf-8')).concepts.all()) for a in dict_com['0']]


from django.core.exceptions import ObjectDoesNotExist

com_sets = defaultdict(list)
for com_key in dict_com.keys():
    inter_set = set([])
    for a in dict_com[com_key]:
        try:
            new_set = set([concept.name for concept in Actor.objects.get(name=unicode(a,'utf-8')).concepts.all()])
        except ObjectDoesNotExist: 
            print unicode(a,'utf-8')
        if not inter_set: inter_set = new_set
        else: inter_set.intersection_update(new_set)
    com_sets[com_key]=inter_set

original_com_sets = com_sets.copy()
for com_key in com_sets.keys():
    [com_sets[com_key].difference_update(com_sets[i]) for i in set(com_sets.keys()).difference(com_key)]

com_broaders = defaultdict(list)
for com_key in com_sets.keys():
    broaders = set([])
    for c in com_sets[com_key]:
        b = set([concept.name for concept in Concept.objects.get(name=c).broaders.all()])
#        if not broaders: broaders = b
        broaders = broaders.union(b)
    com_broaders[com_key]=broaders

"""


"""
In [267]: com_sets
Out[267]: defaultdict(<type 'list'>, {'1': set([u'Humans', u'Female']), '0': set([u'Polymorphism, Single Nucleotide', u'Melanoma', u'Risk Assessment', u'Genetic Predisposition to Disease', u'Uveal Neoplasms', u'Humans', u'Monosomy', u'Chromosomes, Human, Pair 3', u'DNA, Neoplasm', u'Oligonucleotide Array Sequence Analysis', u'Comparative Genomic Hybridization', u'Gene Expression Profiling', u'Cluster Analysis', u'Liver Neoplasms']), '3': set([u'Proportional Hazards Models', u'Humans', u'Retrospective Studies', u'Female', u'Follow-Up Studies']), '2': set([u'Models, Theoretical', u'Thrombolytic Therapy', u'Spectrum Analysis', u'Muscle, Skeletal', u'Models, Neurological', u'Elasticity Imaging Techniques', u'Models, Statistical', u'Magnetic Resonance Imaging', u'Reproducibility of Results', u'Ultrasonic Therapy', u'Ultrasonography, Doppler, Transcranial', u'Equipment Design', u'Viscosity', u'Fibrinolytic Agents', u'Artifacts', u'Liver', u'Tissue Plasminogen Activator', u'Sonication', u'Phantoms, Imaging', u'Cerebral Hemorrhage', u'Image Enhancement', u'Image Interpretation, Computer-Assisted', u'Models, Biological', u'Equipment Failure Analysis', u'Algorithms', u'Signal Processing, Computer-Assisted', u'Sensitivity and Specificity', u'Ultrasonography, Mammary', u'Feasibility Studies', u'Humans', u'Elasticity', u'Ultrasonography, Doppler, Color', u'Stroke', u'Computer-Aided Design', u'Female', u'Rheology', u'Ultrasonography'])})

In [268]: original_com_sets
Out[268]: defaultdict(<type 'list'>, {'1': set([]), '0': set([u'Polymorphism, Single Nucleotide', u'Melanoma', u'Risk Assessment', u'Genetic Predisposition to Disease', u'Uveal Neoplasms', u'Monosomy', u'Chromosomes, Human, Pair 3', u'DNA, Neoplasm', u'Oligonucleotide Array Sequence Analysis', u'Comparative Genomic Hybridization', u'Gene Expression Profiling', u'Cluster Analysis', u'Liver Neoplasms']), '3': set([u'Proportional Hazards Models', u'Retrospective Studies', u'Follow-Up Studies']), '2': set([u'Models, Theoretical', u'Thrombolytic Therapy', u'Spectrum Analysis', u'Muscle, Skeletal', u'Models, Neurological', u'Elasticity Imaging Techniques', u'Models, Statistical', u'Magnetic Resonance Imaging', u'Reproducibility of Results', u'Ultrasonic Therapy', u'Ultrasonography, Doppler, Transcranial', u'Equipment Design', u'Viscosity', u'Fibrinolytic Agents', u'Artifacts', u'Liver', u'Tissue Plasminogen Activator', u'Sonication', u'Phantoms, Imaging', u'Cerebral Hemorrhage', u'Image Enhancement', u'Image Interpretation, Computer-Assisted', u'Models, Biological', u'Equipment Failure Analysis', u'Algorithms', u'Signal Processing, Computer-Assisted', u'Sensitivity and Specificity', u'Ultrasonography, Mammary', u'Feasibility Studies', u'Humans', u'Elasticity', u'Ultrasonography, Doppler, Color', u'Stroke', u'Computer-Aided Design', u'Female', u'Rheology', u'Ultrasonography'])})

In [269]: [len(com_sets[i]) for i in com_sets.keys()]
Out[269]: [2, 14, 5, 37]

In [270]: [len(original_com_sets[i]) for i in original_com_sets.keys()]
Out[270]: [0, 13, 3, 37]

In [303]: com_broaders
Out[303]: defaultdict(<type 'list'>, {'1': set([u'Antioxidants']), '0': set([u'Antioxidants', u'Oligopeptides', u'Ear Diseases', u'Nervous System', u'Morbidity', u'Merkel Cells']), '3': set([u'Antioxidants']), '2': set([u'Health Promotion', u'Rad51 Recombinase', u'Genetic Vectors', u'Protein Biosynthesis', u'Lipids', u'Siblings', u'DNA-Binding Proteins', u'Antioxidants', u'Protein Structure, Secondary', u'Copper', u'Case-Control Studies', u'Reflex, Monosynaptic', u'Sequence Analysis, RNA', u'Simian Acquired Immunodeficiency Syndrome', u'Inflammation', u'Body Mass Index', u'Thorax', u'Posture'])})

"""

"""
[len(com_broaders[i]) for i in com_broaders.keys()]

[[str(j )for j in com_sets[i]] for i in com_sets.keys()]

for i in com_sets.keys():
    print i
    for j in com_sets[i]:
        print j

"""
