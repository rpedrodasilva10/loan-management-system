"""
URLs for lms project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('clients/', include('clients.urls')),
    path('', include_docs_urls(title='Loan Management System', public=True, permission_classes=[])),
]
