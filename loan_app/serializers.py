"""
Serializers for loan api project.
"""

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Loan, Payment

class LoanSerializer(serializers.ModelSerializer):
    """
    Loan model serializer.
    """
    class Meta:
        model = Loan
        fields = ('loan_id', 'client_id', 'amount', 'term', 'rate', 'date', 'installment')
        read_only_fields = ['installment', 'outstanding']

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

    def validate(self, attrs):
        try:
            
            """
            TODO - Needs to validate if Loan._outstanding > 0 to make a payment
            """
            if not attrs['loan'].date < attrs['date']:
                raise serializers.ValidationError(
                    {'date': ['Payment must happen after respective loan approval.']}
                )

            if attrs['amount'] < 0:
                raise serializers.ValidationError(
                    {'amount': ['Amount must be positive.']}
                )
            return attrs
        except Loan.DoesNotExist:
            raise serializers.ValidationError(
                {'loan': ['Loan not found.']}
            )
