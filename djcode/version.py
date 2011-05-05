VERSION = (0, 7, 0, "")

def get_version():
	""" Returns project version as string. """
	if VERSION[3].lower() == "trunk":
		version = "Trunk"
	else:
		version = "%s.%s" % (VERSION[0], VERSION[1])
		if VERSION[2]:
			version = "%s.%s" % (version, VERSION[2])
		version = "%s %s" % (version, VERSION[3])
	return version
	

# vim: set ts=8 sts=8 sw=8 noet:
