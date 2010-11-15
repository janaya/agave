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

from MySQLdb import OperationalError
from agave.models import *
from django import db
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from exceptions import TypeError
import glob
import random
import sys
try:
    from bioreader import *
except ImportError:
    sys.stderr.write("Bioreader must be installed")
    sys.exit(1)

"""
@TODO: refactorize with controller_graph_models_generator
"""

def generate_models(path, num_files=None, year=None):
    """
    parse  XML files
    """
    count = 1
#            if os.path.isdir(self.path):
    if path.endswith('*'):
        pubmed_xml_dir = glob.glob(path)
        if not num_files:
            for pubmed_xml_file in pubmed_xml_dir:
                print
                print 'LOADING FILE %s OUT OF %s' % (count, len(pubmed_xml_dir))
                parse_pubmed_xml_file(pubmed_xml_file, year)
                count += 1
        else:
            for pubmed_xml_file in pubmed_xml_dir[:num_files]:
                print
                print 'LOADING FILE %s OUT OF %s' % (count, len(pubmed_xml_dir))
                parse_pubmed_xml_file(pubmed_xml_file, year)
                count += 1
        return count
#            elif os.path.isfile(self.path):
    elif path.endswith('txt'):
        print 'LOADING FILE %s ' % (path)
        parse_pubmed_xml_file(path)
        count += 1
    else:
        logging.error("Path %s does not exits" % path)

def parse_pubmed_xml_file(inputfile, year=None):
    print 'loading data from %s ...' % inputfile
    data = DataContainer(inputfile, 'pubmed')
    p_sameid = []
    p_without_concepts = []
    as_duplicate = []
    as_same_name = []
    for key in data.keys:
        record = data.read(key)
#            print record.pmid
#        if record.year != '2009': continue
        if not year or record.year == year:
            try:
                # for title take only 255 characters, otherwise, the exception is raised
                p, created = Instance.objects.get_or_create(pmid=record.pmid, title=record.title[:255], year=record.year)
        #                print p.pmid
        #            import ipdb; ipdb.set_trace()
        #            except IntegrityError:
            except:
                print "2 instances with different pmid???"
                p_sameid.append((record.pmid, record.title))
                created = False
                p = None
                continue

            weight = 1.0 / len(record.Lista)
            for actor in record.Lista:
                a_duplicate, a_same_name = generate_actor_and_instance_actor(p, actor, weight)
                as_duplicate += a_duplicate
                as_same_name += a_same_name
            generate_AAp(p)
            # record.MD can be null
            try:
                concepts = record.MD
            except:
                print "\nInstance without concept, ?"
                p_without_concepts.append((record.pmid, record.title))
            else:
                if concepts:
                    weight = 1
                    for concept in concepts:
                        generate_concept_and_instanceconcept(p, concept, weight)
                        generate_actorconcept_from_instance(p, concept, weight)
            #        generate_AAc(record.Lista, concepts)
            #        generate_CCa(record.Lista, concepts)
            generate_CCp(p)
            generate_CCa(p)
            generate_AAc(p)
            generate_AAp(p)
        #        django.db.connection.queries
            db.reset_queries()

        if p_sameid or p_without_concepts or as_duplicate or as_same_name:
            f = open('strange_data.txt', 'a')
            f.write('\n' + inputfile + '\n')
            if p_sameid:
                f.write('\nPUBLICATIONS WITH SAME ID\n')
                f.write('\n'.join(map(",".join, p_sameid)))
            if p_without_concepts:
                f.write('\nPUBLICATIONS WITHOUT CONCEPTS\n')
                f.write('\n'.join(map(",".join, p_without_concepts)))
            if as_duplicate:
                f.write('\nAUTHORS DIFFERENT NAMES\n')
                f.write('\n'.join(map(",".join, as_duplicate)))
            if as_same_name:
                f.write('\nAUTHORS SAME NAME?\n')
                f.write('\n'.join(map(",".join, as_same_name)))
        #    f.write('PUBLICATIONS WITH SAME ID')
        #    f.write('\n'.join(p_sameid))
        #    f.write('PUBLICATIONS WITHOUT CONCEPTS')
        #    f.write('\n'.join(p_without_concepts))
        #    f.write('AUTHORS DIFFERENT NAMES')
        #    f.write('\n'.join(as_duplicate))
        #    f.write('AUTHORS SAME NAME?')
        #    f.write('\n'.join(as_same_name))
            f.close()

def generate_actor_and_instance_actor(p, actor, weight):
    a_duplicate = []
    a_same_name = []
    # the actor can already exists from other instance
    # FIXME check that actors like "Amigorena S S" and "Amigorena Sebastion S"
    try:
        actor_name = actor.strip().replace('  ', ' ')
        actor_name_start = ' '.join([actor.split()[0], actor.split()[1][0]])
        actor_duplicates = Actor.objects.exclude(name=actor_name).filter(name__startswith=actor_name_start)
        if actor_duplicates:
            actor_duplicate_name = actor_duplicates[0].name
            a_duplicate.append((actor_name, actor_duplicate_name))
            print "\nActors possibly the same: "
    #            print [a for a in actor_duplicates]
    #            print actor
            actor = actor_name if len(actor_name) > len(actor_duplicate_name) else actor_duplicate_name
    except IndexError: # in split
        print actor # actor_name u'EMBRACE'
#        import ipdb; ipdb.set_trace()
    except OperationalError: # in if actor_duplicates (because encoding)
        print p
        print actor_name
        print actor_duplicates
        import ipdb; ipdb.set_trace()
    try:
        a, created = Actor.objects.get_or_create(name=actor)
    except OperationalError:
        print "\nActor with same name?"
        import ipdb; ipdb.set_trace()
        name = random.randint(1, 10)
        a, created = Actor.objects.get_or_create(name='%s' % name)
        a_same_name.append((actor, name))
    #    if not self in a.datasets.all():
    #        a.datasets.add(self)
        # a instance must contain only once an actor, unless we are parsing again
        # although we were creating another dataset, the actor-instance weight is the same
    pa, created = InstanceActor.objects.get_or_create(actor=a, instance=p, weight=weight)
#        if not created:
#            print "\nInstance-Actor" + pa.actor.name + pa.instance.title + " already in the database, are you parsing again the XML?"
    return a_duplicate, a_same_name

def generate_concept_and_instanceconcept(p, concept, weight):
    # the concept can already exists from other instance
    concept, created = Concept.objects.get_or_create(name=concept)
#    if not self in concept.datasets.all():
#        concept.datasets.add(self)

    # a instance must contain only once an concept, unless we are parsing again
    # although we were creating another dataset, the concept-instance weight is the same
    pconcept, created = InstanceConcept.objects.get_or_create(instance=p, concept=concept, weight=weight)
#        if not created:
#            print "\nInstance-concept" + pconcept.instance.title + pconcept.concept.name + " already in the database, are you parsing again the XML?"

def generate_actorconcept_from_instance(p, concept, weight):
    for a in p.actors.all():
        # actor can contain several times the same concept (through other instances), then sum the weight
        # depends on the dataset
        concept = Concept.objects.get(name=concept)
        aconcepts = ActorConcept.objects.filter(actor=a, concept=concept)
        if aconcepts:
#            print "\nActor " + a.name +" put the same concept " + concept.name
            aconcept = aconcepts[0]
            aconcept.weight += 1
            aconcept.save()
        else:
            aconcept = ActorConcept.objects.create(actor=a, concept=concept, weight=weight)

#def generate_AAp(pxds):
#    AAp = set()
#    for p in Instance.objects.filter(datasets=pxds):
#        for aa in combinations(p.actors.filter(datasets = pxds),2):
#            AAp.add(aa)
#    return AAp

def generate_AAp(p):
    [AAp.objects.get_or_create(actor_from=aa[0], actor_to=aa[1], instance=p) for aa in combinations(p.actors.all(), 2)]

#def generate_CCp(pxds):
#    CCp = set()
#    for p in Instance.objects.filter(datasets=pxds):
#        for cc in combinations(p.concepts.filter(datasets = pxds),2):
#            CCp.add(cc)
#    return CCp


def generate_CCp(p):
    [CCp.objects.get_or_create(concept_from=cc[0], concept_to=cc[1], instance=p) for cc in combinations(p.concepts.all(), 2)]

def generate_CCa(p):
    for a in p.actors.all():
        for concept_from, concept_to in combinations(p.concepts.all(), 2):
            CCa.objects.get_or_create(concept_from=concept_from, concept_to=concept_to, actor=a)

def generate_AAc(p):
    for concept in p.concepts.all():
        for a_from, a_to in combinations(p.actors.all(), 2):
            AAc.objects.get_or_create(actor_from=a_from, actor_to=a_to, concept=concept)

def generate_CCbb():
    for concept_to_id in CCb.objects.values('concept_to').distinct() :
#        for ccb.concept_from in CCb.objects.filter(concept_to__id = concept_to__id):
        concept = Concept.objects.get(id=concept_to__id)
        for concept_from, concept_to in combinations(concept.narrowers.all(), 2):
            CCbb.objects.get_or_create(concept_from=concept_from, concept_parent=concept, concept_to=concept_to)

def generate_CCbc():
    for concept_from_id in CCb.objects.values('concept_from').distinct() :
#        for ccb.concept_from in CCb.objects.filter(concept_to__id = concept_to__id):
        concept = Concept.objects.get(id=concept_from_id)
        for concept_from, concept_to in combinations(concept.broaders.all(), 2):
            CCbc.objects.get_or_create(concept_from=concept_from, concept_child=concept, concept_to=concept_to)

def generate_AAba():
    for ccb in CCb.objects.exclude(concept_from__not_in_dataset=True, concept_to__not_in_dataset=True):
        for a_from in ccb.concept_from.actors.all():
            for a_to in ccb.concept_to.actors.all():
                if a_from != a_to:
                    AAba.objects.get_or_create(actor_from=a_from, actor_to=a_to, ccba=ccb)
    db.reset_queries()

#    [AAba.objects.get_or_create(actor_from = a_from, actor_to = a_to, ccba = ccb) for a_to in list(ccb.concept_to.actors.all()) for a_from in list(ccb.concept_from.actors.all()) for ccb in list(CCb.objects.exclude(concept_from__not_in_dataset = True, concept_to__not_in_dataset = True)) if a_from != a_to]

##[[[AAba.objects.get_or_create(actor_from = a_from, actor_to = a_to, ccba = ccb) for a_to in ccb.concept_to.actors.all()] for a_from in ccb.concept_from.actors.all()] for ccb in CCb.objects.exclude(concept_from__not_in_dataset = True, concept_to__not_in_dataset = True) if a_from != a_to]

def generate_AAbb():
    for ccbb in CCbb.objects.all():
#    for ccbb in CCbb.objects.values('concept_from', 'concept_to').distinct():
#        ccbb = CCbb.objects.get(concept_from__id=ccbb['concept_from'], concept_to__id=ccbb['concept_to'])
#    for ccbb in [CCbb.objects.get(concept_from__id=ccbb['concept_from'], concept_to__id=ccbb['concept_to'])for ccbb in CCbb.objects.values('concept_from', 'concept_to').distinct()]:
        for a_from in ccbb.concept_from.actors.all():
#        for a_from in Concept.objects.get(id = ccbb['concept_from']).actors.all():
            for a_to in ccbb.concept_to.actors.all():
#            for a_to in Concept.objects.get(id = ccbb['concept_to']).actors.all():
                if a_from != a_to:
#                    for ccbbe in CCbb.objects.filter('concept_from', 'concept_to')
                    AAbb.objects.get_or_create(actor_from=a_from, actor_to=a_to, ccbb=ccbb)
    db.reset_queries()

def generate_AAbc():
    for ccbc in CCbc.objects.all():
        for a_from in ccbc.concept_from.actors.all():
            for a_to in ccbc.concept_to.actors.all():
                if a_from != a_to:
                    AAbc.objects.get_or_create(actor_from=a_from, actor_to=a_to, ccbc=ccbc)
    db.reset_queries()

############

#def generate_AAc_weighted_from_Aconcept():
#    for concept in Concept.objects.all():
#        db.reset_queries()
#        for a1, a2 in combinations(concept.actors.all(), 2):
#            aac1 = AAcw.objects.filter(actor_from = a1, actor_to = a2)
#            aac2 = AAcw.objects.filter(actor_from = a2, actor_to = a1)
#            if aac1:
#                aac1[0].weight += 1
#            elif aac2:
#                aac2[0].weight += 1
#            AAcw.objects.get_or_create(actor_from = a1, actor_to = a2, weight=1)

def generate_AAc_weighted_from_Aconcept():
    for a1, a2 in combinations(Actor.objects.all(), 2):
        w = len(set(a1.concepts.all()).intersection(set(a2.concepts.all())))
        if w:
            AAcw.objects.create(actor_from=a1, actor_to=a2, weight=w)

def generate_AAbc_weighted():
##    ccbc = list(CCbc.objects.values('concept_from', 'concept_to').distinct())
#    ccbcs = list(CCbc.objects.values('concept_from', 'concept_to','ccbc')
#    [ccbcs.remove({'concept_to':ccbbe['concept_from'], 'concept_from': ccbbe['concept_to'],'ccbc':ccbbe['ccbc']}) for ccbbe in ccbcs if {'concept_to':ccbbe['concept_from'], 'concept_from': ccbbe['concept_to'],'ccbc':ccbbe['ccbc']} in ccbcs]
##    ccbcs = list(CCbc.objects.all())
##    [ccbcs.remove(CCbc.objects.get(concept_to = ccbbe.concept_from, concept_from = ccbbe.concept_to)) for ccbbe in ccbcs if CCbc.objects.filter(concept_to = ccbbe.concept_from, concept_from = ccbbe.concept_to)]
#    [ccbbe.delete() for ccbbe in CCbc.objects.all() if CCbc.objects.filter(actor_from = ccbbe.actor_to, actor_to = ccbbe.actor_from, ccbc =ccbbe.ccbc)]
    for ccbc in CCbc.objects.all():
        if CCbc.objects.filter(concept_from=ccbc.concept_to, concept_to=ccbc.concept_from, concept_child=ccbc.concept_child):
            ccbc.delete()
        else:
            for a_from in ccbc.concept_from.actors.all():
                for a_to in ccbc.concept_to.actors.all():
                    if a_from != a_to:
                        a = AAbcw.objects.filter(actor_from=a_from, actor_to=a_to)
                        b = AAbcw.objects.filter(actor_from=a_to, actor_to=a_from)
                        if a:
                            a[0].weight += 0.5
                            a[0].save()
                        elif b:
                            b[0].weight += 0.5
                            b[0].save()
                        else:
                            AAbcw.objects.create(actor_from=a_from, actor_to=a_to, weight=0.5)

def generate_AAbbc_weighted():
    [AAbbcw.objects.create(actor_from=aabcw.actor_from, actor_to=aabcw.actor_to, weight=aabcw.weight) for aabcw in AAbcw.objects.all()]
##    ccbbs = list(CCbb.objects.all())
#    ccbbs = list(CCbb.objects.values('concept_from', 'concept_to','ccbb')
#    [ccbbs.remove({'concept_to':ccbbe['concept_from'], 'concept_from': ccbbe['concept_to'], 'ccbb': ccbbe['ccbb']}) for ccbbe in ccbbs if {'concept_to':ccbbe['concept_from'], 'concept_from': ccbbe['concept_to'], 'ccbb': ccbbe['ccbb']} in ccbbs]
    for ccbb in CCbb.objects.all():
        if CCbb.objects.filter(concept_from=ccbb.concept_to, concept_to=ccbb.concept_from, concept_parent=ccbb.concept_parent):
            ccbb.delete()
        else:
            for a_from in ccbb.concept_from.actors.all():
                for a_to in ccbb.concept_to.actors.all():
                    if a_from != a_to:
                        a = AAbbcw.objects.filter(actor_from=a_from, actor_to=a_to)
                        b = AAbbcw.objects.filter(actor_from=a_to, actor_to=a_from)
                        if a:
                            a[0].weight += 0.5
                            a[0].save()
                        elif b:
                            b[0].weight += 0.5
                            b[0].save()
                        else:
                            AAbbcw.objects.create(actor_from=a_from, actor_to=a_to)

def generate_AAbabc_weighted():
    [AAbabcw.objects.create(actor_from=aabbcw.actor_from, actor_to=aabbcw.actor_to, weight=aabbcw.weight) for aabbcw in AAbbcw.objects.all()]
    ccbas = CCb.objects.exclude(concept_from__not_in_dataset=True).exclude(concept_to__not_in_dataset=True)
    for ccbc in ccbas:
        for a_from in ccbc.concept_from.actors.all():
            for a_to in ccbc.concept_to.actors.all():
                if a_from != a_to:
                    a = AAbabcw.objects.filter(actor_from=a_from, actor_to=a_to)
                    b = AAbabcw.objects.filter(actor_from=a_to, actor_to=a_from)
                    if a:
                        a[0].weight += 0.25
                        a[0].save()
                    elif b:
                        b[0].weight += 0.25
                        b[0].save()
                    else:
                        AAbabcw.objects.create(actor_from=a_from, actor_to=a_to)


#def main(argv):
##    pubmed_xml_dir = glob.glob("../data/inputdata/pubmed_fpgg_data/*")
##    parse_pubmed_xml_dir(pubmed_xml_dir)
##    parse_pubmed_xml_file('../data/inputdata/pubmed_fpgg_data/pubmed_result.txt')
#    generate_models('../data/inputdata/pubmed_fpgg_data/pubmed_result2.txt')

#if __name__ == "__main__":
#    import sys
#    main(sys.argv[1:])

############################################
def generate_CCball():
    for br in  CCb.objects.filter(concept_from__not_in_dataset=False).filter(concept_to__not_in_dataset=False):
        try:
            CCball.objects.get_or_create(concept_from=br.concept_from, concept_to=br.concept_to)
        except ObjectDoesNotExist:
            pass
    db.reset_queries()
    for concept_to_id in CCb.objects.filter(concept_from__not_in_dataset=False).values('concept_to').distinct() :
        try:
            concept = Concept.objects.get(id=concept_to_id['concept_to'])
            for concept_from, concept_to in combinations(concept.narrowers.all(), 2):
                if not CCball.objects.filter(concept_from=concept_to, concept_to=concept_from):
                    CCball.objects.get_or_create(concept_from=concept_from, concept_to=concept_to)
        except ObjectDoesNotExist:
            pass
    db.reset_queries()
    for concept_from_id in CCb.objects.filter(concept_to__not_in_dataset=False).values('concept_from').distinct() :
        try:
            concept = Concept.objects.get(id=concept_from_id['concept_from'])
            for concept_from, concept_to in combinations(concept.broaders.all(), 2):
                if not CCball.objects.filter(concept_from=concept_to, concept_to=concept_from):
                    CCball.objects.get_or_create(concept_from=concept_from, concept_to=concept_to)
        except ObjectDoesNotExist:
            pass
    db.reset_queries()
    cca = list(CCa.objects.values('concept_from', 'concept_to').distinct())
#    [CCball.objects.get_or_create(concept_from=ccae['concept_from'], concept_to= ccae['concept_to']) for ccae in cca  if not CCball.objects.filter(concept_from=ccae['concept_to'], concept_to= ccae['concept_from'])]
#    [CCball.objects.get_or_create(concept_from__id=ccae['concept_from'], concept_to__id= ccae['concept_to']) for ccae in cca  if not CCball.objects.filter(concept_from__id=ccae['concept_to'], concept_to__id= ccae['concept_from'])]
    [CCball.objects.get_or_create(concept_from=Concept.objects.get(id=ccae['concept_from']), concept_to=Concept.objects.get(id=ccae['concept_to'])) for ccae in cca  if not CCball.objects.filter(concept_from=Concept.objects.get(id=ccae['concept_to']), concept_to=Concept.objects.get(id=ccae['concept_from']))]
    db.reset_queries()

#def generate_AAball():
#    for ccb in CCb.objects.exclude(concept_from__not_in_dataset = True, concept_to__not_in_dataset = True):
#        for a_from in ccb.concept_from.actors.all():
#            for a_to in ccb.concept_to.actors.all():
#                if a_from != a_to and not AAball.object.filter(actor_from = a_to, actor_to = a_from):
#                    AAball.objects.get_or_create(actor_from = a_from, actor_to = a_to)
#    db.reset_queries()
#    for ccbb in CCbb.objects.all():
#        for a_from in ccbb.concept_from.actors.all():
#            for a_to in ccbb.concept_to.actors.all():
#                if a_from != a_ and not AAball.object.filter(actor_from = a_to, actor_to = a_from):
#                    AAball.objects.get_or_create(actor_from = a_from, actor_to = a_to, ccbb = ccbb)
#    db.reset_queries()
#    for ccbc in CCbc.objects.all():
#        for a_from in ccbc.concept_from.actors.all():
#            for a_to in ccbc.concept_to.actors.all():
#                if a_from != a_to and not AAball.object.filter(actor_from = a_to, actor_to = a_from):
#                    AAball.objects.get_or_create(actor_from = a_from, actor_to = a_to, ccbc = ccbc)
#    db.reset_queries()


def generate_AAball():
    for ccb in CCball.objects.all():
        for a_from in ccb.concept_from.actors.all():
            for a_to in ccb.concept_to.actors.all():
                if a_from != a_to and not AAball.objects.filter(actor_from=a_to, actor_to=a_from):
                    AAball.objects.get_or_create(actor_from=a_from, actor_to=a_to)
    db.reset_queries()


    aac = list(AAc.objects.values('actor_from', 'actor_to').distinct())
    [AAball.objects.get_or_create(actor_from=aace['actor_from'], actor_to=aace['actor_to']) for aace in aac if not AAball.objects.filtere(actor_from=aace['actor_to'], actor_to=aace['actor_from'])]

def generate_ACb():
    aids = [aconcept['actor'] for aconcept in ActorConcept.objects.filter(weight__gte=10).values('actor').distinct()]
    actors = Actor.objects.filter(id__in=aids)
    cids = [aconcept['concept'] for aconcept in ActorConcept.objects.filter(weight__gte=10).values('concept').distinct()]
    concepts = Concept.objects.filter(id__in=cids)
    for ccb in CCball.objects.filter(concept_from__id__in=cids, concept_to__id__in=cids):
        as_from = ccb.concept_from.actors.filter(id__in=aids)
        as_to = ccb.concept_to.actors.filter(id__in=aids)
#        for a in set(as_to).difference(set(as_from)):
#            ACb.objects.get_or_create(actor=a, concept=ccb.concept_from)
#        for a in set(as_from).difference(set(as_to)):
#            ACb.objects.get_or_create(actor=a, concept=ccb.concept_to)
        for a in as_from:
            ACb.objects.get_or_create(actor=a, concept=ccb.concept_from)
        for a in as_to:
            ACb.objects.get_or_create(actor=a, concept=ccb.concept_to)

##################3

def generate_AAball():
    AAc.objects.filter(actor_from__in=aconcept).filter(actor_to__in=aconcept)

    for aac in AAc.objects.all():
        if not AAcall.object.filter(actor_from=aac.actor_to, actor_to=aac.actor_from):
            AAcall.object.get_or_create(actor_from=aac.actor_from, actor_to=aac.actor_to)
    aac = list(AAc.objects.values('actor_from', 'actor_to').distinct())
    [AAball.objects.get_or_create(actor_from=aace['actor_from'], actor_to=aace['actor_to']) for aace in aac if not AAball.objects.filtere(actor_from=aace['actor_to'], actor_to=aace['actor_from'])]
