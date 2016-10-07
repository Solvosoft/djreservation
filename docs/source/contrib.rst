Contrib CRUD
##############

Create a CRUD (Create, Remove, Update, Detail)  using one class.
It Work if user is loggin.

ObjectView
'''''''''''''

Create simple models, than not need set request.user

Example:

.. code:: python 

    from djreservation.contrib.CRUD import ObjectView
    class TShirt(UserObjectView):
        model = TShirtmodel  # requiered
        template_name_base = "tshirt/tshirt"  # not required but recomendable
        namespace = "tshirt"  # required
        fields = [ ... ]  # not required

    tshirts = TShirt()

set urlpatterns in urls.py 

.. code:: python 

    urlpatterns = [
        ...
     url(r'^tshirts/', include(tshirts.get_urls(), namespace="tshirts")),
    ]

UserObjectView
'''''''''''''''''

If your models have a user field and want to set automátically the user them

from djreservation.contrib.CRUD import UserObjectView

.. code:: python 

    from djreservation.contrib.CRUD import ObjectView
    class SpeakpropposeCRUD(UserObjectView):
        model = Speakproppose  # requiered
        template_name_base = "tshirt/tshirt"  # not required but recomendable
        namespace = "proppose"  # required
        fields = [ fields with out user ]  # not required

    propposes = SpeakpropposeCRUD()

set urlpatterns in urls.py 

.. code:: python 

    urlpatterns = [
        ...
     url(r'^propposes/', include(propposes.get_urls(), namespace="propposes")),
    ]

