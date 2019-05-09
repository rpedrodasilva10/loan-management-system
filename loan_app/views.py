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
                'loan_id': serializer.data['id'],
                'installment': round(float(serializer.data['installment']), 2)
            }
            return Response(content, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentAPIView(generics.ListCreateAPIView):
    """Missing: DOCSTRING"""
    serializer_class = PaymentSerializer
    queryset = Loan.objects.all()

    def get_object(self):
        return get_object_or_404(self.queryset, id=self.kwargs['id'])

    def get(self, request, *args, **kwargs):
        return Response(LoanSerializer(self.get_object()).data, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        try:
            loan = Loan.objects.get(id=self.kwargs.get("id"))
            serializer = PaymentSerializer(data=request.data, context={'loan': loan})
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
