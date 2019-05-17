"""
Serializers for clients application.
"""

import re
from rest_framework import serializers
from pycpfcnpj import cpfcnpj
from .models import Client

class ClientSerializer(serializers.ModelSerializer):
    """
    Client model serializer.
    """

    def validate(self, attrs):
        cpf = attrs['cpf']
        if not cpfcnpj.validate(cpf):
            raise serializers.ValidationError(
                {'cpf': 'Invalid CPF number.'}
            )

        telephone = attrs['telephone']
        pattern_telephone = re.compile(r'^\d{10,11}$')
        # Checks if a given phone is valid acording to format:
        # 11 1234 5678 or 11 9 1234 5678
        # without spaces or signs.
        if not bool((re.fullmatch(pattern_telephone, telephone))):
            raise serializers.ValidationError(
                {'telephone': 'Invalid telephone number.'}
            )

        return attrs

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
