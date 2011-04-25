import datetime
from django.shortcuts import render_to_response
from django.template import RequestContext

from djcode.reservations.forms import Patient_form
from djcode.reservations.models import Medical_office, Patient
from djcode.reservations.models import get_hexdigest

def front_page(request):
	if request.method == 'POST':
		form = Patient_form(request.POST)
		if form.is_valid():
			hexdigest = get_hexdigest(form.cleaned_data["ident_hash"])
			patient, patient_created = Patient.objects.get_or_create(ident_hash=hexdigest,
					defaults={
						"first_name": form.cleaned_data["first_name"],
						"last_name": form.cleaned_data["last_name"],
						"ident_hash": form.cleaned_data["ident_hash"],
						"phone_number": form.cleaned_data["phone_number"],
						"email": form.cleaned_data["email"],
					})

			reservation = form.cleaned_data["reservation"]
			reservation.patient = patient
			reservation.exam_kind = form.cleaned_data["exam_kind"]
			reservation.status = 3
			reservation.booked_at = datetime.datetime.now()
			reservation.save()
	else:
		form = Patient_form()
	
	return render_to_response(
		"index.html",
		{
			"places": Medical_office.objects.order_by("pk"),
			"form": form,
		},
		context_instance=RequestContext(request)
	)

