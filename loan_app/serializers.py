"""Missing: DOCSTRING"""

from rest_framework import serializers

from loan_app.models import Loan, Payment

class LoanSerializer(serializers.ModelSerializer):
    """Missing: DOCSTRING"""
    class Meta:
        model = Loan
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    """Missing: DOCSTRING"""
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['id', 'loan']

    def create(self, validated_data):
        loan = Loan.objects.get(pk=self.context['id'])

        payment = Payment.objects.create(
            loan=loan,
            payment=validated_data.get('payment'),
            date=validated_data.get('date'),
            amount=validated_data.get('amount')
        )
        return payment
