from datetime import date, timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from djcode.reservations.models import Day_status, Medical_office

def is_reservation_on_date(for_date, office):
	""" Checks if reservations exist on selected date. """
	try:
		return Day_status.objects.get(day=for_date, office=office).has_reservations
	except Day_status.DoesNotExist:
		return False

def get_offices(user):
	if user.is_authenticated():
		return Medical_office.objects.all()
	else:
		return Medical_office.objects.filter(public=True)

def send_notification(reservation):
	send_mail(
		_("Visit reservation confirmation"),
		render_to_string(
			"email/first_notification.html",
			{"reservation": reservation}
		),
		settings.DEFAULT_FROM_EMAIL,
		[reservation.patient.email],
		fail_silently=False
	)
