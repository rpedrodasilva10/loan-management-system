from rest_framework import serializers

from loan_app.models import Loan

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = [
            'id',
            'amount',
            'term',
            'rate',
            'date',
            'installment',
        ]
        read_only_fields = ['id', 'installment']


    def create(self, validated_data):
        print(type(validated_data.get('rate')))
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