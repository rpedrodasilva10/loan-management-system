from django.urls import path

from .views import *


app_name = "api"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('payments/', PaymentView.as_view()),
    path('loans/', LoanView.as_view()),
]

