#!/bin/bash

export PYTHONPATH=/opt/python-locals/django/latest-stable

python -c "import django; print 'DJANGO VERSION:', django.VERSION"
