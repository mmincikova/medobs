from django.contrib import admin
from djcode.reservations.models import Medical_office, Office_phone, Patient, Visit_disable_rule, Visit_template

class Office_phone_Inline(admin.TabularInline):
    model = Office_phone

class Medical_office_Admin(admin.ModelAdmin):
	list_display = ("name", "street", "zip_code", "city", "email")
	inlines = [Office_phone_Inline,]
admin.site.register(Medical_office, Medical_office_Admin)

class Office_phone_Admin(admin.ModelAdmin):
	list_display = ("number", "office")
admin.site.register(Office_phone, Office_phone_Admin)

class Patient_Admin(admin.ModelAdmin):
	list_display = ("full_name", "phone_number", "email", "ident_hash")
	search_fields = ("last_name",)
admin.site.register(Patient, Patient_Admin)

class Visit_template_Admin(admin.ModelAdmin):
	list_display = ("__unicode__", "valid_since", "valid_until")
admin.site.register(Visit_template, Visit_template_Admin)

class Visit_disable_rule_Admin(admin.ModelAdmin):
	list_display = ("begin", "end")
admin.site.register(Visit_disable_rule, Visit_disable_rule_Admin)
