# -*- coding: utf-8 -*-
from djcode.version import get_version

def version(request):
	return {"VERSION": get_version()}

# vim: set ts=8 sts=8 sw=8 noet:
