:date: 09-06-2012
:title: Installing Nginx on CentOS 6.2 with php-fpm support
:tags: linux, nginx

Introduction
------------

Some people have been asking me talk about installing nginx and even explain what this really is.
As a part of the introduction I'm going to explain how this works in contrast to the well-known
Apache Http server.

Nginx is a very powerful high-traffic HTTP Server and `reverse proxy`_ . It was released in 2004, 
supporting about 22M of sites across all the world and growing up because of its performance,
stability, low resource consumption and multi-platform.

Warming up and installing
-------------------------

At the writing of this article the official release of Nginx is 1.2.0 which is the first version of the
1.2.x stable branch. But it is not included in the default repositories of CentOS 6.2, that's why it must
be downloaded the `epel repository`_ and the `Remi RPM`_ with the following steps as super user:

.. code-block:: bash

	rpm --import https://fedoraproject.org/static/0608B895.txt
 	rpm -ivh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-5.noarch.rpm
		
	rpm --import http://rpms.famillecollet.com/RPM-GPG-KEY-remi
	rpm -ivh http://rpms.famillecollet.com/enterprise/remi-release-6.rpm
		
	yum -y install yum-priorities
			
We are going to edit the epel.repo file:

.. code-block:: bash	

	vi /etc/yum.repos.d/epel.repo

And add the line to set the epel repo with priority 10:

.. code-block:: INI

	[epel]
	name=Extra Packages for Enterprise Linux 6 - $basearch
	#baseurl=http://download.fedoraproject.org/pub/epel/6/$basearch
	mirrorlist=https://mirrors.fedoraproject.org/metalink?repo=epel-6&arch=$basearch
	failovermethod=priority
	enabled=1
	gpgcheck=1
	gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-6
	priority=10
			
Now let's open the /etc/yum.repos.d/remi.repo and set the enabled=1

.. code-block:: INI 

	[remi]
	name=Les RPM de remi pour Enterprise Linux $releasever - $basearch
	#baseurl=http://rpms.famillecollet.com/enterprise/$releasever/remi/$basearch/
	mirrorlist=http://rpms.famillecollet.com/enterprise/$releasever/remi/mirror
	enabled=1
	gpgcheck=1
	gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-remi
	failovermethod=priority

So, next thing is install it, set it to run when the system starts and start the nginx daemon:

.. code-block:: bash

	yum -y install nginx
	chkconfig --levels 235 nginx on
	/etc/init.d/nginx start
			
After this, you should be able to see with your browser to your ip the classic `Welcome to nginx on EPEL`.

.. image:: /theme/images/nginx-home.png
	:width: 654px
	:height: 403
	:align: center

Now it's the time to set-up and install php-fpm:

.. code-block:: bash

			yum -y install php-fpm php-cli php-mysql php-gd php-imap php-ldap php-odbc php-pear php-xml php-xmlrpc php-eaccelerator php-magickwand php-magpierss php-mbstring php-mcrypt php-mssql php-shout php-snmp php-soap php-tidy
			
Then, we need to do a vi /etc/php.ini file and set the flag cgi.fix_pathinfo as 0, and is important
to set up your timezone, in my case is America/Mexico_City just like this:

.. code-block:: bash

			; cgi.fix_pathinfo provides *real* PATH_INFO/PATH_TRANSLATED support for CGI.  PHP's
			; previous behaviour was to set PATH_TRANSLATED to SCRIPT_FILENAME, and to not grok
			; what PATH_INFO is.  For more information on PATH_INFO, see the cgi specs.  Setting
			; this to 1 will cause PHP CGI to fix its paths to conform to the spec.  A setting
			; of zero causes PHP to behave as before.  Default is 1.  You should fix your scripts
			; to use SCRIPT_FILENAME rather than PATH_TRANSLATED.
			; http://www.php.net/manual/en/ini.core.php#ini.cgi.fix-pathinfo
			cgi.fix_pathinfo=0
			
			[Date]
			; Defines the default timezone used by the date functions
			; http://www.php.net/manual/en/datetime.configuration.php#ini.date.timezone
			date.timezone = America/Mexico_City
			
Now let's start php-fpm as a proxy, after this, php-fpm should be listening on the port 9000 so, if you
have a firewall, add the rule exception.

.. code-block:: bash
	
			chkconfig --levels 235 php-fpm on
			/etc/init.d/php-fpm start


Configuring nginx with php-fpm
------------------------------

At this point you have installed php-fpm and nginx, now is the time to set-up nginx with php support. One thing
that I really like about nginx is the easy-to-read configuration which offers a lot of useful features with some
simple configuration directives. In order to go further you can find more useful documentation on the `configuration`_
site, like increase working processes, and keep-alive settings, is up to you.

Now, let's do add a virtual host (in my case my blog domain josefigueroa.me) with a simple vi /etc/nginx/conf.d/virtual.conf
and modify the server {} section like this:
		
.. code-block:: conf

		server {
		    listen       80;
		    server_name  josefigueroa.me;

		    location / {
		        # You should change to your root path where your app or site locates
		        root   /home/ec2-user/public_html/josefigueroa/;
		        index  index.php index.html index.htm;
		    }

		    # Adding php support
		    location ~ \.php$ {
		            # You should change to your root path where your app or site locates
		            root           /home/ec2-user/public_html/josefigueroa/;
		            try_files $uri = 404;
		            # look at this is where php-fpm is listening on the port 9000
		            fastcgi_pass   127.0.0.1:9000;
		            fastcgi_index  index.php;
		            fastcgi_param  SCRIPT_FILENAME  $document_root$fastcgi_script_name;
		            include        fastcgi_params;
		     }

		    # Deny the access to read .htaccess files, if some Apache configuration is around
		    location ~ /\.ht {
		            deny  all;
		    }
		}


Now after save the file do a simple:

.. code-block:: bash

	/etc/init.d/nginx restart
		
At this point your php-fpm and nginx configuration should be all working, well the time to test, hell yeah, create
a simple phpinfo.php file where is located the well-known phpinfo(); method with vi /path/to/your/site and add:

.. code-block:: php

		<?php
			phpinfo();
		?>

save it and try again should be working like this:

.. image:: /theme/images/nginx-phpinfo.png
	:width: 654px
	:height: 403
	:align: center

Cool, I know maybe you ask 'Hum! but he uses python for his blog' well, sometimes I do development in PHP, so I need it.
Gracias amigos!



.. _reverse proxy: http://en.wikipedia.org/wiki/Reverse_proxy
.. _epel repository: http://fedoraproject.org/wiki/EPEL
.. _configuration: http://wiki.nginx.org/Configuration
.. _Remi RPM: http://rpms.famillecollet.com/