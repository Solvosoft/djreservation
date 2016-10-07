Settings configuration
###########################

.. note: DJRESERVATION_START_RESERVATION_DATETIME and START_RESERVATION_DATETIME settings only work with SimpleProductReservation

* **DJRESERVATION_TOKENIZE**: Reservation can be updated by non-registered user using a token send by mail.  Token only work one time.   default False

* **DJRESERVATION_START_RESERVATION_DATETIME**: initialize start reservation datetime widget with this date. default format '%d/%m/%Y %H:%M'
* **DJRESERVATION_END_RESERVATION_DATETIME**: initialize end reservation datetime widget with this date. default format '%d/%m/%Y %H:%M'
