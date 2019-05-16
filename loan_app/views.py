"""
Views for loan_app application.
"""

from rest_framework import generics, status
from rest_framework.response import Response
from .models import Loan
from .serializers import LoanSerializer, PaymentSerializer

class LoanAPIView(generics.CreateAPIView):
    """
    View for POST /loan endpoint.
    """
    serializer_class = LoanSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            content = {
                'loan_id': serializer.data['loan_id'],
                'instalment': serializer.data['instalment']
            }
            return Response(content, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentAPIView(generics.CreateAPIView):
    """
    View for Post /loan/<:loan_id>/payment endpoint.
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
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
