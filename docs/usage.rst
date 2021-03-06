.. _ref-usage:

=================
Using AGAVE
=================

Initializing publications from a dump of Pubmed XML publications
====================================================================

You can load this dataset and generate the broader patterns relations between
concepts and actor with one command::

    (agaveenv)$ python manage.py initialize_publications

Or step by step: 

#. Load the dataset::

    (agaveenv)$ python manage.py pubmedxml2models

#. Generate the broader patterns relations between concepts::

	(agaveenv)$ python manage.py generate_CCbx_models

#. Generate the broader patterns relations between actors::

	(agaveenv)$ python manage.py generate_AAbx_models


Initializing projects from an external database
====================================================================

You can also load the dataset and generate the broader patterns relations in
one command or do it step by step.
With one command::

    (agaveenv)$ python manage.py initialize_projects

Step by step:

#. Load the dataset::

    (agaveenv)$ python manage.py fpggdb2models
    
   You will have to adapt fpggdb2models code to fit your database


#. Generate the broader patterns relations between concepts::

	(agaveenv)$ python manage.py generate_CCbx_models

#. Generate the broader patterns relations between actors::

	(agaveenv)$ python manage.py generate_AAbx_models


Running AGAVE Web application
==============================

Run the development application
-------------------------------

Inside of agave_prj run::

    (agavenv)$ python manage.py runserver

Point your browser at http://localhost:8000/

(Optional) Configure your Apache web server
-------------------------------------------------------
  
#. Install apache following the process described in :ref:`ref-install`
       
#. Copy the configuration file and edit it to your needs::

    $ cp projects/agave/deploy/agave.apache /etc/apache2/sites-available/agavedomain.com

#. Enable the site and reload Apache::

    $ sudo a2ensite /etc/apache2/sites-available/agavedomain.com
    $ sudo /etc/init.d/apache2 reload

#. Remember to add to /etc/apache2/mods-enabled/mod_wsgi.conf to enable HTTP 
   basic authentication for the REST API::

    WSGIPassAuthorization On

Generating statistics
========================================

Once the model and graphs have been generated

 * Generate statistics::

	(agaveenv)$ python manage.py generate_statistics

Generating global graph analysis
========================================

 * Generate graphs csv::

 	(agaveenv)$ python manage.py generate_graphs_csv

   This will generate .csv files inside output_csv directory

 * Generate global graphs image::

    agave_graph_analysis$ R
    > source('x-generate-AAc_CCa_AAb_CCb.R')

  This will generate .eps files inside output_plots directory

