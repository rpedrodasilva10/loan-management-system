'''
Serializers for loan api project.
'''

from rest_framework import serializers
from .models import Loan, Payment

class LoanSerializer(serializers.ModelSerializer):
    '''
    Loan model serializer.
    '''
    class Meta:
        model = Loan
        fields = ('loan_id', 'client_id', 'amount', 'term', 'rate', 'date', 'instalment')
        read_only_fields = ['instalment', 'outstanding']

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
    '''
    Payment model serializer.
    '''
    class Meta:
        model = Payment
        fields = ('payment_id', 'payment', 'date', 'amount', 'loan')
        extra_kwargs = {
            'amount': {'max_digits': 12, 'decimal_places': 2}
        }

    def validate(self, attrs):

        if attrs['loan'].finished:
            raise serializers.ValidationError(
                {'loan': ['This loan is already fully payed.']}
            )

        if not attrs['loan'].date < attrs['date']:
            raise serializers.ValidationError(
                {'date': ['Payment must happen after respective loan approval.']}
            )

        if attrs['amount'] < 0:
            raise serializers.ValidationError(
                {'amount': ['Amount must be positive.']}
            )
        return attrs
