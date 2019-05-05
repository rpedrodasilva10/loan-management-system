from rest_framework import serializers

from loan_app.models import Loan, Payment

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'
        read_only_fields = ['id', 'installment']


    def create(self, validated_data):
        _rate = float(validated_data.get('rate'))
        _term = int(validated_data.get('term'))
        _amount = float(validated_data.get('amount'))
        r = _rate / 12.0
        _installment = ((r + r / ((1 + r) ** _term - 1)) * _amount)
        loan = Loan.objects.create(
            amount = _amount,
            term = _term,
            rate = _rate,
            date = validated_data.get('date'),
            installment = _installment
        )
        return loan

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['id', 'loan']

    def create(self, validated_data):
        loan = Loan.objects.get(pk = self.context['id'])

        payment = Payment.objects.create(
            loan = loan,
            payment = validated_data.get('payment'),
            date = validated_data.get('date'),
            amount = validated_data.get('amount')
        )
        return payment