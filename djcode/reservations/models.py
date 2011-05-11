from datetime import datetime, date, time, timedelta

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
	order = models.PositiveIntegerField(_("order"), help_text=_("Order of medical offices tabs on the webpage."))
	public = models.BooleanField(_("public"),
		help_text=_("Check if you want to make this medical office accessible for not authorized visitors."))

	class Meta:
		verbose_name = _("medical office")
		verbose_name_plural = _("medical offices")
		ordering = ("order",)

	def __unicode__(self):
		return self.name

	def reservations(self, for_date):
		""" Returns all reservations in office for selected day. """
		since = datetime.combine(for_date, time(0, 0, 0))
		until = datetime.combine(for_date, time(23, 59, 59))
		return self.visit_reservations.filter(starting_time__range=(since, until)).order_by("starting_time")

	def disabled_days(self, start_date, end_date):
		""" Returns list of disabled days from start date to end of month. """
		status_set = self.day_status_set.filter(day__range=(start_date, end_date))
		return [self._date2str(d.day) for d in status_set if not d.has_reservations]

	def _date2str(self, actual_date):
		""" Returns date as string yyyy-m-d (without leading zeros in month and day. """
		return "%d-%d-%d" % (
				int(actual_date.strftime("%Y")),
				int(actual_date.strftime("%m")),
				int(actual_date.strftime("%d")),
			)

	def _get_first_day(self, dt, d_years=0, d_months=0):
		# d_years, d_months are "deltas" to apply to dt
		y, m = dt.year + d_years, dt.month + d_months
		a, m = divmod(m-1, 12)
		return date(y+a, m+1, 1)

	def _get_last_day(self, dt):
		return self._get_first_day(dt, 0, 1) + timedelta(-1)

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
	place = models.ForeignKey(Medical_office, verbose_name=_("medical office"),
			related_name="templates")
	day = models.PositiveSmallIntegerField(_("week day"), choices=DAYS)
	starting_time = models.TimeField(_("starting time"))
	valid_since = models.DateField(_("valid since"),
			help_text=_("This date is included into interval."))
	valid_until = models.DateField(_("valid until"), null=True, blank=True,
			help_text=_("This date is not included into interval."))

	class Meta:
		verbose_name = _("visit template")
		verbose_name_plural = _("visit templates")

	def __unicode__(self):
		return _("%s at %s") % (self.get_day_display(), self.starting_time)

class Visit_disable_rule(models.Model):
	place = models.ForeignKey(Medical_office, verbose_name=_("medical office"),
			related_name="disables")
	begin = models.DateTimeField(_("begin"))
	end = models.DateTimeField(_("end"))

	class Meta:
		verbose_name = _("visit disable rule")
		verbose_name_plural = _("visit disable rules")

	def __unicode__(self):
		return _("From %s to %s") % (self.begin, self.end)

class Examination_kind(models.Model):
	title = models.TextField(_("title"))
	order = models.PositiveIntegerField(_("order"), help_text=_("Order of examination kinds in patient input form."))

	class Meta:
		verbose_name = _("examination kind")
		verbose_name_plural = _("examinations kinds")
		ordering = ("order",)

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
		ordering = ("-starting_time",)

	def __unicode__(self):
		return _("%s at %s") % (self.starting_time, self.place.name)

	def _passed(self):
		if self.starting_time < datetime.now():
			return True
		else:
			return False
	passed = property(_passed)

class Day_status(models.Model):
	day = models.DateField(_("day"))
	place = models.ForeignKey(Medical_office, verbose_name=_("place"))
	has_reservations = models.BooleanField(_("has reservations"))

	class Meta:
		verbose_name = _("day status")
		verbose_name_plural = _("days statuses")
		unique_together = (("day", "place"),)

	def __unicode__(self):
		return self.day.__str__()

def enable_day_status(sender, instance, created, **kwargs):
	for_date = instance.starting_time.date()
	if created:
		day_status, day_status_created = Day_status.objects.get_or_create(
			day=for_date,
			place=instance.place,
			defaults={"has_reservations": True})
		if not day_status_created:
			day_status.has_reservations = True
			day_status.save()

def update_day_status(sender, instance, **kwargs):
	for_date = instance.starting_time.date()
	start = datetime.combine(for_date, time(0, 0, 0))
	end = datetime.combine(for_date, time(23, 59, 59))

	status = Visit_reservation.objects.filter(
			starting_time__range=(start, end),
			place=instance.place
		).exists()

	day_status, day_status_created = Day_status.objects.get_or_create(
		day=for_date,
		place=instance.place,
		defaults={"has_reservations": status})
	if not day_status_created:
		day_status.has_reservations = status
		day_status.save()

models.signals.post_save.connect(enable_day_status, sender=Visit_reservation)
models.signals.post_delete.connect(update_day_status, sender=Visit_reservation)

def gen_days_statuses(sender, instance, created, **kwargs):
	if created:
		actual_date = date.today()
		end_date = actual_date + timedelta(settings.MEDOBS_GEN_DAYS)

		while actual_date <= end_date:
			day_status, day_status_created = Day_status.objects.get_or_create(
				day=actual_date,
				place=instance,
				defaults={"has_reservations": False})
			actual_date += timedelta(1)

models.signals.post_save.connect(gen_days_statuses, sender=Medical_office)
