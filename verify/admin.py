from Crypto.Random import get_random_bytes
from django.contrib import admin

from verify.models import ApiKey


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'key':
            field.initial = get_random_bytes(16).hex()
        return field
