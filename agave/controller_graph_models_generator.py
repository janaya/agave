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

from agave.models import *
try:
    from itertools import combinations
except ImportError:
#    from utils import combinations
    print "python 2.6 is required"

##############################################################################
# CI
##############################################################################

def create_CI_from_I(p, concepts, db='default'):
        weight = 1
        for concept in concepts:
            concept, created = Concept.objects.using(db).get_or_create(name=concept)
            if created: logging.debug("Created C: " + concept)

            pconcept, created = InstanceConcept.objects.using(db).get_or_create(instance=p, concept=concept, weight=weight)
            if created: logging.debug("Created CI: " + pconcept.__unicode__())

def delete_CI_from_I(p, db='default'):
#    [pc.delete() for pc in p.instanceconcept_set.using(db).all()]
    for pc in p.instanceconcept_set.using(db).all():
        logging.debug("Deleted CI: " + pc.__unicode__())
        pc.delete()
##############################################################################
# AI ?
##############################################################################

#def delete_AsI_from_I(p, db='default'):
#    [pa.delete() for pa in p.instanceactor_set.using(db).all()]

##############################################################################
# AAi
##############################################################################
def create_AAp_from_I_A(a, p, db="default"):
    for a_to in p.actors.using(db).exclude(id=a.id):
        if not AAp.objects.using(db).filter(actor_to=a,
                                  actor_from=a_to,
                                  instance=p):
            aap, created = AAp.objects.using(db).get_or_create(actor_from=a,
                                                     actor_to=a_to,
                                                     instance=p)
            if created: logging.debug("Created AAp: " + aap.__unicode__())
            else: logging.debug("Exists AAp: " + aap.__unicode__())

def delete_AAp_from_I(p, db='default'):
    [aap.delete() for aap in p.AA_instance.all()]

def delete_AAp_from_I_A(p, a, db='default'):
#    [aap.delete() for aap in AAp.objects.using(db).filter(instance=p,
#                                                          actor_from=a)]
#    [aap.delete() for aap in AAp.objects.using(db).filter(instance=p,
#                                                          actor_to=a)]
    for aap in AAp.objects.using(db).filter(instance=p, actor_from=a):
        logging.debug("Deleted AAp: " + aap.__unicode__())
        aap.delete()
    for aap in AAp.objects.using(db).filter(instance=p, actor_to=a):
        logging.debug("Deleted AAp: " + aap.__unicode__())
        aap.delete()

##############################################################################
# CCi
##############################################################################

def create_CCp_from_I(c, p, db='default'):
    for c_to in p.concepts.using(db).exclude(id=c.id):
        if not CCp.objects.using(db).filter(concept_from=c_to,
                                  concept_to=c,
                                  instance=p):
            ccp, created = CCp.objects.using(db).get_or_create(concept_from=c,
                                                     concept_to=c_to,
                                                     instance=p)
            if created: logging.debug("Created CCp: " + ccp.__unicode__())
            else: logging.debug("Exists CCp: " + ccp.__unicode__())

def generate_CCp(p, db='default'):
#    [CCp.objects.using(db).get_or_create(concept_from=cc[0], 
#                                            concept_to=cc[1], instance=p)\
#            for cc in combinations(p.concepts.all(), 2)]
    for cc in combinations(p.concepts.all(), 2):
        ccp, created = CCp.objects.using(db).get_or_create(concept_from=cc[0],
                                                          concept_to=cc[1],
                                                          instance=p)
        if created: logging.debug("Created CCp: " + ccp.__unicode__())
        else: logging.debug("Exists CCp: " + ccp.__unicode__())


def delete_CCp_from_I(p, db='default'):
#    [ccp.delete() for ccp in p.CCp_Instance.using(db).all()]
    for ccp in p.CCp_Instance.using(db).all():
        logging.debug("Deleted CCp: " + ccp.__unicode__())
        ccp.delete()

def delete_CCp_from_I_C(p, c, db='default'):
#    [ccp.delete() for ccp in CCp.objects.using(db).filter(instance=p,
#                                                          concept_to=c)]
#    [ccp.delete() for ccp in CCp.objects.using(db).filter(instance=p,
#                                                          concept_from=c)]
    for ccp in CCp.objects.using(db).filter(instance=p, concept_to=c):
        logging.debug("Deleted CCp: " + ccp.__unicode__())
        ccp.delete()
    for ccp in CCp.objects.using(db).filter(instance=p, concept_from=c):
        logging.debug("Deleted CCp: " + ccp.__unicode__())
        ccp.delete()

##############################################################################
# AC
##############################################################################

def create_AC_from_A_C(a, concept, db='default'):
    aconcepts = ActorConcept.objects.using(db).filter(actor=a, concept=concept)
    if aconcepts:
#            print "\nActor " + a.name +" put the same concept " + concept.name
        aconcept = aconcepts[0]
        aconcept.weight += 1
        aconcept.save()
        logging.debug("AC.weight++: " + aconcept.__unicode__())
    else:
        aconcept = ActorConcept.objects.using(db).create(actor=a, concept=concept, weight=1)
        logging.debug("Created AC: " + aconcept.__unicode__())

def create_AC_from_A_I(a, p, db='default'):
    for concept in p.concepts.using(db).all():
        create_AC_from_A_C(a, concept, db)

def create_AC_from_C_I(c, p, db='default'):
    for actor in p.actors.using(db).all():
        create_AC_from_A_C(actor, c, db)

def delete_AC_from_I(p, db='default'):
#    for a in p.actors.all():     
#        for c in p.concepts.all():
#            ac = ActorConcept.objects.using(db).get(actor=a,concept=c)
    actors = p.actors.using(db).all()
    concepts = p.concepts.using(db).all()
    for ac in ActorConcept.objects.using(db).get(actor__in=actors,
                                               concept__in=concepts):
        if ac.weight > 1:
            ac.weight -= 1
            ac.save()
            logging.debug("AC.weight--: " + ac.__unicode__())
        else:
            logging.debug("Deleted AC: " + ac.__unicode__())
            ac.delete()

def delete_AC_from_I_A(p, a, db='default'):
    concepts = p.concepts.using(db).all()
    for ac in ActorConcept.objects.using(db).filter(actor=a, concept__in=concepts):
        if ac.weight > 1:
            ac.weight -= 1
            ac.save()
            logging.debug("AC.weight--: " + ac.__unicode__())
        else:
            logging.debug("Deleted AC: " + ac.__unicode__())
            ac.delete()
#        psc = set(ac.concept.instance_set.using(db).exclude(id=p.id))
#        psa = set(a.instances.using(db).exclude(id=p.id))
#        if not psa.intersection(psc).intersection(psa):
#            ac.delete()

def delete_AC_from_I_C(p, c, db='default'):
    actors = p.actors.using(db).all()
    for ac in ActorConcept.objects.using(db).filter(actor__in=actors, concept=c):
        if ac.weight > 1:
            ac.weight -= 1
            ac.save()
            logging.debug("AC.weight--: " + ac.__unicode__())
        else:
            logging.debug("Deleted AC: " + ac.__unicode__())
            ac.delete()
##############################################################################
# CCa
##############################################################################

def create_CCa_from_A_I(a, p, db="default"):
    """
    see generate_CCa
    """
    for concept_from, concept_to in combinations(p.concepts.using(db).all(), 2):
        if not CCa.objects.using(db).filter(concept_from=concept_to,
                                            concept_to=concept_from,
                                            actor=a):
            cca, created = CCa.objects.using(db).get_or_create(
                                                    concept_from=concept_from,
                                                    concept_to=concept_to,
                                                    actor=a)
            if created: logging.debug("Created CCa: " + cca.__unicode__())
            else: logging.debug("Exists CCa: " + cca.__unicode__())

def create_CCa_from_C_I(c, p, db='default'):
    """
    see generate_CCa
    """
    for a in p.actors.using(db).all():
        for concept_to in p.concepts.using(db).all().exclude(id=c.id):
            if not CCa.objects.using(db).filter(concept_to=c,
                                                concept_from=concept_to,
                                                actor=a):
                cca, created = CCa.objects.using(db).get_or_create(
                                                        concept_from=c,
                                                        concept_to=concept_to,
                                                        actor=a)
                if created: logging.debug("Created CCa: " + cca.__unicode__())
                else: logging.debug("Exists CCa: " + cca.__unicode__())

def delete_CCa_from_I(p, db='default'):
    concepts = p.concepts.using(db).all()
    actors = p.actors.using(db).all()
    for cca in CCa.objects.using(db).filter(concept_from__in=concepts,
                                            concept_to__in=concepts,
                                            actor__in=actors):
        psa = set(cca.actor.instance_set.using(db).exclude(id=p.id))
        pscf = set(cca.concept_from.instance_set.using(db).exclude(id=p.id))
        psct = set(cca.concept_to.instance_set.using(db).exclude(id=p.id))
        if not psa.intersection(pscf).intersection(psct):
            logging.debug("Deleted CCa: " + cca.__unicode__())
            cca.delete()
        else: logging.debug("Not deleted CCa: " + cca.__unicode__())

#    for a in p.actors.all():  
#        for c in p.concepts.all():
#            if not a.instances.exclude(id=p.id) or not c.instances\
#                    .exclude(id=p.id): #concept and actor only in this instance
#                for cca in c.CCa_from.filter(concept_to__in=p.concepts.all(), actor=a):
#                    cca.delete()
#                for cca in c.CCa_to.filter(concept_to__in=p.concepts.all(), actor=a):
#                    cca.delete()
#            else:
#                for cca in c.CCa_from.filter(concept_to__in=p.concepts.all(), actor=a):
#                    ps2 = cca.concept_to.instance_set.exclude(id=p.id)
#                    #if not ps2 and cca.concept_to in ps2 and cca.ps2 : # check one by one
#                    if not ps2: 
#                        cca.delete()
#                for cca in c.CCa_to.filter(concept_to__in=p.concepts.all(), actor=a):
#                    ps2 = cca.concept_to.instance_set.exclude(id=p.id)
#                    #if not ps2 and cca.concept_to in ps2 and cca.ps2 : # check one by one
#                    if not ps2: 
#                        cca.delete()

def delete_CCa_from_I_A(p, a, db='default'):
    concepts = p.concepts.using(db).all()
    # better iterate concepts
    for cca in CCa.objects.using(db).filter(concept_from__in=concepts,
                                            concept_to__in=concepts,
                                            actor=a):
        psa = set(a.instances.using(db).exclude(id=p.id))
        pscf = set(cca.concept_from.instance_set.using(db).exclude(id=p.id))
        psct = set(cca.concept_to.instance_set.using(db).exclude(id=p.id))
        if not psa.intersection(pscf).intersection(psct):
            logging.debug("Deleted CCa: " + cca.__unicode__())
            cca.delete()
        else: logging.debug("Not deleted CCa: " + cca.__unicode__())

def delete_CCa_from_I_C(p, c, db='default'):
    actors = p.actors.using(db).all()
    concepts = p.concepts.using(db).exlude(id=c.id)
    # better iterate concepts
    for cca in CCa.objects.using(db).filter(concept_from=c,
                                            concept_to__in=concepts,
                                            actor__in=actors):
        psa = set(cca.actor.instances.using(db).exclude(id=p.id))
        pscf = set(c.instance_set.using(db).exclude(id=p.id))
        psct = set(cca.concept_to.instance_set.using(db).exclude(id=p.id))
        if not psa.intersection(pscf).intersection(psct):
            logging.debug("Deleted CCa: " + cca.__unicode__())
            cca.delete()
        else: logging.debug("Not deleted CCa: " + cca.__unicode__())
    for cca in CCa.objects.using(db).filter(concept_from__in=concepts,
                                            concept_to=c,
                                            actor__in=actors):
        psa = set(cca.actor.instances.using(db).exclude(id=p.id))
        pscf = set(c.instance_set.using(db).exclude(id=p.id))
        psct = set(cca.concept_from.instance_set.using(db).exclude(id=p.id))
        if not psa.intersection(pscf).intersection(psct):
            logging.debug("Deleted CCa: " + cca.__unicode__())
            cca.delete()
        else: logging.debug("Not deleted CCa: " + cca.__unicode__())
##############################################################################
# AAc
##############################################################################

def create_AAc_from_A_I(a, p, db="default"):
    """
    see generate_AAc
    It is possible to create new AAc with new actor:
    C0 = c1, c2
    A0 = a1, a2
    AAc0 = a2a1c1, a2a1c2
    A1 = a1, a2, a3
    AAc1 = a3a1c1, a3a2c1, a3a1c2, a3a2c2
    """
    for concept in p.concepts.using(db).all():
        for a_to in p.actors.using(db).all().exclude(id=a.id):
            if not AAc.objects.using(db).filter(actor_from=a_to,
                                                actor_to=a,
                                                concept=concept):
                aac, created = AAc.objects.using(db).get_or_create(
                                                            actor_from=a,
                                                            actor_to=a_to,
                                                            concept=concept)
                if created: logging.debug("Created AAc: " + aac.__unicode__())
                else: logging.debug("Exists AAc" + aac.__unicode__())

def create_AAc_from_C_I(c, p, db="default"):
    """
    see generate_AAc
    It is possible to create new AAc with new actor:
    C0 = c1, c2
    A0 = a1, a2
    AAc0 = a2a1c1, a2a1c2
    A1 = a1, a2, a3
    AAc1 = a3a1c1, a3a2c1, a3a1c2, a3a2c2
    """
    for a_from, a_to in combinations(p.actors.using(db).all(), 2):
        if not AAc.objects.using(db).filter(actor_from=a_to,
                                            actor_to=a_from,
                                            concept=c):
            aac, created = AAc.objects.using(db).get_or_create(
                                                    actor_from=a_from,
                                                    actor_to=a_to,
                                                    concept=c)
            if created: logging.debug("Created AAc: " + aac.__unicode__())
            else: logging.debug("Exists AAc" + aac.__unicode__())


def delete_AAc_from_I(p, db='default'):
    concepts = p.concepts.using(db).all()
    actors = p.actors.using(db).all()
    for aac in AAc.objects.using(db).filter(actor_from__in=actors,
                                            actor_to__in=actors,
                                            concept__in=concepts):
        psc = set(aac.concept.instance_set.using(db).exclude(id=p.id))
        psaf = set(aac.actor_from.instance_set.using(db).exclude(id=p.id))
        psat = set(aac.actor_to.instance_set.using(db).exclude(id=p.id))
        if not psc.intersection(psaf).intersection(psat):
            logging.debug("Deleted AAc: " + aac.__unicode__())
            aac.delete()
        else: logging.debug("Not deleted AAc: " + aac.__unicode__())
#    
#    for a in p.actors.all():
#        for c in p.concepts.all():
#            if not a.instances.exclude(id=p.id) or not c.instances\
#                    .exclude(id=p.id): #concept and actor only in this instance
#                for aac in a.AAc_from.filter(actor_to__in=p.actors.all(), 
#                                            concept=c):
#                    aac.delete()
#                for aac in c.AAc_to.filter(actor_to__in=p.actors.all(), 
#                                           concept=c):
#                    aac.delete()
#            else:
#                for aac in c.AAc_from.filter(actor_to__in=p.actors.all(), concept=c):
#                    ps2 = aac.actor_to.instance_set.exclude(id=p.id)
#                    #if not ps2 and cca.concept_to in ps2 and cca.ps2 : # check one by one
#                    if not ps2: 
#                        aac.delete()
#                for aac in c.AAc_to.filter(actor_to__in=p.actors.all(), concept=c):
#                    ps2 = aac.actor_to.instance_set.exclude(id=p.id)
#                    #if not ps2 and cca.concept_to in ps2 and cca.ps2 : # check one by one
#                    if not ps2: 
#                        aac.delete()

def delete_AAc_from_I_A(p, a, db='default'):
    concepts = p.concepts.using(db).all()
    actors = p.actors.using(db).exclude(id=a.id)
    for aac in AAc.objects.using(db).filter(actor_from=a,
                                            actor_to__in=actors,
                                            concept__in=concepts):
        psc = set(aac.concept.instance_set.using(db).exclude(id=p.id))
        psaf = set(a.instances.using(db).exclude(id=p.id))
        psat = set(aac.actor_to.instance_set.using(db).exclude(id=p.id))
        if not psc.intersection(psaf).intersection(psat):
            logging.debug("Deleted AAc: " + aac.__unicode__())
            aac.delete()
        else: logging.debug("Not deleted AAc: " + aac.__unicode__())
    for aac in AAc.objects.using(db).filter(actor_to=a,
                                            actor_from__in=actors,
                                            concept__in=concepts):
        psc = set(aac.concept.instance_set.using(db).exclude(id=p.id))
        psaf = set(a.instances.using(db).exclude(id=p.id))
        psat = set(aac.actor_from.instance_set.using(db).exclude(id=p.id))
        if not psc.intersection(psaf).intersection(psat):
            logging.debug("Deleted AAc: " + aac.__unicode__())
            aac.delete()
        else: logging.debug("Not deleted AAc: " + aac.__unicode__())

def delete_AAc_from_I_C(p, c, db='default'):
    actors = p.actors.using(db).all()
    for aac in AAc.objects.using(db).filter(actor_from__in=actors,
                                            actor_to__in=actors,
                                            concept=c):
        psc = set(c.instance_set.using(db).exclude(id=p.id))
        psaf = set(aac.actor_from.instances.using(db).exclude(id=p.id))
        psat = set(aac.actor_to.instance_set.using(db).exclude(id=p.id))
        if not psc.intersection(psaf).intersection(psat):
            logging.debug("Deleted AAc: " + aac.__unicode__())
            aac.delete()
        else: logging.debug("Not deleted AAc: " + aac.__unicode__())

##############################################################################
# Old functions to refactorize, still being used by initialize models
##############################################################################

#def generate_AAp(pxds):
#    AAp = set()
#    for p in Instance.objects.using(db).filter(datasets=pxds):
#        for aa in combinations(p.actors.filter(datasets = pxds),2):
#            AAp.add(aa)
#    return AAp

def generate_AAp(p, db='default'):
    [AAp.objects.using(db).get_or_create(actor_from=aa[0], actor_to=aa[1], instance=p) for aa in combinations(p.actors.all(), 2)]

#def generate_CCp(pxds):
#    CCp = set()
#    for p in Instance.objects.using(db).filter(datasets=pxds):
#        for cc in combinations(p.concepts.filter(datasets = pxds),2):
#            CCp.add(cc)
#    return CCp


def generate_CCa(p, db='default'):
    for a in p.actors.all():
        for concept_from, concept_to in combinations(p.concepts.all(), 2):
            CCa.objects.using(db).get_or_create(concept_from=concept_from, concept_to=concept_to, actor=a)

def generate_AAc(p, db='default'):
    for concept in p.concepts.all():
        for a_from, a_to in combinations(p.actors.all(), 2):
            AAc.objects.using(db).get_or_create(actor_from=a_from, actor_to=a_to, concept=concept)

def generate_CCbb(db='default'):
    for concept_to_id in CCb.objects.using(db).values('concept_to').distinct() :
#        for ccb.concept_from in CCb.objects.using(db).filter(concept_to__id = concept_to__id):
        concept = Concept.objects.using(db).get(id=concept_to_id)
        for concept_from, concept_to in combinations(concept.narrowers.all(), 2):
            CCbb.objects.using(db).get_or_create(concept_from=concept_from, concept_parent=concept, concept_to=concept_to)

def generate_CCbc(db='default'):
    for concept_from_id in CCb.objects.using(db).values('concept_from').distinct() :
#        for ccb.concept_from in CCb.objects.using(db).filter(concept_to__id = concept_to__id):
        concept = Concept.objects.using(db).get(id=concept_from_id)
        for concept_from, concept_to in combinations(concept.broaders.all(), 2):
            CCbc.objects.using(db).get_or_create(concept_from=concept_from, concept_child=concept, concept_to=concept_to)

def generate_AAba(db='default'):
    for ccb in CCb.objects.using(db).exclude(concept_from__not_in_dataset=True, concept_to__not_in_dataset=True):
        for a_from in ccb.concept_from.actors.all():
            for a_to in ccb.concept_to.actors.all():
                if a_from != a_to:
                    AAba.objects.using(db).get_or_create(actor_from=a_from, actor_to=a_to, ccba=ccb)
    #db.reset_queries()

#    [AAba.objects.using(db).get_or_create(actor_from = a_from, actor_to = a_to, ccba = ccb) for a_to in list(ccb.concept_to.actors.all()) for a_from in list(ccb.concept_from.actors.all()) for ccb in list(CCb.objects.using(db).exclude(concept_from__not_in_dataset = True, concept_to__not_in_dataset = True)) if a_from != a_to]

##[[[AAba.objects.using(db).get_or_create(actor_from = a_from, actor_to = a_to, ccba = ccb) for a_to in ccb.concept_to.actors.all()] for a_from in ccb.concept_from.actors.all()] for ccb in CCb.objects.using(db).exclude(concept_from__not_in_dataset = True, concept_to__not_in_dataset = True) if a_from != a_to]

def generate_AAbb(db='default'):
    for ccbb in CCbb.objects.using(db).all():
#    for ccbb in CCbb.objects.using(db).values('concept_from', 'concept_to').distinct():
#        ccbb = CCbb.objects.using(db).get(concept_from__id=ccbb['concept_from'], concept_to__id=ccbb['concept_to'])
#    for ccbb in [CCbb.objects.using(db).get(concept_from__id=ccbb['concept_from'], concept_to__id=ccbb['concept_to'])for ccbb in CCbb.objects.using(db).values('concept_from', 'concept_to').distinct()]:
        for a_from in ccbb.concept_from.actors.all():
#        for a_from in Concept.objects.using(db).get(id = ccbb['concept_from']).actors.all():
            for a_to in ccbb.concept_to.actors.all():
#            for a_to in Concept.objects.using(db).get(id = ccbb['concept_to']).actors.all():
                if a_from != a_to:
#                    for ccbbe in CCbb.objects.using(db).filter('concept_from', 'concept_to')
                    AAbb.objects.using(db).get_or_create(actor_from=a_from, actor_to=a_to, ccbb=ccbb)
    #db.reset_queries()

def generate_AAbc(db='default'):
    for ccbc in CCbc.objects.using(db).all():
        for a_from in ccbc.concept_from.actors.all():
            for a_to in ccbc.concept_to.actors.all():
                if a_from != a_to:
                    AAbc.objects.using(db).get_or_create(actor_from=a_from, actor_to=a_to, ccbc=ccbc)
    #db.reset_queries()

############

#def generate_AAc_weighted_from_Aconcept():
#    for concept in Concept.objects.using(db).all():
#        #db.reset_queries()
#        for a1, a2 in combinations(concept.actors.all(), 2):
#            aac1 = AAcw.objects.using(db).filter(actor_from = a1, actor_to = a2)
#            aac2 = AAcw.objects.using(db).filter(actor_from = a2, actor_to = a1)
#            if aac1:
#                aac1[0].weight += 1
#            elif aac2:
#                aac2[0].weight += 1
#            AAcw.objects.using(db).get_or_create(actor_from = a1, actor_to = a2, weight=1)

def generate_AAc_weighted_from_Aconcept(db='default'):
    for a1, a2 in combinations(Actor.objects.using(db).all(), 2):
        w = len(set(a1.concepts.all()).intersection(set(a2.concepts.all())))
        if w:
            AAcw.objects.using(db).create(actor_from=a1, actor_to=a2, weight=w)

def generate_AAbc_weighted(db='default'):
##    ccbc = list(CCbc.objects.using(db).values('concept_from', 'concept_to').distinct())
#    ccbcs = list(CCbc.objects.using(db).values('concept_from', 'concept_to','ccbc')
#    [ccbcs.remove({'concept_to':ccbbe['concept_from'], 'concept_from': ccbbe['concept_to'],'ccbc':ccbbe['ccbc']}) for ccbbe in ccbcs if {'concept_to':ccbbe['concept_from'], 'concept_from': ccbbe['concept_to'],'ccbc':ccbbe['ccbc']} in ccbcs]
##    ccbcs = list(CCbc.objects.using(db).all())
##    [ccbcs.remove(CCbc.objects.using(db).get(concept_to = ccbbe.concept_from, concept_from = ccbbe.concept_to)) for ccbbe in ccbcs if CCbc.objects.using(db).filter(concept_to = ccbbe.concept_from, concept_from = ccbbe.concept_to)]
#    [ccbbe.delete() for ccbbe in CCbc.objects.using(db).all() if CCbc.objects.using(db).filter(actor_from = ccbbe.actor_to, actor_to = ccbbe.actor_from, ccbc =ccbbe.ccbc)]
    for ccbc in CCbc.objects.using(db).all():
        if CCbc.objects.using(db).filter(concept_from=ccbc.concept_to, concept_to=ccbc.concept_from, concept_child=ccbc.concept_child):
            ccbc.delete()
        else:
            for a_from in ccbc.concept_from.actors.all():
                for a_to in ccbc.concept_to.actors.all():
                    if a_from != a_to:
                        a = AAbcw.objects.using(db).filter(actor_from=a_from, actor_to=a_to)
                        b = AAbcw.objects.using(db).filter(actor_from=a_to, actor_to=a_from)
                        if a:
                            a[0].weight += 0.5
                            a[0].save()
                        elif b:
                            b[0].weight += 0.5
                            b[0].save()
                        else:
                            AAbcw.objects.using(db).create(actor_from=a_from, actor_to=a_to, weight=0.5)

def generate_AAbbc_weighted(db='default'):
    [AAbbcw.objects.using(db).create(actor_from=aabcw.actor_from, actor_to=aabcw.actor_to, weight=aabcw.weight) for aabcw in AAbcw.objects.using(db).all()]
##    ccbbs = list(CCbb.objects.using(db).all())
#    ccbbs = list(CCbb.objects.using(db).values('concept_from', 'concept_to','ccbb')
#    [ccbbs.remove({'concept_to':ccbbe['concept_from'], 'concept_from': ccbbe['concept_to'], 'ccbb': ccbbe['ccbb']}) for ccbbe in ccbbs if {'concept_to':ccbbe['concept_from'], 'concept_from': ccbbe['concept_to'], 'ccbb': ccbbe['ccbb']} in ccbbs]
    for ccbb in CCbb.objects.using(db).all():
        if CCbb.objects.using(db).filter(concept_from=ccbb.concept_to, concept_to=ccbb.concept_from, concept_parent=ccbb.concept_parent):
            ccbb.delete()
        else:
            for a_from in ccbb.concept_from.actors.all():
                for a_to in ccbb.concept_to.actors.all():
                    if a_from != a_to:
                        a = AAbbcw.objects.using(db).filter(actor_from=a_from, actor_to=a_to)
                        b = AAbbcw.objects.using(db).filter(actor_from=a_to, actor_to=a_from)
                        if a:
                            a[0].weight += 0.5
                            a[0].save()
                        elif b:
                            b[0].weight += 0.5
                            b[0].save()
                        else:
                            AAbbcw.objects.using(db).create(actor_from=a_from, actor_to=a_to)

def generate_AAbabc_weighted(db='default'):
    [AAbabcw.objects.using(db).create(actor_from=aabbcw.actor_from, actor_to=aabbcw.actor_to, weight=aabbcw.weight) for aabbcw in AAbbcw.objects.using(db).all()]
    ccbas = CCb.objects.using(db).exclude(concept_from__not_in_dataset=True).exclude(concept_to__not_in_dataset=True)
    for ccbc in ccbas:
        for a_from in ccbc.concept_from.actors.all():
            for a_to in ccbc.concept_to.actors.all():
                if a_from != a_to:
                    a = AAbabcw.objects.using(db).filter(actor_from=a_from, actor_to=a_to)
                    b = AAbabcw.objects.using(db).filter(actor_from=a_to, actor_to=a_from)
                    if a:
                        a[0].weight += 0.25
                        a[0].save()
                    elif b:
                        b[0].weight += 0.25
                        b[0].save()
                    else:
                        AAbabcw.objects.using(db).create(actor_from=a_from, actor_to=a_to)
