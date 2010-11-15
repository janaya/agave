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
# TODO: Solve settings import error
"""
@TODO: 
    * not get results including descriptors
    * or get them but compute them
    * query Dbpedia with http://dbpedia.org/resource/<meshlabel>
    * get broaders from Dbpedia with Category: predicate?
    * Solve settings import error
"""
from django.core.exceptions import ObjectDoesNotExist
from mesh_skos_broader.mesh_skos_broader_extractor import \
    getMeSHURIfromMeSHname, getbroaders, getnarrowers
from agave.models import Concept, CCb, CCbb, CCbc
import logging

#from django.conf.settings import SPARQL_ENDPOINT_LOCAL
SPARQL_ENDPOINT_LOCAL = False

meshns = "http://www.nlm.nih.gov/mesh/2006"
purlns = "http://purl.org/commons/record/mesh/"
def delete_CCbx_from_C(c, db='default'):
    # just deleting the concept delete all related relations
    # altough remains concepts not in datasets
#    for ccb in CCb.objects.using(db).filter(concept_from=c):
#        broader = ccb.concept_to
#        siblings = broader.narrowers.using(db).exclude(id=c.id)
#        if broader.not_in_dataset and len(siblings) == 1:
#            br = CCb.objects.using(db).get(concept_from=siblings[0],
#                                              concept_to=broader)
#            logging.debug("Deleted CCb (sibling):" + br.__unicode__())
#            br.delete()
#            logging.debug("Deleted C (top):" + broader.__unicode__())
#            # a "top" concept not in ds making a CCba link
#
#            broader.delete()
#        ccb.delete()
#        logging.debug("Deleted CCb:" + ccb.__unicode__())
#
#
#    for ccb in CCb.objects.using(db).filter(concept_to=c):
#        narrower = ccb.concept_from
#        coancestors = narrower.broaders.using(db).exclude(id=c.id)
#        if broader.not_in_dataset and len(sibling) == 1:
#            na = CCb.objects.using(db).get(concept_from=coancestors[0],
#                                              concept_to=narrower)
#            logging.debug("Deleted CCb (sibling):" + br.__unicode__())
#            br.delete()
#            logging.debug("Deleted C (top):" + broader.__unicode__())
#            # a "top" concept not in ds making a CCba link
#
#            broader.delete()
#        ccb.delete()
#        logging.debug("Deleted CCb:" + ccb.__unicode__())


###########################################################################

    for ccbb in CCbb.objects.using(db).filter(concept_from=c,
                                             concept_parent__not_in_dataset=True):

        parent = ccbb.concept_parent
        sibling = ccbb.concept_to

        if len(parent.CCbb_parent.using(db).all()) == 1:
            # delete sibling
            si = CCb.objects.using(db).get(
                                                 concept_from=sibling,
                                                 concept_to=parent)

            logging.debug("Deleted CCb (sibling):" + si.__unicode__())
            si.delete()

        logging.debug("Deleted CCbb:" + ccbb.__unicode__())
        ccbb.delete()

        ccb = CCb.objects.using(db).get(
                                                 concept_from=c,
                                                 concept_to=parent)
        logging.debug("Deleted CCb:" + ccb.__unicode__())
        ccb.delete()

        if len(parent.CCbb_parent.using(db).all()) == 1:
            # delete bottom
            logging.debug("Deleted C (top):" + parent.__unicode__())
            # a "top" concept not in ds making a CCbb link
            parent.delete()

    for ccbb in CCbb.objects.using(db).filter(concept_to=c,
                                             concept_parent__not_in_dataset=True):

        parent = ccbb.concept_parent
        sibling = ccbb.concept_from

        if len(parent.CCbb_parent.using(db).all()) == 1:
            # delete sibling
            si = CCb.objects.using(db).get(
                                                 concept_from=sibling,
                                                 concept_to=parent)

            logging.debug("Deleted CCb (sibling):" + si.__unicode__())
            si.delete()

        logging.debug("Deleted CCbb:" + ccbb.__unicode__())
        ccbb.delete()

        ccb = CCb.objects.using(db).get(
                                                 concept_from=c,
                                                 concept_to=parent)
        logging.debug("Deleted CCb:" + ccb.__unicode__())
        ccb.delete()

        if len(parent.CCbb_parent.using(db).all() == 1):
            # delete bottom
            logging.debug("Deleted C (top):" + parent.__unicode__())
            # a "top" concept not in ds making a CCbb link
            parent.delete()


    for ccbc in CCbc.objects.using(db).filter(concept_from=c,
                                              concept_child__not_in_dataset=True):
        child = ccbc.concept_child
        coancestor = ccbc.concept_to

        if len(child.CCbc_child.using(db).all()) == 1:
            # delete coancestor
            try:
                co = CCb.objects.using(db).get(
                                                 concept_from=child,
                                                 concept_to=coancestor)
            except ObjectDoesNotExist:
                pass
            else:
                logging.debug("Deleted CCb (coancestor):" + co.__unicode__())
                co.delete()

        logging.debug("Deleted CCbc:" + ccbc.__unicode__())
        ccbc.delete()

        ccb = CCb.objects.using(db).get(
                                                 concept_from=child,
                                                 concept_to=c)

        logging.debug("Deleted CCb:" + ccb.__unicode__())
        ccb.delete()

        if len(child.CCbc_child.using(db).all()) == 1:
            # delete bottom
            logging.debug("Deleted C (bottom):" + child.__unicode__())
            # a "bottom" concept not in ds making a CCbc link
            child.delete()



    for ccbc in CCbc.objects.using(db).filter(concept_to=c,
                                              concept_child__not_in_dataset=True):
        child = ccbc.concept_child
        coancestor = ccbc.concept_from

        if len(ccbc.concept_child.CCbc_child.using(db).all()) == 1:
            # delete coancestor
            co = CCb.objects.using(db).get(
                                                 concept_from=child,
                                                 concept_to=coancestor)

            logging.debug("Deleted CCb (coancestor):" + co.__unicode__())
            co.delete()

        logging.debug("Deleted CCbc:" + ccbc.__unicode__())
        ccbc.delete()

        ccb = CCb.objects.using(db).filter(
                                                 concept_from=child,
                                                 concept_to=c)

        logging.debug("Deleted CCb:" + ccb.__unicode__())
        ccb.delete()

        if len(child.CCbc_child.using(db).all()) == 1:
            # delete bottom
            logging.debug("Deleted C (bottom):" + child.__unicode__())
            # a "bottom" concept not in ds making a CCbc link
            child.delete()


#    logging.debug("Deleted C:" + c.__unicode__())
#    c.delete()
def delete_CCbx_from_I(p, db='default'):
    for c in p.concepts.using(db).all():
        delete_CCbx_from_C(c, db)


def create_CCbx_from_C(concept, db='default'):
    if not concept.meshuri:
        concepturi, runningHead = getMeSHURIfromMeSHname(concept.name)
        concept.sparqled_broaders_nc = True
        concept.save()
        if concepturi:
#                if "/".join(concepturi.split("/")[:-1]) == meshns:
            if concepturi.startswith(purlns):
                concept.meshuri = concepturi
#                elif "/".join(concepturi.split("/")[:-1]) == purlns:
            elif concepturi.startswith(meshns):
                concept.meshuri = purlns + concepturi.split("#")[-1]
#                    print "concept.meshuri:"
#                    print concept.meshuri
            if runningHead: concept.runningHead = runningHead
            concept.save()

    if concept.meshuri:

        # get broaders from Neurocommons
        if SPARQL_ENDPOINT_LOCAL:
            broaders = getbroaders(concept.meshuri.split("/")[-1])
        else:
            broaders = getbroaders(concept.meshuri)

        for broader in broaders:
            broader_name = broader['label']
#                print "broader:name "+broader_name
            # concept --> b ?
            if not CCb.objects.using(db).filter(concept_from=concept, concept_to__name__iexact=broader_name):
                # no
                # b created and in dataset?
                if Concept.objects.using(db).filter(name__iexact=broader_name, not_in_dataset=False):
                    # yes
                    b = Concept.objects.using(db).get(name__iexact=broader_name)
#                        print b
                    # concept --> b
                    ccb = CCb.objects.using(db).create(concept_from=concept, concept_to=b)
                    logging.debug("Created CCb: " + ccb.__unicode__())
                else:
                    # can not create concept --> b, but maybe concept --> b --> n_of_b
                    pass
            else:
                # if concept --> b exists, that means n_of_b are created too?
                pass

            # get narrowers of broader
            # concept ---> b <-- n_of_b
            if SPARQL_ENDPOINT_LOCAL:
#                   narrowers = getnarrowers(purlns+"/"+broader['meshuri'].split("#")[-1])
                narrowers = getnarrowers(broader['meshuri'].split("#")[-1])
#                   print "CCbb getnarrowers(%s)" % broader['meshuri'].split("#")[-1]
            else:
                narrowers = getnarrowers(broader['meshuri'])
            for narrower in narrowers:
                narrower_name = narrower['label']
#                    print "narrower_name of broader:"+ narrower_name
                # br <-- n_of_b?
                if narrower_name.lower() == concept.name.lower():
                    continue
                if not CCb.objects.using(db).filter(concept_from__name__iexact=narrower_name, concept_to__name__iexact=broader_name):
                    # no
                    # n_of_b in in db and in ds and if different to concept?
                    if Concept.objects.using(db).filter(name__iexact=narrower_name, not_in_dataset=False):
                        # yes
                        n_of_b = Concept.objects.using(db).get(name__iexact=narrower_name)
#                            print "n_of_b"
#                            print n_of_b
                        # br?
                        if Concept.objects.using(db).filter(name__iexact=broader_name):
                            b = Concept.objects.using(db).get(name__iexact=broader_name)
                        else:
                        # if br did not exist, create but not in ds
                            if SPARQL_ENDPOINT_LOCAL:
                                b = Concept.objects.using(db).create(name=broader_name, meshuri=purlns + broader['meshuri'].split("#")[-1], not_in_dataset=True)
#                                   print "create: %s, %s" % (broader_name,purlns+broader['meshuri'].split("#")[-1])
                            else:
                                b = Concept.objects.using(db).create(name=broader_name, meshuri=broader['meshuri'], not_in_dataset=True)
                                #print "new relation through broader %s!" % b
                            logging.debug("Created C: " + b.__unicode__())
                        # concept --> br maybe already exists if b in ds
                        ccb, _ = CCb.objects.using(db).get_or_create(concept_from=concept, concept_to=b)
                        if _: logging.debug("Created CCb: " + ccb.__unicode__())
                        else: logging.debug("Not created CCb: " + ccb.__unicode__())
                        ccb = CCb.objects.using(db).create(concept_from=n_of_b, concept_to=b)
                        logging.debug("Created CCb: " + ccb.__unicode__())
                        ccbb, _ = CCbb.objects.using(db).get_or_create(concept_from=concept, concept_parent=b, concept_to=n_of_b)
                        if _: logging.debug("Created CCbb: " + ccbb.__unicode__())
                        else: logging.debug("Created CCbb: " + ccbb.__unicode__())
                    else:
                            # if narrower is not in the ds, don't create concept --> b <-- n_of_b
                            pass
                else:
                        # concept --> br <-- n_of_n already exists
                    pass

            # concept --> n --> b_or_n
            if SPARQL_ENDPOINT_LOCAL:
                narrowers = getnarrowers(concept.meshuri.split("/")[-1])
#                print "CCbc getnarrowers(%s)" % concept.meshuri.split("/")[-1]
            else:
                narrowers = getnarrowers(concept.meshuri)
            for narrower in narrowers:
                narrower_name = narrower['label']
#                print "narrower_name"+narrower_name
                if not CCb.objects.using(db).filter(concept_from__name__iexact=narrower_name, concept_to=concept):
                    if Concept.objects.using(db).filter(name__iexact=narrower_name, not_in_dataset=False):
                        # yes
                        n = Concept.objects.using(db).get(name__iexact=narrower_name)
#                        print n
                        # concept <-- n
                        ccb = CCb.objects.using(db).create(concept_from=n, concept_to=concept)
                        logging.debug("Created CCb: " + ccb.__unicode__())


                if SPARQL_ENDPOINT_LOCAL:
#                   broaders = getbroaders(purlns+"/"+narrower['meshuri'].split("#")[-1])
                    broaders = getbroaders(narrower['meshuri'].split("#")[-1])
#                   print "CCbc getnarrowers(%s)" % narrower['meshuri'].split("#")[-1]
                else:
                    broaders = getbroaders(narrower['meshuri'])
                for broader in broaders:
                    broader_name = broader['label']
#                    print "broader_name of narrower"+broader_name
                    if broader_name.lower() == concept.name.lower():
                        continue
                    if not CCb.objects.using(db).filter(concept_from__name__iexact=narrower_name, concept_to__name__iexact=broader_name):
                        if Concept.objects.using(db).filter(name__iexact=broader_name, not_in_dataset=False):
                            b_of_n = Concept.objects.using(db).get(name__iexact=broader_name)
        #                   b_of_n.meshuri = broader['meshuri']
        #                   b_of_n.save()
#                            print "b_of_n"
#                            print b_of_n
                            if Concept.objects.using(db).filter(name__iexact=narrower_name):
                                n = Concept.objects.using(db).get(name__iexact=narrower_name)
                            else:
                                if SPARQL_ENDPOINT_LOCAL:
                                    n = Concept.objects.using(db).create(name=narrower_name, meshuri=purlns + narrower['meshuri'].split("#")[-1], not_in_dataset=True)
                                else:
                                    n = Concept.objects.using(db).create(name=narrower_name, meshuri=narrower['meshuri'], not_in_dataset=True)
#                               
                                logging.debug("Created C (narrower): " + n.__unicode__())
                            ccb, _ = CCb.objects.using(db).get_or_create(concept_from=n, concept_to=concept)
                            if _: logging.debug("Created CCb: " + ccb.__unicode__())
                            else: logging.debug("Created CCb: " + ccb.__unicode__())
#                            print "with n (%s) -> concept (%s)" % (n.name,concept.name)
                            ccb = CCb.objects.using(db).create(concept_from=n, concept_to=b_of_n)
                            logging.debug("Created CCb: " + ccb.__unicode__())
#                            print "with n (%s) -> b_of_n (%s)" % (n.name,b_of_n.name)

                            ccbc, _ = CCbc.objects.using(db).get_or_create(concept_from=concept, concept_child=n, concept_to=b_of_n)
                            if _: logging.debug("Created CCbc: " + ccbc.__unicode__())
                            else: logging.debug("Created CCbc: " + ccbc.__unicode__())

def create_CCbx_from_I(p, db='default'):
    for c in p.concepts.using(db).all():
        create_CCbx_from_C(c, db)

def create_CCbx(db='default'):
#    for concept in Concept.objects.using(db).all():
#    for concept in list(set(Concept.objects.using(db).filter(instance__datasets = dataset))):

#    for concept in Concept.objects.using(db).filter(meshuri = '',datasets = dataset):

#    for concept in Concept.objects.using(db).filter(datasets = dataset)[100:]:
    for concept in Concept.objects.using(db).filter(not_in_dataset=False):
        print "concept: " + concept.name
        create_CCbx_from_C(concept, db)

#def main(argv):
#    create_CCbx()

#if __name__ == "__main__":
#    import sys
#    main(sys.argv[1:])
