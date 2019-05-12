from rest_framework import serializers
from .models import Client
from pycpfcnpj import cpfcnpj
import re

class ClientSerializer(serializers.ModelSerializer):
    """
    Client model serializer
    """
        
    def validate(self, data):
        """
        Validate the data before serializer.save
        """
        pattern = re.compile(r'^([\d]+)$')
        cpf = data['cpf']
        # Checks if a given CPF has only numbers
        if not bool((re.fullmatch(pattern, cpf))):
            raise serializers.ValidationError(
                {'cpf': ['Only numbers are allowed']}
            )
        elif not cpfcnpj.validate(cpf):
            raise serializers.ValidationError(
                {'cpf': ['Invalid CPF.']}
            )
        
        return data

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

    