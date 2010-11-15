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

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from piston.utils import rc
import base64
import logging

class RestTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('admin',
                                             'admin@world.com', 'admin')
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.is_active = True
        self.user.save()
        self.auth_string = 'Basic %s' % base64.encodestring('admin:admin')\
                        .rstrip()

    def tearDown(self):
        self.user.delete()

class BasicAuthTest(RestTests):

    def test_invalid_auth_header(self):
        bad_auth_string = 'Basic %s' % base64.encodestring('admin:admin')\
                            .rstrip()
        response = self.client.get('/rest/projects/actor/',
            HTTP_AUTHORIZATION=bad_auth_string)
        self.assertEquals(response.status_code, rc.ALL_OK)

class ActorHandlerTestCase(RestTests):
#    fixtures = ['tests.json']
#    urls = 'actor_handler'
#    multi_db = True

#    def setUp(self):
#        pass
#
#    def testActorHandlerPost(self):
#        pass
#
#    def testIndexPageView(self):
#        pass

    def test_actor_handler_get_ok(self):
        expected = """[
    {
        "id": "1",
        "name": "test"
    }
]"""
        result = self.client.get('/rest/projects/actor/',
                HTTP_AUTHORIZATION=self.auth_string).content
        self.assertEquals(result, expected)
        logging.debug("get")

    def test_actor_handler_get_id_ok(self):
        expected = """{
    "id": "1",
    "name": "test"
}"""
        result = self.client.get('/rest/projects/actor/1/',
                HTTP_AUTHORIZATION=self.auth_string).content
        self.assertEquals(result, expected)
        logging.debug("get_id")

    def test_actor_handler_post_ok(self):
        values = {
                  'id': 1,
                  'name':'test'
        }
        result = self.client.post('/rest/projects/actor/',
                        values, HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(result.status_code, rc.CREATED.status_code)
        logging.debug("post")

    def test_actor_handler_post_duplicate(self):
        values = {
                  'id': 1,
                  'name':'test'
        }
        result = self.client.post('/rest/projects/actor/',
                        values, HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(result.status_code, rc.DUPLICATE_ENTRY.status_code)
        logging.debug("post")

    def test_actor_handler_put_ok(self):
        values = {
                  'name':'test1'
        }
        result = self.client.put('/rest/projects/actor/1/',
                        values, HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(result.status_code, rc.ALL_OK.status_code)
        logging.debug("put")

    def test_actor_handler_put_not_found(self):
        values = {
                  'name':'test1'
        }
        result = self.client.put('/rest/projects/actor/2/',
                        values, HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(result.status_code, rc.NOT_FOUND.status_code)

    def test_actor_handler_delete_ok(self):
        result = self.client.delete('/rest/projects/actor/1/',
                                    HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(result.status_code, rc.DELETED.status_code)
        logging.debug("put")

    def test_actor_handler_delete_not_found(self):
        result = self.client.delete('/rest/projects/actor/1/',
                                    HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(result.status_code, rc.NOT_FOUND.status_code)


class ConceptHandlerTestCase(RestTests):

    def test_concept_handler_get_ok(self):
        expected = """[
    {
        "id": "1",
        "name": "SNA"
    }
]"""
        result = self.client.get('/rest/projects/concept/',
                HTTP_AUTHORIZATION=self.auth_string).content
        self.assertEquals(result, expected)
        logging.debug("get")

    def test_concept_handler_get_id_ok(self):
        expected = """{
    "id": "1",
    "name": "test"
}"""
        result = self.client.get('/rest/projects/concept/1/',
                HTTP_AUTHORIZATION=self.auth_string).content
        self.assertEquals(result, expected)
        logging.debug("get_id")

    def test_concept_handler_get_id_not_found(self):
        result = self.client.get('/rest/projects/concept/2/',
                HTTP_AUTHORIZATION=self.auth_string).content
        self.assertEquals(result.status_code, rc.NOT_FOUND)
        logging.debug("get_id")

    def test_concept_handler_post_ok(self):
        values = {
            'id':1,
            'name':'SNA'
        }
        result = self.client.post('/rest/projects/concept/',
                        values, HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(result.status_code, rc.CREATED.status_code)
        logging.debug("post")

    def test_concept_handler_post_duplicate(self):
        values = {
            'id':1,
            'name':'SNA'
        }
        result = self.client.post('/rest/projects/concept/',
                        values, HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(result.status_code, rc.DUPLICATE_ENTRY.status_code)
        logging.debug("post")

    def test_concept_handler_put_ok(self):
        values = {
                  'name':'SNA2'
        }
        result = self.client.put('/rest/projects/concept/1/',
                        values, HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(result.status_code, rc.CREATED.status_code)
        logging.debug("put")

    def test_concept_handler_put_not_found(self):
        values = {
                  'name':'SNA2'
        }
        result = self.client.put('/rest/projects/concept/2/',
                        values, HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(result.status_code, rc.NOT_FOUND.status_code)

    def test_concept_handler_delete_ok(self):
        result = self.client.delete('/rest/projects/concept/1/',
                                    HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(result.status_code, rc.DELETED.status_code)
        logging.debug("put")

    def test_concept_handler_delete_not_found(self):
        result = self.client.delete('/rest/projects/concept/2/',
                                    HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(result.status_code, rc.NOT_FOUND.status_code)

class InstanceHandlerTestCase(RestTests):

    def test_instance_handler_get_ok(self):
        expected = """[
    {
        "id": "1",
        "title": "Enrichment of"
    }
]"""
        result = self.client.get('/rest/projects/instance/',
                HTTP_AUTHORIZATION=self.auth_string).content
        self.assertEquals(result, expected)
        logging.debug("get")

    def test_instance_handler_get_id_ok(self):
        expected = """{
    "id": "1",
    "title": "Enrichment of"
}"""
        result = self.client.get('/rest/projects/instance/1/',
                HTTP_AUTHORIZATION=self.auth_string).content
        self.assertEquals(result, expected)
        logging.debug("get_id")

    def test_instance_handler_get_id_not_found(self):
        result = self.client.get('/rest/projects/instance/2/',
                HTTP_AUTHORIZATION=self.auth_string).content
        self.assertEquals(result.status_code, rc.NOT_FOUND)
        logging.debug("get_id")

    def test_instance_handler_post_ok(self):
        values = {
            'id':1,
            'title':'Enrichment of '
        }
        result = self.client.post('/rest/projects/instance/',
                        values, HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(result.status_code, rc.CREATED.status_code)
        logging.debug("post")

    def test_instance_handler_post_duplicate(self):
        values = {
            'id':1,
            'title':'Enrichment of '
        }
        result = self.client.post('/rest/projects/instance/',
                        values, HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(result.status_code, rc.DUPLICATE_ENTRY.status_code)
        logging.debug("post")

    def test_instance_handler_put_ok(self):
        values = {
                  'title':'Enrichment of 2'
        }
        result = self.client.put('/rest/projects/instance/1/',
                        values, HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(result.status_code, rc.CREATED.status_code)
        logging.debug("put")

    def test_instance_handler_put_not_found(self):
        values = {
                  'title':'Enrichment of 2'
        }
        result = self.client.put('/rest/projects/instance/2/',
                        values, HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(result.status_code, rc.NOT_FOUND.status_code)

    def test_instance_handler_delete_ok(self):
        result = self.client.delete('/rest/projects/instance/1/',
                                    HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(result.status_code, rc.DELETED.status_code)
        logging.debug("put")

    def test_instance_handler_delete_not_found(self):
        result = self.client.delete('/rest/projects/instance/2/',
                                    HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(result.status_code, rc.NOT_FOUND.status_code)

class InstanceActorHandlerTestCase(RestTests):

    def test_instanceactor_handler_get_ok(self):
        expected = """[
    {
        "id": "1",
        "weight": "1.0"
    }
]"""
        result = self.client.get('/rest/projects/instance/1/actor/',
                HTTP_AUTHORIZATION=self.auth_string).content
        self.assertEquals(result, expected)
        logging.debug("get")

    def test_instanceactor_handler_get_id_ok(self):
        expected = """{
    "id": "1",
    "weight": "1.0"
}"""
        result = self.client.get('/rest/projects/instance/1/actor/1/',
                HTTP_AUTHORIZATION=self.auth_string).content
        self.assertEquals(result, expected)
        logging.debug("get_id")

    def test_instanceactor_handler_get_id_not_found(self):
        result = self.client.get('/rest/projects/instance/1/actor/2/',
                HTTP_AUTHORIZATION=self.auth_string).content
        self.assertEquals(result.status_code, rc.NOT_FOUND)
        logging.debug("get_id")

    def test_instanceactor_handler_post_ok(self):
        values = {
            'id':1,
            'weight':1.0
        }
        result = self.client.post('/rest/projects/instance/1/actor/1/',
                        values, HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(result.status_code, rc.CREATED.status_code)
        logging.debug("post")

    def test_instanceactor_handler_post_duplicate(self):
        values = {
            'id':1,
            'weight':1.0
        }
        result = self.client.post('/rest/projects/instance/1/actor/1/',
                        values, HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(result.status_code, rc.DUPLICATE_ENTRY.status_code)
        logging.debug("post")

    def test_instanceactor_handler_put_ok(self):
        values = {
            'weight':2.0
        }
        result = self.client.put('/rest/projects/instance/1/actor/1/',
                        values, HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(result.status_code, rc.CREATED.status_code)
        logging.debug("put")

    def test_instanceactor_handler_put_not_found(self):
        values = {
            'weight':2.0
        }
        result = self.client.put('/rest/projects/instance/1/actor/2/',
                        values, HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(result.status_code, rc.NOT_FOUND.status_code)

    def test_instanceactor_handler_delete_ok(self):
        result = self.client.delete('/rest/projects/instance/1/actor/1/',
                                    HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(result.status_code, rc.DELETED.status_code)
        logging.debug("put")

    def test_instanceactor_handler_delete_not_found(self):
        result = self.client.delete('/rest/projects/instance/1/actor/1/',
                                    HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(result.status_code, rc.NOT_FOUND.status_code)

class InstanceConceptHandlerTestCase(RestTests):

    def test_instanceconcept_handler_get_ok(self):
        expected = """[
    {
        "id": "1",
        "weight": "1"
    }
]"""
        result = self.client.get('/rest/projects/instance/1/concept/',
                HTTP_AUTHORIZATION=self.auth_string).content
        self.assertEquals(result, expected)
        logging.debug("get")

    def test_instanceconcept_handler_get_id_ok(self):
        expected = """{
    "id": "1",
    "weight": "1"
}"""
        result = self.client.get('/rest/projects/instance/1/concept/1/',
                HTTP_AUTHORIZATION=self.auth_string).content
        self.assertEquals(result, expected)
        logging.debug("get_id")

    def test_instanceconcept_handler_get_id_not_found(self):
        result = self.client.get('/rest/projects/instance/1/concept/2/',
                HTTP_AUTHORIZATION=self.auth_string).content
        self.assertEquals(result.status_code, rc.NOT_FOUND)
        logging.debug("get_id")

    def test_instanceconcept_handler_post_ok(self):
        values = {
            'id':1,
            'weight':1
        }
        result = self.client.post('/rest/projects/instance/1/concept/1/',
                        values, HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(result.status_code, rc.CREATED.status_code)
        logging.debug("post")


    def test_instanceconcept_handler_post_duplicate(self):
        values = {
            'id':1,
            'weight':1
        }
        result = self.client.post('/rest/projects/instance/1/concept/1/',
                        values, HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(result.status_code, rc.DUPLICATE_ENTRY.status_code)
        logging.debug("post")

    def test_instanceconcept_handler_put_ok(self):
        values = {
            'weight':2
        }
        result = self.client.put('/rest/projects/instance/1/concept/1/',
                        values, HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(result.status_code, rc.CREATED.status_code)
        logging.debug("put")

    def test_instanceconcept_handler_put_not_found(self):
        values = {
            'weight':2
        }
        result = self.client.put('/rest/projects/instance/1/concept/2/',
                        values, HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(result.status_code, rc.NOT_FOUND.status_code)

    def test_instanceconcept_handler_delete_ok(self):
        result = self.client.delete('/rest/projects/instance/1/concept/1/',
                                    HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(result.status_code, rc.DELETED.status_code)
        logging.debug("put")

    def test_instanceconcept_handler_delete_not_found(self):
        result = self.client.delete('/rest/projects/instance/1/concept/1/',
                                    HTTP_AUTHORIZATION=self.auth_string)
        self.assertEquals(result.status_code, rc.NOT_FOUND.status_code)


class JsonRestTestCase(RestTests):
    fixtures = ['test_data.json']

    def setUp(self):
        pass

    def test_AAp(self):
        expected = """var jsondata = {"nodes": [{"type": 2, "nodeName": "Julia Anaya"}, {"type": 1, "nodeName": "Milan Stankovic"}, {"type": 1, "nodeName": "Alexandre Passant"}], "links": [{"source": 0, "target": 1, "value": 1}, {"source": 0, "target": 2, "value": 1}]}"""
#        response = self.client.get('/rest/projects/AA/p/actor/1/')
        response = self.client.get(reverse('graph_graph',
                                           args=['projects', 'AA', 'p', '1']),
                                    HTTP_AUTHORIZATION=self.auth_string)
        self.assertEqual(response.content, expected)

#class AAbTestCase(RestTests):
#
#    def test_aab_get_ok(self):
#        expected = """[
#    {
#        "id": "1",
#        "weight": "1.0"
#    }
#]"""
#        result = self.client.get('/rest/projects/instance/1/actor/',
#                HTTP_AUTHORIZATION=self.auth_string).content
#        self.assertEquals(result, expected)
#        logging.debug("get")
