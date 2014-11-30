#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# Basic settings
AUTHOR = u'crazygit'
SITENAME = u'Wise Turtles'
SITEURL = ''
USE_FOLDER_AS_CATEGORY = True
DEFAULT_CATEGORY = u'其它'
DEFAULT_DATE_FORMAT = '%Y-%m-%d'
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = False
DEFAULT_DATE = "fs"
# path-specific metadata
EXTRA_PATH_METADATA = {
    'extra/CNAME': {'path': 'CNAME'},
    'extra/robots.txt': {'path': 'robots.txt'},
}
# static paths will be copied without parsing their contents
STATIC_PATHS = [
    'extra',
]
PATH = 'content'
PAGE_PATHS = ['pages']
TIMEZONE = 'Asia/Chongqing'
TYPOGRIFY = True
DEFAULT_LANG = u'zh'


# URL settings
ARTICLE_URL = 'posts/{slug}.html'
ARTICLE_SAVE_AS = 'posts/{slug}.html'

# Tag cloud
TAG_CLOUD_STEPS = 4
TAG_CLOUD_MAX_ITEMS = 100

# Theme
THEME = "theme"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("Travis-ci", "https://travis-ci.org/"),
    ("Wercker", "http://wercker.com/"),
    ("Cloudbees", "http://www.cloudbees.com"),
    ("Pelican", "http://docs.getpelican.com/"),
    ("Jinja", "http://jinja.pocoo.org/"),
)

# Pagination
DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
