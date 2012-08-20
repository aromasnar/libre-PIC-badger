Polar Common Project:
=====================

This is the complete Django project for the PIC Badge design website.
Here is the steps you need to do to get it working

1. make sure you have
	- Apache
	- Python 2.5.4  http://www.python.org/download/releases/2.5.4/  (you may use any latest version)
	- mod python    http://httpd.apache.org/modules/python-download.cgi
	- Django 1.1 (the latest)
	- lxml (used by CC license client API, and picbadge API)
	- django-piston (required for Picbadge API.. for restful APIs)
	- python config module (http://www.red-dove.com/config-doc/, http://www.red-dove.com/config/index.html) 

2. move the folder somewhere on the system and remember the path

3. configure Apache's Httpd.conf to direct a url to this project.
	- see APACHE SERVER CONFIGURATION below
	- see documentation on using django with apache server. its on django website see the tutorial

/// Step 4: not required any more.. now it automatically finds n set the path. ///
4. You have to correct the media path in the settings.py ( polarCommonProj/settings.py.
	The path should be absolute.
	steps:
	1. open the file
	2. find "MEDIA_ROOT = "
	3. make sure the path is correct.
		for example. on fluryy.colorado.edu, The project is on /srv/www... so the path would be "/srv/www/polarCommonProj/picBadge/"
		
NOTE: see dokuwiki for the project content details

Thats it!

** by default, debug is enabled so you will get full trace if you find any error:

APACHE SERVER CONFIGURATION:
----------------------------
1. ADD FOLLOWING to enable mod_python support in apache
     LoadModule python_module modules/mod_python.so (make sure it is correcT)

2. add following to redirect url like localhost/picbadge/ to our project

	<Location "/picbadge/">
		SetHandler python-program
		PythonHandler django.core.handlers.modpython	
		SetEnv DJANGO_SETTINGS_MODULE polarCommonProj.settings
		PythonOption django.root /polarCommonProj
		PythonDebug On
		PythonPath "['/CU_Boulder_data/CIRES_Job_data/django'] + sys.path"	
		#NOTE: path to directory where your polarCommonProj Exists
	</Location>
	
	<Location "/picbadgeapi/">
		SetHandler python-program
		PythonHandler django.core.handlers.modpython
		SetEnv DJANGO_SETTINGS_MODULE polarCommonProj.settings
		PythonOption django.root /polarCommonProj
		PythonDebug On
		PythonPath "['/ceddape/badges/trunk'] + sys.path"
		#NOTE: path to directory where your polarCommonProj Exists
	</Location>

RUNNING NOTES:
--------------

	KNOWN PROBLEMS:
	-------------
	if you are using, python 2.5.4 and django 1.1, you might get error "ImproperConfigured: ...."no module csrf found".
	in that case, just go ahead and comment following line in settings.py -> MIDDLEWARE_CLASSES
		#'django.middleware.csrf.CsrfViewMiddleware',
		
		you would also need to comment following lines in views.py
		
		#from django.views.decorators.csrf import csrf_exempt
		#@csrf_exempt
	
	CSS PATH CHANGE:
	----------------
	Before running the project on a new server, we have to change css path in settings.py. we 
	need to provide absolute path to the css folder.

Installing softwares:
--------------------
NOTE: easy_install is python script to automatically install python packages. 

*** django-piston ***

easy_install django-piston.

***lxml***

Required:
---------
libxml2
libxslt

you can use python setuptools (http://pypi.python.org/pypi/setuptools) to install lxml in single click step.
once you have setuptools, you can run following command to install lxml

easy_install lxml

NOTE: if you dont have libxml2 and/or libxslt, here is the steps to install them

	#

	Unpack the distribution archives (the version numbers will be different from this example):

	tar zxvf libxml2-2.6.27.tar.gz
	tar zxvf libxslt-1.1.20.tar.gz

	#

	Compile libxml2:

	cd libxml2-2.6.27
	./configure
	make
	make install

	You will need to have root permission to run the install step.
	#

	Compile libxslt:

	cd libxslt-1.1.20
	./configure
	make
	make install
	