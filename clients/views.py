from rest_framework import generics, status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from .models import Client
from .serializers import ClientSerializer

# Create your views here.

class ClientAPIView(generics.CreateAPIView):
    """
    Create a new client
    """
    serializer_class = ClientSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            content = {
                'client_id': serializer.data['client_id'],
            }
            return Response(content, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
