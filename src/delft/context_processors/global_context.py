from delft.models.preferences import SitePreferences
from delft.serializer.site_preferences import SitePreferencesSerializer


def global_context(request):
    """Global context that will be returned for every request."""
    pref = SitePreferences.preferences()
    pref_data = SitePreferencesSerializer(pref).data
    return {
        'preferences': pref_data,
    }
