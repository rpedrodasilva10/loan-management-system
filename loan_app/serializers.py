"""
Serializers for loan api project.
"""

from rest_framework import serializers
from .models import Loan, Payment

class LoanSerializer(serializers.ModelSerializer):
    """
    Loan model serializer.
    """
    class Meta:
        model = Loan
        fields = ('id', 'amount', 'term', 'rate', 'date', 'installment')
        read_only_fields = ['id', 'installment', 'payments']

class PaymentSerializer(serializers.ModelSerializer):
    """
    Payment model serializer.
    """
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['id', 'loan']

    def create(self, validated_data):
        payment = Payment.objects.create(
            loan=self.context['loan'],
            payment=validated_data.get('payment'),
            date=validated_data.get('date'),
            amount=validated_data.get('amount')
        )
        return payment
