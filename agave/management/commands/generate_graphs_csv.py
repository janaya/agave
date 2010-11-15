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

from agave.controller_graphs_csv_generator import generate_C_names_csv, \
    generate_K_C_names_csv, generate_A_names_csv, generate_AC_csv, generate_CCb_csv, \
    generate_ACb_csv
from django.core.management.base import BaseCommand
#from agave.controller_graphs_csv_generator import *

class Command(BaseCommand):

    def handle(self, *args, **options):
        generate_C_names_csv(1)
        generate_K_C_names_csv()
        generate_A_names_csv(1)
        generate_AC_csv(1)
        generate_CCb_csv()
        generate_ACb_csv()
        print('Successfully initialized\n')
