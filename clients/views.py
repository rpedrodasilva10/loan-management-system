"""
Views for clients application.
"""

from rest_framework import generics, status, views
from rest_framework.response import Response
from .serializers import ClientSerializer
from .models import Client


class ClientListCreateAPIView(generics.ListCreateAPIView):
    """
    Create a client or lists all clients in the database.
    """
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            content = {
                'client_id': serializer.data['client_id'],
            }
            return Response(content, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a client.  
    """
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
