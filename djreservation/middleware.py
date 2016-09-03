# encoding: utf-8

'''
Free as freedom will be 2/9/2016

@author: luisza
'''

from __future__ import unicode_literals
from djreservation.models import Reservation


class ReservationMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.COOKIES.get('reservation'):
            try:
                reservation = Reservation.objects.get(
                    pk=request.COOKIES.get('reservation')
                )
                setattr(request, "reservation", reservation)
            except:
                pass

        response = self.get_response(request)

        return response
