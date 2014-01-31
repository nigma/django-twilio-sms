django-twilio-sms
=================

Twilio integration for SMS-based Django apps

.. image:: https://pypip.in/v/django-twilio-sms/badge.png
    :target: https://pypi.python.org/pypi/django-twilio-sms/
    :alt: Latest Version

.. image:: https://pypip.in/d/django-twilio-sms/badge.png
    :target: https://pypi.python.org/pypi/django-twilio-sms/
    :alt: Downloads

.. image:: https://pypip.in/license/django-twilio-sms/badge.png
    :target: https://pypi.python.org/pypi/django-twilio-sms/
    :alt: License

Developed and used at `en.ig.ma software shop <http://en.ig.ma>`_.


Quickstart
----------

1. Include ``django-twilio-sms`` in your ``requirements.txt`` file.

2. Add ``django_twilio_sms`` to ``INSTALLED_APPS`` and syncdb/migrate.

3. Add the following url to your urlconf:
   
   .. code-block:: python

       url(r"^messaging/", include("django_twilio_sms.urls")),

   this will receive confirmation callbacks for any SMS message
   that you send using ``utils.send_sms``.

4. Create a new view and override ``IncomingSMSView.post_save(self, obj)`` method
   to receive SMS messages via callbacks from Twilio. The received ``obj``
   param will be an instance of ``IncomingSMS`` model.

5. Configure Twilio callback to send notifications to the above view's url.

6. Configure settings:

   - TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER - copy
     credentials from the Twilio panel.

   - TWILIO_CALLBACK_USE_HTTPS - use https or not for delivery confirmation
     callback urls.
   
   - TWILIO_CALLBACK_DOMAIN - optionally set domain name or IP of your site
     (otherwise the server name will be extracted from the request info).
   
   - TWILIO_DRY_MODE - set if you want to run in test mode.


License
-------

``django-twilio-sms`` is released under the MIT license.

Other Resources
---------------

- GitHub repository - https://github.com/nigma/django-twilio-sms
- PyPi Package site - http://pypi.python.org/pypi/django-twilio-sms


Commercial Support
------------------

This app and many other help us build better software
and focus on delivering quality projects faster.
We would love to help you with your next project so get in touch
by dropping an email at en@ig.ma.
