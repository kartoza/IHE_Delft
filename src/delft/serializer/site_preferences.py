from rest_framework import serializers

from delft.models.preferences import SitePreferences


class SitePreferencesSerializer(serializers.ModelSerializer):
    """Site preference serializer."""

    class Meta:  # noqa: D106
        model = SitePreferences
        exclude = ()
