from delft.models.singleton import SingletonModel
from django.db import models
from mdeditor.fields import MDTextField


class SitePreferences(SingletonModel):
    """Preference settings specifically for website."""

    google_analytics_measurement_id = models.CharField(
        default='', max_length=256,
        help_text='Google analytics measurement id'
    )
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
    # -----------------------------------------------
    # ABOUT PAGE
    # -----------------------------------------------
    about_page_title = models.TextField(
        default=''
    )
    about_page_content = MDTextField(default='')

    class Meta:  # noqa: D106
        verbose_name_plural = "site preferences"

    @staticmethod
    def preferences() -> "SitePreferences":
        """Load Site Preference."""
        return SitePreferences.load()

    def __str__(self):
        return 'Site Preference'
