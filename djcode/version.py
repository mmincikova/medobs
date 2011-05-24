from subprocess import Popen, PIPE

def get_version():
	""" Returns project version as string from 'git describe' command. """
	pipe = Popen('git describe', stdout=PIPE, shell=True)
	version = pipe.stdout.read()
	
	if version:
		return version
	else:
		return 'unknown version'

# vim: set ts=8 sts=8 sw=8 noet:
