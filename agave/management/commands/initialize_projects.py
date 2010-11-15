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

from django.core.management.base import BaseCommand, CommandError
from agave.controller_pubmedxml2models import *
from agave.controller_CCbx_models_generator import  *
from agave.controller_graph_models_generator import *

class Command(BaseCommand):
#    args = '<path path ...>'

    def handle(self, *args, **options):
#        generate_models(options['path'])

        fpggdb2models()
        create_CCbx()
        generate_AAba()
        generate_AAbb()
        generate_AAbc()
        print('Successfully initialized"\n')

