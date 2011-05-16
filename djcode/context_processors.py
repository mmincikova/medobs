from django.conf import settings
from djcode.version import get_version

def version(request):
	return {"VERSION": get_version()}


def datepicker_i18n_file(request):
	return {"DATEPICKER_I18N_FILE": settings.DATEPICKER_I18N_FILE}

# vim: set ts=8 sts=8 sw=8 noet:
