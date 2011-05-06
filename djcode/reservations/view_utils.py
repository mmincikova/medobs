from datetime import date, timedelta

from djcode.reservations.models import Day_status, Medical_office

def is_reservation_on_date(for_date):
	""" Checks if reservations exist on selected date. """
	try:
		return Day_status.objects.get(day=for_date).has_reservations
	except Day_status.DoesNotExist:
		return False

def get_places(actual_date, public_only=False):
	if public_only:
		offices = Medical_office.objects.filter(public=True).order_by("pk")
	else:
		offices = Medical_office.objects.order_by("pk")
	return [{
		"id": o.id,
		"name": o.name,
		"reservations": o.reservations(actual_date),
		"disabled_days": o.disabled_days(actual_date)
		} for o in offices]
