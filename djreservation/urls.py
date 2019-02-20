'''
Created on 1/8/2016

@author: luisza
'''
from __future__ import unicode_literals
try:
    from django.conf.urls import url
except:
    from django.urls import re_path as url
from . import views
from .settings import TOKENIZE

urlpatterns = [
    url(r"^reservation/create$",
        views.CreateReservation.as_view(), name="add_user_reservation"),
    url(r"^reservation/finish$",
        views.finish_reservation, name="finish_reservation"),
    url(r"^reservation/delete_product_reservation/(?P<pk>\d+)$",
        views.deleteProduct, name="delete_product_reservation"),
    url(r"reservation/list", views.ReservationList.as_view(),
        name="reservation_list"),
]

if TOKENIZE:
    urlpatterns += [
        url(r"reservation/token/(?P<pk>\d+)/(?P<token>[0-9a-f-]+)/(?P<status>\d)$",
            views.update_reservation_by_token,
            name="reservation_token")
    ]
