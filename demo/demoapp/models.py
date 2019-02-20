from django.db import models
from django.utils.translation import ugettext_lazy as _


class MyObject(models.Model):
    CHOICES = (
        ('0', _('Meters')),
        ('1', _('Milimeters')),
        ('2', _('Centimeters')),
        ('3', _('Liters')),
        ('4', _('Mililiters')),
        ('5', _('Unit'))
    )
    name = models.CharField(max_length=200)
    quantity = models.FloatField()
    measurement_unit = models.CharField(max_length=2, choices=CHOICES)

    def __str__(self):
        return self.name
