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
#   * exclude results from previous results
#   * exclude transitives
#   * include ranking
#   * results with actors
#   * http://www.jstree.com/documentation/json_data#, http://www.jstree.com/documentation/themes

from django.shortcuts import render_to_response, get_object_or_404, Http404
from django.template.loader import render_to_string
from django.template import RequestContext
from django.http import HttpResponse
#import simplejson as json
from django.utils import simplejson as json
from django.contrib.auth.decorators import login_required
from agave.forms import SearchForm
from agave.all import *
from agave.controller_json_graph_generators import *

def search(request):
    if request.method == 'POST':
        print "method post"
        form = SearchForm(request.POST)
        if form.is_valid():
            print "form is valid"
            word = form.cleaned_data['word']

#            if Instance.objects.get()

            html = render_to_string('search.html', {
                'form': form,
                'word': word })
            response = json.dumps({'success': 'True', 'html': html})
        else:
            print "form is not valid"
            html = form.errors.as_ul()
            response = json.dumps({'success':'False', 'html':html})

#        print response
        if request.is_ajax():
            print "request is ajax"
            return HttpResponse(response,
                    content_type="application/javascript")
        else:
            print "request is not ajax"
            return render_to_response('search.html', {
                'form': form,
#                "concept": concept,
                'word': word,
            })
    else:
        print "method not post  "
        form = SearchForm()
        return render_to_response('search.html', {
            'form': form,
    })


def is_actor_or_concept(name, db='default'):
    if not name:
        return (None, None)
    elif Concept.objects.using(db).filter(name=name):
        return ('Concept', Concept.objects.using(db).get(name=name))

    elif Actor.objects.using(db).filter(name=name):
        return ('Actor', Actor.objects.using(db).get(name=name))
    else:
        return(None, None)

def ac_concept(request):
    q = request.GET.get("q", None)
    print q
#    concept = Concept.objects.get(id=q)
#   _ret = get_Aweight_list_from_C(concept)
#    _ret = get_Aweight_list_from_C(q)
    object_type, instance = is_actor_or_concept(q)
    if object_type == 'Concept':
        _ret = get_Aweight_list_from_C(instance)
        ret = dict([("actors", _ret)])
    return HttpResponse(json.dumps(ret), mimetype="text/plain")

def aab_concept(request):
    q = request.GET.get("q", None)
#    concept = Concept.objects.get(id=q)
#    ret = actors_weight_from_broaders_from_concept(concept)
#    #ret = dict([("broader", x) for x in _ret.items()])
    object_type, instance = is_actor_or_concept(q)
    print  instance
    if object_type == 'Concept':
        ret = actors_weight_from_broaders_from_concept(instance)
    return HttpResponse(json.dumps(ret), mimetype="text/plain")

def aan_concept(request):
    q = request.GET.get("q", None)
#    concept = Concept.objects.get(id=q)
#    _ret = actors_weight_from_narrowers_from_concept(concept)
    object_type, instance = is_actor_or_concept(q)
    if object_type == 'Concept':
        _ret = actors_weight_from_narrowers_from_concept(instance)
    ret = [dict(zip(("narrower", "actors"), x)) for x in _ret.items()]
    return HttpResponse(json.dumps(ret), mimetype="text/plain")


def aabnbc_actor(request):
    q = request.GET.get("q", None)
    print q
    object_type, instance = is_actor_or_concept(q)
    if object_type == 'Actor':
        content = aabnbcjsonweights(instance)
    return HttpResponse(content=content, mimetype='text/plain; charset=utf8')

##@login_required
#def graph_js(request, db, graphtype, graphsubtype):
#    """
#    @param graphtype: {AA, CC, AC}
#    @param graphsubtype: {c,p,b,n,s,a} in the case of AA
#    @return: HTTP response with JSON content and 
#        mimetype=text/plain; charset=utf8
#    @TODO: 
#        * generate error if a argument is not provided
#        * generate error or do another thing if argument is not Actor
#    """
##    print request.user
##    if not request.user.is_authenticated():
##        resp = HttpResponse("Authorization Required")
##        resp['WWW-Authenticate'] = 'Basic realm="TestApplication"'
##        resp.status_code = 401
##        return resp
#
#    print "in graph_json"
#    if db == 'projects': db = 'default'
#    print db
#    a = request.GET.get("a", None)
#    print a
#    object_type, instance = is_actor_or_concept(a, db)
#    if object_type == 'Actor':
#        if graphtype == 'AA':
#            if graphsubtype == 'c':
#                content = get_AAc_weight_json_from_A(instance, db)
#            elif graphsubtype == 'p':
#                content = get_AAp_json_from_A(instance, db)
#            elif graphsubtype == 'b':
#                content = get_AAb_weight_json_from_A(instance, db)
#            elif graphsubtype == 'n':
#                content = aanjsonweights(instance, db)
#            elif graphsubtype == 's':
#                content = aabbjsonweights(instance, db)
#            elif graphsubtype == 'a':
#                content = aabcjsonweights(instance, db)
#            elif graphsubtype == 'l':
#                content = get_AAbnbc_weight_json_from_A(instance, db)
#        elif graphtype == 'CC':
#            if graphsubtype == 'a':
#    #            content = aget_AC_weight_json_from_A(instance)
#                pass
#            elif graphsubtype == 'b':
#                content = get_CCb_weight_json_from_A(instance, db)
#    #        elif AAgraphtype=='n':
#    #            content = aanjsonweights(instance)
#    #        elif AAgraphtype=='s':
#    #            content = aabbjsonweights(instance)
#    #        elif AAgraphtype=='a':
#    #            content = aabcjsonweights(instance)
#        elif graphtype == 'AC':
#            if graphsubtype == '1':
#                content = get_AC_weight_json_from_A(instance, db)
#            elif graphsubtype == '2':
#                content = get_AC_weight_2l_json_from_A(instance, db)
#                pass
#    else:
#        # or return error?
#        content = nonejson()
#        #return django.views.defaults.page_not_found()
#    return HttpResponse(content=content, mimetype='text/plain; charset=utf8')
#
#
#from agave.controller_js_graph_generators import *
#def graph_json(request, db, graphtype, graphsubtype):
#    """
#    @param graphtype: {AA, CC, AC}
#    @param graphsubtype: {c,p,b,n,s,a} in the case of AA
#    @return: HTTP response with JSON content and 
#        mimetype=text/plain; charset=utf8
#    @TODO: 
#        * generate error if a argument is not provided
#        * generate error or do another thing if argument is not Actor
#    """
##    print request.user
##    if not request.user.is_authenticated():
##        resp = HttpResponse("Authorization Required")
##        resp['WWW-Authenticate'] = 'Basic realm="TestApplication"'
##        resp.status_code = 401
##        return resp
#
#    print "in graph_json"
#    if db == 'projects': db = 'default'
#    print db
#    a = request.GET.get("a", None)
#    print a
#    object_type, instance = is_actor_or_concept(a, db)
#    if object_type == 'Actor':
#        if graphtype == 'AA':
#            if graphsubtype == 'c':
#                content = get_AAc_weight_json_from_A(instance, db)
#            elif graphsubtype == 'p':
#                content = get_AAp_json_from_A(instance, db)
#            elif graphsubtype == 'b':
#                content = get_AAb_weight_json_from_A(instance, db)
#            elif graphsubtype == 'n':
#                content = aanjsonweights(instance, db)
#            elif graphsubtype == 's':
#                content = aabbjsonweights(instance, db)
#            elif graphsubtype == 'a':
#                content = aabcjsonweights(instance, db)
#            elif graphsubtype == 'e':
#                content = get_AAbnbc_weight_json_from_A(instance, db)
#        elif graphtype == 'CC':
#            if graphsubtype == 'a':
#    #            content = aget_AC_weight_json_from_A(instance)
#                pass
#            elif graphsubtype == 'b':
#                content = get_CCb_weight_json_from_A(instance, db)
#    #        elif AAgraphtype=='n':
#    #            content = aanjsonweights(instance)
#    #        elif AAgraphtype=='s':
#    #            content = aabbjsonweights(instance)
#    #        elif AAgraphtype=='a':
#    #            content = aabcjsonweights(instance)
#        elif graphtype == 'AC':
#            if graphsubtype == '1':
#                content = get_AC_weight_json_from_A(instance, db)
#            elif graphsubtype == '2':
#                content = get_AC_weight_2l_json_from_A(instance, db)
#                pass
#    else:
#        # or return error?
#        content = nonejson()
#        #return django.views.defaults.page_not_found()
#    return HttpResponse(content=content, mimetype='text/plain; charset=utf8')


##@login_required
#def graph_graph(request, db, graphtype, graphsubtype):
def graph_graph(request, db, graphtype, graphsubtype, actor_id):
    """
    @param graphtype: {AA, CC, AC}
    @param graphsubtype: {c,p,b,n,s,a} in the case of AA
    @TODO: 
        * generate error if a argument is not provided
        * generate error or do another thing if argument is not Actor
    """
    if request.method == 'GET':
        print "method get"
#        current_url = request.build_absolute_uri()
#        url = "/rest" + request.path.replace('graph', 'json') + "?a=" + request.GET.get('a', "")
        url = request.path.replace('graph', 'rest')
        print url
        html = render_to_string('graph.html', {'jsonurl': url})
        response = json.dumps({'success': 'True', 'html': html})
#        print response
        if request.is_ajax():
            print "request is ajax"
            return HttpResponse(response,
                    content_type="application/javascript")
        else:
            print "request is not ajax"
            return render_to_response('graph.html', {'jsonurl': url})

def graph_visualization(request, db, graphtype, graphsubtype, actor_id):
    """
    @param graphtype: {AA, CC, AC}
    @param graphsubtype: {c,p,b,n,s,a} in the case of AA
    @TODO: 
        * generate error if a argument is not provided
        * generate error or do another thing if argument is not Actor
    """
    if request.method == 'GET':
        print "method get"
#        current_url = request.build_absolute_uri()
#        url = "/rest" + request.path.replace('graph', 'json') + "?a=" + request.GET.get('a', "")
        url = request.path.replace('graph', 'rest')
        print url
        html = render_to_string('graph_visualization.html', {'jsonurl': url})
        response = json.dumps({'success': 'True', 'html': html})
#        print response
        if request.is_ajax():
            print "request is ajax"
            return HttpResponse(response,
                    content_type="application/javascript")
        else:
            print "request is not ajax"
            return render_to_response('graph_visualization.html', {'jsonurl': url})

def autocomplete_concepts(request):
  if request.GET.has_key('q'):
    concepts = \
      Concept.objects.filter(name__istartswith=request.GET['q'])[:10]
    return HttpResponse('\n'.join(concept.name for concept in concepts))
  return HttpResponse()

def autocomplete_names(request):
  if request.GET.has_key('q'):
    instances = \
      list(Concept.objects.filter(name__istartswith=request.GET['q'])) + \
      list(Actor.objects.filter(name__istartswith=request.GET['q']))[:10]
    return HttpResponse('\n'.join(instance.name for instance in instances))
  return HttpResponse()


#from agave.generate_nxgraph import *
from django.conf import settings
def actors_broaders_concept_image(request):
    q = request.GET.get("q", None)

#    if not os.path.exists(settings.STATIC_ROOT+'/'+q+'1level_broaders_shell+.png'):
#        print "path does not exists"
#        object_type, instance = is_actor_or_concept(q)
#        if object_type == 'Concept':
#            actors_from_concept(instance)

    ret = {'image_url':settings.STATIC_URL + q + '1level_broaders_shell+.png'}
    print ret
    return HttpResponse(json.dumps(ret), mimetype="text/plain")
#    response = HttpResponse(mimetype="image/png")

