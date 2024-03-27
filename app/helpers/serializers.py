"""
Project helper serializers.
"""

import pytz
from django.conf import settings
from rest_framework import serializers


class DateTimeWithTimeZone(serializers.DateTimeField):

    def to_representation(self, instance):
        """Convert datetime to string representation with timezone."""
        if not instance:
            return None

        format = getattr(self, "format", settings.DATETIME_FORMAT)
        local_timezone = pytz.timezone(settings.TIME_ZONE)

        return instance.astimezone(local_timezone).strftime(format)
