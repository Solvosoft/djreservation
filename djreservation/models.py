from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import ugettext_lazy as _
# Create your models here.

auth_user = settings.AUTH_USER_MODEL if getattr(
    settings, "AUTH_USER_MODEL") else User


class Reservation(models.Model):
    BUILDING = 0
    REQUESTED = 1
    STATUS = (
        (0, _("building")),
        (1, _("Requested")),
        (2, _("Acepted")),
        (3, _("Denied")),
        (4, _("Borrowed")),
        (5, _("Returned")),
    )
    user = models.ForeignKey(auth_user)
    reserved_start_date = models.DateTimeField(default=timezone.now)
    return_date = models.DateTimeField()
    status = models.SmallIntegerField(choices=STATUS, default=BUILDING)
    updated_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s  %s  (%s to %s)" % (self.user.get_full_name(),
                                       self.get_status_display(),
                                       self.reserved_start_date.strftime(
            "%Y/%m/%d %H:%S"),
            self.return_date.strftime(
            "%Y/%m/%d %H:%S"),
        )


class Product(models.Model):

    reservation = models.ForeignKey(Reservation)
    amount = models.FloatField()
    amount_field = models.CharField(max_length=150)
    borrowed = models.BooleanField(default=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    @property
    def available_amount(self):
        return getattr(self.content_object, self.amount_field)

    @property
    def amount_without_this_product(self):
        amount_now = self.available_amount
        return amount_now - self.amount

    def __str__(self):
        return "%.2f ) %s" % (self.amount, self.content_object)


class Observation(models.Model):
    reservation = models.ForeignKey(Reservation)
    text = models.TextField()
