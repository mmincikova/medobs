from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import direct_to_template

from djcode.reservations.forms import Patient_form

admin.autodiscover()
urlpatterns = patterns("",
	(r"^$", direct_to_template, {
		"template": "index.html",
		"extra_context": {"form": Patient_form()}
	}, "site_home"),
)

if settings.DEBUG:
        urlpatterns += patterns("",
                (r"^media/(?P<path>.*)$", "django.views.static.serve", {"document_root": settings.MEDIA_ROOT}),
		(r"^admin/doc/", include("django.contrib.admindocs.urls")),
        )

urlpatterns += patterns("",
	(r"^admin/", include(admin.site.urls)),
)
