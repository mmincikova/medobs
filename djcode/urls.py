from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.views.generic.list_detail import object_detail

from djcode.reservations.models import Medical_office

admin.autodiscover()
urlpatterns = patterns("djcode.reservations.views",
	(r"^$", "front_page"),
	(r"^accounts/login/$", login),
	(r"^accounts/logout/$", logout),
	(r"^android/login/$", "login"),
	(r"^android/logout/$", "logout"),
	(r"^office/(?P<office_id>\d+)/(?P<for_date>\d{4}-\d{2}-\d{2})/$", "office_page"),
	(r"^office/(?P<office_id>\d+)/$", "office_page"),
	(r"^reservations/(?P<for_date>\d{4}-\d{2}-\d{2})/(?P<office_id>\d+)/$", "date_reservations"),
	(r"^reservations/(?P<for_date>\d{4}-\d{2}-\d{2})/list/(?P<office_id>\d+)/$", "list_reservations"),
	(r"^reservations/(?P<r_id>\d+)/hold/$", "hold_reservation"),
	(r"^reservations/(?P<r_id>\d+)/unhold/$", "unhold_reservation"),
	(r"^reservations/(?P<r_id>\d+)/unbook/$", "unbook_reservation"),
	(r"^reservations/(?P<r_id>\d+)/disable/$", "disable_reservation"),
	(r"^reservations/(?P<r_id>\d+)/enable/$", "enable_reservation"),
	(r"^reservations/(?P<r_id>\d+)/details/$", "reservation_details"),
	(r"^patient/$", "patient_details"),
	(r"^patient/reservations/$", "patient_reservations"),
	(r"^days_status/(?P<year>\d{4})/(?P<month>\d{2})/(?P<office_id>\d+)/$", "days_status"),
	(r"^booked/(?P<office_id>\d+)/(?P<for_date>\d{4}-\d{2}-\d{2})/$", "booked"),
	(r"^cancel/(?P<object_id>\d+)/$", object_detail, {
		"queryset": Medical_office.objects.all(),
		"template_object_name": "office",
		"template_name": "cancel.html",
	}),
	(r"^offices/$", "list_offices"),
)

if settings.DEBUG:
        urlpatterns += patterns("",
                (r"^media/(?P<path>.*)$", "django.views.static.serve", {"document_root": settings.MEDIA_ROOT}),
		(r"^admin/doc/", include("django.contrib.admindocs.urls")),
        )

urlpatterns += patterns("",
	(r"^admin/", include(admin.site.urls)),
)
