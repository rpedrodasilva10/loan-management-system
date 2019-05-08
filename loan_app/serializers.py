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

    def to_representation(self, instance):
        """
        Converts `id` to '0000-0000-0000-000' format.
        Rounds `installment` to 2 decimals.
        """

        ret = super().to_representation(instance)

        with_zeros = '{:016d}'.format(ret['id'])
        ret['id'] = '-'.join(with_zeros[i:i+4] for i in range(0, len(with_zeros), 4))

        ret['installment'] = round(ret['installment'], 2)
        return ret

class PaymentSerializer(serializers.ModelSerializer):
    """
    Payment model serializer.
    """
    #loan = serializer.HiddenField(default=)
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
