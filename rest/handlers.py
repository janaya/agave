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
from agave.models import Actor, Concept, Instance, InstanceActor, \
    InstanceConcept
from agave.controller_js_graph_generators import *
from agave.controller_CCbx_models_generator import create_CCbx_from_C, \
    delete_CCbx_from_I, delete_CCbx_from_C
from agave.controller_graph_models_generator import create_CI_from_I, \
    generate_CCp, delete_CI_from_I, delete_CCp_from_I, create_AC_from_A_I, \
    create_AAp_from_I_A, create_CCa_from_A_I, create_AAc_from_A_I, \
    delete_AAp_from_I_A, delete_AC_from_I_A, delete_AAc_from_I_A, \
    delete_CCa_from_I_A, create_AC_from_C_I, create_CCp_from_I, \
    create_CCa_from_C_I, create_AAc_from_C_I, delete_AC_from_I_C, \
    delete_AAc_from_I_C, delete_CCa_from_I_C, delete_CCp_from_I_C
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from piston.handler import BaseHandler, AnonymousBaseHandler
from piston.utils import rc #, validate, require_mime #, require_extended
from zemanta_tags.zemanta_tags_extractor import extract_concepts
#import logging
#from django.db import IntegrityError
#from agave.models import Actor, Instance, Concept, InstanceActor, \
#    InstanceConcept

BaseHandler.fields = AnonymousBaseHandler.fields = ()

class ActorHandler(BaseHandler):
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    model = Actor
    fields = ('id', 'name')
#    fields = ('id', 'name', ('instances', ('id', 'name')),
#                            ('concepts', ('id', 'name')))
#    exclude = ('id','concepts','instances')
#    exclude = ()

#    def read(self, request, actor_name=None):
    def read(self, request, db, actor_id=None):
        """
        @return: 
            404 Not Found
            JSON...
        """
        if db == 'projects': db = 'default'
        elif db != 'publications':
            resp = rc.BAD_REQUEST
            resp.write(" No database specified")
            logging.debug(resp)
            return resp
        base = self.model.objects.using(db)
        if actor_id:
            try:
                a = base.get(id=actor_id)
                return a

            except ObjectDoesNotExist:
                return rc.NOT_FOUND
        else:
            return base.all()

        #@classmethod
        #def mymanytomanyfield(cls, myinstance):
            #return myinstance.mymanytomanyfield.all()

#    @validate(ActorForm)
    def create(self, request, db):
        """
        @return: 
            409 Conflict/Duplicate
            201 Created
            400 Bad Request
        Example JSON as POST body:
            "id": "20000",
            "name": "Julia Anaya", 
        """
        if db == 'projects': db = 'default'
        elif db != 'publications':
            resp = rc.BAD_REQUEST
            resp.write(" No database specified")
            logging.debug(resp)
            return resp
        attrs = self.flatten_dict(request.POST)
        if request.content_type:
            try:
                data = request.data
            except AttributeError:
                pass
            else:
                attrs = data
        logging.debug(attrs)
        if 'id' not in attrs or 'name' not in attrs:
            resp = rc.BAD_REQUEST
            resp.write(" Missing id or name")
            logging.debug(resp)
            return resp
#        elif self.model.objects.using(db).filter(id=attrs['id']):
#            logging.debug(rc.DUPLICATE_ENTRY)
#            return rc.DUPLICATE_ENTRY
        else:
            #a = self.model(id=attrs['id'], name=attrs['name'])
            try:
                a = self.model(**attrs)
                a.save(using=db)
            except IntegrityError:
                logging.debug(rc.DUPLICATE_ENTRY)
                return rc.DUPLICATE_ENTRY

#            for p in data['instances']:
#                weight = 1.0/len(p['actors'])
#                Instance(title=p['title'], year=p['year']).save()
#                pa, created = InstanceActor.objects.get_or_create(
#                            actor = a, instance = p, weight = weight)

            logging.debug("Created: " + a.__unicode__())
            return rc.CREATED


#    @validate(ActorForm, 'PUT')
    def update(self, request, db, actor_id):
        """
        Example JSON as PUT body:
            "name": "Michael AA MIGLIOR", 
        """
        if db == 'projects': db = 'default'
        elif db != 'publications':
            resp = rc.BAD_REQUEST
            resp.write(" No database specified")
            logging.debug(resp)
            return resp
        attrs = self.flatten_dict(request.PUT)
        if request.content_type:
            try:
                data = request.data
            except AttributeError:
                pass
            else:
                attrs = data
        logging.debug(attrs)
        if 'name' not in attrs:
            resp = rc.BAD_REQUEST
            resp.write(" Missing name")
            logging.debug(resp)
            return resp

#        if self.exists(**attrs) :
#        if self.model.objects.using(db).filter(**attrs):
#            print "duplicate"
#            return rc.DUPLICATE_ENTRY
##        if attrs.has_key('id'):
##            actor_id = attrs['id']
#        else:
        try:
            a = self.model.objects.using(db).get(id=actor_id)
            print a
        except ObjectDoesNotExist:
            return rc.NOT_FOUND
        else:
            a.name = attrs['name']
            a.save(using=db)

            resp = rc.CREATED
    #        resp.write("Everything went fine!")
            return resp

    def delete(self, request, db, actor_id):
        if db == 'projects': db = 'default'
        elif db != 'publications':
            resp = rc.BAD_REQUEST
            resp.write(" No database specified")
            logging.debug(resp)
            return resp
        try:
#            a = Actor.objects.get(name=attrs['name'])
            a = self.model.objects.using(db).get(id=actor_id)
        except ObjectDoesNotExist:
            return rc.NOT_FOUND
        else:
            logging.debug("Deleted A: " + a.__unicode__())
            a.delete(using=db)
            resp = rc.DELETED
            return resp


#    @classmethod
#    def resource_uri(cls, actor=None):
#        if actor:
#            return ('actors', [actor.id])
#        else: return ('actors', ['id'])
#    @classmethod
#    def resource_uri(cls, db, actor=None):
#        if actor:
#            return ('actors', [db,actor.id])
#        else: return ('actors', [db, 'id'])
#    @classmethod
#    def resource_uri(cls, db, actor=None):
##        print args
#        #print kwargs
#        #args = None
#        #kwargs = None
##        if actor:
##            return ('actors', [actor.id])
##        else: 
#        return ('actors', ['db', 'id'])


#class AnonymousActorHandler(ActorHandler, AnonymousBaseHandler):
#    pass

class InstanceHandler(BaseHandler):
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    model = Instance
    fields = ('id', 'title', 'year', 'abstract')

    def read(self, request, db, instance_id=None): #title):
        if db == 'projects': db = 'default'
        elif db != 'publications':
            resp = rc.BAD_REQUEST
            resp.write(" No database specified")
            logging.debug(resp)
            return resp
        base = self.model.objects.using(db)

#        if title:
#            return base.get(title=title)
        if instance_id:
            try:
                return base.get(id=instance_id)
            except ObjectDoesNotExist:
                return rc.NOT_FOUND
        else:
            return base.all()

    #@require_mime('json')
    def create(self, request, db):
        """
        Example JSON as POST body:
            'id':'20001',
            'title':'Enrichment of Affiliation Networks...',
            'abstract':'As a result of the Linking Open Data project...'
            'year': 2010
        @return: 
            409 Conflict/Duplicate
            201 Created
            400 Bad Request
        @TODO: create concepts, create broaders
        """
        if db == 'projects': db = 'default'
        elif db != 'publications':
            resp = rc.BAD_REQUEST
            resp.write(" No database specified")
            logging.debug(resp)
            return resp
        attrs = self.flatten_dict(request.POST)
        if request.content_type:
            try:
                data = request.data
            except AttributeError:
                pass
            else:
                attrs = data
        logging.debug(attrs)
        if 'id' not in attrs or 'title' not in attrs:
            resp = rc.BAD_REQUEST
            resp.write(" Missing id or title")
            logging.debug(resp)
            return resp
        elif self.model.objects.using(db).filter(id=attrs['id']):
            logging.debug(rc.DUPLICATE_ENTRY)
            return rc.DUPLICATE_ENTRY
        else:
            try:
                p = self.model(id=int(attrs['id']),
                           title=attrs['title'],
                           year=attrs.get('year', None),
                           abstract=attrs.get('abstract', None))

#            p = self.model(**attrs)
                p.save(using=db)
                logging.debug("created I: " + p.__unicode__())
            except IntegrityError:
                logging.debug(rc.DUPLICATE_ENTRY)
                return rc.DUPLICATE_ENTRY
            else:
                if db == 'default' and p.abstract:
                    concepts = extract_concepts(p.abstract)
                    create_CI_from_I(p, concepts, db)
                    generate_CCp(p, db)

            # search broaders
            # update CCb

                return rc.CREATED

    def update(self, request, db, instance_id):
        """
        Example JSON as PUT body:
            "year": "2010", 
            "title": "SEUGNET Laurent - ESPCI"
        """
        if db == 'projects': db = 'default'
        elif db != 'publications':
            resp = rc.BAD_REQUEST
            resp.write(" No database specified")
            logging.debug(resp)
            return resp
        attrs = self.flatten_dict(request.PUT)
        if request.content_type:
            try:
                data = request.data
            except AttributeError:
                pass
            else:
                attrs = data
        logging.debug(attrs)
#        if 'title' not in attrs:
#            resp = rc.BAD_REQUEST
#            resp.write(" Missing title")
#            logging.debug(resp)
#            return resp
        try:
            p = self.model.objects.using(db).get(id=instance_id)
            print p
        except ObjectDoesNotExist:
            return rc.NOT_FOUND
        else:
            if attrs.has_key('title'): p.title = attrs['title']
            if attrs.has_key('year'): p.year = attrs['year']
            if attrs.has_key('abstract'): p.year = attrs['abstract']
                # if abstract changed, regenerate C?
            p.save(using=db)
            logging.debug(rc.ALL_OK)
            return rc.ALL_OK

    def delete(self, request, db, instance_id):
        if db == 'projects': db = 'default'
        elif db != 'publications':
            resp = rc.BAD_REQUEST
            resp.write(" No database specified")
            logging.debug(resp)
            return resp
        try:
            p = self.model.objects.using(db).get(id=instance_id)
        except ObjectDoesNotExist:
            return rc.NOT_FOUND
        else:
            # delete CCp only if concepts extracted from zemanta?
            if p.abstract and db == 'default':
                delete_CI_from_I(p, db)
                delete_CCp_from_I(p, db)
                delete_CCbx_from_I(p, db)
            p.delete(using=db)
            logging.debug("Deleted I: " + p.__unicode__())
            return rc.DELETED

#    @classmethod
#    def resource_uri(cls, instance=None):
#        if instance:
#            return ('instances', [instance.id, ])
#        else: return ('instances', ['id'])

#class AnonymousInstanceHandler(InstanceHandler, AnonymousBaseHandler):
#    pass

class InstanceActorHandler(BaseHandler):
    """
    @TODO: weight mandatory?, id should be given by InstanceActor
    """
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    model = InstanceActor
    fields = ('id', 'weight')

    def read(self, request, db, instance_id, actor_id=None):
        if db == 'projects': db = 'default'
        elif db != 'publications':
            resp = rc.BAD_REQUEST
            resp.write(" No database specified")
            logging.debug(resp)
            return resp
        try:
            p = Instance.objects.using(db).get(id=instance_id)
            print p
        except ObjectDoesNotExist:
            return rc.NOT_FOUND
        base = p.actors.using(db)

        if actor_id:
            try:
                return base.filter(id=actor_id)
            except ObjectDoesNotExist:
                return rc.NOT_FOUND
        else:
            return base.all()

    def create(self, request, db, instance_id, actor_id):
        """
        @param instance_id: project id
        @param actor_id: actor id
        weight: 1/total number of actors in the project
        Example JSON as POST body:
            "id": "2",
            "weight": "1.0", 
        @return: 
            404 Not Found
            409 Conflict/Duplicate
            201 Created
            400 Bad Request
        """
        if db == 'projects': db = 'default'
        elif db != 'publications':
            resp = rc.BAD_REQUEST
            resp.write(" No database specified")
            logging.debug(resp)
            return resp
        logging.debug(str(instance_id) + str(actor_id))
        attrs = self.flatten_dict(request.POST)
        if request.content_type:
            try:
                data = request.data
            except AttributeError:
                pass
            else:
                attrs = data
        logging.debug(attrs)
        if 'id' not in attrs:
            resp = rc.BAD_REQUEST
            resp.write(" Missing id")
            logging.debug(resp)
            return resp
#        elif self.model.objects.using(db).filter(id=attrs['id']):
#            logging.debug(rc.DUPLICATE_ENTRY)
#            return rc.DUPLICATE_ENTRY
        else:
            try:
                p = Instance.objects.using(db).get(id=instance_id)
                a = Actor.objects.using(db).get(id=actor_id)
            except ObjectDoesNotExist:
                logging.debug(rc.NOT_FOUND)
                return rc.NOT_FOUND
            else:
                try:
                    pa = self.model(id=attrs['id'], instance=p, actor=a,
                                    weight=attrs.get('weight', None))
                    pa.save(using=db)
                    logging.debug("Created PA: " + pa.__unicode__())

                except IntegrityError:
                    logging.debug(rc.DUPLICATE_ENTRY)
                    return rc.DUPLICATE_ENTRY
                else:
                    create_AC_from_A_I(a, p, db)
                    print "after AC"
                    create_AAp_from_I_A(a, p, db)
                    print "after AAi"

                    create_CCa_from_A_I(a, p, db)
                    print "after CCa"
                    create_AAc_from_A_I(a, p, db) # a1axcx, a1aycy...
                    print "after AAc"

                    return rc.CREATED

    def update(self, request, db, instance_id, actor_id):
        """
        @param instance_id: project id
        @param actor_id: actor id
        weight: 1/total number of actors in the project
        Example JSON as PUT body:
            "id": "2"
            "weight": "0.3", 
        """
        if db == 'projects': db = 'default'
        elif db != 'publications':
            resp = rc.BAD_REQUEST
            resp.write(" No database specified")
            logging.debug(resp)
            return resp
        attrs = self.flatten_dict(request.POST)
        if request.content_type:
            try:
                data = request.data
            except AttributeError:
                pass
            else:
                attrs = data
        logging.debug(attrs)
        if 'weight' not in attrs:
            resp = rc.BAD_REQUEST
            resp.write(" Missing name")
            logging.debug(resp)
            return resp
        try:
            p = Instance.objects.using(db).get(id=instance_id)
            print p
            a = Actor.objects.using(db).get(id=actor_id)
            print a
            pa = self.model.objects.using(db).get(id=attrs['id'])
        except ObjectDoesNotExist:
            return rc.NOT_FOUND
        else:
            pa.instance = p
            pa.actor = a
            pa.weight = attrs['weight']
            pa.save(using=db)
            logging.debug(rc.ALL_OK)
            return rc.ALL_OK

    def delete(self, request, db, instance_id, actor_id):
        if db == 'projects': db = 'default'
        elif db != 'publications':
            resp = rc.BAD_REQUEST
            resp.write(" No database specified")
            logging.debug(resp)
            return resp
        try:
            pa = self.model.objects.using(db).get(
                                            instance__id=instance_id,
                                            actor__id=actor_id)
            a = pa.actor
            p = pa.instance
        except ObjectDoesNotExist:
            return rc.NOT_FOUND
        else:
            # delete AAp
            delete_AAp_from_I_A(p, a, db)

            # delete AC
            delete_AC_from_I_A(p, a, db)

            # delete AAc
            delete_AAc_from_I_A(p, a, db)

            # delete CCa
            delete_CCa_from_I_A(p, a, db)

            #remove AI
            pa.delete(using=db)
            logging.debug("Deleted AI:" + pa.__unicode__())
            resp = rc.DELETED
            return resp

#    @classmethod
#    def resource_uri(cls, instance, actor=None):
#        if actor:
#            return ('instance_actors', [instance.id], [actor.id])
#        else:
#            return ('instance_actors', [instance.id], ['id'])

#    @classmethod
#    def resource_uri(cls, instance, actor=None):
#        if actor:
#            return ('instance_actors', [instance.id, actor.id])
#        else:
#            return ('instance_actors', [instance.id, 'id'])

#class AnonymousInstanceActorHandler(InstanceActorHandler, AnonymousBaseHandler):
#    pass

class InstanceConceptHandler(BaseHandler):
    """
    @TODO: weight mandatory?, id should be given by InstanceConcept
    """
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    model = InstanceConcept
    fields = ('id', 'weight')

    def read(self, request, db, instance_id, concept_id=None):
        if db == 'projects': db = 'default'
        elif db != 'publications':
            resp = rc.BAD_REQUEST
            resp.write(" No database specified")
            logging.debug(resp)
            return resp
        try:
            p = Instance.objects.using(db).get(id=instance_id)
            print p
        except ObjectDoesNotExist:
            return rc.NOT_FOUND
        base = p.concepts.using(db)

        if concept_id:
            try:
                return base.filter(id=concept_id)
            except:
                return rc.NOT_FOUND
        else:
            return base.all()

    def create(self, request, db, instance_id, concept_id):
        """
        @param instance_id: project id
        @param concept_id: concept id
        weight: 1
        Example JSON as POST body:
            "id": "2"
            "weight": "1", 
        @return:
            404 Not Found
            409 Conflict/Duplicate
            201 Created
            400 Bad Request
        """
        if db == 'projects': db = 'default'
        elif db != 'publications':
            resp = rc.BAD_REQUEST
            resp.write(" No database specified")
            logging.debug(resp)
            return resp
        attrs = self.flatten_dict(request.POST)
        if request.content_type:
            try:
                data = request.data
            except AttributeError:
                pass
            else:
                attrs = data
        logging.debug(attrs)
        if 'id' not in attrs:
            resp = rc.BAD_REQUEST
            resp.write(" Missing id")
            logging.debug(resp)
            return resp
#        elif self.model.objects.using(db).filter(id=attrs['id']):
#            logging.debug(rc.DUPLICATE_ENTRY)
#            return rc.DUPLICATE_ENTRY
        else:
            try:
                p = Instance.objects.using(db).get(id=instance_id)
                c = Concept.objects.using(db).get(id=concept_id)
            except ObjectDoesNotExist:
                logging.debug(rc.NOT_FOUND)
                return rc.NOT_FOUND
            else:
                try:
                    pc = self.model(id=attrs['id'], instance=p, concept=c, weight=attrs.get('weight', None))
                    pc.save(using=db)
                except IntegrityError:
                    logging.debug(rc.DUPLICATE_ENTRY)
                    return rc.DUPLICATE_ENTRY
                else:
                    create_AC_from_C_I(c, p, db)
                    create_CCp_from_I(c, p, db)

                    create_CCa_from_C_I(c, p, db)
                    create_AAc_from_C_I(c, p, db) # a1axcx, a1aycy...

                    return rc.CREATED

    def update(self, request, db, instance_id, concept_id):
        """
        @param instance_id: project id
        @param concept_id: concept id
        weight: 1
        Example JSON as PUT body:
            "id": "2"
            "weight": "1", 
        """
        if db == 'projects': db = 'default'
        elif db != 'publications':
            resp = rc.BAD_REQUEST
            resp.write(" No database specified")
            logging.debug(resp)
            return resp
        attrs = self.flatten_dict(request.POST)
        if request.content_type:
            try:
                data = request.data
            except AttributeError:
                pass
            else:
                attrs = data
        logging.debug(attrs)
        if 'weight' not in attrs:
            resp = rc.BAD_REQUEST
            resp.write(" Missing weight")
            logging.debug(resp)
            return resp
        try:
            p = Instance.objects.using(db).get(id=instance_id)
            print p
            c = Concept.objects.using(db).get(id=concept_id)
            print c
            pc = self.model.objects.using(db).get(id=attrs['id'])
        except ObjectDoesNotExist:
            return rc.NOT_FOUND
        else:
            pc.instance = p
            pc.concept = c
            pc.weight = attrs['weight']
            pc.save(using=db)
            logging.debug(rc.ALL_OK)
            return rc.ALL_OK

    def delete(self, request, db, instance_id, concept_id):
        if db == 'projects': db = 'default'
        elif db != 'publications':
            resp = rc.BAD_REQUEST
            resp.write(" No database specified")
            logging.debug(resp)
            return resp
        try:
            pc = self.model.objects.using(db).get(
                                            instance__id=instance_id,
                                            concept__id=concept_id)
            c = pc.concept
            p = pc.instance
        except ObjectDoesNotExist:
            return rc.NOT_FOUND
        else:
            # delete AAp
            delete_CCp_from_I_C(p, c, db)

            # delete AC
            delete_AC_from_I_C(p, c, db)

            # delete AAc
            delete_AAc_from_I_C(p, c, db)

            # delete CCa
            delete_CCa_from_I_C(p, c, db)
            logging.debug("Deleted CI:" + pc.__unicode__())
            pc.delete(using=db)
            return rc.DELETED

#    @classmethod
#    def resource_uri(cls, instance, concept=None):
#        if concept:
#            return ('instance_concepts', [instance.id, concept.id])
#        else:
#            return ('instance_concepts', [instance.id, 'id'])


#class AnonymousInstanceConceptHandler(InstanceConceptHandler, AnonymousBaseHandler):
#    pass

class ConceptHandler(BaseHandler):
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    model = Concept
    fields = ('id', 'name')

    def read(self, request, db, concept_id=None):
        if db == 'projects': db = 'default'
        elif db != 'publications':
            resp = rc.BAD_REQUEST
            resp.write(" No database specified")
            logging.debug(resp)
            return resp

        base = self.model.objects.using(db)

        if concept_id:
            try:
                return base.get(id=concept_id)
            except:
                return rc.NOT_FOUND
        else:
            return base.all()

    def create(self, request, db):
        """
        Example JSON as POST body:
            "id": "2"
             "name": "Sleep deprivation", 
        @return: 
            409 Conflict/Duplicate
            201 Created
            400 Bad Request
        """
        if db == 'projects': db = 'default'
        elif db != 'publications':
            resp = rc.BAD_REQUEST
            resp.write(" No database specified")
            logging.debug(resp)
            return resp
        attrs = self.flatten_dict(request.POST)
        if request.content_type:
            try:
                data = request.data
            except AttributeError:
                pass
            else:
                attrs = data
        logging.debug(attrs)
        if 'id' not in attrs or 'name' not in attrs:
            resp = rc.BAD_REQUEST
            resp.write(" Missing id or name")
            logging.debug(resp)
            return resp
#        if self.model.using(db).filter(id=attrs['id']):
#            logging.debug(rc.DUPLICATE_ENTRY)
#            return rc.DUPLICATE_ENTRY
        else:
            try:
                c = self.model(**attrs)
                c.save(using=db)
                logging.debug("Created C: " + c.__unicode__())

            except IntegrityError:
                logging.debug(rc.DUPLICATE_ENTRY)
                return rc.DUPLICATE_ENTRY
            else:
                create_CCbx_from_C(c, db)
                return rc.CREATED

    def update(self, request, db, concept_id):
        """
        Example JSON as PUT body:
            "name": "Sleep deprivation2", 
        """
        if db == 'projects': db = 'default'
        elif db != 'publications':
            resp = rc.BAD_REQUEST
            resp.write(" No database specified")
            logging.debug(resp)
            return resp
        attrs = self.flatten_dict(request.PUT)
        if request.content_type:
            try:
                data = request.data
            except AttributeError:
                pass
            else:
                attrs = data
        logging.debug(attrs)
        if 'name' not in attrs:
            resp = rc.BAD_REQUEST
            resp.write(" Missing name")
            logging.debug(resp)
            return resp
        try:
            c = self.model.objects.using(db).get(id=concept_id)
            print c
        except ObjectDoesNotExist:
            return rc.NOT_FOUND
        else:
            c.name = attrs['name']
            c.save(using=db)
            logging.debug(rc.ALL_OK)
            return rc.ALL_OK

    def delete(self, request, db, concept_id):
        if db == 'projects': db = 'default'
        elif db != 'publications':
            resp = rc.BAD_REQUEST
            resp.write(" No database specified")
            logging.debug(resp)
            return resp
        try:
            c = self.model.objects.using(db).get(id=concept_id)
        except ObjectDoesNotExist:
            return rc.NOT_FOUND
        else:
            delete_CCbx_from_C(c)

            c.delete(using=db)
            return rc.DELETED

#    @classmethod
#    def resource_uri(cls, concept=None):
#        if concept:
#            return ('concepts', [concept.id, ])
#        else: return ('concepts', ['id'])

#class AnonymousConceptHandler(ConceptHandler, AnonymousBaseHandler):
#    pass


class GraphsJsonHandler(BaseHandler):
    allowed_methods = ('GET')
#
#    def read(self, request, db, graphtype, graphsubtype):
    def read(self, request, db, graphtype, graphsubtype, actor_id):
        """
        @param graphtype: {AA, CC, AC}
        @param graphsubtype: {c,p,b,n,s,a} in the case of AA
        @return: HTTP response with JSON content and 
            mimetype=text/plain; charset=utf8
        @TODO: 
            * generate error if a argument is not provided
            * generate error or do another thing if argument is not Actor
        """

        if db == 'projects': db = 'default'
        elif db != 'publications':
            resp = rc.BAD_REQUEST
            resp.write(" No database specified")
            logging.debug(resp)
            return resp
#        a = request.GET.get("a", None)
#        print a
#        object_type, instance = is_actor_or_concept(a, db)
        # hack, change this:
#        if Actor.objects.filter(id=actor_id):
#            object_type = 'Actor'
#            instance = Actor.objects.get(id=actor_id)
#        else:
#            object_type = None
#            instance = None

        try:
            instance = Actor.objects.get(id=actor_id)
        except ObjectDoesNotExist:
            # or return error?
            content = nonejson()
            #return Http404
            #return django.views.defaults.page_not_found()
        else:
            if graphtype == 'AA':
                if graphsubtype == 'c':
                    content = get_AAc_weight_json_from_A(instance, db)
                elif graphsubtype == 'p':
                    content = get_AAp_weight_json_from_As(instance, db)
                elif graphsubtype == 'b':
                    content = get_AAb_weight_json_from_A(instance, db)
                elif graphsubtype == 'n':
                    content = get_AAn_weight_json_from_A(instance, db)
                elif graphsubtype == 's':
                    content = get_AAbb_weight_json_from_A(instance, db)
                elif graphsubtype == 'a':
                    content = get_AAbc_weight_json_from_A(instance, db)
                elif graphsubtype == 'l':
                    content = get_AAbnbc_weight_json_from_A(instance, db)
            elif graphtype == 'CC':
                if graphsubtype == 'a':
        #            content = aget_AC_weight_json_from_A(instance)
                    pass
                elif graphsubtype == 'b':
                    content = get_CCb_weight_json_from_A(instance, db)
                elif graphsubtype == 'n':
                    content = get_CCn_weight_json_from_A(instance, db)
        #        elif AAgraphtype=='s':
        #            content = aabbjsonweights(instance)
        #        elif AAgraphtype=='a':
        #            content = aabcjsonweights(instance)
            elif graphtype == 'AC':
                if graphsubtype == '1':
                    content = get_AC_weight_json_from_A(instance, db)
                elif graphsubtype == '2':
                    content = get_AC_weight_2l_json_from_A(instance, db)
                    pass
        return HttpResponse(content=content, mimetype='text/plain; charset=utf8')

#class AnonymousGraphsJsonHandler(GraphsJsonHandler, AnonymousBaseHandler):
#    pass

class GraphsJsonCHandler(BaseHandler):
    allowed_methods = ('GET')
#
#    def read(self, request, db, graphtype, graphsubtype):
    def read(self, request, db, graphtype, graphsubtype, concept_id):
        """
        @param graphtype: {AA, CC, AC}
        @param graphsubtype: {c,p,b,n,s,a} in the case of AA
        @return: HTTP response with JSON content and 
            mimetype=text/plain; charset=utf8
        @TODO: 
            * generate error if a argument is not provided
            * generate error or do another thing if argument is not Actor
        """
        if db == 'projects': db = 'default'
        elif db != 'publications':
            resp = rc.BAD_REQUEST
            resp.write(" No database specified")
            logging.debug(resp)
            return resp
        try:
            instance = Instance.objects.get(id=concept_id)
        except ObjectDoesNotExist:
            # or return error?
            content = nonejson()
            #return Http404
            #return django.views.defaults.page_not_found()
        else:
            if graphtype == 'AC':
                if graphsubtype == '1':
                    content = get_AC_weight_json_from_C(instance, db)

        return HttpResponse(content=content, mimetype='text/plain; charset=utf8')


#
#from agave.controller_js_graph_generators import *
#class GraphsJsHandler(BaseHandler):
#    allowed_methods = ('GET')
##
##    def read(self, request, db, graphtype, graphsubtype):
#    def read(self, request, db, graphtype, graphsubtype, actor_id):
#        """
#        @param graphtype: {AA, CC, AC}
#        @param graphsubtype: {c,p,b,n,s,a} in the case of AA
#        @return: HTTP response with JSON content and 
#            mimetype=text/plain; charset=utf8
#        @TODO: 
#            * generate error if a argument is not provided
#            * generate error or do another thing if argument is not Actor
#        """
#
#        if db == 'projects': db = 'default'
#        elif db != 'publications':
#            resp = rc.BAD_REQUEST
#            resp.write(" No database specified")
#            logging.debug(resp)
#            return resp
##        a = request.GET.get("a", None)
##        print a
##        object_type, instance = is_actor_or_concept(a, db)
#        # hack, change this:
##        if Actor.objects.filter(id=actor_id):
##            object_type = 'Actor'
##            instance = Actor.objects.get(id=actor_id)
##        else:
##            object_type = None
##            instance = None
#
#        try:
#            instance = Actor.objects.get(id=actor_id)
#        except ObjectDoesNotExist:
#            # or return error?
#            content = nonejson()
#            #return Http404
#            #return django.views.defaults.page_not_found()
#        else:
#            if graphtype == 'AA':
#                if graphsubtype == 'c':
#                    content = get_AAc_weight_json_from_A(instance, db)
#                elif graphsubtype == 'p':
#                    content = get_AAp_weight_json_from_As(instance, db)
#                elif graphsubtype == 'b':
#                    content = get_AAb_weight_json_from_A(instance, db)
#                elif graphsubtype == 'n':
#                    content = get_AAn_weight_json_from_A(instance, db)
#                elif graphsubtype == 's':
#                    content = get_AAbb_weight_json_from_A(instance, db)
#                elif graphsubtype == 'a':
#                    content = get_AAbc_weight_json_from_A(instance, db)
#                elif graphsubtype == 'l':
#                    content = get_AAbnbc_weight_json_from_A(instance, db)
#            elif graphtype == 'CC':
#                if graphsubtype == 'a':
#        #            content = aget_AC_weight_json_from_A(instance)
#                    pass
#                elif graphsubtype == 'b':
#                    content = get_CCb_weight_json_from_A(instance, db)
#                elif graphsubtype == 'n':
#                    content = get_CCn_weight_json_from_A(instance, db)
#        #        elif AAgraphtype=='s':
#        #            content = aabbjsonweights(instance)
#        #        elif AAgraphtype=='a':
#        #            content = aabcjsonweights(instance)
#            elif graphtype == 'AC':
#                if graphsubtype == '1':
#                    content = get_AC_weight_json_from_A(instance, db)
#                elif graphsubtype == '2':
#                    content = get_AC_weight_2l_json_from_A(instance, db)
#                    pass
#        return HttpResponse(content=content, mimetype='text/plain; charset=utf8')
#
##class AnonymousGraphsJsonHandler(GraphsJsonHandler, AnonymousBaseHandler):
##    pass
#
#class GraphsJsCHandler(BaseHandler):
#    allowed_methods = ('GET')
##
##    def read(self, request, db, graphtype, graphsubtype):
#    def read(self, request, db, graphtype, graphsubtype, concept_id):
#        """
#        @param graphtype: {AA, CC, AC}
#        @param graphsubtype: {c,p,b,n,s,a} in the case of AA
#        @return: HTTP response with JSON content and 
#            mimetype=text/plain; charset=utf8
#        @TODO: 
#            * generate error if a argument is not provided
#            * generate error or do another thing if argument is not Actor
#        """
#        if db == 'projects': db = 'default'
#        elif db != 'publications':
#            resp = rc.BAD_REQUEST
#            resp.write(" No database specified")
#            logging.debug(resp)
#            return resp
#        try:
#            instance = Instance.objects.get(id=concept_id)
#        except ObjectDoesNotExist:
#            # or return error?
#            content = nonejson()
#            #return Http404
#            #return django.views.defaults.page_not_found()
#        else:
#            if graphtype == 'AC':
#                if graphsubtype == '1':
#                    content = get_AC_weight_json_from_C(instance, db)
#
#        return HttpResponse(content=content, mimetype='text/plain; charset=utf8')


#class AnonymousGraphsJsonCHandler(GraphsJsonHandler, AnonymousBaseHandler):
#    pass

#class GraphsHandler(BaseHandler):
#    allowed_methods = ('GET')
#    def graph_graph(request, db, graphtype, graphsubtype):
#        """
#        @param graphtype: {AA, CC, AC}
#        @param graphsubtype: {c,p,b,n,s,a} in the case of AA
#        @TODO: 
#            * generate error if a argument is not provided
#            * generate error or do another thing if argument is not Actor
#        """
#        if request.method == 'GET':
#            print "method get"
#    #        current_url = request.build_absolute_uri() 
#            url = request.path.replace('graph', 'json') + "?a=" + request.GET.get('a', "")
#            print url
#            html = render_to_string('graph.html', {'jsonurl': url})
#            response = json.dumps({'success': 'True', 'html': html})
#    #        print response
#            if request.is_ajax():
#                print "request is ajax"
#                return HttpResponse(response,
#                        content_type="application/javascript")
#            else:
#                print "request is not ajax"
#                return render_to_response('graph.html', {'jsonurl': url})





#doc = generate_doc(ActorHandler)

#print doc.name # -> 'BlogpostHandler'
##print doc.model # -> <class 'Blogpost'>
#print doc.resource_uri_template # -> '/api/post/{id}'
#methods = doc.get_methods()
#for method in methods:
#   print method.name # -> 'read'
#   print method.signature # -> 'read(post_slug=<optional>)'
#   sig = ''
#   for argn, argdef in method.iter_args():
#      sig += argn
#      if argdef:
#         sig += "=%s" % argdef
#      sig += ', '
#   sig = sig.rstrip(",")
#   print sig # -> 'read(repo_slug=None)'

