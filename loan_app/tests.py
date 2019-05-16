import json
from django.test import TestCase
from pycpfcnpj import gen
from clients.models import Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User


class LoanTest(TestCase):
    """ Test module for Client model """

    def setUp(self):
        self.password = '123'
        self.user = User.objects.create_user(
            'carolina', 'carol@gmail.com', self.password
        )
        Client.objects.create(
            name='Felicity', surname='Jones', email='felicity@gmail.com', telephone='11984345678', cpf=gen.cpf()
        )
        self.client = Client.objects.get(name='Felicity')

    def test_post_valid_loan(self):
        loan = APIClient()
        loan.login(username=self.user.username, password=self.password)
        response = loan.post(
            reverse('loan-create'),
            json.dumps({'client_id': self.client.client_id,
                        'amount': 1000,
                        'term': 12,
                        'rate': 0.05,
                        'date': '2019-05-09 03:18Z'
                        }),
            content_type='application/json'
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_invalid_loan(self):
        loan = APIClient()
        loan.login(username=self.user.username, password=self.password)
        response = loan.post(
            reverse('loan-create'),
            json.dumps({'client_id': self.client.client_id,
                        'amount': '',
                        'term': 12,
                        'rate': 0.05,
                        'date': '2019-05-09 03:18Z'
                        }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
