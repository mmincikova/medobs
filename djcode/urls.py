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
	(r"^reservations/(?P<for_date>\d{4}-\d{2}-\d{2})/$", "date_reservations"),
	(r"^reservations/(?P<r_id>\d+)/hold/$", "hold_reservation"),
	(r"^reservations/(?P<r_id>\d+)/unhold/$", "unhold_reservation"),
	(r"^reservations/(?P<r_id>\d+)/unbook/$", "unbook_reservation"),
	(r"^reservations/(?P<r_id>\d+)/disable/$", "disable_reservation"),
	(r"^reservations/(?P<r_id>\d+)/enable/$", "enable_reservation"),
	(r"^booked/(?P<object_id>\d+)/$", object_detail, {
		"queryset": Medical_office.objects.all(),
		"template_object_name": "place",
		"template_name": "booked.html",
	}),
	(r"^cancel/(?P<object_id>\d+)/$", object_detail, {
		"queryset": Medical_office.objects.all(),
		"template_object_name": "place",
		"template_name": "cancel.html",
	}),
)

if settings.DEBUG:
        urlpatterns += patterns("",
                (r"^media/(?P<path>.*)$", "django.views.static.serve", {"document_root": settings.MEDIA_ROOT}),
		(r"^admin/doc/", include("django.contrib.admindocs.urls")),
        )

urlpatterns += patterns("",
	(r"^admin/", include(admin.site.urls)),
)
