from django.contrib import admin
from . import models


@admin.register(models.Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "enabled",
        "featured",
        "order",
        "website_url",
    )

    list_filter = ("enabled",)
