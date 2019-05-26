"""
URLs for clients application.
"""

from django.urls import path

from .views import (
    ClientListCreateAPIView,
    ClientDetailView
)

urlpatterns = [
    path('', ClientListCreateAPIView.as_view(), name='client-create'),
    path('<int:pk>/', ClientDetailView.as_view(), name='client-detail')
]
