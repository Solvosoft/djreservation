# encoding: utf-8

'''
Free as freedom will be 2/9/2016

@author: luisza
'''

from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Product, Reservation


class ReservationForm(forms.ModelForm):

    def clean(self):
        if hasattr(self, 'request'):
            if hasattr(self.request, "reservation"):
                raise forms.ValidationError(
                    _("You can not create reservation with active reservation"))
            cleaned_data = super(ReservationForm, self).clean()

    class Meta:
        model = Reservation
        fields = '__all__'
        exclude = ['user', 'status']


class ProductForm(forms.ModelForm):
    model_instance = forms.CharField(widget=forms.HiddenInput)
    available_amount = forms.FloatField(widget=forms.HiddenInput)

    def clean(self):
        cleaned_data = super(ProductForm, self).clean()

        if cleaned_data['amount'] <= 0:
            raise forms.ValidationError(
                _("You amount correct, requested 0 or negative value"))

        if cleaned_data['amount'] > cleaned_data['available_amount']:
            raise forms.ValidationError(
                _("You requested more than product available"))

    class Meta:
        model = Product
        fields = ['amount']
