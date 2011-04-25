from django import forms
from django.contrib.localflavor.cz.forms import CZBirthNumberField
from django.utils.translation import ugettext_lazy as _

from djcode.reservations.models import Examination_kind, Patient, Visit_reservation

class Patient_form(forms.ModelForm):
	label_suffix = ":"
	class Meta:
		model = Patient

	ident_hash = CZBirthNumberField(label=_("Birth number"))
	reservation = forms.ModelChoiceField(
		queryset=Visit_reservation.objects.all(),
		widget=forms.HiddenInput()
	)
	exam_kind = forms.ModelChoiceField(
		empty_label=None,
		queryset=Examination_kind.objects.all(),
		widget=forms.RadioSelect()
	)
