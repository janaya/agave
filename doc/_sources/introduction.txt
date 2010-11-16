.. _ref-introduction:

============
About AGAVE
============

AGAVE reads a dataset based on the tripartite model of tagging
(**Actors**: users, authors, etc, **Concepts**: tags, keywords and **Instances**: 
publications, pictures, etc.), create broader/narrower relations between 
Concepts, generate graphs, analyze them and provides and interface
to interactively visualize the graphs.

AGAVE is composed by the following modules:
 * ``agave``: main module that generate the graphs and plot the visualizations. 
   It also contains the logic to convert Pubmed XML data or other database to the 
   internal schema, generate the different graphs and to export them in csv or 
   JSON format for further visualization or analysis. It contains: 
  * ``pubmedxml2models``: to import XML Pubmed publications dataset
  * ``fpggdb2models``: to import projects from another database
  * ``graph_models_generator``: to create the basic models from datasets
  * ``CCbx_models_generator``: to query SPARQL endpoint to extract broaders relations
  * ``json_graph_generators``: to generate JSON graphs data to visualize interactively
  * ``graphs_queries``: to query the graphs
  * ``graphs_csv_generator``: to generate the CSV files for use in ``agave_graph_analysis`` module
  * ``statistics_generator``: to generate basic stadistics about the dataset and graphs
 * ``agave_prj``: umbrella module (a Django project).
 * ``zemanta_tags``: module to extract concepts from Instances abstract using zemanta API.  
 * ``mesh_skos_broader``: module to extract broaders relations between Concepts from SPARQL endpoints.
   Currently it uses Neurocommons Sparql endpoint and Medical Subject Headings (MeSH),
   but can be easily adapted to other LOD sources or other domains.
 * ``agave_graph_analysis``: module to generate network analysis and static graph images

Technologies
============
 * uses broader/narrower properties from `SKOS`_ ontology to determine relations between concepts
 * uses `SPARQL`_ to extract SKOS broader/narrower relations

Publications
============
AGAVE implements the research approach exposed in `Enrichment of affiliation networks and information discovery in SKOS-based 
datasets`_

Install
=======
To install AGAVE see :ref:`ref-install`

Download
========
You can download this project in either
 * `zip`_ or
 * `tar`_ formats.
 
You can also clone the project with `Git`_ by running::
    $ git clone git://github.com/janaya/agave

Bugs and features
=================
If you wish to signal a bug or report a feature request, please fill-in an issue on the `AGAVE issue tracker`_

License
=======
AGAVE is copyright 2010 by `DERI`_, `National University of Ireland, Galway`_ 
and is covered by the `New BSD license`_

Contact
========
(julia.anaya at gmail dot com)

Acknowledgments
================
AGAVE has been supported by Science Foundation Ireland under grant number SFI/08/CE/I1380 (Líon 2) and `Hypios Research, Paris`_ .

.. _Enrichment of affiliation networks and information discovery in SKOS-based datasets: http://www.inf.unibz.it/krdb/events/swap2010/paper-28.pdf
.. _SKOS: http://www.w3.org/2004/02/skos/
.. _SPARQL: http://www.w3.org/TR/rdf-sparql-query/
.. _zip: http://github.com/janaya/agave/zipball/master
.. _tar: http://github.com/janaya/agave/tarball/master
.. _AGAVE issue tracker: https://github.com/janaya/agave/issues
.. _Git: http://git-scm.com
.. _DERI: <http://deri.ie/
.. _National University of Ireland, Galway: http://nuigalway.ie/
.. _New BSD license: http://www.opensource.org/licenses/bsd-license.php
.. _Hypios Research, Paris: http://research.hypios.com/