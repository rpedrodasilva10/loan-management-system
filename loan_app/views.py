"""
Views for loan_app application.
"""

from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import Http404
from datetime import datetime
from django.core.exceptions import ValidationError

from .models import Loan

from .serializers import LoanSerializer, PaymentSerializer, BalanceSerializer

class LoanAPIView(generics.CreateAPIView):
    """
    Create a loan application.
    """
    serializer_class = LoanSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoanSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                content = {
                    'loan_id': serializer.data['loan_id'],
                    'instalment': serializer.data['instalment']
                }
                return Response(content, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as error:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)


class PaymentAPIView(generics.CreateAPIView):
    """
    Create a new payment (made / missed) for loan <:loan_id>.
    """
    serializer_class = PaymentSerializer
    queryset = Loan.objects.all()

    def post(self, request, *args, **kwargs):
        if request.POST:
            data = request.POST.dict()
        else:
            data = request.data
        data.update({'loan_id': self.kwargs.get("loan_id")})
        serializer = PaymentSerializer(data=data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as error:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

class BalanceApiView(generics.ListAPIView):
    '''
    Get the outstanding balance of a loan <:loan_id> at the moment of the requisition.
    '''
    serializer_class = BalanceSerializer
    queryset = Loan.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            loan = get_object_or_404(
                Loan.objects.all(),
                loan_id=self.kwargs.get("loan_id")
            )
            date = datetime.now()
            content = {'balance': loan.get_balance(date)}
            return Response(content, status=status.HTTP_200_OK)
        except Http404:
            content = {'loan_id': 'Loan not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
