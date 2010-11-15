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

from django.db import models
from agave.models import *
##############################################################################
# EVALUATION (not being used)
##############################################################################


GRAPH_TYPES = (
    ('AAc', u'Actors linked by concepts in common'),
    ('AAb', u'Actors linked by broader concepts'),
    ('AAn', u'Actors linked by narrower concepts'),
    ('AAs', u'Actors linked by sibling concepts'),
    ('AAa', u'Actors linked by co-ancestors concepts'),
)
class Evaluation(models.Model):
    actor = models.ForeignKey(Actor, blank=True, null=True, editable=False)
#    graph_type = models.ChoiceField(choices=GRAPH_TYPES)
    graph_type = models.CharField(max_length=3, choices=GRAPH_TYPES, blank=True, null=True, editable=False) #widget=forms.Select(choices=TITLE_CHOICES)
    total_nodes = models.PositiveIntegerField()
    not_known_nodes = models.PositiveIntegerField()
    interesting_not_known_nodes = models.PositiveIntegerField()

    def __unicode__(self):
        return u"%s, %s, %s" % (self.actor, self.graph_type, self.interesting_not_known_nodes)

