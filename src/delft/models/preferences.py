from django.db import models

from delft.models.singleton import SingletonModel


class SitePreferences(SingletonModel):
    """Preference settings specifically for website."""

    # -----------------------------------------------
    # LANDING PAGE
    # -----------------------------------------------
    landing_page_banner = models.ImageField(
        null=True, blank=True,
        upload_to='settings/images'
    )
    landing_page_banner_title = models.TextField(
        default=''
    )
    landing_page_banner_description = models.TextField(
        default=''
    )

    class Meta:  # noqa: D106
        verbose_name_plural = "site preferences"

    @staticmethod
    def preferences() -> "SitePreferences":
        """Load Site Preference."""
        return SitePreferences.load()

    def __str__(self):
        return 'Site Preference'
