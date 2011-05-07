from datetime import date, timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import NoArgsCommand
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from djcode.reservations.models import Medical_office

class Command(NoArgsCommand):
	help = "Sends notification emails about tomorrow reservations"

	def handle_noargs(self, **options):
		actual_date = date.today() + timedelta(1)
		for place in Medical_office.objects.all():
			for r in place.reservations(actual_date):
				if r.status == 3 and r.patient.email:
					send_mail(
						_("Notification about upcoming visit reservation"),
						render_to_string(
							"email/second_notification.txt",
							{"reservation": r}
						),
						settings.DEFAULT_FROM_EMAIL,
						[r.patient.email],
						fail_silently=False
					)
