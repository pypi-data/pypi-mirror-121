from django.db import models
from django.utils.translation import ugettext_lazy as _


class Sponsor(models.Model):
    name = models.CharField(
        verbose_name=_("Nom"),
        max_length=256,
    )

    description = models.TextField(
        verbose_name=_("Description"),
        max_length=2_000,
        blank=True,
        null=True,
    )

    website_url = models.URLField(
        verbose_name=_("URL du site"),
        blank=True,
        null=True,
    )

    featured = models.BooleanField(
        verbose_name=_("Mis en avant"),
        default=False,
        editable=True,
    )

    logo = models.FileField(
        verbose_name=_("Logo"),
    )

    enabled = models.BooleanField(
        verbose_name=_("Activé"),
    )

    order = models.PositiveIntegerField(
        verbose_name=_("Ordre"),
        default=1,
    )

    class Meta:
        ordering = ("order",)

    def __str__(self):
        return self.name
