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


from django.contrib import admin
from models import *

class ActorInline(admin.TabularInline):
    model = Actor
    extra = 0

class ConoceptInline(admin.TabularInline):
    model = Concept
    extra = 0

class InstanceActorInline(admin.TabularInline):
    model = Instance.actors.through
    extra = 0
    classes = ['collapse', 'collapsed']
    readonly_fields = ('instance', 'actor', 'weight')

class InstanceConceptInline(admin.TabularInline):
    model = Instance.concepts.through
    extra = 0
    readonly_fields = ('instance', 'concept', 'weight')

class ActorConceptInline(admin.TabularInline):
    model = Actor.concepts.through
    extra = 0
    readonly_fields = ('actor', 'concept', 'weight')

#class ConoceptBroaderInline(admin.TabularInline):
#    model = Concept.broaders.through
#    extra = 0

#class ConoceptInline(admin.TabularInline):
#    model = CCb.concept_to.through
#    extra = 0

class BroaderToInline(admin.TabularInline):
    model = CCb
    fk_name = "concept_to"
    extra = 0
#    readonly_fields = ('concept_from')

class BroaderFromInline(admin.TabularInline):
    model = CCb
    fk_name = "concept_from"
    extra = 0
#    readonly_fields = ('concept_to')

class CCaFromInline(admin.TabularInline):
    model = CCa
    fk_name = "concept_from"
    extra = 0

class BroaderAdmin(admin.ModelAdmin):
    readonly_fields = ('concept_from', 'concept_to')
    list_filter = ('concept_to',)
    list_display = ('concept_from', 'concept_to',)
    search_fields = ['concept_to__name', 'concept_from__name']
#    inlines = [
#        BroaderFromInline,
#    ]

#class ConceptAdmin(admin.ModelAdmin):
#    search_fields = ['name']
#    ordering = ('name',)
##    search_fields = ['instance_concept_set__title']
##    inlines = [
##        InstanceInline,
##    ]

#class ConoceptInline(admin.TabularInline):
#    model = CCb.concept_to

class InstanceAdmin(admin.ModelAdmin):
    readonly_fields = ('pmid', 'title', 'actors', 'concepts')
    list_display = ('pmid', 'title')#, 'year') #, 'actors')
 #   list_filter = ('pmid','title') #,'actors')
    search_fields = ['pmid', 'title'] #, 'actors__name', 'Mall__name']
    ordering = ('title',)
    inlines = [
        InstanceActorInline,
        InstanceConceptInline,
    ]


class ActorAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'concepts', 'instances')
    search_fields = ['name'] #, 'instance_set__title']
    ordering = ('name',)
#    list_display = ('all_instances_str', )
    inlines = [
#        ActorConceptInline,
        ActorConceptInline,
        InstanceActorInline,
#        CCaInline,
    ]

class ConceptAdmin(admin.ModelAdmin):
    exclude = ('dburi', 'sparqled_broaders_db', 'sparqled_broaders_nc')
    readonly_fields = ('name', 'meshuri', 'actors', 'broaders', 'runningHead', 'not_in_dataset')
    search_fields = ['name'] # ,'instance_concept_set__title']
    ordering = ('name',)
#    list_display = ()
    inlines = [
        ActorConceptInline,
        InstanceConceptInline,
        BroaderToInline,
        BroaderFromInline,
#        CCaFromInline,
    ]

class CCaAdmin(admin.ModelAdmin):
    readonly_fields = ('concept_from', 'concept_to', 'actor')
    search_fields = ['concept_from', 'concept_to', 'actor']
    ordering = ('concept_from', 'concept_to', 'actor')
#    inlines = [
#    ]

class CCbbAdmin(admin.ModelAdmin):
    readonly_fields = ('concept_from', 'concept_to', 'concept_parent')
    search_fields = ['concept_from', 'concept_to', 'concept_parent']
    ordering = ('concept_from', 'concept_to', 'concept_parent')
#    inlines = [
#    ]

class CCbcAdmin(admin.ModelAdmin):
    readonly_fields = ('concept_from', 'concept_to', 'concept_child')
    search_fields = ['concept_from', 'concept_to', 'concept_child']
    ordering = ('concept_from', 'concept_to', 'concept_child')
#    inlines = [
#    ]

class AAcAdmin(admin.ModelAdmin):
    readonly_fields = ('actor_from', 'actor_to', 'concept')
    search_fields = ['actor_from', 'actor_to', 'concept']
    ordering = ('actor_from', 'actor_to', 'concept')
#    inlines = [
#    ]

class AAbaAdmin(admin.ModelAdmin):
    readonly_fields = ('actor_from', 'actor_to', 'ccba')
    search_fields = ['actor_from', 'actor_to', 'ccba']
    ordering = ('actor_from', 'actor_to', 'ccba')
#    inlines = [
#    ]

class AAbbAdmin(admin.ModelAdmin):
    readonly_fields = ('actor_from', 'actor_to', 'ccbb')
    search_fields = ['actor_from', 'actor_to', 'ccbb']
    ordering = ('actor_from', 'actor_to', 'ccbb')
#    inlines = [
#    ]

class AAbcAdmin(admin.ModelAdmin):
    readonly_fields = ('actor_from', 'actor_to', 'ccbc')
    search_fields = ['actor_from', 'actor_to', 'ccbc']
    ordering = ('actor_from', 'actor_to', 'ccbc')
#    inlines = [
#    ]

admin.site.register(Instance, InstanceAdmin)
admin.site.register(Actor, ActorAdmin)
#admin.site.register(Concept, ConceptAdmin)
admin.site.register(Concept, ConceptAdmin)
admin.site.register(CCb, BroaderAdmin)

admin.site.register(CCa, CCaAdmin)
admin.site.register(CCbb, CCbbAdmin)
admin.site.register(CCbc, CCbcAdmin)

admin.site.register(AAc, AAcAdmin)
admin.site.register(AAba, AAbaAdmin)
admin.site.register(AAbb, AAbbAdmin)
admin.site.register(AAbc, AAbcAdmin)
