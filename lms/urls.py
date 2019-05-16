"""
URLs for lms project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('loan_app.urls')),
    path('clients/', include('clients.urls')),
    path('docs/', include_docs_urls(title='Loan Management System', public=True, permission_classes=[])),
]
