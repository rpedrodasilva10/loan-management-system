"""
Admin class for clients application.
"""

from django.contrib import admin
from .models import Client

class ClientAdmin(admin.ModelAdmin):
    """
    Helper class for admin.
    Defines which Client fields are shown in the interface.
    """
    list_display = ('client_id', 'name', 'surname', 'email', 'telephone', 'cpf')

# Register your models here.
admin.site.register(Client, ClientAdmin)
