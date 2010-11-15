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

#from string import Template
#s = Template()
#regex doesn't work on 4Store

#DBPEDIA_SPARQL_ENDPOINT = "http://dbpedia.org/sparql"
#NC_SPARQL_ENDPOINT = ""http://sparql.neurocommons.org/sparql"
#NC_SPARQL_ENDPOINT = \
#"http://localhost:8080/openrdf-sesame/repositories/sesame_mesh"
#HCLS_SPARQL_ENDPOINT = "http://hcls.deri.org/sparql"
#LOCAL_SPARQL_ENDPOINT = \
#    "http://localhost:8080/openrdf-sesame/repositories/sesame_mesh"

RDF_NS = "rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>"
SKOS_NS = "skos:<http://www.w3.org/2004/02/skos/core#>"
MESH_NS = "mesh:<http://purl.org/science/owl/mesh/>"
MH_NS = "mh:<http://purl.org/commons/record/mesh/>"
MESH_ESWC06_NS = "mesh:<http://www.nlm.nih.gov/mesh/2006#>"

NC_FROM = " from <http://purl.org/science/graph/mesh/mesh-skos> " 
LOCAL_FROM = ""
FROM = LOCAL_FROM

PREFIX = " PREFIX "
PREFIX_RDF = PREFIX + RDF_NS
PREFIX_SKOS = PREFIX + SKOS_NS 
PREFIX_MESH = PREFIX + MESH_NS
PREFIX_MH = PREFIX + MH_NS

PREFIXES_NC = PREFIX_RDF + PREFIX_MESH + PREFIX_SKOS

#       where {
#            { ?meshuri  skos:altLabel """ + '"' + concept + '"' + """@en } 
#            UNION 
#            { ?meshuri  skos:prefLabel """ + '"' + concept + '"' + """@en } 
#            UNION 
#            { ?meshuri  skos:hiddenLabel """ + '"' + concept + '"' + """@en } 
#            OPTIONAL {?meshuri mesh:runningHead ?runningHead}.
#        }"""
query_meshuri_from_label = """
    SELECT *
        """ + FROM + """
       WHERE {
           ?meshuri rdf:type skos:Concept. 
           ?meshuri skos:prefLabel ?name.
           OPTIONAL {?meshuri mesh:runningHead ?runningHead}.
           FILTER regex(?name, "%s", "i" ) 
       }"""
query_meshuri_from_label = """
    SELECT *
        """ + FROM + """
       WHERE {
           ?meshuri rdf:type skos:Concept. 
           ?meshuri skos:prefLabel "%s"@en.
           OPTIONAL {?meshuri mesh:runningHead ?runningHead}. 
       }"""
t_query_meshuri_from_label = PREFIXES_NC + query_meshuri_from_label


query_dbpedia_from_meshuri = """
    SELECT *
        WHERE {
            ?dburi rdfs:seeAlso <%s>
    }"""
t_query_dbpedia_from_meshuri = PREFIX_RDF + query_dbpedia_from_meshuri

query_broader_from_uri = """
    SELECT *
        """ + FROM + """
        WHERE { 
            mesh:%s skos:broader ?broader.
            ?broader a skos:Concept.
            ?broader skos:prefLabel ?label.
        }
"""

t_query_broader_from_uri = PREFIXES_NC + query_broader_from_uri

query_broader_from_uri_eswc06 = """
    SELECT *
        WHERE { 
            <%s> skos:broader ?broader.
            ?broader a skos:Concept.
            ?broader skos:prefLabel ?label.
        }
"""
t_query_broader_from_uri_eswc06 = PREFIX_SKOS + query_broader_from_uri_eswc06

query_narrower_from_uri = """
    SELECT *
        """ + FROM + """
        WHERE { 
            ?narrower skos:broader mesh:%s.
            ?narrower a skos:Concept.
            ?narrower skos:prefLabel ?label.
        }
"""
t_query_narrower_from_uri = PREFIXES_NC + query_narrower_from_uri

query_narrower_from_uri_eswc06 = """
    SELECT *
        WHERE {
            ?narrower skos:broader  <%s>.
            ?narrower a skos:Concept.
            ?narrower skos:prefLabel ?label.
        }
"""

t_query_narrower_from_uri_eswc06 = PREFIX_SKOS + query_narrower_from_uri_eswc06
    
