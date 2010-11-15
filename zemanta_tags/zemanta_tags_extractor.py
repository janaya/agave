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

import urllib
from django.utils import simplejson
from django.conf import settings

def extract_concepts(text):
    text = text.encode('utf8')
    gateway = 'http://api.zemanta.com/services/rest/0.0/'
    args = {'method': 'zemanta.suggest',
#        'api_key': 'key1234',
            'api_key': settings.ZEMANTA_KEY,
            'text': text,
            'return_categories': 'dmoz',
            'format': 'json',
    #        'return_rdf_links': 0,
            'return_images':0,
            'personal_scope':0,
            'articles_limit':0
            }
    args_enc = urllib.urlencode(args)
#    args_enc = urllib.quote(args)

    raw_output = urllib.urlopen(gateway, args_enc).read()
    output = simplejson.loads(raw_output)
    #pprint(output)
#    tags = [output['markup']['links'][i]['target']['title'] for i in range(len(output['markup']['links'])) if output['markup']['links'][i]['confidence']>0.1]
#    keywords = [output['keywords'][i]['name'] for i in range(len(output['keywords'])) if output['keywords'][i]['confidence']>0.1]
#    categories_set = set()
##    [[categories_set.add(j) for j in output['categories'][i]['name'].split('/')[1:]] for i in range(len(output['categories']))]
#    [[categories_set.add(' '.join(j.split('_'))) for j in output['categories'][i]['name'].split('/')[1:]] for i in range(len(output['categories'])) if output['categories'][i]['confidence']>0.1]
#    concepts = set(tags+keywords+list(categories_set))
#    return concepts
    tags = set()
    [[tags.add(j['title']) for j in i['target'] if (j['type'] == 'ncbi' or j['type'] == 'wikipedia')] for i in output['markup']['links'] if i['confidence'] > 0.1]
    return tags
