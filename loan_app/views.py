from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.

# Importing models
from .models import *

# Gets All Loans
class LoanView(APIView):
    def get(self, request):
        loans = Loan.objects.all()
        return Response({"loans": loans})

# Gets All Payments
class PaymentView(APIView):
    def get(self, request):
        payments = Payment.objects.all()
        return Response({"payments": payments})
