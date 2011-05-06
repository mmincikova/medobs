from datetime import date, timedelta

from djcode.reservations.models import Day_status, Medical_office

def is_reservation_on_date(for_date, place):
	""" Checks if reservations exist on selected date. """
	try:
		return Day_status.objects.get(day=for_date, place=place).has_reservations
	except Day_status.DoesNotExist:
		return False

def get_places(user):
	if user.is_authenticated():
		return Medical_office.objects.order_by("pk")
	else:
		return Medical_office.objects.filter(public=True).order_by("pk")
