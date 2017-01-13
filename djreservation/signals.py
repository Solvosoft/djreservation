# encoding: utf-8

'''
Free as freedom will be 5/10/2016

@author: luisza
'''
from __future__ import unicode_literals

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from djreservation.email import send_reservation_email
from djreservation.models import Reservation


@receiver(pre_save, sender=Reservation)
def update_product_related(sender, **kwargs):
    instance = kwargs['instance']
    if instance.pk is None:
        return
    status = sender.objects.filter(
        pk=instance.pk).values('status')[0]['status']
    if instance.status == status:
        return

    send_reservation_email(instance, instance.user)