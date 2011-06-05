#!/bin/bash
# Load test data. Run from 'djcode' directory.

./manage.py reset reservations
./manage.py loaddata reservations/fixtures/medobs.json

./manage.py medobstemplates "My first office" 06:00 08:00 30
./manage.py medobstemplates "My second office" 06:00 08:00 30
./manage.py medobstemplates "My third non-public office" 06:00 08:00 30

./manage.py medobsgen
