'''
Created on 1/8/2016

@author: luisza
'''

from django.urls import path, re_path
from . import views
from .settings import TOKENIZE

urlpatterns = [
    path("reservation/create", views.CreateReservation.as_view(), name="add_user_reservation"),
    path("reservation/finish", views.finish_reservation, name="finish_reservation"),
    path("reservation/delete_product_reservation/<int:pk>/", views.deleteProduct, name="delete_product_reservation"),
    path("reservation/list", views.ReservationList.as_view(), name="reservation_list"),
]

if TOKENIZE:
    urlpatterns += [
        re_path(r"reservation/token/(?P<pk>\d+)/(?P<token>[0-9a-f-]+)/(?P<status>\d)$",
            views.update_reservation_by_token,
            name="reservation_token")
    ]
