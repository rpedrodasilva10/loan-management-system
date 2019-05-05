from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from .models import Loan
from .serializers import LoanSerializer

class LoanAPIView(generics.CreateAPIView):
    serializer_class = LoanSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = LoanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            content = {
                'loan_id': serializer.data['id'],
                'installment': float(serializer.data['installment'])
            }
            return Response(content, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)