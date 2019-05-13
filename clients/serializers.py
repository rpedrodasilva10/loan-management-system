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
        cpf = data['cpf']
        pattern_cpf = re.compile(r'^([\d]+)$')
        # Checks if a given CPF has only numbers
        if not bool((re.fullmatch(pattern_cpf, cpf))):
            raise serializers.ValidationError(
                {'cpf': ['Only numbers are allowed in a CPF.']}
            )
        elif not cpfcnpj.validate(cpf):
            raise serializers.ValidationError(
                {'cpf': ['Invalid CPF number.']}
            )
        
        telephone = data['telephone']
        pattern_telephone = re.compile(r'^([\d]+){10,11}$')
        # Checks if a given phone is valid acording to format:
        # 11 1234 5678 or 11 9 1234 5678 
        # without the spaces or signs
        if not bool((re.fullmatch(pattern_telephone, telephone))):
            raise serializers.ValidationError(
                {'telephone': ['Invalid telephone number.']}
            )

        # Checks name string
        name = data['name']
        pattern_name = re.compile(r'^([\s[a-zA-Z]+)$')
        if not bool((re.fullmatch(pattern_name, name))):
            raise serializers.ValidationError(
                {'name': ['Invalid name.']}
            )
        
        # Checks surname string
        surname = data['surname']
        if not bool((re.fullmatch(pattern_name, surname))):
            raise serializers.ValidationError(
                {'surname': ['Invalid surname.']}
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

    