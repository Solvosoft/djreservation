# encoding: utf-8

'''
Free as freedom will be 5/10/2016

@author: luisza
'''

from __future__ import unicode_literals
from django.conf import settings
from django.utils import timezone
from datetime import datetime

TOKENIZE = getattr(settings, 'DJRESERVATION_TOKENIZE', False)

START_RESERVATION_DATETIME = getattr(
    settings, 'DJRESERVATION_START_RESERVATION_DATETIME', None)

END_RESERVATION_DATETIME = getattr(
    settings, 'DJRESERVATION_END_RESERVATION_DATETIME', None)

if START_RESERVATION_DATETIME:
    START_RESERVATION_DATETIME = datetime.strptime(
        START_RESERVATION_DATETIME, '%d/%m/%Y %H:%M')

if END_RESERVATION_DATETIME:
    END_RESERVATION_DATETIME = datetime.strptime(
        END_RESERVATION_DATETIME, '%d/%m/%Y %H:%M')
