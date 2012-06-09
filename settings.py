# -*- coding: utf-8 -*-
AUTHOR = 'Jose Figueroa'
SITENAME = u"Viva la rèsistance"
SITEURL = ''
TIMEZONE = "America/Mexico_City"
THEME = 'theme'

DISQUS_SITENAME = "josefig"
#REVERSE_CATEGORY_ORDER = True
DEFAULT_PAGINATION = 5
RELATIVE_URLS = False

from collections import namedtuple
link = namedtuple('link', ('description','name','url'))

LINKS = (	
		link('unixmexico', name='Unixmexico', url='http://unixmexico.org'),
		link('cofradia', name='Cofradia', url='http://cofradia.org'),
		link('hacker', name='Hacker news', url='http://news.ycombinator.com'),
		link('ide', name='Ide One',url='http://ideone.com'),
		link('jsfiddle', name='Jsfiddle', url='http://jsfiddle.net'),
		)

SOCIAL = (('twitter', 'http://twitter.com/el_figueroac'),
					('github', 'http://github.com/josefig'),
					('facebook', 'http://facebook.com/flako.figueroa')
					)

#STATIC_PATHS = ["pictures",]
#FILES_TO_COPY = (('extra/robots.txt','robots.txt'),)
GOOGLE_ANALYTICS = 'UA-30180401-1'
ARTICLE_DIR = 'posts'
ARTICLE_URL = 'posts/{slug}/'
ARTICLE_SAVE_AS = 'posts/{slug}/index.html'

PAGE_URL = '{slug}'
PAGE_SAVE_AS = '{slug}/index.html'

FEED_RSS = 'posts/feed/latest'
