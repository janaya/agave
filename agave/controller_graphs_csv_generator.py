from agave.models import *
from datetime import datetime
from django.conf import settings
import codecs

#for file names with timestamp
#datetime.now().strftime("%Y%m%d%H%M")

def generate_C_names_csv(threshold=10):
    f = codecs.open(settings.CSV_OUTPUT_PATH  + "/C-names.csv", "w", encoding="utf-8")
    f.write("index;name\n")
    cids = [aconcept['concept'] for aconcept in ActorConcept.objects.filter(weight__gte=threshold).values('concept').distinct()]
    for m in Concept.objects.filter(id__in=cids, not_in_dataset=False):
        f.write(str(m.id) + ";" + m.__unicode__() + "\n")
    f.close()

def generate_K_names_csv():
    f = codecs.open(settings.CSV_OUTPUT_PATH  + "/K-names.csv", "w", encoding="utf-8")
    f.write("index;name\n")
    for m in Concept.objects.all():
        f.write(str(m.id) + ";" + m.__unicode__() + "\n")
    f.close()

def generate_K_C_names_csv():
    f = codecs.open(settings.CSV_OUTPUT_PATH  + "/K-C-names.csv", "w", encoding="utf-8")
    for m in Concept.objects.filter(not_in_dataset=True):
        f.write(str(m.id) + ";" + m.__unicode__() + "\n")
    f.close()

def generate_A_names_csv(threshold=10):
    f = codecs.open(settings.CSV_OUTPUT_PATH  + "/A-names.csv", "w", encoding="utf-8")
    f.write("index;name\n")
    aids = [aconcept['actor'] for aconcept in ActorConcept.objects.filter(weight__gte=threshold).values('actor').distinct()]
    for a in Actor.objects.filter(id__in=aids):
#        f.write(str(a.id)+","+a.__unicode__()+"\n")
        f.write(str(a.id) + ";" + a.__unicode__() + "\n")
    f.close()

def generate_CCb_csv():
    f = codecs.open(settings.CSV_OUTPUT_PATH  + "/CCb.csv", "w", encoding="utf-8")
    for ccb in  CCb.objects.filter(concept_from__not_in_dataset=False, concept_to__not_in_dataset=False):
        f.write("C" + str(ccb.concept_from.id) + ",C" + str(ccb.concept_to.id) + "\n")
    f.close()

def generate_KKb_csv():
    f = codecs.open(settings.CSV_OUTPUT_PATH  + "/KKb.csv", "w", encoding="utf-8")
    for ccb in  CCb.objects.all():
        f.write('"C' + str(ccb.concept_from.id) + '","C' + str(ccb.concept_to.id) + '"\n')
    f.close()

def generate_AC_csv(threshold=10):
    f = open(settings.CSV_OUTPUT_PATH  + "/AC.csv", "w")
    f.write("A,C\n")
    ac = "\n".join(['"A%(actor__id)s","C%(concept__id)s"' % a for a in ActorConcept.objects.filter(weight__gte=threshold).values('actor__id', 'concept__id')])
    f.write(ac)
    f.close()

def generate_AP_csv():
    f = open(settings.CSV_OUTPUT_PATH  + "/all-AP.csv", "w")
    f.write("A,P,w\n")
    ac = "\n".join(['"A%(actor__id)s", "C%(instance__id)s", %(weight)s' % a for a in InstanceActor.objects.values('actor__id', 'instance__id', 'weight').order_by('actor__id', 'instance__id')])
    f.write(ac)
    f.close()

def cca():
#    return CCa.objects.values('concept_from','concept_to').distinct().count()
    cca = list(CCa.objects.values('concept_from', 'concept_to').distinct())
#    new_cca = [ccae for ccae in cca if not {'concept_to':ccae['concept_from'], 'concept_from': ccae['concept_to']} in cca]
#    return new_cca
    [cca.remove({'concept_to':ccae['concept_from'], 'concept_from': ccae['concept_to']}) for ccae in cca  if {'concept_to':ccae['concept_from'], 'concept_from': ccae['concept_to']} in cca]
    return cca

def generate_cca_csv():
    ccai = cca()
    f = open(settings.CSV_OUTPUT_PATH  + "/all-CCa.csv", "w")
    f.write("C,C\n")
    ac = "\n".join(['"C%(concept_from)s", "C%(concept_to)s"' % a for a in ccai])
    f.write(ac)
    f.close()

def aac():
#    return AAc.objects.values('actor_from','actor_to').distinct().count()
    aac = list(AAc.objects.values('actor_from', 'actor_to').distinct())
#    new_aac = [aace for aace in aac if not {'actor_to':aace['actor_from'], 'actor_from': aace['actor_to']} in aac]
#    return new_aac
    [aac.remove({'actor_to':aace['actor_from'], 'actor_from': aace['actor_to']}) for aace in aac if {'actor_to':aace['actor_from'], 'actor_from': aace['actor_to']} in aac]
    return aac

def generate_aac_csv():
    aac = aac()
    f = open(settings.CSV_OUTPUT_PATH  + "/all-AAc.csv", "w")
    f.write("A,A\n")
    ac = "\n".join(['"C%(actor_from)s", "C%(actor_to)s"' % a for a in aac])
    f.write(ac)
    f.close()

def generate_CCball_csv():
    f = open(settings.CSV_OUTPUT_PATH  + "/CCball.csv", "w")
    f.write("C,C,w\n")
    ac = "\n".join(['"C%(concept_from__id)s", "C%(concept_to__id)s"' % a for a in CCball.objects.values('concept_from__id', 'concept_to__id')])
    f.write(ac)
    f.close()

def generate_AAball_csv():
    f = open(settings.CSV_OUTPUT_PATH  + "/AAball.csv", "w")
    f.write("A,A,w\n")
    ac = "\n".join(['"A%(actor_from__id)s", "A%(actor_to__id)s"' % a for a in AAball.objects.values('actor_from__id', 'actor_to__id')])
    f.write(ac)
    f.close()


def generate_ACb_csv():
#    f = codecs.open(settings.CSV_OUTPUT_PATH  + "/all-AAcw-"+datetime.now().strftime("%Y%m%d%H%M")+".csv","w",encoding="utf-8")
    f = open(settings.CSV_OUTPUT_PATH  + "/ACb.csv", "w")
    f.write("A,C\n")
    ac = "\n".join(['"A%(actor__id)s","C%(concept__id)s"' % a for a in ACb.objects.values('actor__id', 'concept__id')])
#    for aconcepts in ActorConcept.objects.all():
#        f.write('"A'+str(aconcepts.actor.id)+'","C'+str(aconcepts.concept.id)+'",'+str(aconcepts.weight)+'\n')
    f.write(ac)
    f.close()

#CCa - CCp

#AAc - AAp

#CCbbc - CCa

#AAbabc - AAc
