from django.contrib import admin
from djcode.reservations.models import Patient

class Patient_Admin(admin.ModelAdmin):
	list_display = ("full_name", "phone_number", "email", "ident_hash")
	search_fields = ("last_name",)
admin.site.register(Patient, Patient_Admin)
