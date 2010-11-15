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

from agave.controller_pubmedxml2models import generate_models
from django.conf import settings
from django.core.management.base import BaseCommand
from optparse import make_option
import os.path

pubmed_path = os.path.join(
                os.path.abspath(
                    os.path.join(settings.PROJECT_ROOT, '../../')),
                                'pubmed-fpgg-data/*')

class Command(BaseCommand):
#    args = '<poll_id poll_id ...>'
    help = 'Initialize publications database with Pubmed XML file'
    option_list = BaseCommand.option_list + (
        make_option('--path', '-p', dest='path', default=pubmed_path,
            help='Path to Pubmed XML file/s'),
        make_option('--numberfiles', '-n', dest='numberfiles', default=None,
            help='Number of files to parse')
    )

    def handle(self, *args, **options):
#        generate_models()
        path = options.get('path', pubmed_path)
        numberfiles = options.get('numberfiles', None)
        generate_models(path, numberfiles)

#        generate_models(os.path.join(os.path.abspath(
#                                os.path.join(settings.PROJECT_ROOT, '../../')),
#                                'pubmed-fpgg-data/*'), 5)
#        generate_models(os.path.join(os.path.abspath(
#                                os.path.join(settings.PROJECT_ROOT, '../../')),
#                                'pubmed-fpgg-data/pubmed_result(8).txt'))
#        generate_models('../../data/inputdata/pubmed_fpgg_data/pubmed_result2.txt')
        print('Successfully initialized\n')
