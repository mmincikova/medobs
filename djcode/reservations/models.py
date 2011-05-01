from datetime import datetime, date, time

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

	def has_reservation(self):
		if self.visit_reservations.filter(starting_time__gte=datetime.now()).exists():
			return True
		else:
			return False
	has_reservation.boolean = True

	def save(self, *args, **kwargs):
		if not self.id:
			self.ident_hash = get_hexdigest(self.ident_hash)
		super(Patient, self).save(*args, **kwargs)

class Medical_office(models.Model):
	name = models.CharField(_("name"), max_length=100)
	street = models.TextField(_("street"))
	zip_code = models.CharField(_("zip code"), max_length=20)
	city = models.CharField(_("city"), max_length=100)
	email = models.EmailField(_("e-mail address"), blank=True)

	class Meta:
		verbose_name = _("medical office")
		verbose_name_plural = _("medical offices")

	def __unicode__(self):
		return self.name

	def reservations(self, for_date):
		""" Returns all reservations in office for selected day. """
		since = datetime.combine(for_date, time(0, 0, 0))
		until = datetime.combine(for_date, time(23, 59, 59))
		return self.visit_reservations.filter(
				starting_time__gte=since,
				starting_time__lte=until
			).order_by("starting_time")

class Office_phone(models.Model):
	number = models.CharField(_("number"), max_length=50)
	office = models.ForeignKey(Medical_office, verbose_name=_("medical office"),
			related_name="phone_numbers")

	class Meta:
		verbose_name = _("office phone")
		verbose_name_plural = _("office phones")

	def __unicode__(self):
		return self.number

class Visit_template(models.Model):
	DAYS = (
		(1, _("Monday")),
		(2, _("Tuesday")),
		(3, _("Wednesday")),
		(4, _("Thursday")),
		(5, _("Friday")),
		(6, _("Saturday")),
		(7, _("Sunday")),
	)
	day = models.PositiveSmallIntegerField(_("day"), choices=DAYS)
	starting_time = models.TimeField(_("starting time"))
	valid_since = models.DateField(_("valid since"),
			help_text=_("This date is included into interval."))
	valid_until = models.DateField(_("valid until"), null=True, blank=True,
			help_text=_("This date is not included into interval."))
	place = models.ForeignKey(Medical_office, verbose_name=_("place"),
			related_name="templates")

	class Meta:
		verbose_name = _("visit template")
		verbose_name_plural = _("visit templates")

	def __unicode__(self):
		return _("%s at %s") % (self.get_day_display(), self.starting_time)

class Visit_disable_rule(models.Model):
	begin = models.DateTimeField(_("begin"))
	end = models.DateTimeField(_("end"))
	place = models.ForeignKey(Medical_office, verbose_name=_("place"),
			related_name="disables")

	class Meta:
		verbose_name = _("visit disable rule")
		verbose_name_plural = _("visit disable rules")

	def __unicode__(self):
		return _("From %s to %s") % (self.begin, self.end)

class Examination_kind(models.Model):
	title = models.TextField(_("title"))

	class Meta:
		verbose_name = _("examination kind")
		verbose_name_plural = _("examinations kinds")

	def __unicode__(self):
		return self.title

class Visit_reservation(models.Model):
	STATUS_CHOICES = (
		(1, _("disabled")),
		(2, _("enabled")),
		(3, _("booked")),
		(4, _("in held")),
	)
	starting_time = models.DateTimeField(_("starting time"))
	place = models.ForeignKey(Medical_office, verbose_name=_("place"),
			related_name="visit_reservations")
	patient = models.ForeignKey(Patient, verbose_name=_("patient"), null=True, blank=True,
			related_name="visit_reservations")
	exam_kind = models.ForeignKey(Examination_kind, verbose_name=_("examination kind"),
			null=True, blank=True)
	status = models.PositiveSmallIntegerField(_("status"), default=2, choices=STATUS_CHOICES)
	booked_at = models.DateTimeField(_("booked at"), null=True, blank=True)

	class Meta:
		verbose_name = _("visit reservation")
		verbose_name_plural = _("visit reservations")

	def __unicode__(self):
		return _("%s at %s") % (self.starting_time, self.place.name)
