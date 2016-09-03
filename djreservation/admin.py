from django.contrib import admin
from .models import Reservation, Observation, Product
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string


# Register your models here.


class ObservationInline(admin.StackedInline):
    model = Observation
    #fields = '__all__'
    extra = 0


class ReservationAdmin(admin.ModelAdmin):
    readonly_fields = ["user", "updated_datetime",
                       "list_of_products"]

    list_display = ['user', 'status', "reserved_start_date", "return_date"]
    list_filter = ['status']
    search_fields = ['user__firstname', "user__lastname"]
    inlines = [ObservationInline]
    fieldsets = (
        (None, {
            'fields': (
                ("user", "status", "updated_datetime"),
                ("reserved_start_date", "return_date"),
                ("list_of_products")
            )
        }),
    )

    def list_of_products(self, instance):

        return mark_safe(render_to_string(
            'djreservation/product_admin_reservation.html',
            {"instance": instance}
        ))

    list_of_products.short_description = "list of products"

    def save_model(self, request, obj, form, change):
        dev = admin.ModelAdmin.save_model(self, request, obj, form, change)
        if 'djreservation_product_list' in request.POST:
            product_pks = request.POST.getlist("djreservation_product_list")
            obj.product_set.all().exclude(
                pk__in=product_pks).update(borrowed=False)

            obj.product_set.all().filter(
                pk__in=product_pks).update(borrowed=True)
        return dev

admin.site.register(Reservation, ReservationAdmin)
