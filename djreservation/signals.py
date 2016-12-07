# encoding: utf-8

'''
Free as freedom will be 5/10/2016

@author: luisza
'''

from __future__ import unicode_literals

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from djreservation.models import Reservation
from djreservation.email import send_reservation_email

"""
@receiver(post_save, sender=Reservation)
def update_product_related(sender, **kwargs):
    instance = kwargs['instance']
    if kwargs['created']:
        print("TERMINAR AQUI")
    print(kwargs)

"""


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

    # ACCEPTED reservation status
    if instance.status == str(sender.ACCEPTED):
        for product in instance.product_set.filter(borrowed=True):
            ref_obj = product.content_object
            setattr(ref_obj, product.amount_field,
                    getattr(ref_obj, product.amount_field) - product.amount)
            ref_obj.save()

    # RETURNED reservation status
    elif instance.status == str(sender.RETURNED):
        for product in instance.product_set.filter():
            ref_obj = product.content_object
            setattr(ref_obj, product.amount_field, getattr(ref_obj, product.amount_field) + product.amount)
            ref_obj.save()