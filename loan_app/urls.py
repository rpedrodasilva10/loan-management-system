from django.urls import path

from .views import (
    LoanAPIView,
    PaymentAPIView
)

urlpatterns = [
    path('loans/', LoanAPIView.as_view(), name='loan-create'),
    path('loans/<int:id>/payments', PaymentAPIView.as_view(), name = 'payment-create'),
    #path('loans/<int:id>/balance', PaymentAPIView.as_view(), name = 'payment-list'),
]