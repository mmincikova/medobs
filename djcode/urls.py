from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.list_detail import object_detail

from djcode.reservations.models import Medical_office

admin.autodiscover()
urlpatterns = patterns("djcode.reservations.views",
	(r"^$", "front_page"),
	(r"^booked/(?P<object_id>\d+)/$", object_detail, {
		"queryset": Medical_office.objects.all(),
		"template_object_name": "place",
		"template_name": "booked.html",
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
