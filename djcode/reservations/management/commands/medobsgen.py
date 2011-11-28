import datetime

from django.conf import settings
from django.core.management.base import NoArgsCommand
from django.db import transaction
from django.db.models import Q

from djcode.reservations.models import Day_status, Medical_office, Visit_disable_rule
from djcode.reservations.models import Visit_reservation, Visit_template

class Command(NoArgsCommand):
	help = "Pregenerate Visit_reservation records by Visit_template"

	def handle_noargs(self, **options):
		try:
			for office in Medical_office.objects.all():
				print '\nI: Office: %s' % office
				
				end_day = datetime.date.today() + datetime.timedelta(office.days_to_generate)
				print 'I: Days to generate: %d' % office.days_to_generate

				sid = transaction.savepoint()

				try:
					day = Visit_reservation.objects.filter(office = office).latest("starting_time").starting_time.date()
				except Visit_reservation.DoesNotExist:
					day = datetime.date.today()
				day += datetime.timedelta(1)

				while day <= end_day:
					day_status, day_status_created = Day_status.objects.get_or_create(
						day=day,
						office=office,
						defaults={"has_reservations": False})

					templates = Visit_template.objects.filter(day = day.isoweekday())
					templates = templates.filter(office = office, valid_since__lte = day)
					templates = templates.filter(Q(valid_until__exact=None) | Q(valid_until__gt=day))

					for tmp in templates:
						starting_time = datetime.datetime.combine(day, tmp.starting_time)

						if Visit_disable_rule.objects.filter(begin__lte = starting_time,
								end__gte = starting_time, office = office):
							status = 1 # disabled
						else:
							status = 2 # enabled

						print 'I: Creating reservation: %s' % (starting_time)
						Visit_reservation.objects.create(
							starting_time=starting_time,
							office=office,
							status=status,
							authenticated_only=tmp.authenticated_only
						)

					day += datetime.timedelta(1)

				transaction.savepoint_commit(sid)
		except ValueError:
			transaction.savepoint_rollback(sid)
