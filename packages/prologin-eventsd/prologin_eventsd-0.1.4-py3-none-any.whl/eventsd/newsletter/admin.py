from django.contrib import admin
from . import models

@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('email', 'confirmed', 'created_at')
    list_filter = ('confirmed', )
    search_fields = ('email',)
    readonly_fields = ("confirm_token", "unsubscribe_token")