"""
URLs for loan_app application.
"""

from django.urls import path
from .views import (
    LoanAPIView,
    PaymentAPIView
)

urlpatterns = [
    path('loans/', LoanAPIView.as_view(), name='loan-create'),
    path('loans/<str:loan_id>/payments', PaymentAPIView.as_view(), name='payment-create'),
]
