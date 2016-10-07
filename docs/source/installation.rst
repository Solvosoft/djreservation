Installation
###############


Install with pip 

.. code:: bash

	$ pip install django-reservation

In settings.py 
''''''''''''''''''

Set "djreservation" in your INSTALLED_APPS.

.. code:: python

	INSTALLED_APPS = [
			...
		'djreservation'
	]

Set 'djreservation.middleware.ReservationMiddleware' in MIDDLEWARE

.. code:: python

	MIDDLEWARE = [
			...
		'djreservation.middleware.ReservationMiddleware'
	]

.. note:: Middleware is not necesary if you just use `SimpleProductReservation`


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

In urls.py
'''''''''''

Append django reservation to  urlpatterns 

.. code:: python 

	from djreservation import urls as djreservation_urls

	urlpatterns = [
		...
		
	] + djreservation_urls.urlpatterns

