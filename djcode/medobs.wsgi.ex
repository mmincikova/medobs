import os
import sys

sys.path.insert(1, '/opt/python-locals/django/latest-stable/')

sys.path.append('/var/www/medobs/')
sys.path.append('/var/www/medobs/djcode/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'djcode.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

# vim: set ts=8 sts=8 sw=8 noet:
