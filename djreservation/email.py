# encoding: utf-8

'''
Free as freedom will be 3/9/2016

@author: luisza
'''

from __future__ import unicode_literals
from .models import Reservation
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.conf import settings

BUILDING = Reservation.BUILDING
REQUESTED = Reservation.REQUESTED
ACCEPTED = Reservation.ACCEPTED
DENIED = Reservation.DENIED
BORROWED = Reservation.BORROWED
RETURNED = Reservation.RETURNED


def send_html_email(subject, template, context=None):
    if context is None:
        context = {}
    reservation = context['reservation']
    message = render_to_string(template,
                               context)
    send_mail(
        subject=subject,
        message=_('Please, use an email with html support'),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[reservation.user.email],
        fail_silently=True,
        html_message=message
    )


def email_requested(reservation, user):
    send_html_email(
        _('Reservation requested: reserv-%d') % (reservation.pk),
        'djreservation/mail/requested.txt',
        context={
            'reservation': reservation,
            'user': user
        })


def email_accepted(reservation, user):
    send_html_email(
        subject=_('Reservation accepted: reserv-%d') % (reservation.pk),
        template='djreservation/mail/accepted.txt',
        context={
            'reservation': reservation,
            'user': user
        })


def email_denied(reservation, user):
    send_html_email(
        _('Reservation denied: reserv-%d') % (reservation.pk),
        'djreservation/mail/denied.txt',
        context={
            'reservation': reservation,
            'user': user
        })


def email_borrowed(reservation, user):
    send_html_email(
        _('Reservation borrowed: reserv-%d') % (reservation.pk),
        'djreservation/mail/borrowed.txt',
        context={
            'reservation': reservation,
            'user': user
        })


def email_returned(reservation, user):
    send_html_email(
        _('Reservation returned: reserv-%d') % (reservation.pk),
        'djreservation/mail/returned.txt',
        context={
            'reservation': reservation,
            'user': user
        })


def email_building(reservation, user):
    pass


email_functions = {
    BUILDING: email_building,
    REQUESTED: email_requested,
    ACCEPTED: email_accepted,
    DENIED: email_denied,
    BORROWED: email_borrowed,
    RETURNED: email_returned
}


def send_reservation_email(reservation, user):
    email_functions[reservation.status](reservation, user)
