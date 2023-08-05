from django.db import models
import hashlib
import uuid
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

def get_hash(token):
    m = hashlib.sha512()
    m.update(token.encode('utf-8'))
    return m.hexdigest()[:72]

class Address(models.Model):
    id = models.UUIDField(
        verbose_name=_("ID"),
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
        unique=True,
    )

    email = models.EmailField(
        verbose_name=_("Adresse électronique")
    )

    confirmed = models.BooleanField(
        verbose_name=_("Confirmé"),
        default=False,
        editable=True,
    )

    created_at = models.DateTimeField(
        verbose_name=_("Date d'inscription"),
        auto_now_add=True,
    )

    @property
    def confirm_token(self):
        return get_hash(
            self.email +
            '_subscribe_' +
            settings.EVENTSD_NEWSLETTER_CONFIRM_SALT
        )
    
    @property
    def unsubscribe_token(self):
        return get_hash(
            self.email +
            '_unsubscribe_' +
            settings.EVENTSD_NEWSLETTER_CONFIRM_SALT
        )

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = _("addresse")
        verbose_name_plural = _("adresses")