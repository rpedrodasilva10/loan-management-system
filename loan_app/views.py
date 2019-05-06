from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from .models import Loan, Payment
from .serializers import LoanSerializer, PaymentSerializer

from .services import calc_installment

class LoanAPIView(generics.CreateAPIView):
    serializer_class = LoanSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoanSerializer(data=calc_installment(request.data))
        if serializer.is_valid():
            serializer.save()
            content = {
                'loan_id': serializer.data['id'],
                'installment': float(serializer.data['installment'])
            }
            return Response(content, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer

    def post(self, request, *args, **kwargs):
        serializer = PaymentSerializer(data=request.data, context={'id': self.kwargs.get("id")})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
