"""
URLs for clients application.
"""

from django.urls import path

from .views import (
    ClientAPIView
)

urlpatterns = [
    path('', ClientAPIView.as_view(), name='client-create'),
]
