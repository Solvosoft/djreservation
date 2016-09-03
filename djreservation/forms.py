# encoding: utf-8

'''
Free as freedom will be 2/9/2016

@author: luisza
'''

from __future__ import unicode_literals
from django import forms
from .models import Product, Reservation


class ReservationForm(forms.ModelForm):

    def clean(self):
        if hasattr(self.request, "reservation"):
            raise forms.ValidationError(
                "You can not create reservation with active reservation")

    class Meta:
        model = Reservation
        fields = '__all__'
        exclude = ['user', 'status']


class ProductForm(forms.ModelForm):
    model_instance = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = Product
        fields = ['amount']
