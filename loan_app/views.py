'''
TODO
'''
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Loan
from .serializers import LoanSerializer, PaymentSerializer


class LoanAPIView(generics.CreateAPIView):
    '''
    TODO
    '''
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
    '''
    TODO
    '''
    serializer_class = PaymentSerializer
    queryset = Loan.objects.all()

    def post(self, request, *args, **kwargs):
        
        # The standard QueryDict object it's not mutable
        # we need to create a new one with mutable=True
        mutable_data = request.POST.copy()
        mutable_data.mutable = True
        mutable_data.update(
            {'loan': self.kwargs.get("loan")}
        )
        serializer = PaymentSerializer(data=mutable_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
