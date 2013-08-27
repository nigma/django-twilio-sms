#-*- coding: utf-8 -*-

from __future__ import unicode_literals

from decimal import Decimal
import logging

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.encoding import force_text

from twilio.rest import TwilioRestClient

from .models import OutgoingSMS

logger = logging.getLogger("django-twilio-sms.utils")


def build_callback_url(request, urlname, message):
    """
    Build Twilio callback url for confirming message delivery status

    :type message: OutgoingSMS
    """
    location = reverse(urlname, kwargs={"pk": message.pk})

    callback_domain = getattr(settings, "TWILIO_CALLBACK_DOMAIN", None)
    if callback_domain:
        url = "{}://{}{}".format(
            "https" if getattr(settings, "TWILIO_CALLBACK_USE_HTTPS", False) else "http",
            callback_domain,
            location
        )

    elif request is not None:
        url = request.build_absolute_uri(location)
    else:
        raise ValueError(
            "Unable to build callback url. Configure TWILIO_CALLBACK_DOMAIN "
            "or pass request object to function call"
        )
    return url


def send_sms(request, to_number, body, callback_urlname="sms_status_callback"):
    """
    Create :class:`OutgoingSMS` object and send SMS using Twilio.
    """
    client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    from_number = settings.TWILIO_PHONE_NUMBER

    message = OutgoingSMS.objects.create(
        from_number=from_number,
        to_number=to_number,
        body=body,
    )

    status_callback = None
    if callback_urlname:
        status_callback = build_callback_url(request, callback_urlname, message)

    logger.debug("Sending SMS message to %s with callback url %s: %s.",
                 to_number, status_callback, body)

    if not getattr(settings, "TWILIO_DRY_MODE", False):
        sent = client.sms.messages.create(
            to=to_number,
            from_=from_number,
            body=body,
            status_callback=status_callback
        )
        logger.debug("SMS message sent: %s", sent.__dict__)

        message.sms_sid = sent.sid
        message.account_sid = sent.account_sid
        message.status = sent.status
        message.to_parsed = sent.to
        if sent.price:
            message.price = Decimal(force_text(sent.price))
            message.price_unit = sent.price_unit
        message.sent_at = sent.date_created
        message.save(update_fields=[
            "sms_sid", "account_sid", "status", "to_parsed",
            "price", "price_unit", "sent_at"
        ])
    else:
        logger.info("SMS: from %s to %s: %s", from_number, to_number, body)
    return message
