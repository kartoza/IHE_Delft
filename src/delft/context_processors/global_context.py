from delft.models.preferences import SitePreferences
from delft.serializer.site_preferences import SitePreferencesSerializer
from delft.serializer.website_link import WebsiteLinkSerializer
from delft.models.website_link import WebsiteLink


def global_context(request):
    """Global context that will be returned for every request."""
    pref = SitePreferences.preferences()
    pref_data = SitePreferencesSerializer(pref).data
    return {
        "preferences": pref_data,
        "links": {
            "footer": WebsiteLinkSerializer(WebsiteLink.footers(), many=True).data
        },
    }
