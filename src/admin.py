# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin

from .models import IncomingSMS, OutgoingSMS


class IncomingSMSAdmin(admin.ModelAdmin):
    list_display = [
        "sms_sid", "account_sid",
        "from_number", "from_city", "from_state", "from_zip", "from_country",
        "to_number", "body",
        "created_at"
    ]
    list_filter = ["to_number", "from_country", "from_state", "from_city", ]
    search_fields = ["from_number", "body"]


class OutgoingSMSAdmin(admin.ModelAdmin):
    list_display = [
        "id", "sms_sid", "account_sid",
        "from_number", "to_number", "to_parsed",
        "body",
        "created_at", "sent_at", "delivered_at", "status",
        "price", "price_unit"
    ]
    list_filter = ["from_number", "status"]
    search_fields = ["to_number", "body"]

admin.site.register(IncomingSMS, IncomingSMSAdmin)
admin.site.register(OutgoingSMS, OutgoingSMSAdmin)
