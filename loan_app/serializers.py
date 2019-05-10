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
        fields = ('id', 'loan_id', 'amount', 'term', 'rate', 'date', 'installment')
        read_only_fields = ['installment']

    def to_representation(self, instance):
        """
        Rounds `installment` to 2 decimals.
        """

        ret = super().to_representation(instance)

        ret['installment'] = round(ret['installment'], 2)
        return ret

class PaymentSerializer(serializers.ModelSerializer):
    """
    Payment model serializer.
    """
    class Meta:
        model = Payment
        fields = ('payment', 'date', 'amount', 'loan')

    def create(self, validated_data):
        return Payment.objects.create(
            loan=validated_data.get('loan'),
            payment=validated_data.get('payment'),
            date=validated_data.get('date'),
            amount=validated_data.get('amount')
        )

    def validate(self, attrs):
        if attrs['date'] < attrs['loan'].date:
            raise serializers.ValidationError(
                {'date': ['Payment date must be greater than the refered loan creation date.']}
            )

        if attrs['amount'] < 0:
            raise serializers.ValidationError(
                {'amount': ['Amount must be positive.']}
            )

        return attrs
