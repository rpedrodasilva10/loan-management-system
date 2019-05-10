from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('loan_app.urls')),
    path('clients/', include('clients.urls')),
]
