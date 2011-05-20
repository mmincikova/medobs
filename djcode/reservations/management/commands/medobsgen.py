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
			sid = transaction.savepoint()

			try:
				day = Visit_reservation.objects.latest("starting_time").starting_time.date()
			except Visit_reservation.DoesNotExist:
				day = datetime.date.today()
			day += datetime.timedelta(1)

			end_day = datetime.date.today() + datetime.timedelta(settings.MEDOBS_GEN_DAYS)

			while day <= end_day:
				for office in Medical_office.objects.all():
					day_status, day_status_created = Day_status.objects.get_or_create(
						day=day,
						place=office,
						defaults={"has_reservations": False})

				templates = Visit_template.objects.filter(day = day.isoweekday())
				templates = templates.filter(valid_since__lte = day)
				templates = templates.filter(Q(valid_until__exact=None) | Q(valid_until__gt=day))

				for tmp in templates:
					starting_time = datetime.datetime.combine(day, tmp.starting_time)

					if Visit_disable_rule.objects.filter(begin__gte=starting_time):
						status = 1 # disabled
					else:
						status = 2 # enabled
					
					print 'I: Creating reservation: %s %s' % (tmp.place.name, starting_time)
					Visit_reservation.objects.create(
						starting_time=starting_time,
						place=tmp.place,
						status=status
					)

				day += datetime.timedelta(1)

			transaction.savepoint_commit(sid)
		except ValueError:
			transaction.savepoint_rollback(sid)
