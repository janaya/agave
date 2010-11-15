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

from agave.models import Instance, Actor, Concept, ActorConcept, AAp, CCp, CCa, \
    AAc, CCb, CCbb, CCbc, AAba, AAbb, AAbc
from django.db.models import Count
from itertools import combinations


def n_p():
    return Instance.objects.count()

def n_a():
    return Actor.objects.count()

def n_c():
    return Concept.objects.exclude(not_in_dataset=True).count()

def n_c_notinds():
    return Concept.objects.count()


def avg_a_p(na=None, np=None):
    if na and np:
        return float(na) / np
    else:
        return n_a() / n_p()

def avg_c_p(nc=None, np=None):
    if nc and np:
        return float(nc) / np
    else:
        return n_c() / n_p()

def avg_c_a(nc=None, na=None):
    if na and nc:
        return float(nc) / na
    else:
        return n_c() / n_a()

def avg_a_c(na=None, nc=None):
    if na and nc:
        return float(na) / nc
    else:
        return n_a() / n_c()


def n_ac():
    ActorConcept.objects.count()


def aap():
    aap = list(AAp.objects.values('actor_from', 'actor_to').distinct())
    aap = list(AAp.objects.aggregate(
                        Count('actor_from', 'actor_to', distinct=True)))


def n_aap():
    AAp = set()
    for p in Instance.objects.all():
        for a_from, a_to in combinations([a for a in p.actors.all()], 2):
            if (a_to, a_from) not in AAp and a_to != a_from:
                AAp.add((a_from, a_to))
    return len(AAp)

def ccp():
#    return CCa.objects.values('concept_from','concept_to').distinct().count()
    ccp = list(CCp.objects.values('concept_from', 'concept_to').distinct())
#    new_cca = [ccae for ccae in cca if not {'concept_to':ccae['concept_from'], 'concept_from': ccae['concept_to']} in cca]
#    return new_cca
    [ccp.remove({'concept_to':ccpe['concept_from'],
                 'concept_from': ccpe['concept_to']})
                 for ccpe in ccp
                    if {'concept_to':ccpe['concept_from'],
                        'concept_from': ccpe['concept_to']} in ccp]
    return cca

def n_ccp(ccp=None):
    if ccp:
        return len(ccp)
    else:
        CCp = set()
        for p in Instance.objects.all():
            for c_from, c_to in combinations([c for c in p.concepts.all()], 2):
                if (c_to, c_from) not in AAp and c_to != c_from:
                    CCp.add((c_from, c_to))
        return len(CCp)


def perc_a_b(a, b):
    return float(a) / b * 100

def cca():
#    return CCa.objects.values('concept_from','concept_to').distinct().count()
    cca = list(CCa.objects.values('concept_from', 'concept_to').distinct())
#    new_cca = [ccae for ccae in cca if not {'concept_to':ccae['concept_from'], 'concept_from': ccae['concept_to']} in cca]
#    return new_cca
    [cca.remove({'concept_to':ccae['concept_from'],
                 'concept_from': ccae['concept_to']})
                 for ccae in cca
                    if {'concept_to':ccae['concept_from'],
                        'concept_from': ccae['concept_to']} in cca]
    return cca

def n_cca(cca=None):
    if cca:
        return len(cca)
    else:
    #    return CCa.objects.values('concept_from','concept_to').distinct().count()
        cca = CCa.objects.values('concept_from', 'concept_to').distinct()
        new_cca = [ccae for ccae in cca
                   if not {'concept_to':ccae['concept_from'],
                           'concept_from': ccae['concept_to']} in cca]
        return new_cca

def aac():
#    return AAc.objects.values('actor_from','actor_to').distinct().count()
    aac = list(AAc.objects.values('actor_from', 'actor_to').distinct())
#    new_aac = [aace for aace in aac if not {'actor_to':aace['actor_from'], 'actor_from': aace['actor_to']} in aac]
#    return new_aac
    [aac.remove({'actor_to':aace['actor_from'],
                 'actor_from': aace['actor_to']})
                 for aace in aac if {'actor_to':aace['actor_from'],
                                     'actor_from': aace['actor_to']} in aac]
    return aac

def n_aac(aac=None):
    if aac:
        return len(aac)
    else:
    #    return AAc.objects.values('actor_from','actor_to').distinct().count()
        aac = AAc.objects.values('actor_from', 'actor_to').distinct()
        new_aac = [aace for aace in aac
                   if not {'actor_to':aace['actor_from'],
                                                'actor_from': aace['actor_to']} in aac]
        return len(new_aac)

def max_AC(na=None, nc=None):
    if na and nc:
        return na * nc
    else:
        return n_a()*n_c()


def max_AA(na=None):
    if na:
        return na * (na - 1) / 2
    else:
        return n_a()*(n_a() - 1) / 2

def max_CC(nc=None):
    if nc:
        return nc * (nc - 1) / 2
    else:
        return n_c()*(n_c() - 1) / 2

def max_CC_notinds(nc_notinds=None):
    if nc_notinds:
        return nc_notinds * (nc_notinds - 1) / 2
    else:
        return n_c_notinds()*(n_c_notinds() - 1) / 2


def ccba():
    return CCb.objects.exclude(concept_from__not_in_dataset=True)\
                       .exclude(concept_to__not_in_dataset=True)

def n_ccba(ccba=None):
    if ccba:
        return len(ccba)
    else:
    #    return CCb.objects.exclude(concept_from__not_in_dataset=True).exclude(concept_to__not_in_dataset=True).count()
        ccba = CCb.objects.exclude(concept_from__not_in_dataset=True).exclude(concept_to__not_in_dataset=True)
        return len(ccba)

def ccbb():
#    return CCbb.objects.values('concept_from', 'concept_to').distinct()
    ccbb = list(CCbb.objects.values('concept_from', 'concept_to').distinct())
    [ccbb.remove({'concept_to':ccbbe['concept_from'],
                  'concept_from': ccbbe['concept_to']})
        for ccbbe in ccbb if {'concept_to':ccbbe['concept_from'],
                              'concept_from': ccbbe['concept_to']} in ccbb]
    return ccbb

def n_ccbb(ccbb=None):
    return len(ccbb)

def ccbc():
#    return CCbc.objects.values('concept_from', 'concept_to').distinct()
    ccbc = list(CCbc.objects.values('concept_from', 'concept_to').distinct())
    [ccbc.remove({'concept_to':ccbbe['concept_from'],
                  'concept_from': ccbbe['concept_to']})
        for ccbbe in ccbc
            if {'concept_to':ccbbe['concept_from'],
                'concept_from': ccbbe['concept_to']} in ccbc]
    return ccbc

def n_ccbc(ccbc=None):
    return len(ccbc)

def aaba():
    aaba = list(AAba.objects.values('actor_from', 'actor_to').distinct())
#    new_aaba = [aabae for aabae in aaba if not {'actor_to':aabae['actor_from'], 'actor_from': aabae['actor_to']} in aaba]
#    return new_aaba
    [aaba.remove({'actor_to':aabae['actor_from'],
                  'actor_from': aabae['actor_to']})
        for aabae in aaba if {'actor_to':aabae['actor_from'],
                              'actor_from': aabae['actor_to']} in aaba]
    return aaba

def n_aaba(aaba=None):
    if aaba:
        return len(aaba)
    else:
        return AAba.objects.values('actor_from', 'actor_to').distinct().count()

def aabb():
    aabb = list(AAbb.objects.values('actor_from', 'actor_to').distinct())
#    new_aabb = [aabbe for aabbe in aabb if not {'actor_to':aabbe['actor_from'], 'actor_from': aabbe['actor_to']} in aabb]
#    return new_aabb
    [aabb.remove({'actor_to':aabbe['actor_from'],
                  'actor_from': aabbe['actor_to']})
        for aabbe in aabb if {'actor_to':aabbe['actor_from'],
                              'actor_from': aabbe['actor_to']} in aabb]
    return aabb

def n_aabb(aabb=None):
    if aabb:
        return len(aabb)
    else:
        return AAbb.objects.values('actor_from', 'actor_to').distinct().count()

def aabc():
#    aabc = AAbc.objects.values('actor_from', 'actor_to').distinct()
#    new_aabc = [aabce for aabce in aabc if not {'actor_to':aabce['actor_from'], 'actor_from': aabce['actor_to']} in aabc]
    aabc = list(AAbc.objects.values('actor_from', 'actor_to').distinct())
    [aabc.remove({'actor_to':aabce['actor_from'],
                  'actor_from': aabce['actor_to']})
        for aabce in aabc if {'actor_to':aabce['actor_from'],
                              'actor_from': aabce['actor_to']} in aabc]
    return aabc

def n_aabc(aabc=None):
    if aabc:
        return len(aabc)
    else:
        return AAbc.objects.values('actor_from', 'actor_to').distinct().count()

def new_ccba_cca(ccba=None, cca=None):
    if ccba and cca:
        ccba = ccba.values('concept_from', 'concept_to')
        new_ccba = [ccbae
            for ccbae in ccba
                if {'concept_from':ccbae['concept_to'],
                    'concept_to':ccbae['concept_from']} not in cca and
                                                            ccbae not in cca]
        return new_ccba
    else:
    #    a = [(,),(,)]
    #    b = [(,),(,)]
    #    [(x,y) fro x,y in a if not (((x,y) in b) or ((y,x) in b))]

        cca = CCa.objects.values('concept_from', 'concept_to').distinct()
    #    new_cca = [ccae for ccae in cca if not {'concept_to':ccae['concept_from'], 'concept_from': ccae['concept_to']} in cca]
        ccba = CCb.objects.exclude(concept_from__not_in_dataset=True)\
            .exclude(concept_to__not_in_dataset=True)\
            .values('concept_from', 'concept_to')
        new_ccba = [ccbae
            for ccbae in ccba
                if {'concept_from':ccbae['concept_to'],
                    'concept_to':ccbae['concept_from']} not in cca and
                    {'concept_from':ccbae['concept_from'],
                     'concept_to':ccbae['concept_to']} not in cca]
        return len(new_ccba)

def n_new_ccba_cca(new_ccba):
    return len(new_ccba)

def new_ccbb_cca(ccbb=None, cca=None):
    if ccbb and cca:
        new_ccbb = [ccbae
            for ccbae in ccbb
                if {'concept_from':ccbae['concept_to'],
                    'concept_to':ccbae['concept_from']} not in cca and
                                                            ccbae not in cca]
        return new_ccbb
    else:
        cca = CCa.objects.values('concept_from', 'concept_to').distinct()
    #    new_cca = [ccae for ccae in cca if not {'concept_to':ccae['concept_from'], 'concept_from': ccae['concept_to']} in cca]
        ccbb = CCbb.objects.values('concept_from', 'concept_to').distinct()
        new_ccba = [ccbae
            for ccbae in ccbb
                if {'concept_from':ccbae['concept_to'],
                    'concept_to':ccbae['concept_from']} not in cca and
                    {'concept_from':ccbae['concept_from'],
                     'concept_to':ccbae['concept_to']} not in cca]
        return len(new_ccba)

def n_new_ccbb_cca(new_ccbb):
    return len(new_ccbb)

def new_ccbc_cca(ccbc=None, cca=None):
    if ccbc and cca:
        new_ccbc = [ccbae
            for ccbae in ccbc
                if {'concept_from':ccbae['concept_to'],
                    'concept_to':ccbae['concept_from']} not in cca and
                                                            ccbae not in cca]
        return new_ccbc
    else:
        cca = CCa.objects.values('concept_from', 'concept_to').distinct()
    #    new_cca = [ccae for ccae in cca if not {'concept_to':ccae['concept_from'], 'concept_from': ccae['concept_to']} in cca]
        ccbc = CCbc.objects.values('concept_from', 'concept_to').distinct()
        CCb.objects.exclude(concept_from__not_in_dataset=True)\
            .exclude(concept_to__not_in_dataset=True)\
            .values('concept_from', 'concept_to')
        new_ccba = [ccbae
            for ccbae in ccba
                if {'concept_from':ccbae['concept_to'],
                    'concept_to':ccbae['concept_from']} not in cca and
                    {'concept_from':ccbae['concept_from'],
                     'concept_to':ccbae['concept_to']} not in cca]
        return len(new_ccba)

def n_new_ccbc_cca(new_ccbc):
    return len(new_ccbc)

def new_aaba_aac(aaba, aac):
    new_aaba = [ccbae for ccbae in aaba if {'actor_from':ccbae['actor_to'], 'actor_to':ccbae['actor_from']} not in aac and ccbae not in aac]
    return new_aaba

def n_new_aaba_aac(new_aaba):
    return len(new_aaba)

def new_aabb_aac(aabb, aac):
    new_aabb = [ccbae for ccbae in aabb if {'actor_from':ccbae['actor_to'], 'actor_to':ccbae['actor_from']} not in aac and ccbae not in aac]
    return new_aabb

def n_new_aabb_aac(new_aabb):
    return len(new_aabb)

def new_aabc_aac(aabc, aac):
    new_aabc = [ccbae for ccbae in aabc if {'actor_from':ccbae['actor_to'], 'actor_to':ccbae['actor_from']} not in aac and ccbae not in aac]
    return new_aabc

def n_new_aabc_aac(new_aabc):
    return len(new_aabc)


def n_ccba_wotrans():
    return CCb.objects.exclude(concept_from__not_in_dataset=True).exclude(concept_to__not_in_dataset=True).count()

def n_ccbb_wotrans():
    return CCbb.objects.values('concept_from', 'concept_to').distinct().count()

def n_ccbc_wotrans():
    return CCbc.objects.values('concept_from', 'concept_to').distinct().count()

def n_aaba_wotrans():
    return AAba.objects.values('actor_from', 'actor_to').distinct().count()

def n_aabb_wotrans():
    return AAba.objects.values('actor_from', 'actor_to').distinct().count()

def n_aabc_wotrans():
    return AAba.objects.values('actor_from', 'actor_to').distinct().count()


def print_statistics():
    np = n_p()
    print "Instances\t%s" % np
    na = n_a()
    print "Actors\t%s" % na
    nc = n_c()
    print "MeSHs\t%s" % nc
    nc_notinds = n_c_notinds()
    print "MeSHs not in dataset\t%s" % nc_notinds
    print "Actors/Instance\t%s" % avg_a_p(na, np)
    print "MeSHs/Publicaton\t%s" % avg_c_p(nc, np)
    print "MeSHs/Actor\t%s" % avg_c_a(nc, na)
    print "Actor/MeSHs\t%s" % avg_a_c(na, nc)

    lcca = cca()
    print "CCa\t%s" % n_cca(lcca)
    laac = aac()
    print "AAc\t%s" % n_aac(laac)

    print "max AC\t%s" % max_AC(na, nc)
    print "max CC\t%s" % max_CC(nc)
    print "max AA\t%s" % max_AA(na)
    print "max CC not in dataset\t%s" % max_CC_notinds(nc_notinds)

    lccba = ccba()
    print "CCba\t%s" % n_ccba(lccba)
    new_ccba = new_ccba_cca(lccba, lcca)
    print "CCba not in CCa\t%s" % n_new_ccba_cca(new_ccba)
    lccbb = ccbb()
    print "CCbb\t%s" % n_ccbb(lccbb)
    new_ccbb = new_ccbb_cca(lccbb, lcca)
    print "CCbb not in CCa\t%s" % n_new_ccbb_cca(new_ccbb)
    lccbc = ccbc()
    print "CCbc\t%s" % n_ccbc(lccbc)
    new_ccbc = new_ccbc_cca(lccbc, lcca)
    print "CCbc not in CCa\t%s" % n_new_ccbc_cca(new_ccbc)
    laaba = aaba()
    print "AAba\t%s" % n_aaba(laaba)
    new_aaba = new_aaba_aac(laaba, laac)
    print "AAba not in AAc\t%s" % n_new_aaba_aac(new_aaba)
    laabb = aabb()
    print "AAbb\t%s" % n_aabb(laabb)
    new_aabb = new_aabb_aac(laabb, laac)
    print "AAbb not in AAc\t%s" % n_new_aabb_aac(new_aabb)
    laabc = aabc()
    print "AAbc\t%s" % n_aabc(laabc)
    new_aabc = new_aabc_aac(laabc, laac)
    print "AAbc not in AAc\t%s" % n_new_aabc_aac(new_aabc)



#def print_statistics_latex():

#    'np' : n_p(),
#    'na' : n_a(),
#    'nc' : n_c(),
#    'nc_notinds' : n_c_notinds(),
#    
#    'avgap': avg_a_p(na,np),
#    'avgcp': avg_c_p(nc,np),
#    'avgca': avg_c_a(nc,na),
#    'avgac': avg_a_c(na,nc),
#    
#    'lcca': cca(),
#    'ncca': n_cca(lcca),
#    'laac' : aac(),
#    'naac': n_aac(laac),
#    
#    'maxAC': max_AC(na,nc),
#    'maxCC': max_CC(nc),
#    'maxAA': max_AA(na),
#    'maxCC_notinds': max_CC_notinds(nc_notinds),
#    
#    lccba = ccba()
#    n_ccba(lccba)
#    new_ccba = new_ccba_cca(lccba, lcca)
#    n_new_ccba_cca(new_ccba)
#    lccbb = ccbb()
#    n_ccbb(lccbb)
#    new_ccbb = new_ccbb_cca(lccbb, lcca)
#    n_new_ccbb_cca(new_ccbb)
#    lccbc = ccbc()
#    n_ccbc(lccbc)
#    new_ccbc = new_ccbc_cca(lccbc, lcca)
#    n_new_ccbc_cca(new_ccbc)
#    laaba = aaba()
#    n_aaba(laaba)
#    new_aaba = new_aaba_aac(laaba, laac)
#    n_new_aaba_aac(new_aaba)
#    laabb = aabb()
#    n_aabb(laabb)
#    new_aabb = new_aabb_aac(laabb, laac)
#    n_new_aabb_aac(new_aabb)
#    laabc = aabc()
#    n_aabc(laabc)
#    new_aabc = new_aabc_aac(laabc, laac)
#    n_new_aabc_aac(new_aabc)

#    """
#\begin{table}[htbp]
#\centering
#\subtable[Caption for table 1]{
#    \begin{tabular}{|c|x{1.5cm}|}
#	\hline 
#	Instances & %(np)s \tabularnewline
#	\hline 
#	Actors & %(na)s \tabularnewline
#	\hline 
#	MeSHs & %(nc)s \tabularnewline
#	\hline 
#	MeSHs not in dataset & %(c_notinds)s \tabularnewline
#	\hline
#	\end{tabular}
#    \label{tab:firsttable}
#}
#\subtable[Caption for table 2]{
#	\begin{tabular}{|c|x{1.5cm}|}
#	\hline 
#	Actors/Instance & %(a_p)\tabularnewline
#	\hline 
#	MeSHs/Instance & %(c_p)\tabularnewline
#	\hline 
#	MeSHs/Actor & %(c_a)\tabularnewline
#	\hline 
#	Actor/MeSHS & %(a_c)\tabularnewline
#	\hline
#	\end{tabular}
#    \label{tab:secondtable}
#}
#\caption{Caption for total table}
#\label{tbl:totaltable}
#\end{table}

#\begin{table}[htbp]
#\centering
#\begin{tabular}{|y{2.5cm}|x{2cm}|x{2cm}|}
#\hline 
# & Num. edges & Num. edges complete graph \tabularnewline
#\hline
#\hline 
#AC & 259164  & 87248548 \tabularnewline
#\hline 
#AAc &  & 92310078 \tabularnewline
#\hline 
#CCa &  & 20611410 \tabularnewline
#\hline 
#CCba & 7353 & 20611410 \tabularnewline
#\hline 
#CCba + C not in dataset & 12179 & 32477770 \tabularnewline
#\hline 
#CCbb & 9768 &  \tabularnewline
#\hline 
#CCbc & 9764 &  \tabularnewline
#\hline 
#AAba &  & \tabularnewline
#\hline 
#AAbb &  & \tabularnewline
#\hline 
#AAbc & 1809693 & \tabularnewline
#\hline 
#\end{tabular}
#\caption{Caption for total table}
#\end{table}
#""" % {'p': n_p(), ''}

"""
$\midP\mid$

:%s/Actors\/Instance &/\$\\midA\\mid\/\\midI\\mid\$/g
:%s/MeSHs\/Instance &/\$\\midC\\mid\/\\midI\\mid\$/g
:%s/MeSHs\/Actor &/\$\\midC\\mid\/\\midC\\mid\$/g
:%s/Actor\/MeSHS &/\$\\midA\\mid\/\\midC\\mid\$/g

:%s/E_{ac}/E_{AC}/g
:%s/E_{aa_{c}}/E_{AA_{c}}/g
%s/E_{cc_{a}}/E_{CC_{a}}/g

$\midE_{X}\mid$

$\midE_{AC}\mid$
$\midE_{AA_{c}}\mid$
$\midE_{CC_{a}}\mid$

$\midE_{CC_{ba}}\mid$
$\midE_{CC_{bb}}\mid$
$\midE_{CC_{bc}}\mid$
$\midE_{AA_{ba}}\mid$
$\midE_{AA_{bb}}\mid$
$\midE_{AA_{bc}}\mid$
"""
