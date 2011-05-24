#!/usr/bin/python
""" Automaticaly generate Medobs 'visit template' by selecting start/end times and interval """

import datetime

from django.core.management.base import BaseCommand, CommandError
from djcode.reservations.models import Medical_office, Visit_template


TEMPLATE_VALID_SINCE = '2000-01-01'

def create_visit_template(office, starttime, endtime, interval):
	intervaltime = datetime.timedelta(minutes=interval)

	templatetime = starttime
	while templatetime.time() <= endtime.time():
		for day in Visit_template.DAYS:
			if day[0] <= 5: # do not create templates for Saturday and Sunday
				if not Visit_template.objects.filter(office=office, day=day[0], starting_time=templatetime.time()):
					print 'I: Creating template:  %s %s %s' % (office.name, day[1], templatetime.time())
					Visit_template.objects.create(office=office, day=day[0], starting_time=templatetime.time(), valid_since=TEMPLATE_VALID_SINCE)
				else:
					print 'W: Template already exists:  %s %s %s ... (skipping)' % (office.name, day[1], templatetime.time())

		templatetime = templatetime + intervaltime

class Command(BaseCommand):
	help = __doc__
	args = "starttime(HH:MM) endtime(HH:MM) interval(MM)"
	
	def handle(self, *args, **options):
		if len(args) != 3:
			raise CommandError("Missing some command parameters.")
		
		starttime = datetime.datetime.strptime(args[0], '%H:%M')
		endtime = datetime.datetime.strptime(args[1], '%H:%M')
		interval = int(args[2])
		
		for office in Medical_office.objects.all():
			create_visit_template(office, starttime, endtime, interval)

# vim: set ts=8 sts=8 sw=8 noet:
