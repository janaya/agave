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

from django import forms
#from agave.models import PubmedXMLDataset

class SearchForm(forms.Form):
#    keywords = forms.CharField(max_length=100)
    word = forms.CharField(max_length=100)
#    dataset = forms.ChoiceField(choices = [(ds.id, ds.name) for ds in PubmedXMLDataset.objects.all()],initial=[PubmedXMLDataset.objects.get(name="all").id],widget = forms.RadioSelect)

from agave.models import Actor, Instance, Concept

class ActorForm(forms.ModelForm):
   class Meta:
      model = Actor

class InstanceForm(forms.ModelForm):
   class Meta:
      model = Instance

class ConoceptForm(forms.ModelForm):
   class Meta:
      model = Concept

