from django.conf import settings
from django.db import models
from django.utils.hashcompat import sha_constructor
from django.utils.translation import ugettext_lazy as _

def get_hexdigest(user_input):
	return sha_constructor(settings.SECRET_KEY + user_input).hexdigest()

class Patient(models.Model):
	first_name = models.CharField(_("first name"), max_length=100)
	last_name = models.CharField(_("last name"), max_length=100)
	ident_hash = models.CharField(_("identify hash"), max_length=128, unique=True)
	phone_number = models.CharField(_("phone number"), max_length=100)
	email = models.EmailField(_("e-mail address"), blank=True)

	class Meta:
		verbose_name = _("patient")
		verbose_name_plural = _("patients")

	def __unicode__(self):
		return self.full_name
		
	def _get_full_name(self):
		"Returns the person's full name. Last name first."
		return "%s %s" % (self.last_name, self.first_name)
	full_name = property(_get_full_name)

	def save(self, *args, **kwargs):
		if not self.id:
			self.ident_hash = get_hexdigest(self.ident_hash)
		super(Patient, self).save(*args, **kwargs)


