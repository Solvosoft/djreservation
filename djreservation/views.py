from django.shortcuts import render, get_object_or_404,\
    redirect
from django.views.generic.edit import CreateView
from .models import Product, Reservation, ReservationToken
from .forms import ProductForm, ReservationForm
from django.http.response import HttpResponseRedirect, Http404
try:
    from django.core.urlresolvers import reverse
except:
    from django.urls import reverse

from django.utils.translation import ugettext_lazy as _
from .email import send_reservation_email
from django.views.generic.list import ListView

from django.contrib import messages

# Create your views here.

from .settings import (END_RESERVATION_DATETIME,
                       START_RESERVATION_DATETIME,
                       TOKENIZE)


def get_base_url(request):
    protocol = request.is_secure() and 'https://' or 'http://'
    domain = request.META['HTTP_HOST']
    return protocol + domain


class ReservationList(ListView):
    model = Reservation
    paginate_by = 10

    def get_queryset(self):
        queryset = ListView.get_queryset(self)
        queryset = queryset.filter(user=self.request.user).exclude(
            status=Reservation.BUILDING).order_by('-updated_datetime', 'status')
        return queryset


class CreateReservation(CreateView):
    model = Reservation
    form_class = ReservationForm
    success_url = "/"

    def get_success_url(self):
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        return super(CreateReservation, self).get_success_url()

    def get_success_view(self):
        response = HttpResponseRedirect(self.get_success_url())
        response.set_cookie("reservation", str(self.object.pk))
        return response

    def get_form_class(self):
        form = CreateView.get_form_class(self)

        form.request = self.request
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        if TOKENIZE:
            ReservationToken.objects.create(
                reservation=self.object,
                base_url=get_base_url(self.request))
        send_reservation_email(self.object, self.request.user)

        messages.success(self.request, _('Reservation created'))

        return self.get_success_view()


def finish_reservation(request):
    if not hasattr(request, 'reservation'):
        raise Http404(_("No reservation object started"))

    if request.method == "GET":
        response = render(
            request,
            'djreservation/reservation_confirm.html',
            {"reservation": request.reservation})
    elif request.method == "POST":
        reservation = request.reservation
        reservation.status = reservation.REQUESTED
        reservation.save()
        request.reservation = None
        send_reservation_email(reservation, request.user)
        response = render(
            request, 'djreservation/reservation_finished.html')
        response.set_cookie("reservation", "0")
        messages.success(request, _('Reservation finised'))
    return response


class SimpleProductReservation(CreateView):
    model = Reservation
    form_class = ReservationForm
    success_url = "/"
    base_model = None
    amount_field = None
    max_amount_field = None
    extra_display_field = None
    template_name = 'djreservation/simple_reservation.html'
    product_form_class = ProductForm
    product_form = None

    def get_product_form(self, instance, post_context=False):
        self.product_form.initial['model_instance'] = self.pk

        if not post_context:
            self.product_form.initial['amount'] = 1
        if self.max_amount_field and hasattr(instance, self.max_amount_field):
            self.product_form.initial['available_amount'] = getattr(
                instance, self.max_amount_field)
            if post_context:
                self.product_form.fields['available_amount'].value = getattr(
                    instance, self.max_amount_field)
        return self.product_form

    def get_context_data(self, **kwargs):
        context = CreateView.get_context_data(self, **kwargs)
        instance = get_object_or_404(self.base_model, pk=self.pk)
        context['object'] = instance

        context['product_form'] = self.get_product_form(instance)
        return context

    def get_form_kwargs(self):
        kwargs = CreateView.get_form_kwargs(self)
        if END_RESERVATION_DATETIME:
            kwargs['initial']['reserved_end_date'] = END_RESERVATION_DATETIME
        if START_RESERVATION_DATETIME:
            kwargs['initial'][
                'reserved_start_date'] = START_RESERVATION_DATETIME
        return kwargs

    def form_valid(self, form):
        if not self.product_form.is_valid():
            return self.form_invalid(form)

        reservation = form.save(commit=False)
        reservation.user = self.request.user
        reservation.status = Reservation.REQUESTED
        reservation.save()
        self.object = Product(
            amount=self.product_form.cleaned_data['amount'],
            amount_field=self.amount_field,
            reservation=reservation,
            content_object=self.base_instance
        )
        self.object.save()

        if TOKENIZE:
            ReservationToken.objects.create(
                reservation=reservation,
                base_url=get_base_url(self.request)
            )

        send_reservation_email(reservation, self.request.user)
        messages.success(self.request, _('Reservation created successful'))
        return self.get_success_view()

    def get(self, request, *args, **kwargs):

        self.pk = kwargs.pop('pk')
        self.product_form = self.product_form_class()
        return super(SimpleProductReservation, self).get(
            request, *args, **kwargs
        )

    def post(self, request, *args, **kwargs):
        self.pk = kwargs.pop('pk')
        self.product_form = self.product_form_class(request.POST)
        self.base_instance = get_object_or_404(self.base_model, pk=self.pk)
        self.get_product_form(self.base_instance, post_context=True)
        self.product_form.is_valid()
        return CreateView.post(self, request, *args, **kwargs)

    def get_success_view(self):
        return HttpResponseRedirect(self.get_success_url())


class ProductReservationView(CreateView):
    model = Product
    base_model = None
    amount_field = None
    extra_display_field = None
    form_class = ProductForm
    success_url = "/"

    def get_success_view(self):
        return HttpResponseRedirect(self.get_success_url())

    def get_available_amount(self):
        return getattr(self.instance, self.amount_field)

    def get_extra_fields(self):
        extra_fields = []
        for field in self.extra_display_field:
            if hasattr(self.instance, "get_%s_display" % field):
                value = getattr(self.instance, "get_%s_display" % field)()
            else:
                value = getattr(self.instance, field)
            extra_fields.append({
                'label': self.instance._meta.get_field(
                    field).verbose_name,
                'value': value
            })
        return extra_fields

    def get_context_data(self, **kwargs):
        context = CreateView.get_context_data(self, **kwargs)

        context['extra_fields'] = self.get_extra_fields()
        context["instance"] = self.instance
        context["available_amount"] = self.get_available_amount()
        return context

    def form_valid(self, form):
        self.object = Product(
            amount=form.cleaned_data['amount'],
            amount_field=self.amount_field,
            reservation=self.request.reservation,
            content_object=self.instance,

        )
        self.object.save()
        messages.success(self.request, _('Product added successful'))
        return self.get_success_view()

    def get_form_kwargs(self):
        kwargs = CreateView.get_form_kwargs(self)
        kwargs['initial']['model_instance'] = str(self.instance.pk)
        kwargs['initial']["available_amount"] = self.get_available_amount()
        return kwargs

    def get(self, request, *args, **kwargs):
        if "modelpk" in kwargs:
            model_pk = kwargs.pop("modelpk")
            self.instance = self.base_model.objects.get(pk=model_pk)
        return CreateView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if "modelpk" in kwargs:
            model_pk = kwargs.pop("modelpk")
            self.instance = self.base_model.objects.get(pk=model_pk)
        elif "model_instance" in request.POST:
            self.instance = self.base_model.objects.get(
                pk=request.POST.get("model_instance"))

        return CreateView.post(self, request, *args, **kwargs)


def deleteProduct(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, _('Product deleted successful'))
    return redirect(reverse("finish_reservation"))


def update_reservation_by_token(request, pk, token, status):
    token_reservation = get_object_or_404(ReservationToken, reservation=pk,
                                          token=token)
    status_available = list(dict(Reservation.STATUS).keys())
    if int(status) not in status_available:
        raise Http404()

    reservation = token_reservation.reservation

    if int(status) == Reservation.ACCEPTED:
        reservation.product_set.all().update(borrowed=True)
    reservation.status = status
    reservation.save()
    token_reservation.delete()
    messages.success(request, _('Reservation updated successful'))
    return redirect("/")
