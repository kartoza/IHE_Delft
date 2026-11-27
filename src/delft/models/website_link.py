from django.db import models
from django.db.models import Q

PLACEMENT_CHOICES = [
    ("Footer", "Footer"),
]


class WebsiteLink(models.Model):
    """Additional website links."""

    url = models.TextField()
    title = models.CharField(max_length=56, null=True, blank=True)
    icon = models.ImageField(upload_to="delft/icon", null=True, blank=True)
    placement = models.CharField(
        max_length=10,
        choices=PLACEMENT_CHOICES,
        help_text="The placement of the website link.",
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="The order of the website link, from top to bottom or left to right.",
    )

    def __str__(self):
        return self.url

    class Meta:  # noqa: D106
        ordering = ["order"]

    @staticmethod
    def footers():
        """Footer links that have a title or an icon to display."""
        has_title = Q(title__isnull=False) & ~Q(title="")
        has_icon = Q(icon__isnull=False) & ~Q(icon="")
        return WebsiteLink.objects.filter(placement="Footer").filter(
            has_title | has_icon
        )
