Django reservation system
=============================

* Customizable reservations (you can provide your own reservation model)

  .. image:: https://github.com/luisza/djreservation/blob/master/demo/img/ReserveObject.png?raw=true

* Generic reservation create view and reserve product view

  .. image:: https://github.com/luisza/djreservation/blob/master/demo/img/creating_reservation.png?raw=true

* Reservation list filter by user

  .. image:: https://github.com/luisza/djreservation/blob/master/demo/img/userreservationlist.png?raw=true

* Email notifications with template system
* Django Admin backend for administrative proposuse like Accept, Borrow, Denied reservations
* Parcial reservations in admin (Not all products can be borrowed)

  .. image:: https://github.com/luisza/djreservation/blob/master/demo/img/ReservationAdmin.png?raw=true

* UI based on Twitter Bootstrap
* Using i18n to handle translations

Documentation
-----------------

See in readthedocs.io_

.. _readthedocs.io: http://djreservation.readthedocs.io/en/latest/

Installation
--------------------

Install with pip 

.. code:: bash

	$ pip install django-reservation

In settings.py 
''''''''''''''''''

Set "djreservation" in your INSTALLED_APPS.

Set 'djreservation.middleware.ReservationMiddleware' in MIDDLEWARE

.. code:: python

	MIDDLEWARE = [
			...
		'djreservation.middleware.ReservationMiddleware'
	]

Configure your email settings

.. code:: python

	DEFAULT_FROM_EMAIL = "mail@example.com"
	EMAIL_HOST = "localhost"
	EMAIL_PORT = "1025"



Configure database
''''''''''''''''''''''

Run migrations 

.. code:: bash

	python manage.py migrate

In your code
''''''''''''''''''

Where you want, create a view for reserve a product 

.. code:: python 

	from djreservation.views import ProductReservationView

	class MyObjectReservation(ProductReservationView):
		base_model = MyObject     # required
		amount_field = 'quantity' # required
		extra_display_field = ['measurement_unit'] # not required

In urls.py
'''''''''''

Append django reservation to  urlpatterns 

.. code:: python 

	from djreservation import urls as djreservation_urls

	urlpatterns = [
		...
		url(r"^reservation/create/(?P<modelpk>\d+)$", MyObjectReservation.as_view())
	]
	urlpatterns += djreservation_urls.urlpatterns





