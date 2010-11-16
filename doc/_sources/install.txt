.. _ref-install:

=================================
Installing AGAVE in Debian/Ubuntu
=================================

Install requirements
=================================

#. Installing basic requirements (Python and MySQL)

   In Debian Unstable:: 

     $ sudo aptitude install mysql-server python2.6 python-setuptools 
       libmysqlclient-dev python2.6-dev

   In Debian Lenny, you will have add unstable repository or backports for python2.6 support:

 * Add to /etc/apt/sources.list::

        deb http://ftp.us.debian.org/debian unstable main non-free contrib

 * Add to /etc/apt/preferences::

        Package: *
        Pin: release a=stable
        Pin-Priority: 700

        Package: *
        Pin: release a=unstable
        Pin-Priority: 600

 * Then install the packages::

     $ sudo aptitude install python2.6/unstable python-setuptools/unstable

#. (Optional) Installing Apache2 web server and WSGI 

   In Debian Unstable:: 
 
    $ sudo aptitude install libapache2-mod-wsgi

   In Debian Lenny (edit sources.list as explained above.)::

     $ sudo aptitude install libapache2-mod-wsgi/unstable
       

#. Installing requirements to download other software from git and mercurial::

    $ sudo aptitude install git-core mercurial

#. Installing requirements for the virtualenv::

    $ sudo easy_install pip
    $ sudo pip install virtualenv
  
#. (Optional) Installing R packages (for ``agave_graph_analysis`` module)::
   
    $ sudo aptitude install r-base r-base-dev r-cran-lattice r-cran-matrix 
      r-recommended r-base-core r-base-html r-cran-boot r-cran-class 
      r-cran-cluster r-cran-codetools r-cran-foreign r-cran-kernsmooth 
      r-cran-lattice r-cran-mass r-cran-matrix r-cran-mgcv r-cran-nlme 
      r-cran-nnet r-cran-rpart  r-cran-spatial r-cran-survival r-doc-html ess

  Then install remaining R packages from R shell::

    $ R
    > install.packages("sqldf")
    > install.packages("igraph")
	> install.packages("ppls")
	> install.packages("gplots")

#. (Optional) To setup you our local Sesame repository (see :ref:`ref-installsesame`)

Installing AGAVE
====================

#. Download the application::

    $ git clone git://github.com/janaya/agave

#. Create a virtualenv (you can choose any path to install the virtualenv)::

    $ virtualenv --no-site-packages /path/to/agaveenv -p python2.6

#. Activate the virtualenv and install dependencies::

    $ source /path/to/agaveenv/bin/activate
    (agaveenv)$ pip install -E agaveenv -r agave/requirements/external_apps.txt

#. (Optional) Download bioreader (only needed for ``pubmedxml2models``) inside agave_prj or inside 
   /path/to/agaveenv/lib/python2.6/site-packages::

	$ cd /path/to/agaveenv/lib/python2.6/site-packages/
	$ hg clone http://bitbucket.org/jagan/bioreader

Creating the databases
=================================

Currently AGAVE is designed to work with two databases, one for storing 
publications and one for storing projects. The second database is optional. 
To create both::

     $ mysql 
     mysql> CREATE DATABASE agave_pr DEFAULT CHARACTER SET utf8 
            DEFAULT COLLATE utf8_general_ci;
     mysql> CREATE DATABASE agave_pu DEFAULT CHARACTER SET utf8 
            DEFAULT COLLATE utf8_general_ci;
     mysql> grant all privileges on agave_pr.* to user identified by 'userpw';
     mysql> grant all privileges on agave_pu.* to user identified by 'userpw';
       
Customizing settings
=================================

Create a local_settings.py file inside the project directory
(/path/to/agave/agave_prj).

* Set your databases names, user and password, for instance::
    
    DATABASES - {
    'default': {
        'NAME': 'agave_pr',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'user',
        'PASSWORD': 'userpw'
    },
    'instances': {
        'NAME': 'agave_pu',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'user',
        'PASSWORD': 'userpw'
    }
	}
	
* (Optional) for ``zemanta_tags`` module, set::
    
	ZEMANTA_KEY - 'yourapikey'
    
* (Optional) if you're initializing app with an external database, 
  set also the name, user and password, for instance::
    
    SN_DBSERVER - 'localhost'
    SN_DBNAME - 'dbuser'
    SN_DBUSER - 'dbpw'
    SN_DBPW - 'extranet_fpgg'
    
* (Optional) In case you're running a local MeSH-SKOS repository  (see :ref:`ref-installsesame`), set::
 
 	SPARQL_ENDPOINT_LOCAL = True

Initializing databases
=================================

To create the initial schema, run::

    (agaveenv)$ cd agave_prj/
    (agaveenv)$ python manage.py syncdb
    (agaveenv)$ python manage.py syncdb --database-instances

Now you can  insert data using the REST API (see :ref:`ref-api`) or initializing the 
databases with the command line (see :ref:`ref-usage`).

