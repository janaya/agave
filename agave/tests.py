from django.test import TestCase
from tests_models import *

class MainTestCase(RestTests):
    def test_rest_all(self):
        tc = ActorHandlerTestCase
        tc.test_actor_handler_post_ok
        tc.test_actor_handler_post_duplicate
        tc.test_actor_handler_get_id_ok
        tc.test_actor_handler_get_ok
        tc.test_actor_handler_put_ok
        tc.test_actor_handler_put_not_found
        tc.test_actor_handler_delete_ok
        tc.test_actor_handler_delete_not_found

        tc = InstanceHandlerTestCase
        tc.test_instance_handler_post_ok
        tc.test_instance_handler_post_duplicate
        tc.test_instance_handler_get_id_ok
        tc.test_instance_handler_get_ok
        tc.test_instance_handler_put_ok
        tc.test_instance_handler_put_not_found
        tc.test_instance_handler_delete_ok
        tc.test_instance_handler_delete_not_found

        tc = ConceptHandlerTestCase
        tc.test_concept_handler_post_ok
        tc.test_concept_handler_post_duplicate
        tc.test_concept_handler_get_id_ok
        tc.test_concept_handler_get_ok
        tc.test_concept_handler_put_ok
        tc.test_concept_handler_put_not_found
        tc.test_concept_handler_delete_ok
        tc.test_concept_handler_delete_not_found

        tc = InstanceHandlerTestCase
        tc.test_instance_handler_post_ok
        tc = ActorHandlerTestCase
        tc.test_actor_handler_post_ok

        tc = InstanceActorHandlerTestCase
        tc.test_instanceactor_handler_post_ok
        tc.test_instanceactor_handler_get_id_ok
        tc.test_instanceactor_handler_get_id_not_found
        tc.test_instanceactor_handler_get_ok
        tc.test_instanceactor_handler_put_ok
        tc.test_instanceactor_handler_put_not_found
        tc.test_instanceactor_handler_delete_ok
        tc.test_instanceactor_handler_delete_not_found

        tc = InstanceHandlerTestCase
        tc.test_instance_handler_post_duplicate
        tc = ConceptHandlerTestCase
        tc.test_concept_handler_post_ok

        tc = InstanceConceptHandlerTestCase
        tc.test_instanceconcept_handler_post_ok
        tc.test_instanceconcept_handler_get_id_ok
        tc.test_instanceconcept_handler_get_id_not_found
        tc.test_instanceconcept_handler_get_ok
        tc.test_instanceconcept_handler_put_ok
        tc.test_instanceconcept_handler_put_not_found
        tc.test_instanceconcept_handler_delete_ok
        tc.test_instanceconcept_handler_delete_not_found

        tc = ConceptHandlerTestCase
        tc.test_concept_handler_delete_ok
        tc = ActorHandlerTestCase
        tc.test_actor_handler_delete_ok
        tc = InstanceHandlerTestCase
        tc.test_instance_handler_delete_ok

    def test_rest_post_all(self):
        tc = InstanceHandlerTestCase
        tc.test_instance_handler_post_ok
        tc = ActorHandlerTestCase
        tc.test_actor_handler_post_ok
        tc = InstanceActorHandlerTestCase
        tc.test_instanceactor_handler_post_ok
        tc = ConceptHandlerTestCase
        tc.test_concept_handler_post_ok
        tc = InstanceConceptHandlerTestCase
        tc.test_instanceconcept_handler_post_ok
#        import os
#        command = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
#                                            '../agave_prj/manage.py'))
#        file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
#                                            'fixtures/test_data.json')
#        print command
#        os.system('python ' + command + ' dumpdata agave > ' + file)

    def test_rest_json_all(self):
        tc = JsonRestTestCase
        tc.test_AAp

#from django.test.testcases.unittest import TestLoader
#suite = unittest.TestLoader().loadTestsFromTestCase(MainTestCase)

#./manage.py test agave.MainTestCase.test_rest_all -v 2
