'''
Created on 1/8/2016

@author: nashyra
'''
from __future__ import unicode_literals
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^reservation/create$",
        views.CreateReservation.as_view(), name="add_user_reservation"),
    url(r"^reservation/finish$",
        views.finish_reservation, name="finish_reservation"),
    url(r"^reservation/delete_product_reservation/(?P<pk>\d+)$",
        views.deleteProduct, name="delete_product_reservation")
]
