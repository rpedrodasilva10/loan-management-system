"""
Tests for clients application.
"""

from django.test import TestCase
from clients.models import Client

class ClientTest(TestCase):
    """
    Test module for client model.
    """

    def setUp(self):
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
        print(client_jones)

        self.assertEqual(
            client_jones.get_client(),
            "Felicity Jones e-mail felicity@gmail.com telephone 11984345678 CPF 34598712387"
        )
