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

from django.db import IntegrityError, models
from django.utils.translation import ugettext_lazy as _
from exceptions import TypeError
import glob
import logging
import os.path
try:
    from itertools import combinations
except ImportError:
#    from utils import combinations
    print "python 2.6 is required"
#try:
#    import networkx as nx
#    from networkx.exception import NetworkXError
#except ImportError:
#    print "networkx must be installed"
#try:
#    from matplotlib import pyplot as plt
#except ImportError:
#    print "matplotlib must be installed"
#try:
#    import pylab as P
#except ImportError:
#    print "pylab must be installed"
#import pickle

#try:
#    from bioreader import *
#except ImportError:
#    print "bioreader must be installed"

#from fpggsna.models import *
#from crel.models import *
#_mysql_exceptions.IntegrityError
#from pysqlite2.dbapi2 import IntegrityError

##############################################################################
# BASIC MODELS
##############################################################################


class Instance(models.Model):
    pmid = models.CharField(_('pubmed id'), max_length=8, null=True, blank=True)
#    title = models.CharField(_('title'), max_length=255, unique=True)
    title = models.CharField(_('title'), max_length=255)
    year = models.CharField(_('year'), max_length=4, null=True, blank=True)
    abstract = models.TextField(_('abstract'), null=True, blank=True)
#    journal = models.CharField(_('journal'), max_length=255)
#    concept = models.ManyToManyField('Concept', verbose_name = _('concept'), related_name= 'instance_concept_set') # concept, ListaMs, m
#    concepts = models.ManyToManyField('Concept', through='concept_actor') # concept, ListaMs, m
    concepts = models.ManyToManyField('Concept', through='InstanceConcept') # concept, ListaMs, m
#    conceptMay = models.ManyToManyField('Concept', verbose_name = _('conceptmay'), related_name= 'instance_conceptmay_set')
#    MQ = models.ManyToManyField('Concept', verbose_name = _('mq'), related_name= 'instance_mq_set')
#    MQMay = models.ManyToManyField('Concept', verbose_name = _('mqmay'), related_name= 'instance_mqmay_set')
#    Mall = models.ManyToManyField('Concept', verbose_name = _('mall'), related_name= 'instance_mall_set')
    actors = models.ManyToManyField('Actor', through='InstanceActor') #, related_name = 'instance_set')# Lista

#    datasets = models.ManyToManyField('PubmedXMLDataset', through='Instance_Datasets')
#    datasets = models.ManyToManyField('PubmedXMLDataset')

    def num_actors(self):
        return len(self.actors.all())

    def num_concepts(self):
        return len(self.concepts.all())

    def __unicode__(self):
        return self.title

class InstanceActor(models.Model):
    instance = models.ForeignKey(Instance)
    actor = models.ForeignKey('Actor')
    weight = models.FloatField(null=True)

    def __unicode__(self):
        return "(" + self.instance.__unicode__() + ", " + self.actor.__unicode__() + ", " + str(self.weight) + ")"

class InstanceConcept(models.Model):
    instance = models.ForeignKey(Instance)
    concept = models.ForeignKey('Concept')
    weight = models.PositiveIntegerField(null=True)

    def __unicode__(self):
        return self.instance.__unicode__() + ", " + self.concept.__unicode__() + ", " + str(self.weight)

class Actor(models.Model):
#    name = models.CharField(_('actor name'), max_length=255, unique=True)
    name = models.CharField(_('actor name'), max_length=255)
    concepts = models.ManyToManyField('Concept', through='ActorConcept') # concept, ListaMs, m
    instances = models.ManyToManyField(Instance, through='InstanceActor')
#    coathor = M2M ('self', through='A_A_by_concept')
#    concept_rel_by_actor ForeignKey(Concept_concept_by_Actor)
#    datasets = models.ManyToManyField('PubmedXMLDataset')

    def __unicode__(self):
        return self.name

class ConceptBase(models.Model):
    name = models.CharField(_('concept word'), unique=True, max_length=255)
    meshuri = models.URLField(verify_exists=False, max_length=255, null=False)
    dburi = models.URLField(verify_exists=False, max_length=255, null=False)
    sparqled_broaders_nc = models.BooleanField(default=False)
    sparqled_broaders_db = models.BooleanField(default=False)
    #related_concept = ManyToManyField('Concept', through)
    #alter table crel_concept add runningHead varchar(255);
    runningHead = models.CharField(max_length=255, null=True)

    class Meta:
        abstract = True


    def __unicode__(self):
        return self.name

#class Conocept(models.Model):
#    name = models.SlugField(_('concept word'), unique=True)
#    actors = models.ManyToManyField(Actor,through='concept_actor')

class Concept(ConceptBase):
    actors = models.ManyToManyField(Actor, through='ActorConcept')
#    broaders = models.ManyToManyField('self', through='CCb', symmetrical=False)
    broaders = models.ManyToManyField('self', through='CCb', symmetrical=False, related_name='narrowers')
#    datasets = models.ManyToManyField('PubmedXMLDataset')
    #alter table crel_concept add not_in_dataset bool NOT NULL;
    not_in_dataset = models.BooleanField(default=False)


#class BroaderAAllManager(models.Manager):
#    def get_query_set(self):
#        pxds = PubmedXMLDataset.objects.get(name = "all")
#        return super(BroaderAAllManager, self).get_query_set().filter(datasets = pxds).filter(concept_from__not_in_dataset = False).filter(concept_to__not_in_dataset = False)

#class BroaderAResult2Manager(models.Manager):
#    def get_query_set(self):
#        pxds = PubmedXMLDataset.objects.get(name = "pubmed_result2.txt")
#        return super(BroaderAResult2Manager, self).get_query_set().filter(datasets = pxds).filter(concept_from__not_in_dataset = False).filter(concept_to__not_in_dataset = False)

class ActorConcept(models.Model):
    actor = models.ForeignKey(Actor)
    concept = models.ForeignKey(Concept)
    weight = models.PositiveIntegerField(null=True)
#    dataset = models.ForeignKey('PubmedXMLDataset')

    def __unicode__(self):
        return u"%s, %s, %s" % (self.actor, self.concept, self.weight)

##############################################################################
# CONCEPTS GRAPHS
##############################################################################

class CCp(models.Model):
    concept_from = models.ForeignKey(Concept, related_name='CCp_from')
    concept_to = models.ForeignKey(Concept, related_name='CCp_to')
#    actors = models.ManyToManyField(Actor,related_name='CCa_actors')
#    weight = models.PositiveIntegerField(null=True)
    instance = models.ForeignKey(Instance, related_name='CCp_Instance')

    def __unicode__(self):
        return u"%s, %s, %s" % (self.concept_from, self.instance, self.concept_to)

class CCa(models.Model):
    concept_from = models.ForeignKey(Concept, related_name='CCa_from')
    concept_to = models.ForeignKey(Concept, related_name='CCa_to')
#    actors = models.ManyToManyField(Actor,related_name='CCa_actors')
#    weight = models.PositiveIntegerField(null=True)
    actor = models.ForeignKey(Actor, related_name='CCa_actor')

    def __unicode__(self):
        return u"%s, %s, %s" % (self.concept_from, self.actor, self.concept_to)

#class CCpt(models.Model):
#    concept_from = models.ForeignKey(Concept, related_name='CCp_from')
#    concept_to = models.ForeignKey(Concept, related_name='CCp_to')

#    def __unicode__(self):
#        return u"%s, %s" % (self.concept_from, self.concept_to)

#class CCat(models.Model):
#    concept_from = models.ForeignKey(Concept, related_name='CCa_from')
#    concept_to = models.ForeignKey(Concept, related_name='CCa_to')
##    actors = models.ManyToManyField(Actor,related_name='CCa_actors')
##    weight = models.PositiveIntegerField(null=True)
#    actor = models.ForeignKey(Actor,related_name='CCa_actor')

#    def __unicode__(self):
#        return u"%s, %s" % (self.concept_from, self.concept_to)

##############################################################################
# CONCEPTS GRAPHS WITH BROADER PATTERNS
##############################################################################

class CCb(models.Model):
    concept_from = models.ForeignKey(Concept, related_name='has_broaders')
    concept_to = models.ForeignKey(Concept, related_name='is_broader_of')
#    transitive = models.BooleanField(default=False)
#    datasets = models.ManyToManyField('PubmedXMLDataset')
#    objects = models.Manager()
#    broadersAAll = BroaderAAllManager()
#    broadersAResult2 = BroaderAResult2Manager()

#    def actors_from(self, pxds):
#        return self.concept_to.actors.filter(datasets = pxds)

#    def actors_to(self, pxds):
#        return self.concept_to.actors.filter(datasets = pxds)

    def __unicode__(self):
        return u"%s, %s" % (self.concept_from, self.concept_to)

class CCbb(models.Model):
    concept_from = models.ForeignKey(Concept, related_name='CCbb_from')
    concept_parent = models.ForeignKey(Concept, related_name='CCbb_parent')
    concept_to = models.ForeignKey(Concept, related_name='CCbb_to')

    def __unicode__(self):
        return u"%s, %s, %s" % (self.concept_from, self.concept_parent,
                                self.concept_to)

class CCbc(models.Model):
    concept_from = models.ForeignKey(Concept, related_name='CCbc_from')
    concept_child = models.ForeignKey(Concept, related_name='CCbc_child')
    concept_to = models.ForeignKey(Concept, related_name='CCbc_to')

    def __unicode__(self):
        return u"%s, %s, %s" % (self.concept_from, self.concept_child,
                                self.concept_to)

class CCball(models.Model):
    concept_from = models.ForeignKey(Concept, related_name='CCball_from')
    concept_to = models.ForeignKey(Concept, related_name='CCball_to')

    def __unicode__(self):
        return u"%s, %s" % (self.concept_from, self.concept_to)

##############################################################################
# ACTORS GRAPHS
##############################################################################

class AAp(models.Model):
    actor_from = models.ForeignKey(Actor, related_name='AAp_from')
    actor_to = models.ForeignKey(Actor, related_name='AAp_to')
    instance = models.ForeignKey(Instance, related_name='AA_instance')

    def __unicode__(self):
        return u"%s, %s, %s" % (self.actor_from, self.instance,
                                self.actor_to)

class AAc(models.Model):
    actor_from = models.ForeignKey(Actor, related_name='AAc_from')
    actor_to = models.ForeignKey(Actor, related_name='AAc_to')
#    concepts = models.ManyToManyField(Concept,related_name='AAc_concepts')
#    weight = models.PositiveIntegerField(null=True)
    concept = models.ForeignKey(Concept, related_name='AAc_concept')

    def __unicode__(self):
        return u"%s, %s, %s" % (self.actor_from, self.concept,
                                self.actor_to)

##############################################################################
# ACTORS GRAPHS WITH BROADERS PATTERNS
##############################################################################

class AAba(models.Model):
    actor_from = models.ForeignKey(Actor, related_name='AAba_from')
    actor_to = models.ForeignKey(Actor, related_name='AAba_to')
#    concepts = models.ManyToManyField(Concept,related_name='AAba_concepts')
#    weight = models.PositiveIntegerField(null=True)
    ccba = models.ForeignKey(CCb, related_name='AAba_CCba')

    def __unicode__(self):
        return u"%s, %s, %s" % (self.actor_from, self.ccba, self.actor_to)


class AAbb(models.Model):
    actor_from = models.ForeignKey(Actor, related_name='AAbb_from')
    actor_to = models.ForeignKey(Actor, related_name='AAbb_to')
#    concepts = models.ManyToManyField(Concept,related_name='AAba_concepts')
#    weight = models.PositiveIntegerField(null=True)
    ccbb = models.ForeignKey(CCbb, related_name='AAbb_CCbb')

    def __unicode__(self):
        return u"%s, %s, %s" % (self.actor_from, self.actor_to, self.ccbb)

class AAbc(models.Model):
    actor_from = models.ForeignKey(Actor, related_name='AAbc_from')
    actor_to = models.ForeignKey(Actor, related_name='AAbc_to')
#    concepts = models.ManyToManyField(Concept,related_name='AAba_concepts')
#    weight = models.PositiveIntegerField(null=True)
    ccbc = models.ForeignKey(CCbc, related_name='AAbc_CCbc')

    def __unicode__(self):
        return u"%s, %s, %s" % (self.actor_from, self.ccbc, self.actor_to)

class AAbabc(models.Model):
    actor_from = models.ForeignKey(Actor, related_name='AAbabc_from')
    actor_to = models.ForeignKey(Actor, related_name='AAbabc_to')
    weight = models.PositiveIntegerField(null=True)

    def __unicode__(self):
        return u"%s, %s, %s" % (self.actor_from, self.actor_to, self.ccbc)

class AAcw(models.Model):
    actor_from = models.ForeignKey(Actor, related_name='AAcw_from')
    actor_to = models.ForeignKey(Actor, related_name='AAcw_to')
    weight = models.PositiveIntegerField(null=True)

    def __unicode__(self):
        return u"%s, %s" % (self.actor_from, self.actor_to,)

class AAbcw(models.Model):
    actor_from = models.ForeignKey(Actor, related_name='AAbcw_from')
    actor_to = models.ForeignKey(Actor, related_name='AAbcw_to')
    weight = models.PositiveIntegerField(null=True)

    def __unicode__(self):
        return u"%s, %s" % (self.actor_from, self.actor_to,)

class AAbbcw(models.Model):
    actor_from = models.ForeignKey(Actor, related_name='AAbbcw_from')
    actor_to = models.ForeignKey(Actor, related_name='AAbbcw_to')
    weight = models.PositiveIntegerField(null=True)

    def __unicode__(self):
        return u"%s, %s" % (self.actor_from, self.actor_to,)

class AAbabcw(models.Model):
    actor_from = models.ForeignKey(Actor, related_name='AAbabcw_from')
    actor_to = models.ForeignKey(Actor, related_name='AAbabcw_to')
    weight = models.PositiveIntegerField(null=True)

    def __unicode__(self):
        return u"%s, %s" % (self.actor_from, self.actor_to,)

class AAball(models.Model):
    actor_from = models.ForeignKey(Actor, related_name='AAball_from')
    actor_to = models.ForeignKey(Actor, related_name='AAball_to')

    def __unicode__(self):
        return u"%s, %s" % (self.actor_from, self.actor_to,)

##############################################################################
# ACTORS-CONCEPTS GRAPHS WITH BROADERS
##############################################################################


class ACb(models.Model):
    actor = models.ForeignKey(Actor)
    concept = models.ForeignKey(Concept)

    def __unicode__(self):
        return u"%s, %s, %s" % (self.actor, self.concept)
