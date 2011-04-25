from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from djcode.reservations.forms import Patient_form
from djcode.reservations.models import Medical_office

def front_page(request):
	form = Patient_form()
	
	return render_to_response(
		"index.html",
		{
			"places": Medical_office.objects.order_by("pk"),
			"form": form,
		},
		context_instance=RequestContext(request)
	)

