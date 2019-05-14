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
        pattern_cpf = re.compile(r'^([\d]+)$')
        # Checks if a given CPF has only numbers.
        if not bool((re.fullmatch(pattern_cpf, cpf))):
            raise serializers.ValidationError(
                {'cpf': ['Only numbers are allowed in a CPF.']}
            )
        if not cpfcnpj.validate(cpf):
            raise serializers.ValidationError(
                {'cpf': ['Invalid CPF number.']}
            )

        telephone = attrs['telephone']
        pattern_telephone = re.compile(r'^([\d]+){10,11}$')
        # Checks if a given phone is valid acording to format:
        # 11 1234 5678 or 11 9 1234 5678
        # without spaces or signs.
        if not bool((re.fullmatch(pattern_telephone, telephone))):
            raise serializers.ValidationError(
                {'telephone': ['Invalid telephone number.']}
            )

        # Checks name string
        name = attrs['name']
        pattern_name = re.compile(r'^([\s[a-zA-Z]+)$')
        if not bool((re.fullmatch(pattern_name, name))):
            raise serializers.ValidationError(
                {'name': ['Invalid name.']}
            )

        # Checks surname string
        surname = attrs['surname']
        if not bool((re.fullmatch(pattern_name, surname))):
            raise serializers.ValidationError(
                {'surname': ['Invalid surname.']}
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
