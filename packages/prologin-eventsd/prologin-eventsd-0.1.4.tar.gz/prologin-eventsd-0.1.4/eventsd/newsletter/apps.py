from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class NewsletterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = "eventsd.newsletter"
    label = "eventsd_newsletter"
    verbose_name = _("Newsletter")
