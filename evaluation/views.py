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

from django.shortcuts import render_to_response, get_object_or_404, Http404
from django.http import HttpResponse
#import simplejson as json
from django.utils import simplejson as json
from evaluation.forms import EvaluationForm
from agave.models import Actor

#def evaluation(request):
#    if request.method == 'POST':
#        print "request is POST"

#        form = EvaluationForm(request.POST)
#        if form.is_valid():
#            print form
#            a = form.cleaned_data['actor_name']
#            print a
#            actor=Actor.objects.get(name=a)
##            new_evaluation = form.save()
#            new_evaluation = form.save(commit=False)
#            new_evaluation.actor=actor
#            new_evaluation.save()
#            return render_to_response('evaluation.html', {
#                'form': form,
#            })
#    else:
#        print "request is GET"
#        a = request.GET.get("a", None)
#        print a
#        form = EvaluationForm(initial={'actor_name':a})
#    return render_to_response('evaluation.html', {
#        'form': form,
##        'a':a,
#    })




#def evalAA(request,AAgraphtype): #,actor):
#    if request.method == 'POST':
#        print "request is POST"

#        form = EvaluationForm(request.POST)
#        if form.is_valid():
#            print form
#            a = form.cleaned_data['actor_name']
#            gt = form.cleaned_data['graph_type_name']
#            print a
#            actor=Actor.objects.get(name=a)
##            new_evaluation = form.save()
#            new_evaluation = form.save(commit=False)
#            new_evaluation.actor=actor
#            new_evaluation.graph_type= gt
#            new_evaluation.save()
#            form = EvaluationForm(new_evaluation)
#            return render_to_response('evaluation.html', {
#                'form': form,
#            })
#    else:
#        print "request is GET"
#        a = request.GET.get("a", None)
#        print a
#        form = EvaluationForm(initial={'actor_name':a, 'graph_type_name':"AA"+AAgraphtype})
#    return render_to_response('evaluation .html', {
#        'form': form,
##        'a':a,
#    })

def evalAA(request, AAgraphtype): #,actor):
    if request.method == 'POST':
        print "request is POST"

        form = EvaluationForm(request.POST)
#        js = request.POST.get('js', None) 

        if form.is_valid():

            print form
            a = form.cleaned_data['actor_name']
            gt = form.cleaned_data['graph_type_name']
            print a
            actor = Actor.objects.get(name=a)
#            new_evaluation = form.save()
            new_evaluation = form.save(commit=False)
            new_evaluation.actor = actor
            new_evaluation.graph_type = gt
            new_evaluation.save()
#            form = EvaluationForm(new_evaluation)
#            html = render_to_string('evalAjax.html', {
#                'form': form,
#            })
            html = "Thanks"
            if not request.is_ajax():
                print "request is not ajax"
#                jsaction = 'window.location.pathname="/"'
#                data = simplejson.dumps({'OK':jsaction})
                return render_to_response('evalAjax.html')
            else:
#                return HttpResponseRedirect('/')
                print "request is ajax"
#                response = json.dumps({'success': 'True', 'html': html})
                response = json.dumps(html)
                return HttpResponse(response,
                    content_type="application/javascript")

        else: # from is not valid
            html = form.errors.as_ul()
            if not request.is_ajax():
                print "request is not ajax"
#                data = simplejson.dumps(form.errors)
#                return render_to_response('eval.html', {'form': form})
                pass
            else:
                print "request is ajax"
#                response = json.dumps({'success':'False', 'html':html})
                response = json.dumps(html)
                return HttpResponse(response,
                    content_type="application/javascript")

    else:
        print "request is GET"
        a = request.GET.get("a", None)
        print a
        form = EvaluationForm(initial={'actor_name':a, 'graph_type_name':"AA" + AAgraphtype})
        return render_to_response('evalAjax.html', {
            'form': form,
    #        'a':a,
        })


def graphevalAA(request, AAgraphtype): #,actor):
    if request.method == 'GET':
        print "method get"
        return render_to_response('grapheval.html', {
        'graph': "/json/AA/" + AAgraphtype + "/?a=" + request.GET.get('a', ""),
        'eval': "/eval/AA/" + AAgraphtype + "/?a=" + request.GET.get('a', "")
        })

