"""
Tests for clients application.
"""

import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from pycpfcnpj import gen
from rest_framework import status
from rest_framework.test import APIClient

from clients.models import Client

class ClientTest(TestCase):
    """
    Test module for client model.
    """

    def setUp(self):
        self.password = '123'
        self.user = User.objects.create_user(
            'carolina', 'carol@gmail.com', self.password
        )

        Client.objects.create(
            name='Felicity',
            surname='Jones',
            email='felicity@gmail.com',
            telephone='11984345678',
            cpf='34598712387'
        )

    def test_puppy_breed(self):
        """
        TODO
        """
        client_jones = Client.objects.get(name='Felicity')

        self.assertEqual(
            client_jones.__str__(), "1 - Felicity Jones")

    def test_post_valid_client(self):
        """
        TODO
        """
        client = APIClient()
        client.login(username=self.user.username, password=self.password)
        response = client.post(
            reverse('client-create'),
            json.dumps({'name': 'Luis',
                        'surname': 'Martins',
                        'email': 'lu@gmail.com',
                        'telephone': '51981790346',
                        'cpf': gen.cpf()}
                       ),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_client(self):
        """
        TODO
        """
        client = APIClient()
        client.login(username=self.user.username, password=self.password)
        response = client.post(
            reverse('client-create'),
            json.dumps({'name': '',
                        'surname': 'Gonzalves',
                        'email': 'lu@gmail.com',
                        'telephone': '1199345678',
                        'cpf': gen.cpf()}
                       ),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)