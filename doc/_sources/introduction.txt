.. _ref-introduction:

============
About AGAVE
============


AGAVE reads a dataset based on the tripartite model of tagging
(**Actors**: users, authors, etc, **Concepts**: tags, keywords and **Instances**: 
publicatons, pictures, etc.), create broader/narrower relations between 
Concepts, generate graphs, analyse them and provides and interface
to interactively visualise the graphs.

AGAVE implements the research approach exposed in the paper
`Enrichment of affiliation networks and information discovery in SKOS-based datasets`_ 


AGAVE is composed by the following modules:
 * ``agave``: main module that generate the graphs and plot the visualizations. 
   It also contains the logic to convert Pubmed XML data or other database to the 
   internal schema, generate the different graphs and to export them in csv or 
   JSON format for further visualisation or analysis.
 * ``agave_prj``: umbrella module (a Django project).
 * ``zemanta_tags``: module to extract concepts from Instances abstract using zemanta API.  
 * ``mesh_skos_broader``: module to extract broaders relations between Concepts from SPARQL endpoints.
   Currently it uses Neurocommons endpoint and Medical Subject Headings (MeSH),
   but can be easily adapted to other endpoints or other kind of Concepts.
 * ``agave_graph_analysis``: module to generate network analysis and static graph images

.. _Enrichment of affiliation networks and information discovery in SKOS-based datasets: http://www.inf.unibz.it/krdb/events/swap2010/paper-28.pdf
.. module5: module to match projects tags with instances tags?
