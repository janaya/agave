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

import sys
try:
    from SPARQLWrapper import SPARQLWrapper, JSON
    from SPARQLWrapper.SPARQLExceptions import QueryBadFormed
except ImportError:
    sys.stderr.write("SPARQLWrapper must be installed")
    sys.exit(1)
from urllib2 import HTTPError
#from django.conf.settings import SPARQL_ENDPOINT_LOCAL
#SPARQL_ENDPOINT_LOCAL = False
from django.conf import settings
from mesh_skos_broader.query_templates import *
import logging

DBPEDIA_SPARQL_ENDPOINT = "http://dbpedia.org/sparql"

NC_SPARQL_ENDPOINT = \
    "http://localhost:8080/openrdf-sesame/repositories/sesame_mesh"

HCLS_SPARQL_ENDPOINT = \
    "http://hcls.deri.org/sparql"

LOCAL_SPARQL_ENDPOINT = \
    "http://localhost:8080/openrdf-sesame/repositories/sesame_mesh"

if settings.SPARQL_ENDPOINT_LOCAL:
    SPARQL_ENDPOINT = LOCAL_SPARQL_ENDPOINT
    FROM = LOCAL_FROM
else: 
    SPARQL_ENDPOINT = NC_SPARQL_ENDPOINT
    FROM = NC_FROM

def sparql_query(query):
    sparql = SPARQLWrapper(SPARQL_ENDPOINT)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
    except QueryBadFormed, e:
        logging.debug(query)
        logging.debug(e)
        sys.exit(1)
    except HTTPError, e:
        logging.debug(query)
        logging.debug(e)
        sys.exit(1)
    else:
        bindings = results["results"]["bindings"]
        return bindings

def getMeSHURIfromMeSHname(concept):
    """query Neurocommons to get the MeSH URI from a MeSH descriptor name"""
    bindings = sparql_query(t_query_meshuri_from_label % concept)
    if bindings:
        meshuri = bindings[0]["meshuri"]["value"]
        if bindings[0].get("runningHead", False):
            runningHead = bindings[0]["runningHead"]["value"]
        else: runningHead = None
        return meshuri, runningHead
    else:
        return None, None

def getDBURIfromMeSHURI(concepturi):
    """query HCLS to get the DBpedia URI from MeSH URI"""
    bindings = sparql_query(t_query_dbpedia_from_meshuri % concepturi)
    if bindings:
        dburi = bindings[0]["dburi"]["value"]
#    print "Done, fechted: " + str(dburi)
    return dburi

def getbroaders(concepturi):
#    broaderlabels = []
    broaders = []
    bindings = sparql_query(t_query_broader_from_uri_eswc06 % concepturi)
    for b in bindings:
        broaders.append({'meshuri': b["broader"]["value"], 'label': b["label"]["value"]})
##        broaderuri = b["broader"]["value"]
#        broaderlabels.append(b["label"]["value"])
#    return broaderlabels
#    print "Done"
    return broaders

def getnarrowers(concepturi):
#    broaderlabels = []
    narrowers = []
    bindings = sparql_query(t_query_narrower_from_uri_eswc06 % concepturi)
    for b in bindings:
##        broaderuri = b["broader"]["value"]
#        broaderlabels.append(b["label"]["value"])
#    return broaderlabels
        narrowers.append({'meshuri': b["narrower"]["value"], 'label': b["label"]["value"]})
#    print "Done"
    return narrowers

#def getDBbroader(dburi):
#    broaderlabels = []
#    bindings = sparql_query(t_query_broader_dbpedia % dburi)
#    for b in bindings:
##        broaderuri = b["broader"]["value"]
#        broaderlabels.append(b["label"]["value"])
##    print "Done"
#    return broaderlabels

#if __name__ == "__main__":
#
#    concept = "Phagocytes"
#    concepturi = getMeSHURIfromMeSHname(concept)
#    dburi = getDBURIfromMeSHURI(concepturi)
#    broaders = getbroader(concepturi)
#    print ', '.join(broaders)
#    narrowers = getnarrower(concepturi)
#    print ', '.join(narrowers)

