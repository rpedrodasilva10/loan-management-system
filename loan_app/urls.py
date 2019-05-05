from django.urls import path

from .views import (
    LoanAPIView,
)

urlpatterns = [
    path('loans/', LoanAPIView.as_view(), name = 'loan-create'),
]
