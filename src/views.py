#-*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging

from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin

from rest_framework import status
from twilio import twiml

from .decorators import twilio_view
from .models import OutgoingSMS
from .serializers import SMSRequestSerializer, SMSStatusSerializer

logger = logging.getLogger("django-twilio-sms.views")


class TwilioView(View):
    """
    Base view for Twilio callbacks
    """

    response_text = None

    def get_data(self):
        return self.request.POST

    def post(self, request, *args, **kwargs):
        data = self.get_data()
        return self.handle_request(data)

    def handle_request(self, data):
        return self.get_response(data)

    def get_response_text(self):
        return self.response_text

    def get_response(self, message, **kwargs):
        response = twiml.Response()

        response_text = self.get_response_text()
        if response_text:
            response.sms(response_text)

        response = HttpResponse(str(response), mimetype='application/xml')
        return response


class IncomingSMSView(TwilioView):
    """
    Base view for handling incoming SMS messages.

    Override to add custom logic and configure url in the Twilio admin panel.
    """

    def handle_request(self, data):
        logger.debug("Received SMS message: %r", data)

        serializer = SMSRequestSerializer(data=data)
        if serializer.is_valid():
            self.object = serializer.save(force_insert=True)
            self.post_save(self.object)
        else:
            logger.error(
                "Failed validation of received SMS message: %s",
                serializer.errors,
                extra={"request": self.request}
            )
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        return self.get_response(message=self.object, data=data)

    def post_save(self, obj):
        pass


class SMSStatusCallbackView(SingleObjectMixin, TwilioView):
    """
    Callback view for tracking status of sent messages.

    Configure callback url in the Twilio admin panel.
    """

    model = OutgoingSMS

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(SMSStatusCallbackView, self).post(request, *args, **kwargs)

    def handle_request(self, data):
        logger.debug("Callback for sent SMS message status %s: %r", self.object.pk, data)

        serializer = SMSStatusSerializer(instance=self.object, data=data)
        if serializer.is_valid():
            self.object = serializer.save(force_update=True)
            self.post_save(self.object)
            logger.debug(
                "Updated message status %s, %s: %s",
                self.object.pk, self.object.sms_sid, self.object.status
            )
        else:
            logger.error(
                "Failed SMS status callback: %s",
                serializer.errors,
                extra={"request": self.request}
            )
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        return self.get_response(message=self.object)

    def post_save(self, obj):
        pass

sms_status_callback_view = twilio_view(SMSStatusCallbackView.as_view())
