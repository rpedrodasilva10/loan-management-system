from django.contrib import admin
from .models import Client

class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_id', 'name', 'surname', 'email', 'telephone', 'cpf')

# Register your models here.
admin.site.register(Client, ClientAdmin)
