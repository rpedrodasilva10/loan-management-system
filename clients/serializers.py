from rest_framework import serializers
from .models import Client

class ClientSerializer(serializers.ModelSerializer):
    """
    Client model serializer
    """
    class Meta:
        model = Client
        fields = (
            'client_id',
            'name',
            'surname',
            'email',
            'telephone',
            'cpf'
        )
