Basic usage
##############

djreservation have two different approachs: 
   * **ProductReservationView:** You have a  shop cart for a reservation in determinate period of time.
   * **SimpleProductReservation:** You reserve one product in determinate period of time.

Both views inherit from CreateView_. so all verifications and functions are included and of course you can overwrite.

.. _CreateView: https://docs.djangoproject.com/en/1.10/ref/class-based-views/generic-editing/#createview

The main diferent is the way how the user make a reservation

ProductReservationView:
''''''''''''''''''''''''

In this approach exist a button that start the reservation process, suppose your are the user, when start you need to set the period of time you want the reservation, then you reserve all products you want and as final step you finish the reservation and an email is send you.

How to implement that behaviour:

Create a view for reserve a product 

.. code:: python 

	from djreservation.views import ProductReservationView

	class MyObjectReservation(ProductReservationView):
		base_model = MyObject     # required
		amount_field = 'quantity' # required
		extra_display_field = ['measurement_unit'] # not required

Set the urlpatterns in your urls.py 

.. code:: python 

	urlpatterns = [
		...
		url(r"^reservation/create$", MyObjectReservation.as_view())
	]


SimpleProductReservation:
''''''''''''''''''''''''''''
In this approach you can reserve a product for a period of time, like a room in a hotel. 

.. code:: python 

    from djreservation.views import SimpleProductReservation
    from .models import MyModel


    class RoomReservation(SimpleProductReservation):
        base_model = MyModel     # required
        amount_field = 'quantity'  # required
        max_amount_field = 'max_amount' # required
        extra_display_field = []  # not required

Set the urlpatterns in your urls.py 

.. code:: python 

	urlpatterns = [
		...
		url(r"^reservationroom/create$", RoomReservation.as_view())
	]


Templates 
''''''''''''

djreservation require a template 'base.html' with the follow blocks

.. code:: html

    {% block css%} {%endblock%}

    {% block content %}
    {%endblock%}

    {% block js %}
    {%endblock%}

you can overwrite wathever template you want base in `app templates`_

.. _app templates: https://github.com/luisza/djreservation/blob/master/djreservation/templates/
