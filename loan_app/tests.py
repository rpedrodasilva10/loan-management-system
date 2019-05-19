"""
Tests for loan_app application.
"""

import json
import datetime
from decimal import Decimal
from pycpfcnpj import gen
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from loan_app.models import Loan
from clients.models import Client


class LoanTest(TestCase):
    """ Test module for Client model """

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
            cpf=gen.cpf()
        )
        self.client_jones = Client.objects.get(name='Felicity')

        Client.objects.create(
            name='Julia',
            surname='Silva',
            email='julia@gmail.com',
            telephone='11984345678',
            cpf=gen.cpf()
        )
        self.client_silva = Client.objects.get(name='Julia')

        Loan.objects.create(
            client_id=self.client_jones,
            amount=1000,
            term=12,
            rate=0.05,
            date='2019-05-19 03:18Z'
        )
        self.loan_jones = Loan.objects.get(client_id=self.client_jones.client_id)

    def test_post_valid_loan(self):
        """
        TODO
        """
        loan = APIClient()
        loan.login(username=self.user.username, password=self.password)
        response = loan.post(
            reverse('loan-create'),
            json.dumps({'client_id': self.client_silva.client_id,
                        'amount': 1000,
                        'term': 12,
                        'rate': 0.05,
                        'date': '2019-05-19 14:40Z'
                        }),
            content_type='application/json'
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_invalid_loan(self):
        """
        TODO
        """
        loan = APIClient()
        loan.login(username=self.user.username, password=self.password)
        response = loan.post(
            reverse('loan-create'),
            json.dumps({'client_id': self.client_silva.client_id,
                        'amount': '',
                        'term': 12,
                        'rate': 0.05,
                        'date': '2019-05-19 14:40Z'
                        }),
            content_type='application/json'
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_payment(self):
        payment = APIClient()
        payment.login(username=self.user.username, password=self.password)
        response = payment.post(
            reverse('payment-create', kwargs={'loan_id': self.loan_jones.loan_id}),
            json.dumps({'loan_id': self.loan_jones.loan_id,
                        'payment': 'made',
                        'date': '2019-05-18 20:09Z',
                        'amount': 85.60
                        }),
            content_type='application/json'
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_balance(self):
        self.assertEqual(self.loan_jones.get_balance(self.loan_jones.date), Decimal('1027.20')) 
        