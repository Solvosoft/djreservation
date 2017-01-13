# encoding: utf-8


'''
Created on 10/12/2016

@author: luisza
'''
from __future__ import unicode_literals
from djreservation.models import Reservation


def proccess_reservation(obj, differ_obj, change_status):
    if obj.status == Reservation.BUILDING or obj.status == Reservation.REQUESTED:
        return
    if obj.status == Reservation.ACCEPTED:
        accepted_reservation(obj, differ_obj, change_status)
    elif obj.status == Reservation.DENIED:
        denied_reservation(obj, differ_obj, change_status)
    elif obj.status == Reservation.BORROWED:
        borrowed_reservation(obj, differ_obj, change_status)
    elif obj.status == Reservation.RETURNED:
        returned_reservation(obj, differ_obj, change_status)


def denied_reservation(instance, differ_obj, change_status):
    pass


def accepted_reservation(instance, differ_obj, change_status):
    pass


def borrowed_reservation(instance, differ_obj, change_status):
    not_borrowed = []
    if change_status:
        query = instance.product_set.filter(borrowed=True)
    else:
        query = instance.product_set.filter(pk__in=differ_obj, borrowed=True)
        not_borrowed = instance.product_set.filter(
            pk__in=differ_obj, borrowed=False)
    for product in query:
        ref_obj = product.content_object
        setattr(ref_obj, product.amount_field,
                getattr(ref_obj, product.amount_field) - product.amount)
        ref_obj.save()

    for product in not_borrowed:
        ref_obj = product.content_object
        setattr(ref_obj, product.amount_field,
                getattr(ref_obj, product.amount_field) + product.amount)
        ref_obj.save()


def returned_reservation(instance, differ_obj, change_status):

    if change_status:
        query = instance.product_set.filter(borrowed=True)
    else:
        query = instance.product_set.filter(pk_in=differ_obj, borrowed=True)

    for product in query:
        ref_obj = product.content_object
        setattr(ref_obj, product.amount_field, getattr(
            ref_obj, product.amount_field) + product.amount)
        ref_obj.save()
