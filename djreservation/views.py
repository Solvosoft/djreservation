from django.shortcuts import render, get_object_or_404,\
    redirect
from django.views.generic.edit import CreateView
from .models import Product, Reservation
from .forms import ProductForm, ReservationForm
from django.http.response import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from .email import send_reservation_email
from django.views.generic.list import ListView
# Create your views here.


class ReservationList(ListView):
    model = Reservation
    paginate_by = 10

    def get_queryset(self):
        queryset = ListView.get_queryset(self)
        queryset = queryset.filter(user=self.request.user).exclude(
            status=Reservation.BUILDING).order_by('status')
        return queryset


class CreateReservation(CreateView):
    model = Reservation
    form_class = ReservationForm
    success_url = "/"

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
        send_reservation_email(self.object, self.request.user)
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
    return response


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
            content_object=self.instance
        )
        self.object.save()
        return self.get_success_view()

    def get_form_kwargs(self):
        kwargs = CreateView.get_form_kwargs(self)
        kwargs['initial']['model_instance'] = str(self.instance.pk)
        return kwargs

    def get(self, request, *args, **kwargs):
        if "modelpk" in kwargs:
            print(kwargs)
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
    return redirect(reverse("finish_reservation"))
