"""Missing: DOCSTRING"""

from rest_framework import generics, status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from .models import Loan
from .serializers import LoanSerializer, PaymentSerializer


class LoanAPIView(generics.CreateAPIView):
    """Missing: DOCSTRING"""
    serializer_class = LoanSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            content = {
                'loan_id': serializer.data['loan_id'],
                'installment': round(float(serializer.data['installment']), 2)
            }
            return Response(content, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentAPIView(generics.CreateAPIView):
    """Missing: DOCSTRING"""
    serializer_class = PaymentSerializer
    queryset = Loan.objects.all()

    def post(self, request, *args, **kwargs):
        try:
            if request.POST:
                data = request.POST.dict()
            else:
                data = request.data
            obj = get_object_or_404(
                self.queryset, loan_id=self.kwargs.get("loan_id")
            )
            serializer = PaymentSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(loan=obj)
                return Response(status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
