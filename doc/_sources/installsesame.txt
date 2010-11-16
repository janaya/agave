.. _ref-installsesame:

=======================================================================
Installing a local mesh-skos repository with Sesame in Debian/Ubuntu
=======================================================================

#. Install java::

    $ sudo sun-java6-jre sun-java6-jdk

#. Download tomcat::

	$ wget http://archive.apache.org/dist/tomcat/tomcat-6/v6.0.26/bin/apache-tomcat-6.0.26.tar.gz
	$ tar -xvzf apache-tomcat-6.0.26.tar.gz
	$ sudo mv apache-tomcat-6.0.26 /usr/local/bin
	$ rm apache-tomcat-6.0.26.tar.gz
	
#. Configure tomcat manager user::

	sudo vim /usr/local/bin/apache-tomcat-6.0.26/conf/tomcat-users.xml

   Add a manager role::
    
	<role rolename="manager"/>
	<user username="tomcat" password="tomcat" roles="manager"/>

#. Download and install the Java ODBC plugin::

	$ wget http://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-5.1.13.tar.gz/from/http://mysql.easynet.be/
	$ tar -xvzf mysql-connector-java-5.1.13.tar.gz
	$ sudo cp mysql-connector-java-5.1.13/mysql-connector-java-5.1.13-bin.jar /usr/local/bin/apache-tomcat-6.0.26/lib/
	$ rm -rf mysql-connector-java-5.1.13*

#. Download and install Sesame:

   You could also install it through the Tomcat Manager web interface after starting Sesame server: 
   http://localhost:8080/manager/html
   
   To do it in the shell:: 
   
	$ wget http://downloads.sourceforge.net/project/sesame/Sesame%202/2.3.2/openrdf-sesame-2.3.2-sdk.tar.gz?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fsesame%2Ffiles%2FSesame%25202%2F2.3.2%2F&ts=1289313287&use_mirror=heanet
	$ tar -xvzf openrdf-sesame-2.3.2-sdk.tar.gz
    $ cp openrdf-sesame-2.3.2-sdk/war/openrdf-*.war /usr/local/bin/apache-tomcat-6.0.26/webapps
    $ rm -rf openrdf-sesame-2.3.2-sdk*

#. Start Sesame server::

	$ sudo /usr/local/bin/apache-tomcat-6.0.26/bin/catalina.sh start

#. Create the Sesame MySQL database::

	$ CREATE DATABASE sesame_store;
	$ grant all privileges on sesame_store.* to 'sesameuser'@'%' identified by 'sesamepw';

#. Create the mesh-skos Sesame repository:

   Through the web interface:
   
   Go to http://localhost:8080/openrdf-workbench/repositories/SYSTEM/
   
   Click on ``New Repository``, on ``Type`` select ``Mysql RDF Store``,
   introduce the ``Title`` and ``ID``, the database name, user and password
  
#. Download mesh-skos bundles::

	$ mkdir ncbundles
	$ cd ncbundles  
	$ rsync -a rsync.neurocommons.org::mesh/ mesh/

   Downloading also the mesh-eswc06 bundle will add transitive dataset

#. Add mesh-skos bundles to Sesame repository

   Through the web interface:
   
   Go to http://localhost:8080/openrdf-workbench/repositories/
   
   Click on ``Add`` and select ncbundles/mesh/mesh-skos/meshdata.rdf file
   
   Do the same with ncbundles/mesh/mesh-skos/meshstructure.rdf file