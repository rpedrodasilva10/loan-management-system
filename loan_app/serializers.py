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
        fields = ('loan_id', 'amount', 'term', 'rate', 'date', 'installment')
        read_only_fields = ['installment']

    def to_representation(self, instance):
        """
        Rounds `installment` to 2 decimals.
        """
        ret = super().to_representation(instance)
        ret['installment'] = round(ret['installment'], 2)
        return ret

    def validate(self, attrs):
        if attrs['amount'] < 0:
            raise serializers.ValidationError(
                {'amount': ['Amount must be positive.']}
            )

        if attrs['term'] < 0:
            raise serializers.ValidationError(
                {'term': ['Term must be positive.']}
            )

        if attrs['rate'] < 0:
            raise serializers.ValidationError(
                {'rate': ['Rate must be positive.']}
            )
        return attrs

class PaymentSerializer(serializers.ModelSerializer):
    """
    Payment model serializer.
    """
    class Meta:
        model = Payment
        fields = ('payment_id', 'payment', 'date', 'amount', 'loan')

    def create(self, validated_data):
        # needed to add a layer of validation here, because of peculiarity of loan
        if validated_data['loan'].date < validated_data['date']:
            return Payment.objects.create(**validated_data)
        raise serializers.ValidationError(
            {'date': ['Payment must happen after respective loan approval.']}
        )

    def validate(self, attrs):
        if attrs['amount'] < 0:
            raise serializers.ValidationError(
                {'amount': ['Amount must be positive.']}
            )
        return attrs
