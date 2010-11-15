.. _ref-requirements:

=================================
AGAVE requirements
=================================

To get started with AGAVE you must have the following installed:

 * `MySQL`_ 5.1+ 
 * `Python`_ 2.6+  
 * `virtualenv`_ 1.4.7+

See :ref:`ref-install` to know how to install it.

Some of the next requirements are optional or will be installed automatically 
following the process explained in :ref:`ref-install`

 * `Django`_ 1.2+
 * `bioreader`_ (optional) to initialise database with Pubmed XML files.
    It can also be downloaded on `sourceforge`_ or as `NLTK contributions`_  
 * `SPARQLWrapper`_ 1.4.1+ for ``mesh_skos_broader`` module
 * `R`_ 2.12+ (optional) for ``agave_graph_analysis`` module
..  * `NetworkX`_ 1.1+
..  * `NumPy`_ 1.4+
..  * `matplotlib`_ 0.99+
..  * `R`_ 2.12+


.. _MySQL: http://www.mysql.com/
.. _Python: http://python.org/
.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _Django: http://www.djangoproject.com/
.. _bioreader: http://bitbucket.org/jagan/bioreader/
.. _SPARQLWrapper: http://sparql-wrapper.sourceforge.net/
.. _NetworkX: http://networkx.lanl.gov/
.. _NumPy: http://numpy.scipy.org/
.. _matplotlib: http://matplotlib.sourceforge.net/
.. _R: http://cran.r-project.org/
.. _sourceforge: http://sourceforge.net/projects/bioinforread/
.. _NLTK contributions: http://code.google.com/p/nltk/source/browse/trunk/nltk_contrib/nltk_contrib/bioreader/?r=8404