from rest_framework import serializers
from .models import Client
from pycpfcnpj import cpfcnpj
from re import compile, fullmatch

class ClientSerializer(serializers.ModelSerializer):
    """
    Client model serializer
    """
        
    def validate(self, data):
        
        pattern = compile(r"\d")
        cpf = data['cpf']
        # Checks if a given CPF has only numbers
        if not fullmatch(pattern, cpf): 
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

    