"""
Views for clients application.
"""

from rest_framework import generics, status, views
from rest_framework.response import Response
from .serializers import ClientSerializer
from .models import Client


class ClientAPIView(views.APIView):
    """
    Create a new client.
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

    def get(self, request, *args, **kwargs):
        content = []
        client_id = self.kwargs.get("client_id")
        if None == client_id:
            clients = Client.objects.all()
        else:
            clients = Client.objects.get(client_id=client_id)
        for client in clients:
            content.append(
                {
                    "client_id": client.client_id,
                    "name": client.name,
                    "surname": client.surname,
                    "email": client.email,
                    "telephone": client.telephone,
                    "cpf": client.cpf
                }
            )

        return Response(content, status=status.HTTP_200_OK)
