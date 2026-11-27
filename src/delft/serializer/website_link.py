from rest_framework import serializers

from delft.models.website_link import WebsiteLink


class WebsiteLinkSerializer(serializers.ModelSerializer):
    """Website link serializer."""

    class Meta:  # noqa: D106
        model = WebsiteLink
        exclude = ()
