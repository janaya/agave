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
from django import db
from django.conf import settings
from django.db import IntegrityError, IntegrityError
from django.utils import simplejson
from exceptions import TypeError
from pprint import pprint
from agave.controller_graph_models_generator import *
from zemanta_tags.zemanta_tags_extractor import *
from agave.models import *
import MySQLdb
import glob
import random
import urllib

#from fpggsna.models import *
#_mysql_exceptions.IntegrityError
#from pysqlite2.dbapi2 import IntegrityError
SN_DBSERVER = settings.SN_DBSERVER
SN_DBUSER = settings.SN_DBUSER
SN_DBPW = settings.SN_DBUSER
SN_DBNAME = settings.SN_DBNAME

def fpggdb2models():
    db = 'default'

    db = MySQLdb.connect(SN_DBSERVER, SN_DBUSER, SN_DBPW, SN_DBNAME, use_unicode=True, charset='utf8')
    c = db.cursor()

    #extract project
    c.execute("""SELECT id,name,abstract FROM fpgg_project""")
    projects = c.fetchall()
    t = a = ""

    for project in projects:
        i, t, a = project
        print t
        print a
        p, created = Instance.objects.get_or_create(id=i, title=t.encode("utf-8"), abstract=a.encode("utf-8"))


        # extract concepts
        if p.abstract:
            concepts = extract_concepts(p.abstract)
            create_CI_from_I(p, concepts, db)
            generate_CCp(p, db)


        #extract actors
        c.execute("""select  id,fpgg_user_id, fpgg_project_id from fpgg_project_user where fpgg_project_id=%s""", i)
        projectactors = c.fetchall()
        if projectactors:
            weight = 1.0 / len(projectactors)
            f = l = ""
            for projectactor in projectactors:
                c.execute("""select id,first_name,last_name from fpgg_user where id=%s""", projectactor[1])
                actor = c.fetchone()
                i, f, l = actor
                a, created = Actor.objects.using(db).get_or_create(id=i, name=f.encode("utf-8") + ' ' + l.encode("utf-8"))
    #            print "actor %s created" % actor[1]

                pa, created = InstanceActor.objects.using(db).get_or_create(id=projectactor[0], actor=a, instance=p, weight=weight)

                create_AAp_from_I_A(a, p, db)
                create_AC_from_A_I(a, p, db)
                create_CCa_from_A_I(a, p, db)
                create_AAc_from_A_I(a, p, db)


    db.close()
